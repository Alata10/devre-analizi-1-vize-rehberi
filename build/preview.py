# -*- coding: utf-8 -*-
"""
İçerik önizleme ve doğrulama aracı.

    python build/preview.py q1            # content/q1.py'yi doğrula, şemaları çiz, preview-q1.html üret
    python build/preview.py q1 --shot     # + Edge ile ekran görüntüsü al (preview/q1_*.png parçaları)
    python build/preview.py q1 --shot --dark

Ekran görüntülerini read_file ile açıp: devre şeması orijinalle birebir mi, KaTeX hatası (kırmızı yazı) var mı,
taşma var mı — kontrol et.
"""
import importlib
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'content'))

from circuitkit import render_all  # noqa: E402
from render import render_problem, HEAD, SCRIPTS  # noqa: E402

REQUIRED = ["id", "topic", "code", "title", "source", "question", "steps", "answer", "exam"]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def validate(mod):
    errors = []
    ids = set()
    circuits = getattr(mod, "CIRCUITS", {})
    for p in mod.PROBLEMS:
        for k in REQUIRED:
            if k not in p or p[k] in (None, "", []):
                errors.append(f"{p.get('id', '?')}: eksik alan '{k}'")
        if p.get("id") in ids:
            errors.append(f"{p['id']}: tekrar eden id")
        ids.add(p.get("id"))
        if p.get("circuit") and p["circuit"] not in circuits:
            errors.append(f"{p['id']}: circuit '{p['circuit']}' CIRCUITS içinde yok")
        if p.get("image") and not os.path.exists(os.path.join(ROOT, "img", p["image"])):
            errors.append(f"{p['id']}: görsel bulunamadı img/{p['image']}")
        for i, s in enumerate(p.get("steps", []), 1):
            if "title" not in s:
                errors.append(f"{p['id']} adım {i}: title yok")
            for fld in ("math",):
                t = s.get(fld, "")
                if t.count("{") != t.count("}"):
                    errors.append(f"{p['id']} adım {i}: '{fld}' içinde süslü parantez dengesiz")
                if "$" in t:
                    errors.append(f"{p['id']} adım {i}: 'math' alanında $ kullanma (zaten display math)")
        if p.get("exam", "").count("{") != p.get("exam", "").count("}"):
            errors.append(f"{p['id']}: exam süslü parantez dengesiz")
    return errors


def shoot(html_path, out_prefix, n_problems, dark=False):
    url = "file:///" + html_path.replace("\\", "/")
    if dark:
        url += "#dark"
    h = min(32000, 600 + 2600 * max(1, n_problems))
    png = out_prefix + "_full.png"
    import tempfile
    profile = tempfile.mkdtemp(prefix="edgeprev_")
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                    f"--user-data-dir={profile}",
                    "--virtual-time-budget=8000", f"--window-size=1100,{h}",
                    f"--screenshot={png}", url], capture_output=True, timeout=180)
    for _ in range(30):
        if os.path.exists(png):
            break
        time.sleep(1)
    from PIL import Image
    im = Image.open(png).convert("RGB")
    # alttaki boşluğu kırp
    w, H = im.size
    bg = im.getpixel((5, H - 5))
    y = H - 1
    px = im.load()
    while y > 0:
        row_diff = any(sum(abs(a - b) for a, b in zip(px[x, y], bg)) > 30 for x in range(0, w, 7))
        if row_diff:
            break
        y -= 1
    im = im.crop((0, 0, w, min(H, y + 40)))
    parts = []
    step = 1800
    for i, top in enumerate(range(0, im.size[1], step)):
        part = im.crop((0, top, w, min(im.size[1], top + step)))
        path = f"{out_prefix}_{i + 1:02d}.png"
        part.save(path)
        parts.append(path)
    os.remove(png)
    return parts


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    name = sys.argv[1]
    mod = importlib.import_module(name)
    errs = validate(mod)
    if errs:
        print("DOĞRULAMA HATALARI:")
        for e in errs:
            print("  -", e)
    else:
        print(f"Doğrulama OK — {len(mod.PROBLEMS)} problem.")
    render_all(getattr(mod, "CIRCUITS", {}))
    print("Şemalar circuits/ klasörüne yazıldı:", ", ".join(getattr(mod, "CIRCUITS", {}).keys()))

    body = "".join(render_problem(p, i) for i, p in enumerate(mod.PROBLEMS, 1))
    page = (HEAD.format(title=f"Önizleme — {name}", ver="dev")
            + '<body><script>if(location.hash==="#dark")document.documentElement.dataset.theme="dark";else document.documentElement.dataset.theme="light";</script>'
            + f'<main class="main"><div class="content">{body}</div></main>'
            + SCRIPTS.format(ver="dev"))
    out = os.path.join(ROOT, f"preview-{name}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print("Önizleme:", out)

    if "--shot" in sys.argv:
        os.makedirs(os.path.join(ROOT, "preview"), exist_ok=True)
        dark = "--dark" in sys.argv
        prefix = os.path.join(ROOT, "preview", name + ("_dark" if dark else ""))
        parts = shoot(out, prefix, len(mod.PROBLEMS), dark)
        print("Ekran görüntüleri:")
        for p in parts:
            print("  ", p)


if __name__ == "__main__":
    main()
