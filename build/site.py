# -*- coding: utf-8 -*-
"""
Siteyi üretir:  python build/site.py
Çıktı: index.html + circuits/*.svg  (assets/, img/ hazır dosyalar)
"""
import importlib
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'content'))

import schemdraw  # noqa: E402
from circuitkit import elm, render, render_all  # noqa: E402
from render import render_problem, HEAD, SCRIPTS, TOPICS, esc  # noqa: E402

SIDE_NAMES = {1: "Maks. güç", 2: "Süperpozisyon", 3: "Düğüm / çevre", 4: "Güç dengesi"}
CONTENT_MODULES = ["q1", "q1b", "q1c", "q2", "q3a", "q3b", "q4a", "q4b"]
VER = time.strftime("%Y%m%d%H%M")

ICON = {
    "bolt": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 4.5 13.5H11l-1 8.5L19.5 10H13z"/></svg>',
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "moon": '<svg class="theme-ico-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z"/></svg>',
    "sun": '<svg class="theme-ico-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "coffee": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5z"/><path d="M17 10h1.5a2.5 2.5 0 0 1 0 5H17"/><path d="M8 3v2M12 3v2"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "check": '<svg viewBox="0 0 20 20"><path d="M5 10.5l3.2 3.2L15 7"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>',
}


# ---------------------------------------------------------------------------
# yardımcı semboller (Bölüm 0)
# ---------------------------------------------------------------------------
def _sym(fn):
    def draw(d):
        fn(d)
    return draw


SYMBOLS = {
    "sym-v": _sym(lambda d: (d.config(unit=1.4), d.add(elm.SourceV().up()))),
    "sym-i": _sym(lambda d: (d.config(unit=1.4), d.add(elm.SourceI().up()))),
    "sym-dv": _sym(lambda d: (d.config(unit=1.4), d.add(elm.SourceControlledV().up()))),
    "sym-di": _sym(lambda d: (d.config(unit=1.4), d.add(elm.SourceControlledI().up()))),
}


def load_problems():
    problems, circuits = [], {}
    for name in CONTENT_MODULES:
        try:
            mod = importlib.import_module(name)
        except ModuleNotFoundError:
            print(f"[uyarı] {name}.py yok, atlandı")
            continue
        problems.extend(mod.PROBLEMS)
        circuits.update(getattr(mod, "CIRCUITS", {}))
    return problems, circuits


