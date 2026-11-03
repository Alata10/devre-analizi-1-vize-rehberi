# -*- coding: utf-8 -*-
"""
GitHub Pages'e tek commit ile yayınlar (Git Data API).
    python build/deploy.py "commit mesajı"
Token proje dışında tutulur: GH_TOKEN_FILE ortam değişkeni veya aşağıdaki varsayılan yol.
"""
import base64
import hashlib
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
TOKEN_FILE = os.environ.get(
    "GH_TOKEN_FILE",
    r"C:\Users\alata\.gemini\antigravity\brain\76d83025-f889-4f51-949c-a68b855dafea\scratch\gh_token.txt")
REPO = "devre-analizi-1-vize-rehberi"

INCLUDE_DIRS = ["assets", "img", "circuits", "build"]
INCLUDE_FILES = ["index.html", "README.md", ".nojekyll"]
SKIP_PARTS = {"__pycache__", "preview"}


def api(method, url, token, body=None):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(6):
        try:
            req = urllib.request.Request(
                url if url.startswith("http") else "https://api.github.com" + url,
                method=method,
                data=data,
                headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                         "User-Agent": "da1-deployer", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode() or "{}")
        except Exception as e:
            if attempt == 5:
                raise
            time.sleep(1.2 * (attempt + 1))


def files():
    out = []
    for f in INCLUDE_FILES:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            out.append(f)
    for d in INCLUDE_DIRS:
        for base, dirs, fs in os.walk(os.path.join(ROOT, d)):
            dirs[:] = [x for x in dirs if x not in SKIP_PARTS]
            for f in fs:
                if f.endswith((".pyc",)):
                    continue
                rel = os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/")
                out.append(rel)
    return sorted(out)


def main():
    msg = sys.argv[1] if len(sys.argv) > 1 else "Siteyi güncelle"
    token = open(TOKEN_FILE, encoding="utf-8").read().strip()
    owner = api("GET", "/user", token)["login"]
    repo = f"/repos/{owner}/{REPO}"
    ref = api("GET", f"{repo}/git/ref/heads/main", token)
    parent = ref["object"]["sha"]
    known_shas = set()
    try:
        old_tree = api("GET", f"{repo}/git/trees/{parent}?recursive=1", token)
        known_shas = {item["sha"] for item in old_tree.get("tree", []) if item.get("type") == "blob"}
    except Exception:
        pass

    tree = []
    fl = files()
    uploaded = 0
    for i, rel in enumerate(fl, 1):
        with open(os.path.join(ROOT, rel), "rb") as fh:
            data = fh.read()
        git_sha = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
        if git_sha in known_shas:
            sha = git_sha
        else:
            blob = api("POST", f"{repo}/git/blobs", token,
                       {"content": base64.b64encode(data).decode(), "encoding": "base64"})
            sha = blob["sha"]
            uploaded += 1
        tree.append({"path": rel, "mode": "100644", "type": "blob", "sha": sha})
        if i % 25 == 0:
            print(f"  {i}/{len(fl)} dosya işlendi ({uploaded} yeni yüklendi)")
    t = api("POST", f"{repo}/git/trees", token, {"tree": tree})
    c = api("POST", f"{repo}/git/commits", token, {"message": msg, "tree": t["sha"], "parents": [parent]})
    api("PATCH", f"{repo}/git/refs/heads/main", token, {"sha": c["sha"], "force": False})
    print(f"Yayınlandı: {len(fl)} dosya, commit {c['sha'][:7]}")
    print(f"https://{owner.lower()}.github.io/{REPO}/")


if __name__ == "__main__":
    main()
