# -*- coding: utf-8 -*-
"""HTML parçalarını üreten ortak fonksiyonlar (site.py ve preview.py kullanır)."""
import html as _html

LEVELS = {1: "Temel", 2: "Orta", 3: "Zor"}
TOPICS = {
    1: ("Soru 1", "Maksimum güç transferi"),
    2: ("Soru 2", "Kaynak dönüşümü & süperpozisyon"),
    3: ("Soru 3", "Düğüm gerilimleri & çevre akımları"),
    4: ("Soru 4", "Güç hesabı & güç dengesi"),
}


def esc(s):
    return _html.escape(s, quote=True)


def display_math(tex):
    return f'<div class="math-display">\\[{tex}\\]</div>'


def render_problem(p, number):
    pid = p["id"]
    level = LEVELS.get(p.get("level", 2), "Orta")
    featured = '<span class="tag tag-hot">Tahtada çözüldü</span>' if p.get("featured") else ""

    # --- figür: çözüm şeması + orijinal görsel (sekme) ---
    fig_tabs, fig_panes = [], []
    if p.get("circuit"):
        fig_tabs.append(f'<button class="seg-btn is-active" data-fig="schem">Çözüm şeması</button>')
        cap = p.get("circuit_caption", "")
        fig_panes.append(
            f'<figure class="fig-pane" data-pane="schem">'
            f'<img class="zoomable schematic" loading="lazy" src="circuits/{esc(p["circuit"])}.svg" '
            f'alt="{esc(p["code"])} çözüm şeması">'
            + (f'<figcaption>{cap}</figcaption>' if cap else "") + '</figure>'
        )
    if p.get("image"):
        active = "" if fig_tabs else " is-active"
        fig_tabs.append(f'<button class="seg-btn{active}" data-fig="orig">Kitaptaki şekil</button>')
        hidden = " hidden" if p.get("circuit") else ""
        fig_panes.append(
            f'<figure class="fig-pane"{hidden} data-pane="orig">'
            f'<img class="zoomable original" loading="lazy" src="img/{esc(p["image"])}" '
            f'alt="{esc(p["code"])} orijinal şekil"><figcaption>Nilsson &amp; Riedel — {esc(p["code"])} (çalışma yaprağından)</figcaption></figure>'
        )
    figure_html = ""
    if fig_panes:
        tabs = f'<div class="seg seg-sm fig-tabs">{"".join(fig_tabs)}</div>' if len(fig_tabs) > 1 else ""
        figure_html = f'<div class="figure-block">{tabs}{"".join(fig_panes)}</div>'

    strategy = ""
    if p.get("strategy"):
        items = "".join(f"<li>{s}</li>" for s in p["strategy"])
        strategy = f'<aside class="callout callout-plan"><div class="callout-title">Çözüm planı</div><ol>{items}</ol></aside>'

    steps = []
    for i, s in enumerate(p.get("steps", []), 1):
        body = f'<p>{s["body"]}</p>' if s.get("body") else ""
        math = display_math(s["math"]) if s.get("math") else ""
        note = f'<p class="step-note">{s["note"]}</p>' if s.get("note") else ""
        steps.append(
            f'<li class="step" data-step="{i}"><div class="step-marker">{i}</div>'
            f'<div class="step-content"><h4 class="step-title">{s["title"]}</h4>{body}{math}{note}</div></li>'
        )
    n_steps = len(steps)

    answer = ""
    if p.get("answer"):
        chips = "".join(f'<span class="answer-chip">\\({a}\\)</span>' for a in p["answer"])
        answer = f'<div class="answer"><div class="answer-label">Sonuç</div><div class="answer-chips">{chips}</div></div>'

    exam = ""
    if p.get("exam"):
        exam = (f'<div class="view" data-view="exam" hidden><div class="paper">'
                f'<div class="paper-head"><span>Sınav kağıdına yazılacaklar</span><span>{esc(p["code"])}</span></div>'
                f'{display_math(p["exam"])}</div></div>')

    traps = ""
    if p.get("traps"):
        items = "".join(f"<li>{t}</li>" for t in p["traps"])
        traps = f'<details class="traps"><summary>Sık yapılan hatalar</summary><ul>{items}</ul></details>'

    view_btns = '<button class="seg-btn is-active" data-view-btn="detail">Detaylı anlatım</button>'
    if exam:
        view_btns += '<button class="seg-btn" data-view-btn="exam">Sınav kağıdı</button>'
    view_btns += '<button class="seg-btn" data-view-btn="step">Adım adım</button>'

    topic_short = TOPICS[p["topic"]][0]
    return f'''
<article class="problem" id="{esc(pid)}" data-pid="{esc(pid)}" data-topic="{p["topic"]}" data-steps="{n_steps}"
  data-search="{esc((p["code"] + " " + p["title"] + " " + p.get("source", "")).lower())}">
  <header class="problem-head">
    <div class="problem-meta">
      <span class="pcode">{esc(p["code"])}</span>
      <span class="tag">{topic_short}</span>
      <span class="tag tag-level" data-level="{p.get("level", 2)}">{level}</span>
      {featured}
      <button class="done-toggle" data-done="{esc(pid)}" aria-pressed="false" title="Tamamlandı olarak işaretle">
        <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 10.5l3.2 3.2L15 7"/></svg><span>Tamamla</span>
      </button>
    </div>
    <h3 class="problem-title"><span class="pnum">{number}.</span> {p["title"]}</h3>
    <div class="problem-source">{esc(p.get("source", ""))}</div>
  </header>
  {figure_html}
  <div class="question"><span class="q-label">Soru</span><div>{p["question"]}</div></div>
  <div class="view-bar"><div class="seg">{view_btns}</div></div>
  <div class="view" data-view="detail">
    {strategy}
    <ol class="steps">{"".join(steps)}</ol>
    <div class="stepper" hidden>
      <span class="stepper-count"></span>
      <div class="stepper-actions">
        <button class="btn btn-ghost" data-stepper="prev">Geri</button>
        <button class="btn btn-primary" data-stepper="next">Sonraki adım</button>
        <button class="btn btn-ghost" data-stepper="all">Hepsini göster</button>
      </div>
    </div>
  </div>
  {exam}
  {answer}
  {traps}
  <footer class="problem-foot">
    <button class="btn btn-done" data-done="{esc(pid)}"><span class="done-off">Anladım, bu soruyu tamamladım</span><span class="done-on">Tamamlandı ✓</span></button>
  </footer>
</article>'''


HEAD = '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Devre Analizi I — Tuna Göksu vize hazırlığı: bağımlı kaynaklı 4 soru tipi, adım adım çözümler.">
<meta property="og:title" content="Devre Analizi I — Vize Rehberi">
<meta property="og:description" content="Bağımlı kaynaklı 4 soru tipi: maksimum güç, süperpozisyon/kaynak dönüşümü, düğüm/çevre analizi, güç dengesi. Adım adım çözümler.">
<meta name="theme-color" content="#0B0F19">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230EA5E9'/%3E%3Cpath d='M17.5 4 7 18h7l-1.5 10L24 13h-7z' fill='white'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/katex/katex.min.css">
<link rel="stylesheet" href="assets/style.css?v={ver}">
<script>(function(){{try{{var q=new URLSearchParams(location.search).get('theme');var t=q||localStorage.getItem('da1-theme');if(!t){{t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}}document.documentElement.dataset.theme=t}}catch(e){{}}}})();</script>
</head>
'''

SCRIPTS = '''
<script defer src="assets/katex/katex.min.js"></script>
<script defer src="assets/katex/auto-render.min.js"></script>
<script defer src="assets/app.js?v={ver}"></script>
</body></html>
'''