# ---------------------------------------------------------------------------
# statik bölümler
# ---------------------------------------------------------------------------
FUNDAMENTALS = r'''
<section class="section prose" id="temel">
  <div class="section-head">
    <div class="section-kicker">BÖLÜM 0 · 15 DAKİKA</div>
    <h2>Sıfırdan başlayanlar için temel kurallar</h2>
    <p>Sınavdaki dört sorunun hepsi aynı birkaç kurala dayanıyor. Bu bölümü bitirmeden soru çözümlerine geçme —
    öğrencilerin çoğu formülü değil, <strong>işaretleri</strong> karıştırdığı için puan kaybediyor.</p>
  </div>

  <h3>1 · Yuvarlak kaynak mı, baklava kaynak mı?</h3>
  <div class="symbol-row">
    <div class="symbol"><img src="circuits/sym-v.svg" alt="" class="sym-img"><b>Bağımsız gerilim</b>değeri sabit: 110 V</div>
    <div class="symbol"><img src="circuits/sym-i.svg" alt="" class="sym-img"><b>Bağımsız akım</b>değeri sabit: 5 mA</div>
    <div class="symbol"><img src="circuits/sym-dv.svg" alt="" class="sym-img"><b>Bağımlı gerilim</b>içinde +/−: $3i_\Delta$, $4V_x$</div>
    <div class="symbol"><img src="circuits/sym-di.svg" alt="" class="sym-img"><b>Bağımlı akım</b>içinde ok: $0.1v_\Delta$, $2i_b$</div>
  </div>
  <p>Baklavanın değeri devrenin başka bir yerindeki bir büyüklüğe bağlıdır. Yanında $3i_\Delta$ yazsa bile içinde
  <strong>+/−</strong> varsa o bir <strong>gerilim</strong> kaynağıdır (birimi volt); içinde <strong>ok</strong> varsa
  <strong>akım</strong> kaynağıdır (birimi amper). Bilinmeyen sayısı artar; bu yüzden her bağımlı kaynak için bir
  <em>ek denklem</em> yazarız.</p>

  <div class="rule-grid">
    <div class="rule">
      <h4><span class="badge">2</span>Ohm yasası — yön kuralı</h4>
      <p>Bir dirençten geçen akım, akımın <strong>çıktığı</strong> düğümden <strong>vardığı</strong> düğüm çıkarılıp dirence bölünür.</p>
      <div class="math-display">\[ i_{a\to b} = \frac{V_a - V_b}{R} \]</div>
    </div>
    <div class="rule">
      <h4><span class="badge">3</span>KCL — düğüm denklemi</h4>
      <p>Bu sitede tek kural: düğümden <strong>çıkan</strong> akımlar $+$, düğüme <strong>giren</strong> akım kaynakları $-$ yazılır, toplam sıfır.</p>
      <div class="math-display">\[ \sum i_{\text{çıkan}} = 0 \]</div>
    </div>
    <div class="rule">
      <h4><span class="badge">4</span>KVL — çevre denklemi</h4>
      <p>Kapalı gözü saat yönünde dolaş. Bir elemana hangi işaretinden girersen o işareti yaz. Dirençte: kendi akımın eksi komşu gözün akımı.</p>
      <div class="math-display">\[ \sum v = 0, \qquad v_R = R\,(I_1 - I_2) \]</div>
    </div>
    <div class="rule">
      <h4><span class="badge">5</span>Ek denklem (tahtadaki “ek 1, ek 2”)</h4>
      <p>Bağımlı kaynağın kontrol değişkenini hemen düğüm gerilimleri (veya çevre akımları) cinsinden yaz.</p>
      <div class="math-display">\[ v_\Delta = V_{+} - V_{-}, \qquad i_\Delta = \frac{V_{\text{çıkış}} - V_{\text{varış}}}{R} \]</div>
    </div>
  </div>

  <h3>6 · Güç: alıyor mu, veriyor mu? (pasif işaret kuralı)</h3>
  <div class="board-photo" style="grid-template-columns:180px 1fr">
    <img class="zoomable" src="img/PASSIVE_ORIG.webp" alt="Pasif işaret kuralı" style="aspect-ratio:auto;object-fit:contain;background:#fff;padding:6px;filter:var(--img-filter)">
    <div>
      <p>Akım elemanın <strong>+</strong> ucundan giriyorsa $p = +v\,i$, <strong>−</strong> ucundan giriyorsa $p = -v\,i$.</p>
      <p style="margin-top:8px">$p > 0$ ise eleman güç <strong>harcar</strong> (emer), $p < 0$ ise güç <strong>üretir</strong> (verir).
      Dirençler her zaman harcar. Doğruluk kontrolü: tüm elemanlar için $\sum p = 0$.</p>
    </div>
  </div>

  <h3>7 · Açık devre ve kısa devre</h3>
  <div class="rule-grid">
    <div class="rule">
      <h4><span class="badge">oc</span>Açık devre (open circuit)</h4>
      <p>Uçlar arasında hiçbir şey yok: akım <strong>sıfır</strong>, gerilim herhangi bir değer olabilir. Yükü söktüğünde a–b arasında ölçtüğün gerilim $V_{oc} = V_{Th}$.</p>
    </div>
    <div class="rule">
      <h4><span class="badge">sc</span>Kısa devre (short circuit)</h4>
      <p>Uçlar düz telle bağlı: gerilim <strong>sıfır</strong>, akım herhangi bir değer olabilir. Bu telden geçen akım $I_{sc}$; $R_{Th} = V_{Th}/I_{sc}$.</p>
    </div>
  </div>

  <aside class="callout callout-tip" style="margin-top:22px">
    <div class="callout-title">Süperdüğüm ve süperçevre — bir cümlede</div>
    İki düğüm arasında <strong>yalnızca gerilim kaynağı</strong> varsa o iki düğümü tek bir “süperdüğüm” olarak düşün: KCL'yi ikisinin
    toplamı için yaz, ayrıca $V_a - V_b = $ kaynak gerilimi denklemini ekle. İki göz arasında <strong>akım kaynağı</strong> varsa
    “süperçevre” kur: KVL'yi iki gözün dış sınırı boyunca yaz, ayrıca $I_a - I_b = $ kaynak akımı denklemini ekle.
  </aside>
</section>
'''

