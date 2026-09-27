#!/usr/bin/env python3
"""Upload the ClipMe money-page videos to YouTube with the Data API v3.

Reads OAuth credentials from environment variables (never hard-code them):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   (scope: youtube.force-ssl)

For each numbered folder, in order, it uploads:
  - video.mp4  with the title/description/tags from youtube.json, thumbnail.jpg and captions.srt
  - short.mp4  with the title/description from short-description.txt and short-captions.srt
and adds every long video to one playlist. Progress is saved to uploaded.json, so a rerun
skips anything already uploaded (quota or network interruptions are safe to resume).

Note: until Google approves the API project's audit, YouTube locks API uploads as Private.

  python3 upload_to_youtube.py                  # everything, private
  python3 upload_to_youtube.py --only 01 02     # just these folders
  python3 upload_to_youtube.py --privacy unlisted --playlist "ClipMe answers"
  python3 upload_to_youtube.py --dry-run
"""
import argparse, json, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "uploaded.json")
API = "https://www.googleapis.com/youtube/v3"
UPLOAD = "https://www.googleapis.com/upload/youtube/v3"
CATEGORY_SCIENCE_TECH = "28"


def token():
    missing = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if missing:
        sys.exit("Missing environment variables: " + ", ".join(missing))
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def check(r):
    if r.status_code >= 400:
        sys.exit("YouTube API error %d: %s" % (r.status_code, r.text[:800]))
    return r


def upload_video(tok, path, title, description, tags, privacy):
    body = {"snippet": {"title": title[:100], "description": description[:5000], "tags": tags,
                        "categoryId": CATEGORY_SCIENCE_TECH, "defaultLanguage": "en"},
            "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}}
    size = os.path.getsize(path)
    r = check(requests.post(UPLOAD + "/videos", params={"uploadType": "resumable", "part": "snippet,status"},
                            headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json",
                                     "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)},
                            data=json.dumps(body), timeout=60))
    with open(path, "rb") as f:
        r = check(requests.put(r.headers["Location"], headers={"Authorization": "Bearer " + tok,
                               "Content-Type": "video/mp4"}, data=f, timeout=1800))
    return r.json()["id"]


def set_thumbnail(tok, vid, path):
    with open(path, "rb") as f:
        check(requests.post(UPLOAD + "/thumbnails/set", params={"videoId": vid},
                            headers={"Authorization": "Bearer " + tok, "Content-Type": "image/jpeg"}, data=f, timeout=120))


def add_captions(tok, vid, path):
    meta = {"snippet": {"videoId": vid, "language": "en", "name": "English"}}
    boundary = "clipmecaptions"
    with open(path, "rb") as f:
        srt = f.read()
    payload = (("--%s\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n%s\r\n--%s\r\n"
                "Content-Type: application/octet-stream\r\n\r\n") % (boundary, json.dumps(meta), boundary)).encode() \
        + srt + ("\r\n--%s--" % boundary).encode()
    check(requests.post(UPLOAD + "/captions", params={"uploadType": "multipart", "part": "snippet"},
                        headers={"Authorization": "Bearer " + tok,
                                 "Content-Type": "multipart/related; boundary=" + boundary}, data=payload, timeout=120))


def playlist_id(tok, name, privacy):
    r = check(requests.post(API + "/playlists", params={"part": "snippet,status"},
                            headers={"Authorization": "Bearer " + tok},
                            json={"snippet": {"title": name}, "status": {"privacyStatus": privacy}}, timeout=60))
    return r.json()["id"]


def add_to_playlist(tok, pl, vid):
    check(requests.post(API + "/playlistItems", params={"part": "snippet"}, headers={"Authorization": "Bearer " + tok},
                        json={"snippet": {"playlistId": pl, "resourceId": {"kind": "youtube#video", "videoId": vid}}},
                        timeout=60))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", help="folder number prefixes, e.g. 01 02")
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    ap.add_argument("--playlist", default="ClipMe: stream clipping answers")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    folders = sorted(d for d in os.listdir(HERE) if os.path.isdir(os.path.join(HERE, d)) and d[:2].isdigit())
    if a.only:
        folders = [d for d in folders if d[:2] in a.only]
    tok = None if a.dry_run else token()

    def save():
        json.dump(state, open(STATE, "w"), indent=1)

    if not a.dry_run and "_playlist" not in state:
        state["_playlist"] = playlist_id(tok, a.playlist, a.privacy); save()

    for d in folders:
        p = lambda f: os.path.join(HERE, d, f)
        s = state.setdefault(d, {})
        meta = json.load(open(p("youtube.json")))
        short_txt = open(p("short-description.txt")).read().strip().split("\n")
        jobs = [("video", p("video.mp4"), meta["title"], meta["description"], meta["tags"], p("captions.srt"), p("thumbnail.jpg")),
                ("short", p("short.mp4"), short_txt[0], "\n".join(short_txt[2:]), meta["tags"], p("short-captions.srt"), None)]
        for kind, path, title, desc, tags, srt, thumb in jobs:
            if s.get(kind):
                print("skip  %s %s (already %s)" % (d, kind, s[kind])); continue
            print("%s %s %s: %s" % ("would upload" if a.dry_run else "upload", d, kind, title))
            if a.dry_run:
                continue
            tok = token()  # access tokens last an hour; refresh per upload
            vid = upload_video(tok, path, title, desc, tags, a.privacy)
            s[kind] = vid; save()
            add_captions(tok, vid, srt)
            if thumb:
                set_thumbnail(tok, vid, thumb)
                add_to_playlist(tok, state["_playlist"], vid)
            print("   -> https://youtu.be/" + vid)
            time.sleep(2)
    print("done")


if __name__ == "__main__":
    main()
