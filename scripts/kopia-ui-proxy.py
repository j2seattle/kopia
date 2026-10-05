#!/usr/bin/env python3
"""Sign-in page in front of the Kopia UI.

Kopia protects the UI with HTTP basic auth. Chrome on this laptop does not
show that prompt, so the browser only renders the words "Missing credentials."
This proxy serves a normal form, checks the password against Kopia, and then
adds the basic-auth header on later requests. Repository clients keep using
port 51515 directly and never hit this process.
"""

import base64
import html
import http.client
import secrets
import ssl
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM_HOST = "127.0.0.1"
UPSTREAM_PORT = 51515
LISTEN = ("0.0.0.0", 51516)
CERT = "/etc/kopia/tls.cert"
KEY = "/etc/kopia/tls.key"
COOKIE = "kopia_session"
SESSION_SECONDS = 12 * 60 * 60

SESSIONS = {}
LOCK = threading.Lock()
CTX = ssl._create_unverified_context()

SKIP_RESPONSE_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "www-authenticate",
    "set-cookie",
    "content-length",
}


def prune():
    now = time.time()
    with LOCK:
        dead = [token for token, row in SESSIONS.items() if row[2] < now]
        for token in dead:
            del SESSIONS[token]


def session_from(header):
    if not header:
        return None
    prune()
    token = None
    for part in header.split(";"):
        part = part.strip()
        if part.startswith(COOKIE + "="):
            token = part.split("=", 1)[1]
    if not token:
        return None
    with LOCK:
        row = SESSIONS.get(token)
    if not row:
        return None
    return token, row[0], row[1]