TOPIC_INTRO = {
    1: dict(
        kicker="SINAV SORUSU 1 · 25 PUAN",
        title="Maksimum güç transferi (bağımlı kaynaklı)",
        lead="Tahtadaki 1. madde. Yükü (R<sub>o</sub> veya R<sub>L</sub>) sökersin, devrenin geri kalanını Thévenin eşdeğerine indirirsin. Bağımlı kaynak olduğu için kaynakları öldürüp direnç toplamak <strong>yasak</strong>.",
        recipe=["Yükü sök, kontrol değişkenleri için ek denklemleri yaz.",
                "Açık devre: düğüm analiziyle $V_{Th} = V_{ab}$.",
                "Kısa devre: a–b'yi birleştir, $I_{sc}$'yi bul.",
                "$R_L = R_{Th} = V_{Th}/I_{sc}$, &nbsp;$P_{max} = \\dfrac{V_{Th}^2}{4R_{Th}}$."],
        callout=("warn", "Devrede bağımsız kaynak yoksa",
                 "$V_{Th} = 0$ ve $I_{sc} = 0$ çıkar ($0/0$). Bu durumda a–b uçlarına kendin 1 V'luk test kaynağı bağla, çektiği akımı bul: $R_{Th} = 1/i_T$ (P4.79)."),
    ),
    2: dict(
        kicker="SINAV SORUSU 2 · 25 PUAN",
        title="Kaynak dönüşümü veya süperpozisyon",
        lead="Tahtadaki 2. madde. İki yöntemin de tek bir altın kuralı var ve öğrencilerin büyük kısmı tam o kuralı çiğnediği için puan kaybediyor.",
        recipe=["Süperpozisyon: bağımsız kaynakları birer birer bırak.",
                "Kapatılan gerilim kaynağı → kısa devre, akım kaynağı → açık devre.",
                "Bağımlı kaynaklar her alt devrede <strong>aynen kalır</strong>.",
                "Katkıları işaretleriyle topla: $v = v' + v''$."],
        callout=("danger", "İki altın kural",
                 "Süperpozisyonda <strong>bağımlı kaynak asla kapatılmaz</strong>. Kaynak dönüşümünde <strong>kontrol değişkeninin bulunduğu dala dokunulmaz</strong> (o direnç dönüşümle yok olursa $v_\\Delta$ veya $i_x$ da kaybolur)."),
    ),
    3: dict(
        kicker="SINAV SORUSU 3 · 25 PUAN",
        title="Düğüm gerilimleri veya çevre akımları",
        lead="Tahtadaki 3. madde. Önce hangi yöntemin daha az denklem vereceğine karar ver, sonra mekanik olarak yaz.",
        recipe=["Referans düğümü seç (genelde en çok elemanın bağlı olduğu alt tel).",
                "Bağımlı kaynakların kontrol değişkenlerini bilinmeyenler cinsinden yaz.",
                "Her bilinmeyen düğüm/göz için KCL/KVL; gerilim kaynağı varsa süperdüğüm.",
                "Çöz, istenen akım/gerilimleri ve gerekiyorsa güçleri hesapla."],
        callout=("tip", "Hangi yöntem?",
                 "Düğüm sayısı − 1 ile göz sayısını karşılaştır; azı kazanır. Çok sayıda akım kaynağı varsa düğüm, çok sayıda gerilim kaynağı varsa çevre yöntemi genelde kolaydır."),
    ),
    4: dict(
        kicker="SINAV SORUSU 4 · 25 PUAN",
        title="Güç hesabı ve güç dengesi",
        lead="Tahtadaki 4. madde: ilk üç bölümü içeren, güç hesabının da istendiği soru. Devreyi çöz, sonra her eleman için pasif işaret kuralını uygula.",
        recipe=["Bilinmeyen akım ve gerilimleri KCL/KVL/Ohm ile bul.",
                "Her eleman için akımın + uçtan girip girmediğine bak.",
                "$p = \\pm v i$; pozitif = harcar, negatif = üretir.",
                "Sağlama: $\\sum p = 0$. Tutmuyorsa bir işaret yanlıştır."],
        callout=("tip", "Puanı garantileyen alışkanlık",
                 "Güçleri bir tabloya yaz: eleman · $v$ · $i$ · işaret · $p$. Hoca sonucu tablodan bir bakışta kontrol eder, sen de $\\sum p = 0$ ile hatanı kendin yakalarsın."),
    ),
}

