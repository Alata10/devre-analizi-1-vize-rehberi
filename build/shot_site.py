# -*- coding: utf-8 -*-
"""Tam site ekran görüntüsü: python build/shot_site.py [genişlik] [yükseklik] [--dark] [--hash=xyz]"""
import os
import subprocess
import sys
import tempfile
import time

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

args = [a for a in sys.argv[1:] if not a.startswith('--')]
w = int(args[0]) if args else 1440
h = int(args[1]) if len(args) > 1 else 6000
dark = '--dark' in sys.argv
tag = f"site_{w}{'_dark' if dark else ''}"
out = os.path.join(ROOT, 'preview', tag + '_full.png')
os.makedirs(os.path.dirname(out), exist_ok=True)
if os.path.exists(out):
    os.remove(out)
url = 'file:///' + os.path.join(ROOT, 'index.html').replace('\\', '/')
if dark:
    url += '?theme=dark'
profile = tempfile.mkdtemp(prefix='edgesite_')
subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
                f'--user-data-dir={profile}', '--virtual-time-budget=9000',
                f'--window-size={w},{h}', f'--screenshot={out}', url], capture_output=True, timeout=180)
for _ in range(30):
    if os.path.exists(out):
        break
    time.sleep(1)
im = Image.open(out)
W, H = im.size
step = 1700 if w > 800 else 2400
paths = []
for i, t in enumerate(range(0, H, step)):
    p = os.path.join(ROOT, 'preview', f'{tag}_{i + 1:02d}.png')
    im.crop((0, t, W, min(H, t + step))).save(p)
    paths.append(p)
print('\n'.join(paths))