def check_login(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    conn = http.client.HTTPSConnection(UPSTREAM_HOST, UPSTREAM_PORT, context=CTX, timeout=15)
    try:
        conn.request("GET", "/", headers={"Authorization": "Basic " + token})
        resp = conn.getresponse()
        resp.read()
        return resp.status == 200
    finally:
        conn.close()


LOGIN_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kopia sign in</title>
<style>
  body { margin: 0; min-height: 100vh; display: grid; place-items: center;
         background: #121418; color: #e8e8e8; font: 16px/1.4 system-ui, sans-serif; }
  form { width: min(22rem, 92vw); display: grid; gap: 0.75rem; }
  h1 { font-size: 1.25rem; margin: 0; }
  p { margin: 0; color: #b4b4b4; }
  label { display: grid; gap: 0.25rem; }
  input { font: inherit; padding: 0.55rem 0.65rem; border-radius: 6px;
          border: 1px solid #3a3f48; background: #1c2026; color: inherit; }
  button { font: inherit; padding: 0.6rem; border: 0; border-radius: 6px;
           background: #3d7eff; color: white; cursor: pointer; }
  .err { color: #ff8b8b; }
</style>
</head>
<body>
<form method="post" action="/login">
  <h1>Kopia</h1>
  <p>Sign in to the backup UI.</p>
  {error}
  <label>Username <input name="username" autocomplete="username" value="{username}" required></label>
  <label>Password <input name="password" type="password" autocomplete="current-password" required autofocus></label>
  <button type="submit">Sign in</button>
</form>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    server_version = "kopia-ui-proxy"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        if self.path.startswith("/login"):
            print("login request", self.command)
            return
        super().log_message(fmt, *args)

    def do_GET(self):
        self.route()

    def do_HEAD(self):
        self.route()

    def do_POST(self):
        self.route()

    def do_PUT(self):
        self.route()

    def do_DELETE(self):
        self.route()

    def do_PATCH(self):
        self.route()

    def route(self):
        path = self.path.split("?", 1)[0]
        if path == "/logout":
            self.logout()
            return
        if path == "/login":
            self.login()
            return
        found = session_from(self.headers.get("Cookie"))
        if not found:
            if path.startswith("/api/"):
                self.send_error_text(401, "Sign in required.")
                return
            self.send_form("")
            return
        _, username, password = found
        self.proxy(username, password)

    def read_body(self, limit):
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length < 0 or length > limit:
            return None
        return self.rfile.read(length) if length else b""

    def login(self):
        error = ""
        username = "kopia"
        if self.command == "POST":
            raw = self.read_body(8192)
            if raw is None:
                self.send_error_text(413, "Sign-in form was too large.")
                return
            form = urllib.parse.parse_qs(raw.decode("utf-8", "replace"), keep_blank_values=True)
            username = (form.get("username") or [""])[0]
            password = (form.get("password") or [""])[0]
            try:
                ok = check_login(username, password)
            except Exception:
                self.send_error_text(502, "Kopia did not answer. Try again in a moment.")
                return
            if ok:
                token = secrets.token_urlsafe(32)
                with LOCK:
                    SESSIONS[token] = (username, password, time.time() + SESSION_SECONDS)
                self.send_response(303)
                self.send_header("Location", "/")
                self.send_header("Cache-Control", "no-store")
                self.send_header(
                    "Set-Cookie",
                    f"{COOKIE}={token}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age={SESSION_SECONDS}",
                )
                self.send_header("Content-Length", "0")
                self.end_headers()
                print("login accepted")
                return
            error = "Those credentials were not accepted."
            print("login rejected")
        self.send_form(error, username)

    def logout(self):
        found = session_from(self.headers.get("Cookie"))
        if found:
            with LOCK:
                SESSIONS.pop(found[0], None)
        self.send_response(303)
        self.send_header("Location", "/")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Set-Cookie", f"{COOKIE}=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def send_form(self, error, username="kopia"):
        err = f'<p class="err">{html.escape(error)}</p>' if error else ""
        body = (
            LOGIN_PAGE.replace("{error}", err).replace("{username}", html.escape(username, quote=True))
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def send_error_text(self, status, message):
        body = message.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def proxy(self, username, password):
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length < 0 or length > 64 * 1024 * 1024:
            self.send_error_text(413, "Request is too large.")
            return
        body = self.rfile.read(length) if length else None
        token = base64.b64encode(f"{username}:{password}".encode()).decode()
        headers = {"Authorization": "Basic " + token}
        content_type = self.headers.get("Content-Type")
        if content_type:
            headers["Content-Type"] = content_type
        accept = self.headers.get("Accept")
        if accept:
            headers["Accept"] = accept
        # Kopia binds API calls to a CSRF token in the page and cookies set with it.
        # Dropping either one makes every page after sign-in return 401.
        cookie = self.headers.get("Cookie")
        if cookie:
            headers["Cookie"] = cookie
        csrf = self.headers.get("X-Kopia-Csrf-Token")
        if csrf:
            headers["X-Kopia-Csrf-Token"] = csrf
        conn = http.client.HTTPSConnection(UPSTREAM_HOST, UPSTREAM_PORT, context=CTX, timeout=300)
        try:
            conn.request(self.command, self.path, body=body, headers=headers)
            resp = conn.getresponse()
        except Exception:
            self.send_error_text(502, "Kopia did not answer.")
            return
        self.send_response(resp.status)
        for key, value in resp.headers.items():
            if key.lower() in SKIP_RESPONSE_HEADERS:
                continue
            self.send_header(key, value)
        for cookie in resp.headers.get_all("Set-Cookie") or []:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Cache-Control", "no-store")
        upstream_len = resp.headers.get("Content-Length")
        if self.command == "HEAD":
            if upstream_len is not None:
                self.send_header("Content-Length", upstream_len)
            self.end_headers()
            conn.close()
            return
        if upstream_len is None:
            payload = resp.read()
            conn.close()
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_header("Content-Length", upstream_len)
        self.end_headers()
        remaining = int(upstream_len)
        while remaining:
            chunk = resp.read(min(65536, remaining))
            if not chunk:
                break
            self.wfile.write(chunk)
            remaining -= len(chunk)
        conn.close()


def main():
    server = ThreadingHTTPServer(LISTEN, Handler)
    tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    tls.load_cert_chain(CERT, KEY)
    server.socket = tls.wrap_socket(server.socket, server_side=True)
    print("listening", LISTEN)
    server.serve_forever()


if __name__ == "__main__":
    main()