CHEAT = r'''
<div class="overlay" id="cheat" role="dialog" aria-modal="true" aria-labelledby="cheatTitle">
  <div class="modal">
    <div class="modal-head"><h2 id="cheatTitle">Son gece 5 dakikalık özet</h2>
      <button class="icon-btn" data-close aria-label="Kapat">{close}</button></div>
    <div class="modal-body">
      <div class="cheat-grid">
        <div class="cheat" style="--c:#0EA5E9">
          <h3><span>01</span>Maksimum güç</h3>
          <div class="math-display">\[ R_L = R_{Th} = \frac{V_{Th}}{I_{sc}}, \qquad P_{max} = \frac{V_{Th}^2}{4R_{Th}} \]</div>
          <div class="golden">Bağımsız kaynak yoksa: 1 V test kaynağı, $R_{Th} = 1/i_T$.</div>
        </div>
        <div class="cheat" style="--c:#10B981">
          <h3><span>02</span>Kaynak dönüşümü</h3>
          <div class="math-display">\[ v_s \text{ seri } R \;\Longleftrightarrow\; i_s = \frac{v_s}{R} \text{ paralel } R \]</div>
          <div class="golden">Kontrol değişkeninin bulunduğu dala dokunma. Akım okunun ucu + kutbu gösterir.</div>
        </div>
        <div class="cheat" style="--c:#F59E0B">
          <h3><span>03</span>Süperpozisyon</h3>
          <ul><li>Gerilim kaynağı kapalı → kısa devre</li><li>Akım kaynağı kapalı → açık devre</li><li>Sonuç: $v = v' + v''$ (işaretli topla)</li></ul>
          <div class="golden">Bağımlı kaynak asla kapatılmaz.</div>
        </div>
        <div class="cheat" style="--c:#EC4899">
          <h3><span>04</span>Pasif işaret &amp; güç</h3>
          <div class="math-display">\[ p = \begin{cases} +vi & \text{akım + uçtan giriyor} \\ -vi & \text{akım − uçtan giriyor} \end{cases} \]</div>
          <div class="golden">$p&gt;0$ harcar, $p&lt;0$ üretir. Her zaman $\sum p = 0$.</div>
        </div>
        <div class="cheat" style="--c:#6366F1">
          <h3><span>05</span>Düğüm analizi</h3>
          <ul><li>Çıkan akımlar $+$, giren kaynak akımları $-$</li><li>$i = (V_{\text{çıkış}} - V_{\text{varış}})/R$</li><li>Arada sadece gerilim kaynağı → süperdüğüm</li></ul>
        </div>
        <div class="cheat" style="--c:#14B8A6">
          <h3><span>06</span>Sınav kağıdı düzeni</h3>
          <ul><li>Sağ üste: ek 1, ek 2 (kontrol değişkenleri)</li><li>Denklemleri numarala: (I), (II)</li><li>Sonuçları kutu içine al, birim yaz</li></ul>
        </div>
      </div>
    </div>
  </div>
</div>
'''


def topic_section(t, probs, start_no):
    meta = TOPIC_INTRO[t]
    recipe = "".join(f"<div>{r}</div>" for r in meta["recipe"])
    kind, ctitle, ctext = meta["callout"]
    cards = "".join(render_problem(p, start_no + i) for i, p in enumerate(probs))
    return f'''
<section class="section" id="soru{t}">
  <div class="section-head">
    <div class="section-kicker">{meta["kicker"]}</div>
    <h2>{meta["title"]}</h2>
    <p>{meta["lead"]}</p>
  </div>
  <div class="topic-recipe">{recipe}</div>
  <aside class="callout callout-{kind} glass"><div class="callout-title">{ctitle}</div>{ctext}</aside>
  <div class="problem-list">{cards}</div>
</section>'''


