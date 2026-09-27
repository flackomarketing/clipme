#!/usr/bin/env python3
"""Run this ON YOUR OWN COMPUTER (not in a cloud session) to get a YouTube refresh token.

1. In Google Cloud Console > APIs & Services > Credentials, create an OAuth client of type "Desktop app"
   and download its JSON (client_secret_....json).
2. python3 get_refresh_token.py path/to/client_secret.json
3. A browser opens: sign in as the @clipmeapp channel's Google account and allow access.
4. The script prints YT_CLIENT_ID, YT_CLIENT_SECRET and YT_REFRESH_TOKEN. Paste them into the
   cloud environment's settings (environment menu > Edit), never into a chat.

Needs no extra packages (standard library only).
"""
import http.server, json, secrets, sys, urllib.parse, urllib.request, webbrowser

SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[1]))
    cfg = cfg.get("installed") or cfg.get("web") or cfg
    cid, csec = cfg["client_id"], cfg["client_secret"]
    state = secrets.token_urlsafe(16)
    got = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            got.update({k: v[0] for k, v in q.items()})
            self.send_response(200); self.end_headers()
            self.wfile.write(b"Done. You can close this tab and go back to the terminal.")

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", 0), H)
    redirect = "http://127.0.0.1:%d" % srv.server_port
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": cid, "redirect_uri": redirect, "response_type": "code", "scope": SCOPE,
        "access_type": "offline", "prompt": "consent", "state": state})
    print("Opening your browser. If it doesn't open, visit:\n" + url)
    webbrowser.open(url)
    while "code" not in got and "error" not in got:
        srv.handle_request()
    if got.get("state") != state or "code" not in got:
        sys.exit("Authorization failed: %s" % got.get("error", "state mismatch"))
    data = urllib.parse.urlencode({"code": got["code"], "client_id": cid, "client_secret": csec,
                                   "redirect_uri": redirect, "grant_type": "authorization_code"}).encode()
    tok = json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data=data))
    if "refresh_token" not in tok:
        sys.exit("No refresh token returned. Remove the app's access at myaccount.google.com/permissions and rerun.")
    print("\nAdd these three to the cloud environment settings (not to a chat):\n")
    print("YT_CLIENT_ID=" + cid)
    print("YT_CLIENT_SECRET=" + csec)
    print("YT_REFRESH_TOKEN=" + tok["refresh_token"])


if __name__ == "__main__":
    main()