def sidebar(by_topic):
    out = ['<nav class="sidebar" aria-label="İçindekiler">']
    out.append('<div class="side-group"><div class="side-label">Başlangıç</div>'
               '<a class="side-link" href="#giris">Sınav formatı</a>'
               '<a class="side-link" href="#temel">Temel kurallar</a></div>')
    for t in (1, 2, 3, 4):
        short, long_ = TOPICS[t]
        out.append(f'<div class="side-group"><div class="side-label"><span>{short} · {SIDE_NAMES[t]}</span>'
                   f'<span class="side-count" data-topic-count="{t}"></span></div>')
        out.append(f'<a class="side-link" href="#soru{t}">Konu özeti</a>')
        for p in by_topic[t]:
            plain = p["title"].replace("$", "")
            out.append(
                f'<a class="side-link" href="#{esc(p["id"])}" data-pid="{esc(p["id"])}" '
                f'data-search="{esc((p["code"] + " " + plain).lower())}" title="{esc(plain)}">'
                f'<span class="dot">{ICON["check"]}</span><span>{esc(p["code"])}</span></a>')
        out.append('</div>')
    out.append('<div class="side-group"><div class="side-label">Pratik</div>'
               '<a class="side-link" href="#deneme">Deneme sınavları</a>'
               '<a class="side-link" href="#" onclick="document.getElementById(\'cheatBtn\').click();return false;">Son gece özeti</a></div>')
    out.append('<div class="side-group" style="padding:0 10px"><button class="btn btn-ghost" id="resetProgress" style="width:100%;height:34px;font-size:.82rem">İlerlemeyi sıfırla</button></div>')
    out.append('</nav>')
    return "".join(out)


def header():
    return f'''
<div class="read-progress"><span id="readBar"></span></div>
<header class="site-header">
  <button class="icon-btn menu-btn" id="menuBtn" aria-label="Menü">{ICON["menu"]}</button>
  <a class="brand" href="#giris"><span class="brand-mark">{ICON["bolt"]}</span>Devre Analizi I <small>· Vize Rehberi</small></a>
  <div class="header-spacer"></div>
  <label class="search">{ICON["search"]}<input id="search" type="search" placeholder="Soru ara: P4.88, süperdüğüm…" autocomplete="off"><kbd>/</kbd></label>
  <div class="ring" title="Vizeye hazırlık oranın">
    <svg viewBox="0 0 30 30"><circle class="ring-bg" cx="15" cy="15" r="12"/><circle class="ring-fg" id="ringFg" cx="15" cy="15" r="12"/></svg>
    <span class="ring-label">Hazırlık</span> <b data-progress-text>%0</b>
  </div>
  <button class="hdr-btn" id="cheatBtn">{ICON["coffee"]}<span class="lbl">Son gece özeti</span></button>
  <button class="icon-btn" id="themeBtn" aria-label="Tema değiştir">{ICON["moon"]}{ICON["sun"]}</button>
</header>'''


def hero(by_topic):
    cards = []
    for t in (1, 2, 3, 4):
        short, long_ = TOPICS[t]
        codes = ", ".join(p["code"] for p in by_topic[t][:5]) + (" …" if len(by_topic[t]) > 5 else "")
        cards.append(f'''
      <a class="exam-card" href="#soru{t}">
        <span class="pts">25 puan</span>
        <span class="n">{short.upper()}</span>
        <h3>{long_}</h3>
        <p>{len(by_topic[t])} çözümlü soru · {esc(codes)}</p>
        <div class="bar"><span data-topic-bar="{t}"></span></div>
      </a>''')
    return f'''
<section class="hero" id="giris">
  <div class="eyebrow"><i></i>Tuna Göksu · Vize · 4 klasik soru, hepsi bağımlı kaynaklı</div>
  <h1>Devre Analizi I vizesine<br><span class="grad">sıfırdan, adım adım</span> hazırlan.</h1>
  <p class="lead">Hocanın tahtaya yazdığı dört soru tipinin her biri için çalışma yapraklarındaki tüm bağımlı kaynaklı sorular:
  tek bir cebir adımı atlanmadan, kitap kalitesinde şemalarla ve sınav kağıdına aynen yazabileceğin formatta.</p>
  <div class="hero-actions">
    <a class="btn btn-primary btn-lg" href="#temel">Sıfırdan başla</a>
    <a class="btn btn-ghost btn-lg" href="#p4-87">Tahtadaki soruya git</a>
    <a class="btn btn-ghost btn-lg" href="#deneme">Deneme çöz</a>
  </div>
  <div class="exam-map">{"".join(cards)}</div>
  <div class="board-photo">
    <img class="zoomable" src="img/WHITEBOARD_PHOTO.webp" alt="Sınıf tahtası: sınavın 4 sorusu">
    <p><strong>Tahtadan:</strong> “1- Maksimum güç transferi (bağımlı kaynak içeren devrede) · 2- Kaynak dönüşümü veya süperpozisyon sorusu ·
    3- Analiz sorusu, düğüm gerilimleri veya çevre akımları · 4- 1, 2 ve 3. bölümü içeren, güç hesapları da olan bir soru.”
    Üstte P4.87'nin çözümüne ait <em>ek 1</em> ve <em>ek 2</em> satırları görülüyor. Büyütmek için fotoğrafa tıkla.</p>
  </div>
</section>'''


def mock_section(by_topic):
    mocks = []
    names = ["Tahta provası", "Karma deneme", "Zorlayıcı deneme", "Tekrar denemesi", "Genel prova"]
    for k in range(5):
        items = []
        for t in (1, 2, 3, 4):
            lst = by_topic[t]
            if lst:
                items.append(lst[k % len(lst)]["id"])
        mocks.append(dict(title=f"Deneme {k + 1} — {names[k]}",
                          desc="4 soru · 90 dakika · her soru 25 puan", items=items))
    import json
    return f'''
<section class="section" id="deneme">
  <div class="section-head">
    <div class="section-kicker">PRATİK · SINAV SİMÜLASYONU</div>
    <h2>Deneme sınavları</h2>
    <p>Gerçek sınav formatında: dört klasik soru, 90 dakika. Süreyi başlat, kağıda çöz, sonra cevapları açıp kendine puan ver.
    Takıldığın soruda “tam çözüme git” bağlantısı seni adım adım anlatıma götürür.</p>
  </div>
  <div id="mock">
    <div class="seg mock-tabs" id="mockTabs"></div>
    <div class="mock-shell" id="mockShell"></div>
  </div>
</section>
<script>window.MOCKS = {json.dumps(mocks, ensure_ascii=False)};</script>'''


def build():
    problems, circuits = load_problems()
    render_all(circuits)
    render_all(SYMBOLS)
    print(f"{len(problems)} problem, {len(circuits)} şema")

    by_topic = {t: [p for p in problems if p["topic"] == t] for t in (1, 2, 3, 4)}
    body = [header(), '<div class="layout">', sidebar(by_topic),
            '<main class="main"><div class="content">', hero(by_topic), FUNDAMENTALS]
    n = 1
    for t in (1, 2, 3, 4):
        body.append(topic_section(t, by_topic[t], n))
        n += len(by_topic[t])
    body.append(mock_section(by_topic))
    body.append('''<footer class="site-footer">Devre Analizi I · Tuna Göksu vize hazırlık notları. Kaynak: Nilsson &amp; Riedel,
      <em>Electric Circuits</em> ve ders çalışma yaprakları. İlerlemen yalnızca bu tarayıcıda saklanır.</footer>''')
    body.append('</div></main></div>')
    body.append(CHEAT.replace("{close}", ICON["close"]))
    body.append('<div class="overlay" id="lightbox" role="dialog" aria-modal="true"><div data-lb-close style="text-align:center">'
                '<img id="lightboxImg" class="lightbox-img" alt=""><div class="lightbox-cap" id="lightboxCap"></div></div></div>')
    body.append('<div class="toast" id="toast" role="status" aria-live="polite"></div><canvas id="confetti"></canvas>')

    html = HEAD.format(title="Devre Analizi I — Vize Rehberi (Tuna Göksu)", ver=VER) + "<body>" + "".join(body) + SCRIPTS.format(ver=VER)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html yazıldı:", round(len(html.encode('utf-8')) / 1024), "KB")


if __name__ == "__main__":
    build()
