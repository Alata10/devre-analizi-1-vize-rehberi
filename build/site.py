# -*- coding: utf-8 -*-
"""
Siteyi üretir:  python build/site.py
Çıktı: index.html + circuits/*.svg  (assets/, img/ hazır dosyalar)
"""
import importlib
import json
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

SIDE_NAMES = {
    4: "1. Kademe · Güç & Temel",
    3: "2. Kademe · Düğüm & Çevre",
    2: "3. Kademe · Dönüşüm & Süper.",
    1: "4. Kademe · Maks. Güç",
}
# Varsayılan öğrenme sırası: Kolaydan Zora (4 -> 3 -> 2 -> 1)
TOPIC_ORDER_EASY = (4, 3, 2, 1)
CONTENT_MODULES = ["q1", "q1b", "q1c", "q2", "q3a", "q3b", "q4a", "q4b"]
VER = time.strftime("%Y%m%d%H%M")

# Her konu içinde kolaydan zora pedagojik sıra ve seviye (1: Kolay, 2: Orta, 3: Zor)
PROBLEM_ORDER = {
    4: [
        ("p2-1", 1),
        ("p2-2", 1),
        ("p2-18", 1),
        ("p2-15", 1),
        ("p2-10", 1),
        ("p2-32", 1),
        ("fig2-23", 2),
        ("p2-9", 2),
        ("p2-37", 2),
        ("p2-36", 3),
    ],
    3: [
        ("cy2-s2-d2", 1),
        ("cy2-s2-d1", 1),
        ("cy2-s1-d6", 1),
        ("cy2-s2-d3", 2),
        ("cy2-s2-d4", 2),
        ("p4-48", 2),
        ("p4-42", 2),
        ("cy2-s2-d5", 3),
        ("p4-52", 3),
        ("p4-53", 3),
    ],
    2: [
        ("p4-59", 1),
        ("p4-60", 1),
        ("p4-97", 2),
        ("p4-98", 2),
        ("p4-56", 3),
    ],
    1: [
        ("p5-119", 1),
        ("p4-79", 2),
        ("p4-87", 2),
        ("p4-88", 2),
        ("p5-117", 2),
        ("p4-89", 3),
        ("p4-90", 3),
        ("p4-91", 3),
    ],
}

TIER_META = {
    1: (
        "1. AŞAMA · KOLAY (TEMEL ISINMA SORULARI)",
        "Konunun mantığını ve işaret kurallarını oturtmak için en sade devrelerden başlıyoruz.",
        "easy",
    ),
    2: (
        "2. AŞAMA · ORTA SEVİYE (KLASİK VİZE SORULARI)",
        "Tuna Hoca'nın sınavda doğrudan sormayı sevdiği standart zorluktaki bağımlı kaynaklı sorular.",
        "med",
    ),
    3: (
        "3. AŞAMA · ZOR SEVİYE (İLERİ DÜZEY & ÇOKLU BAĞIMLI KAYNAK)",
        "Süperdüğüm, süperçevre ve birden fazla bağımlı kaynak içeren, 100'ü garantileyen sorular.",
        "hard",
    ),
}

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


def sort_by_topic(problems):
    by_id = {p["id"]: dict(p) for p in problems}
    by_topic = {}
    for t in (1, 2, 3, 4):
        ordered = []
        seen = set()
        for pid, lvl in PROBLEM_ORDER.get(t, []):
            if pid in by_id:
                item = by_id[pid]
                item["level"] = lvl
                ordered.append(item)
                seen.add(pid)
        for p in problems:
            if p["topic"] == t and p["id"] not in seen:
                ordered.append(dict(p))
        by_topic[t] = ordered
    return by_topic


# ---------------------------------------------------------------------------
# BÖLÜM 0: GENEL TANIMLAR VE NELERE DİKKAT ETMEK LAZIM?
# ---------------------------------------------------------------------------
FUNDAMENTALS = r'''
<section class="section prose" id="temel">
  <div class="section-head">
    <div class="section-kicker">BÖLÜM 0 · GENEL TANIMLAR VE ALTIN KURALLAR</div>
    <h2>Sıfırdan başlayanlar için genel tanımlar ve dikkat edilecek noktalar</h2>
    <p>Hiç temelinin olmadığını varsayarak önce sınavda kullanacağımız <strong>tüm kavramların genel tanımını</strong>,
    ardından da sınavda öğrencilerin en çok puan kaybettiği <strong>dikkat edilmesi gereken noktaları</strong> tek tek açıklıyoruz.
    Sorulara geçmeden önce bu sayfayı mutlaka oku.</p>
  </div>

  <h3>1 · Temel devre kavramları (Düğüm, Kol ve Çevre nedir?)</h3>
  <div class="rule-grid">
    <div class="rule">
      <h4><span class="badge">A</span>Düğüm (Node) ve Esas Düğüm</h4>
      <p><strong>Genel tanım:</strong> İki veya daha fazla devre elemanının uçlarının birleştiği bağlantı noktasına <strong>düğüm</strong> denir.
      Üç veya daha fazla kolun birleştiği noktalara ise <strong>esas düğüm (essential node)</strong> denir. Arada hiçbir eleman olmadan düz telle bağlı noktalar <em>tek ve aynı düğümdür</em>.</p>
    </div>
    <div class="rule">
      <h4><span class="badge">B</span>Referans Düğüm (Toprak / 0 V)</h4>
      <p><strong>Genel tanım:</strong> Düğüm gerilimleri yönteminde potansiyelini $0\ \text{V}$ kabul ettiğimiz düğümdür ($\perp$ sembolü).
      Genellikle devrenin en altındaki uzun ortak tel referans seçilir; diğer her düğümün gerilimi ($V_1, V_2$) bu alt tele göre ölçülür.</p>
    </div>
    <div class="rule">
      <h4><span class="badge">C</span>Kol (Branch)</h4>
      <p><strong>Genel tanım:</strong> İki düğüm arasında yer alan ve içinden <strong>aynı tek akımın</strong> geçtiği seri elemanlar dizisidir.
      Bir kolda direnç ile akım kaynağı seri bağlıysa, o kolun akımı doğrudan akım kaynağının değerine eşittir!</p>
    </div>
    <div class="rule">
      <h4><span class="badge">D</span>Çevre (Loop) ve Göz (Mesh)</h4>
      <p><strong>Genel tanım:</strong> Bir düğümden başlayıp hiçbir düğümden iki kez geçmeden başlangıç noktasına dönen kapalı yola <strong>çevre</strong>;
      içinde başka hiçbir iç pencere barındırmayan en küçük kapalı pencerelere ise <strong>göz (mesh)</strong> denir.</p>
    </div>
  </div>

  <h3>2 · Bağımsız kaynak (yuvarlak) ve Bağımlı kaynak (baklava) nedir?</h3>
  <div class="symbol-row">
    <div class="symbol"><img src="circuits/sym-v.svg" alt="" class="sym-img"><b>Bağımsız gerilim kaynağı</b>Değeri sabittir: $110\ \text{V}$, $25\ \text{V}$</div>
    <div class="symbol"><img src="circuits/sym-i.svg" alt="" class="sym-img"><b>Bağımsız akım kaynağı</b>Değeri sabittir: $5\ \text{mA}$, $19\ \text{A}$</div>
    <div class="symbol"><img src="circuits/sym-dv.svg" alt="" class="sym-img"><b>Bağımlı gerilim kaynağı</b>İçinde $+/−$ vardır: $3i_\Delta$, $4V_x$</div>
    <div class="symbol"><img src="circuits/sym-di.svg" alt="" class="sym-img"><b>Bağımlı akım kaynağı</b>İçinde ok vardır: $0.1v_\Delta$, $2i_b$</div>
  </div>
  <div class="callout callout-plan" style="margin-top:14px">
    <div class="callout-title">Genel tanım — Bağımlı kaynağı nasıl okursun?</div>
    <ul>
      <li><strong>Şekline bak:</strong> Daire ise <strong>bağımsız</strong> (değeri dışarıdan sabit verilmiş), baklava (eşkenar dörtgen) ise <strong>bağımlı</strong> (değeri devrenin başka bir yerindeki $v_\Delta$ veya $i_\Delta$'ya bağlı) kaynaktır.</li>
      <li><strong>İçindeki işarete bak (yanındaki harfe değil!):</strong> Baklavanın yanında $3i_\Delta$ yazsa bile, baklavanın <strong>içinde $+/−$ işareti varsa bu bir GERİLİM kaynağıdır</strong> (birimi Volt'tur). Baklavanın <strong>içinde OK varsa bu bir AKIM kaynağıdır</strong> (birimi Amper'dir).</li>
      <li><strong>Ek denklem kuralı:</strong> Devrede kaç tane bağımlı kaynak varsa, o kaynakların kontrol değişkenlerini ($v_\Delta, i_\Delta, i_\phi, v_x$) düğüm gerilimleri veya çevre akımları cinsinden yazan <strong>ek denklem</strong> (Tuna Hoca'nın tahtada <em>ek 1, ek 2</em> dediği satırlar) en başta kağıdın sağ üstüne yazılır.</li>
    </ul>
  </div>

  <h3>3 · Dört temel denklem kuralı (Ohm, KCL, KVL ve Güç)</h3>
  <div class="rule-grid">
    <div class="rule">
      <h4><span class="badge">1</span>Ohm Yasası — Direnç Akımının Yönü</h4>
      <p>Bir $R$ direncinden $a$ düğümünden $b$ düğümüne doğru geçen akım, <strong>akım okunun çıktığı düğümün geriliminden vardığı düğümün gerilimi çıkarılıp</strong> dirence bölünmesiyle bulunur:</p>
      <div class="math-display">\[ i_{a\to b} = \frac{V_a - V_b}{R}, \qquad v_R = V_{+} - V_{-} \]</div>
    </div>
    <div class="rule">
      <h4><span class="badge">2</span>Kirchhoff Akımlar Yasası (KCL)</h4>
      <p>Bir düğümden <strong>çıkan akımların</strong> cebirsel toplamı sıfırdır. Bu rehberde kafa karışıklığını önlemek için tek standart kullanıyoruz: <strong>Düğümden çıkan kollar $+$, düğüme giren kaynaklar $-$ alınır:</strong></p>
      <div class="math-display">\[ \sum i_{\text{çıkan}} = 0 \implies \frac{V_1 - V_2}{R} + i_{\text{çıkan kaynak}} - i_{\text{giren kaynak}} = 0 \]</div>
    </div>
    <div class="rule">
      <h4><span class="badge">3</span>Kirchhoff Gerilimler Yasası (KVL)</h4>
      <p>Kapalı bir gözde saat yönünde dolaşırken elemanların gerilim düşümlerinin toplamı sıfırdır. Kaynağa $+$ uçtan girersen $+V$, $-$ uçtan girersen $-V$; ortak dirençte ise $R(I_{\text{kendi}} - I_{\text{komşu}})$ yazılır:</p>
      <div class="math-display">\[ \sum v = 0, \qquad v_{\text{ortak direnç}} = R\,(I_{\text{kendi}} - I_{\text{komşu}}) \]</div>
    </div>
    <div class="rule">
      <h4><span class="badge">4</span>Pasif İşaret Kuralı ve Güç Dengesi</h4>
      <p>Akım elemanın <strong>$+$ kutbundan içeri giriyorsa</strong> $p = +v\cdot i$; <strong>$-$ kutbundan içeri giriyorsa</strong> (veya $+$ kutbundan çıkıyorsa) $p = -v\cdot i$ yazılır:</p>
      <div class="math-display">\[ p > 0 \implies \text{Güç harcar (emer)}, \qquad p < 0 \implies \text{Güç üretir (verir)}, \qquad \sum_{\text{tüm devre}} p = 0 \]</div>
    </div>
  </div>

  <div class="board-photo" style="grid-template-columns:180px 1fr; margin-top:16px">
    <img class="zoomable" src="img/PASSIVE_ORIG.webp" alt="Pasif işaret kuralı" style="aspect-ratio:auto;object-fit:contain;background:#fff;padding:6px;filter:var(--img-filter)">
    <div>
      <p><strong>Pasif İşaret Kuralı Özeti:</strong> Dirençlerin gücü her zaman pozitiftir ($p_R = i^2 R = v^2 / R > 0$, daima güç harcar).
      Bağımsız veya bağımlı kaynaklar ise akımın yönüne göre <strong>güç üretebilir ($p < 0$) veya güç harcayabilir ($p > 0$)</strong>.
      Sınavda sağlamayı her zaman $\sum P_{\text{üretilen}} = \sum P_{\text{harcanan}}$ ($\sum p = 0$) ile yap!</p>
    </div>
  </div>

  <h3 id="dikkat">4 · Sınavda nelere dikkat etmek lazım? (En çok puan kaybettiren 8 ölümcül hata)</h3>
  <aside class="callout callout-danger">
    <div class="callout-title">Sınavda kalemi oynatmadan önce bu 8 maddeyi ezbere bil!</div>
    <ol>
      <li><strong>Kontrol akımının ($i_\Delta, i_\phi, i_b$) ok yönüne dikkat et:</strong> Öğrencilerin yarısı alışkanlıkla her yatay dirençte $i_\Delta = (V_1 - V_2)/R$ yazar. Oysa <strong>P4.87, P4.97 ve P4.53</strong> sorularında ok <strong>sağdan sola</strong> ($V_2 \to V_1$) bakar! Ok sola bakıyorsa $i_\Delta = (V_2 - V_1)/R$ yazmak zorundasın.</li>
      <li><strong>Gerilim kaynaklarının $+/−$ kutbuna dikkat et:</strong> Dikey bir gerilim kaynağının $+$ ucu her zaman üstte olmaz! Örneğin <strong>P4.87</strong>'de $3i_\Delta$ kaynağının $+$ ucu alttadır; <strong>P4.53</strong> ve <strong>P4.42</strong>'de sağdaki kaynakların $-$ ucu üsttedir ($V_3 = -240\ \text{V}$).</li>
      <li><strong>Bağımlı kaynak varken dirençleri seri/paralel toplayıp $R_{Th}$ bulmaya çalışma:</strong> Devrede bağımlı kaynak varsa kaynakları kapatıp eşdeğer direnç bulmak <strong>kesinlikle yasaktır</strong>. Her zaman $R_{Th} = \dfrac{V_{Th}}{I_{sc}}$ (veya bağımsız kaynak yoksa $1\ \text{V}$ test kaynağı) kullanılır.</li>
      <li><strong>Süperpozisyonda bağımlı kaynağı ASLA kapatma:</strong> Süperpozisyonda yalnızca <em>bağımsız</em> kaynaklar sırayla kapatılır (gerilim kaynağı $\to$ kısa devre, akım kaynağı $\to$ açık devre). Baklava şeklindeki bağımlı kaynaklar her alt devrede çalışmaya devam eder.</li>
      <li><strong>Kaynak dönüşümünde kontrol değişkeninin olduğu dala DOKUNMA:</strong> Üzerinde $v_\Delta$ veya $i_x$ tanımlı olan direnci başka bir dirençle birleştirirsen kontrol değişkenini yok edersin. Yan kolları dönüştür, kontrol dalını koru!</li>
      <li><strong>Maksimum güç formülündeki $4$ çarpanını unutma:</strong> Maksimum güç transferi şartı $R_L = R_{Th}$'dir ve aktarılan güç $P_{\max} = \dfrac{V_{Th}^2}{\mathbf{4}\,R_{Th}}$'dir (paydada $4$ vardır, çünkü gerilimin yarısı yükte, yarısı iç dirençte düşer).</li>
      <li><strong>$\text{k}\Omega$ ve $\text{mA}$ birim uyumuna dikkat et:</strong> Dirençler $\text{k}\Omega$ ($10^3\ \Omega$) ise akımı $\text{mA}$ ($10^{-3}\ \text{A}$) aldığında $10^3 \times 10^{-3} = 1$ birbirini götürür ($\text{mA} \times \text{k}\Omega = \text{V}$). Ancak güç hesaplarken $I^2 R$ yaparsan $(\text{mA})^2 \times \text{k}\Omega = \text{mW}$ ($10^{-3}\ \text{W}$) çıkar!</li>
      <li><strong>Payda eşitlerken sabit sayıyı çarpmayı unutma:</strong> Örneğin $\dfrac{V_1}{40} + \dfrac{V_1 - V_2}{5} - 19 = 0$ denklemini $40$ ile çarparken sadece kesirleri değil, $-19$ sayısını da $40$ ile çarparak $-760$ yazmayı unutma!</li>
    </ol>
  </aside>
</section>
'''


# ---------------------------------------------------------------------------
# KONU ANLATIMLARI (GENEL TANIM + YÖNTEM + NELERE DİKKAT ETMELİ)
# ---------------------------------------------------------------------------
TOPIC_INTRO = {
    4: dict(
        kicker="1. KADEME (BAŞLANGIÇ · KOLAYDAN ZORA) · TAHTADAKİ 4. SORU (25 PUAN)",
        title="Temel Yasalar, Güç Hesabı ve Güç Dengesi (∑p = 0)",
        lead=(
            "Neden buradan başlıyoruz? Çünkü sınavdaki diğer tüm konular (düğüm analizi, süperpozisyon, Thévenin) "
            "buradaki Ohm yasası, KCL, KVL ve pasif işaret kuralı üzerine kuruludur. En kolay 1 gözlü devrelerden başlayıp "
            "çok kademeli güç dengesi sorularına doğru adım adım ilerliyoruz."
        ),
        definition=r'''
        <div class="theory-box">
          <h4>📘 Genel Tanım: Güç Hesabı ve Tellegen Teoremi ($\sum p = 0$) Nedir?</h4>
          <p>Bir devre elemanının uçları arasındaki gerilim $v$ ve içinden geçen akım $i$ ise, o elemanın anlık gücü $p = \pm v \cdot i$ bağıntısıyla bulunur.
          <strong>Pasif İşaret Kuralı (Passive Sign Convention):</strong></p>
          <ul>
            <li>Akım oku elemanın <strong>$+$ kutbundan içeri giriyorsa:</strong> $p = +v \cdot i$ yazılır. Sonuç <strong>pozitif ($p > 0$)</strong> çıkarsa eleman devreden enerji <strong>alıyor (güç harcıyor / emiyor)</strong> demektir.</li>
            <li>Akım oku elemanın <strong>$-$ kutbundan içeri giriyorsa (yani $+$ kutbundan çıkıyorsa):</strong> $p = -v \cdot i$ yazılır. Sonuç <strong>negatif ($p < 0$)</strong> çıkarsa eleman devreye enerji <strong>veriyor (güç üretiyor)</strong> demektir.</li>
            <li><strong>Dirençler:</strong> Her zaman güç harcar ($p_R = i^2 R = \dfrac{v^2}{R} \ge 0$).</li>
            <li><strong>Enerjinin Korunumu (Güç Dengesi):</strong> Kapalı bir devrede üretilen toplam güç, harcanan toplam güce birebir eşittir: $\sum P_{\text{üretilen}} = \sum P_{\text{harcanan}}$ yani tüm elemanların işaretli güçleri toplamı $\boxed{\sum p = 0}$ olmak zorundadır.</li>
          </ul>
        </div>
        ''',
        recipe=[
            "Önce devredeki bilinmeyen düğüm gerilimlerini ve kol akımlarını KCL / KVL / Ohm yasası ile bul.",
            "Her eleman için akımın $+$ uçtan mı yoksa $-$ uçtan mı girdiğini tek tek kontrol et.",
            "$+$ uçtan giriyorsa $p = +vi$, $+$ uçtan çıkıyorsa $p = -vi$ hesapla (dirençlerde doğrudan $i^2 R$).",
            "En sonda tüm elemanların güçlerini toplayarak $\\sum p = 0$ sağlamasını sınav kağıdında göster.",
        ],
        watchout=[
            "<strong>Akım kaynağının uç gerilimi sıfır değildir!</strong> Akım kaynağının gücü bulunurken, bağlı olduğu iki düğüm arasındaki gerilim farkı ($V_A - V_B$) hesaplanıp kaynak akımıyla çarpılır.",
            "<strong>Gerilim kaynağının akımı KCL ile bulunur:</strong> Gerilim kaynağının içinden geçen akımı Ohm yasasıyla ($V/R$) bulamazsın; kaynağın bağlı olduğu düğümde KCL yazarak bulursun.",
            "<strong>Bağımlı kaynaklar da güç emebilir:</strong> Baklava kaynakların her zaman güç ürettiğini sanma; $p > 0$ çıkarsa o bağımlı kaynak güç harcıyordur.",
        ],
    ),
    3: dict(
        kicker="2. KADEME (TEMEL ANALİZ) · TAHTADAKİ 3. SORU (25 PUAN)",
        title="Düğüm Gerilimleri (Süperdüğüm) ve Çevre Akımları (Süperçevre)",
        lead=(
            "Temel KCL ve KVL kurallarını öğrendikten sonra, çok düğümlü ve çok gözlü devreleri sistematik olarak çözmeyi öğreniyoruz. "
            "Önce tek/iki düğümlü kolay sorulardan başlayıp, sınavın kilit noktası olan Süperdüğüm (Supernode) ve Süperçevre (Supermesh) sorularına geçiyoruz."
        ),
        definition=r'''
        <div class="theory-box">
          <h4>📘 Genel Tanım: Düğüm Gerilimleri ve Çevre Akımları Yöntemi Nedir?</h4>
          <ul>
            <li><strong>Düğüm Gerilimleri Yöntemi (Node-Voltage Method):</strong> Devredeki alt ortak teli referans ($0\ \text{V}$) seçip, kalan her esas düğüme bir gerilim ismi ($V_1, V_2, \dots$) veririz. Her düğümden <em>çıkan kol akımlarının toplamını sıfıra eşitleyerek</em> ($\sum i_{\text{çıkan}} = 0$) denklem sistemini kurarız.</li>
            <li><strong>Süperdüğüm (Supernode) Nedir?</strong> Referans olmayan iki düğüm ($V_1$ ve $V_2$) arasında <strong>dirençsiz bir gerilim kaynağı</strong> (bağımsız veya bağımlı) varsa, o gerilim kaynağının içinden geçen akımı Ohm yasasıyla yazamayız. Bu yüzden iki düğümü ve aradaki kaynağı <strong>kesikli bir kapsül içine alıp tek bir büyük düğüm (süperdüğüm)</strong> gibi düşünürüz:
              <br>1) Kapsülün dışına çıkan tüm kolların KCL toplamını sıfıra eşitleriz.
              <br>2) Kapsülün içindeki kaynak için $V_{+} - V_{-} = V_{\text{kaynak}}$ kısıtlama denklemini yazarız.</li>
            <li><strong>Çevre Akımları Yöntemi (Mesh-Current Method):</strong> Her pencereye (göze) saat yönünde dönen bir çevre akımı ($i_1, i_2, \dots$) atarız. Her gözde saat yönünde KVL ($\sum v = 0$) yazarız; iki gözün ortak direncinden geçen net akım $(i_{\text{kendi}} - i_{\text{komşu}})$ olur.</li>
            <li><strong>Süperçevre (Supermesh) Nedir?</strong> İki komşu gözün ($i_2$ ve $i_3$) ortak kolunda bir <strong>akım kaynağı</strong> varsa, o akım kaynağının uç gerilimini bilmediğimiz için ortak kolu atlayıp iki gözün <strong>dış çevresi boyunca tek bir KVL (süperçevre)</strong> yazarız; ayrıca $i_{\text{aynı yön}} - i_{\text{ters yön}} = I_{\text{kaynak}}$ kısıt denklemini ekleriz.</li>
          </ul>
        </div>
        ''',
        recipe=[
            "Sağ üste bağımlı kaynakların kontrol değişkenlerini ($v_\\Delta, i_\\Delta$) düğüm gerilimleri veya çevre akımları cinsinden yaz (ek 1, ek 2).",
            "Düğüm analizinde: referansa bağlı gerilim kaynağı varsa o düğümün gerilimini doğrudan sabitle (örn. $V_3 = -240\\ \\text{V}$).",
            "Çevre analizinde: dış kolda akım kaynağı varsa o gözün çevre akımını doğrudan sabitle (örn. $i_3 = -1.7v_\\Delta$).",
            "KCL/KVL denklemlerini en küçük ortak katla (EKOK) çarparak kesirlerden kurtul ve tam sayı katsayılarla çöz.",
        ],
        watchout=[
            "<strong>Kenar düğüm / kenar göz kısayolunu kaçırma:</strong> Bir gerilim kaynağının bir ucu referansta (toprakta) ise o düğüm için KCL yazılmaz, gerilimi zaten bellidir! Aynı şekilde dış kolda akım kaynağı varsa o göze KVL yazılmaz, çevre akımı zaten bellidir!",
            "<strong>Dirençle seri bağlı gerilim kaynağı süperdüğüm değildir:</strong> İki düğüm arasında hem $5\\ \\Omega$ direnç hem de $11.5i_o$ gerilim kaynağı seri bağlıysa (bkz. ÇY2 s.2 d.4), o kolun akımı doğrudan $\\dfrac{v_3 - 11.5i_o}{5}$ olarak yazılır; süperdüğüm yapmaya gerek yoktur.",
            "<strong>Ortak dirençte işaret:</strong> Çevre 1'i yazarken ortak direnç terimi $R(i_1 - i_2)$ iken, Çevre 2'yi yazarken $R(i_2 - i_1)$ olur.",
        ],
    ),
    2: dict(
        kicker="3. KADEME (DEVRE SADELEŞTİRME) · TAHTADAKİ 2. SORU (25 PUAN)",
        title="Kaynak Dönüşümü ve Süperpozisyon (Toplamsallık)",
        lead=(
            "Düğüm ve çevre analizini kavradıktan sonra, karmaşık devreleri küçük parçalara bölerek veya seri-paralel dönüştürerek "
            "çözen iki yönteme geçiyoruz. Önce bağımsız kaynaklı kolay dönüşümlerle ısınıp, ardından bağımlı kaynaklı süperpozisyon ve dönüşüm sorularını çözüyoruz."
        ),
        definition=r'''
        <div class="theory-box">
          <h4>📘 Genel Tanım: Kaynak Dönüşümü ve Süperpozisyon Nedir?</h4>
          <ul>
            <li><strong>Kaynak Dönüşümü (Source Transformation):</strong> Bir $v_s$ gerilim kaynağı ile ona <strong>seri</strong> bağlı $R$ direnci, dış devre açısından $i_s = \dfrac{v_s}{R}$ değerinde bir akım kaynağı ile ona <strong>paralel</strong> bağlı aynı $R$ direncine tamamen eşdeğerdir (veya tam tersi: $v_s = i_s \cdot R$). Dönüşüm yapılırken akım kaynağının oku her zaman gerilim kaynağının <strong>$+$ kutbuna doğru</strong> bakar.</li>
            <li><strong>Süperpozisyon (Toplamsallık / Superposition) Yöntemi:</strong> Doğrusal bir devrede birden fazla <em>bağımsız kaynak</em> varsa, aranan bir akım veya gerilim, her bir bağımsız kaynağın <strong>tek başına</strong> devrede bırakılmasıyla bulunan katkılarının cebirsel toplamına eşittir ($v_o = v_o' + v_o''$).</li>
            <li><strong>Kaynağı Kapatmak (Öldürmek) Ne Demektir?</strong>
              <br>• Kapatılan <strong>bağımsız gerilim kaynağı</strong> ($V = 0$) yerine <strong>düz tel (kısa devre)</strong> çizilir.
              <br>• Kapatılan <strong>bağımsız akım kaynağı</strong> ($I = 0$) devreden sökülüp uçları <strong>boşta (açık devre)</strong> bırakılır.</li>
          </ul>
        </div>
        ''',
        recipe=[
            "<strong>Kaynak dönüşümünde:</strong> Aranan büyüklüğün ($v_o, i_o$) ve kontrol değişkeninin ($v_\\Delta, i_x$) bulunduğu dallara dokunmadan, en uzak uçtan başlayarak seri $\\leftrightarrow$ paralel dönüşümlerle devreyi tek göze/düğüme indirge.",
            "<strong>Süperpozisyonda (1. Alt Devre):</strong> 1. bağımsız kaynağı aktif bırak, diğer bağımsız kaynakları kapat; bağımlı kaynağı koruyarak $v_o'$ (veya $i'$) değerini bul.",
            "<strong>Süperpozisyonda (2. Alt Devre):</strong> 2. bağımsız kaynağı aktif bırak, 1. bağımsız kaynağı kapat; bağımlı kaynağı koruyarak $v_o''$ (veya $i''$) değerini bul.",
            "<strong>Toplam:</strong> Bulduğun alt devre sonuçlarını işaretlerine dikkat ederek topla: $v_o = v_o' + v_o''$.",
        ],
        watchout=[
            "<strong>ALTIN KURAL 1 (Süperpozisyon):</strong> Baklava şeklindeki <strong>bağımlı kaynaklar ASLA kapatılmaz!</strong> Her alt devrede kontrol değişkeni ($i_\\phi', i_\\phi''$) yeniden hesaplanır.",
            "<strong>ALTIN KURAL 2 (Kaynak Dönüşümü):</strong> Bağımlı kaynağın kontrol değişkeninin ($v_a, v_\\Delta$) üzerinde bulunduğu direnç dalına <strong>kesinlikle kaynak dönüşümü uygulanmaz</strong> ve başka dirençlerle birleştirilmez.",
            "<strong>Alt teldeki dirençleri unutma:</strong> Merdiven devrelerde (örn. P4.60) sadece üst teldeki dirençleri değil, alt teldeki seri dirençleri de ($6 + 3 + 6 = 15\\ \\text{k}\\Omega$) toplamaya dikkat et.",
        ],
    ),
    1: dict(
        kicker="4. KADEME (ZİRVE / SENTEZ) · TAHTADAKİ 1. SORU (25 PUAN)",
        title="Thévenin / Norton Eşdeğeri ve Maksimum Güç Transferi",
        lead=(
            "Sınavın 1. sorusu ama öğrenme sıramızın son halkası! Çünkü bir devrenin Thévenin eşdeğerini ve maksimum gücünü bulmak için "
            "önceki üç kademede öğrendiğimiz düğüm analizini, çevre analizini ve açık/kısa devre kurallarını bir arada kullanıyoruz."
        ),
        definition=r'''
        <div class="theory-box">
          <h4>📘 Genel Tanım: Thévenin Eşdeğeri ve Maksimum Güç Transferi Nedir?</h4>
          <ul>
            <li><strong>Thévenin Teoremi:</strong> İçinde ne kadar çok direnç, bağımsız kaynak ve bağımlı kaynak olursa olsun, iki uçlu ($a$–$b$) doğrusal bir devre; dışarıdan bakıldığında tek bir <strong>Thévenin gerilim kaynağı ($V_{Th}$)</strong> ve ona seri bağlı tek bir <strong>Thévenin direnci ($R_{Th}$)</strong> ile birebir aynı davranışı gösterir.</li>
            <li><strong>Açık Devre Gerilimi ($V_{Th} = V_{oc}$):</strong> $a$–$b$ uçlarındaki yük direncini ($R_o$ veya $R_L$) devreden söktüğümüzde $a$ ile $b$ uçları arasında oluşan gerilimdir ($V_{Th} = V_a - V_b$).</li>
            <li><strong>Kısa Devre (Norton) Akımı ($I_{sc} = I_N$):</strong> $a$ ile $b$ uçlarını düz bir telle birleştirdiğimizde $a$'dan $b$'ye doğru geçen akımdır. Bağımlı kaynaklı devrelerde Thévenin direnci her zaman şu oranla bulunur:
              <div class="math-display">\[ R_{Th} = \frac{V_{Th}}{I_{sc}} \]</div></li>
            <li><strong>Maksimum Güç Transferi Şartı ve Formülü:</strong> $a$–$b$ uçlarına bağlanan ayarlı bir $R_L$ (veya $R_o$) yük direncinin devreden <strong>mümkün olan en büyük gücü</strong> çekebilmesi için yük direnci Thévenin direncine eşit seçilmelidir:
              <div class="math-display">\[ \boxed{R_L = R_{Th}} \qquad \text{ve bu durumda çekilen maksimum güç:} \qquad \boxed{P_{\max} = \frac{V_{Th}^2}{4\,R_{Th}}} \]</div></li>
          </ul>
        </div>
        ''',
        recipe=[
            "<strong>1. Adım (Hazırlık):</strong> $R_o$ (veya $R_L$) yük direncini $a$–$b$ uçlarından sök; bağımlı kaynakların kontrol değişkenlerini (ek 1, ek 2) yaz.",
            "<strong>2. Adım (Açık Devre $\\to V_{Th}$):</strong> $a$–$b$ uçları açıkken düğüm veya çevre analiziyle $V_{Th} = V_{ab}$ gerilimini bul.",
            "<strong>3. Adım (Kısa Devre $\\to I_{sc}$):</strong> $a$–$b$ uçlarını düz telle kısa devre et ($V_a = V_b$ olur) ve bu telden geçen $I_{sc}$ akımını bul.",
            "<strong>4. Adım (Sonuç):</strong> $R_o = R_{Th} = \\dfrac{V_{Th}}{I_{sc}}$ ve $P_{\\max} = \\dfrac{V_{Th}^2}{4R_{Th}}$ formüllerini uygula.",
        ],
        watchout=[
            "<strong>ÖZEL DURUM (Devrede hiç bağımsız kaynak yoksa — P4.79):</strong> Devrede sadece dirençler ve bağımlı kaynaklar varsa $V_{Th} = 0$ ve $I_{sc} = 0$ çıkar ($0/0$ belirsizliği!). Bu durumda $a$–$b$ uçlarına dışarıdan $v_T = 1\\ \\text{V}$'luk bir test kaynağı bağlayıp çektiği $i_T$ akımını bulursun: $R_{Th} = \\dfrac{1\\ \\text{V}}{i_T}$.",
            "<strong>Kısa devrede paralel direnç düşer:</strong> $a$–$b$ uçlarını kısa devre ettiğinde $a$–$b$ uçlarına paralel bağlı olan direncin iki ucu da aynı potansiyele gelir ($v = 0$), dolayısıyla o dirençten akım geçmez ($i = 0$)!",
            "<strong>Kontrol değişkeni yük kolundaysa (P4.89):</strong> Kontrol akımı $i_\\phi$ doğrudan yük direnci $R_o$'nun üzerinden geçiyorsa, açık devrede yük söküldüğü için $i_\\phi = 0$ olur ve bağımlı kaynak sıfırlanır!",
        ],
    ),
}

CHEAT = r'''
<div class="overlay" id="cheat" role="dialog" aria-modal="true" aria-labelledby="cheatTitle">
  <div class="modal">
    <div class="modal-head"><h2 id="cheatTitle">Son gece 5 dakikalık özet &amp; dikkat edilecekler</h2>
      <button class="icon-btn" data-close aria-label="Kapat">{close}</button></div>
    <div class="modal-body">
      <div class="cheat-grid">
        <div class="cheat" style="--c:#0EA5E9">
          <h3><span>01</span>Maksimum güç transferi (Soru 1)</h3>
          <div class="math-display">\[ R_L = R_{Th} = \frac{V_{Th}}{I_{sc}}, \qquad P_{max} = \frac{V_{Th}^2}{4R_{Th}} \]</div>
          <div class="golden">Bağımlı kaynak varken kaynakları kapatıp eşdeğer direnç toplamak YASAK! Bağımsız kaynak yoksa $a$–$b$'ye $1\ \text{V}$ test kaynağı bağla: $R_{Th} = 1/i_T$.</div>
        </div>
        <div class="cheat" style="--c:#10B981">
          <h3><span>02</span>Kaynak dönüşümü (Soru 2a)</h3>
          <div class="math-display">\[ v_s \text{ seri } R \;\Longleftrightarrow\; i_s = \frac{v_s}{R} \text{ paralel } R \]</div>
          <div class="golden">Kontrol değişkeninin ($v_\Delta, i_x$) bulunduğu dala ASLA dokunma! Akım okunun ucu her zaman $+$ kutbu gösterir.</div>
        </div>
        <div class="cheat" style="--c:#F59E0B">
          <h3><span>03</span>Süperpozisyon (Soru 2b)</h3>
          <ul><li>Bağımsız gerilim kaynağı kapalı → <strong>kısa devre (düz tel)</strong></li><li>Bağımsız akım kaynağı kapalı → <strong>açık devre (kopuk tel)</strong></li><li>Sonuç: $v = v' + v''$ (işaretli topla)</li></ul>
          <div class="golden">Baklava şeklindeki bağımlı kaynak ASLA kapatılmaz; her alt devrede çalışır.</div>
        </div>
        <div class="cheat" style="--c:#EC4899">
          <h3><span>04</span>Pasif işaret &amp; güç dengesi (Soru 4)</h3>
          <div class="math-display">\[ p = \begin{cases} +vi & \text{akım + uçtan giriyor (harcar)} \\ -vi & \text{akım − uçtan giriyor (üretir)} \end{cases} \]</div>
          <div class="golden">$p&gt;0$ harcar (emer), $p&lt;0$ üretir. Her devrede mutlaka $\sum p = 0$ sağlamasını yap!</div>
        </div>
        <div class="cheat" style="--c:#6366F1">
          <h3><span>05</span>Düğüm &amp; Süperdüğüm (Soru 3a)</h3>
          <ul><li>Düğümden çıkan akımlar $+$, giren kaynak akımları $-$</li><li>$i = (V_{\text{çıkış}} - V_{\text{varış}})/R$ (ok yönüne dikkat!)</li><li>İki düğüm arasında sadece gerilim kaynağı varsa → <strong>süperdüğüm</strong></li></ul>
        </div>
        <div class="cheat" style="--c:#14B8A6">
          <h3><span>06</span>Çevre &amp; Süperçevre (Soru 3b)</h3>
          <ul><li>Saat yönünde dolaş, ilk girdiğin kutup işaretini yaz</li><li>Ortak dirençte: $R(I_{\text{kendi}} - I_{\text{komşu}})$</li><li>İki göz arasında akım kaynağı varsa → <strong>süperçevre</strong></li></ul>
        </div>
      </div>
    </div>
  </div>
</div>
'''


def topic_section(t, probs, start_no, stage_idx):
    meta = TOPIC_INTRO[t]
    recipe = "".join(f"<div>{r}</div>" for r in meta["recipe"])
    watch_items = "".join(f"<li>{w}</li>" for w in meta["watchout"])
    watchout_html = (
        f'<aside class="callout callout-warn glass">'
        f'<div class="callout-title">⚠️ Bu konuda nelere dikkat etmek lazım? (Puan kaybettiren noktalar)</div>'
        f'<ul>{watch_items}</ul></aside>'
    )

    # Problemleri zorluk aşamasına (1 -> 2 -> 3) göre alt başlıklarla grupla
    cards_parts = []
    cur_lvl = None
    idx = start_no
    for p in probs:
        lvl = p.get("level", 2)
        if lvl != cur_lvl:
            cur_lvl = lvl
            t_title, t_desc, t_cls = TIER_META[lvl]
            cards_parts.append(
                f'<div class="tier-banner tier-{t_cls}" data-tier-banner="{lvl}">'
                f'<div class="tier-badge">{t_title}</div>'
                f'<div class="tier-desc">{t_desc}</div>'
                f'</div>'
            )
        cards_parts.append(render_problem(p, idx))
        idx += 1

    return f'''
<section class="section topic-section" id="soru{t}" data-topic-sec="{t}" data-stage-order="{stage_idx}" data-exam-order="{t}">
  <div class="section-head">
    <div class="section-kicker">{meta["kicker"]}</div>
    <h2>{meta["title"]}</h2>
    <p>{meta["lead"]}</p>
  </div>
  {meta["definition"]}
  <h3 class="subhead-sm">Adım Adım Çözüm Şablonu</h3>
  <div class="topic-recipe">{recipe}</div>
  {watchout_html}
  <div class="problem-list">{"".join(cards_parts)}</div>
</section>'''


def sidebar(by_topic):
    out = ['<nav class="sidebar" aria-label="İçindekiler">']
    out.append('<div class="side-group"><div class="side-label">Başlangıç Rehberi</div>'
               '<a class="side-link" href="#giris">Sınav formatı &amp; yol haritası</a>'
               '<a class="side-link" href="#temel">Genel tanımlar (Bölüm 0)</a>'
               '<a class="side-link" href="#dikkat">Nelere dikkat etmeli? (8 Kural)</a></div>')
    out.append('<div id="sidebarTopics">')
    for stage_idx, t in enumerate(TOPIC_ORDER_EASY, 1):
        short, _ = TOPICS[t]
        out.append(
            f'<div class="side-group" data-side-topic="{t}" data-stage-order="{stage_idx}" data-exam-order="{t}">'
            f'<div class="side-label"><span>{SIDE_NAMES[t]} ({short})</span>'
            f'<span class="side-count" data-topic-count="{t}"></span></div>'
        )
        out.append(f'<a class="side-link" href="#soru{t}">📘 Konu tanımı &amp; püf noktaları</a>')
        for p in by_topic[t]:
            plain = p["title"].replace("$", "")
            lvl = p.get("level", 2)
            lvl_tag = {1: "Kolay", 2: "Orta", 3: "Zor"}.get(lvl, "Orta")
            out.append(
                f'<a class="side-link" href="#{esc(p["id"])}" data-pid="{esc(p["id"])}" data-level="{lvl}" '
                f'data-search="{esc((p["code"] + " " + plain).lower())}" title="{esc(plain)}">'
                f'<span class="dot">{ICON["check"]}</span><span>{esc(p["code"])}</span>'
                f'<span class="code lvl-pill" data-level="{lvl}">{lvl_tag}</span></a>'
            )
        out.append('</div>')
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
  <label class="search">{ICON["search"]}<input id="search" type="search" placeholder="Soru ara: P4.87, süperdüğüm…" autocomplete="off"><kbd>/</kbd></label>
  <div class="ring" title="Vizeye hazırlık oranın">
    <svg viewBox="0 0 30 30"><circle class="ring-bg" cx="15" cy="15" r="12"/><circle class="ring-fg" id="ringFg" cx="15" cy="15" r="12"/></svg>
    <span class="ring-label">Hazırlık</span> <b data-progress-text>%0</b>
  </div>
  <button class="hdr-btn" id="cheatBtn">{ICON["coffee"]}<span class="lbl">Son gece özeti</span></button>
  <button class="icon-btn" id="themeBtn" aria-label="Tema değiştir">{ICON["moon"]}{ICON["sun"]}</button>
</header>'''


def hero(by_topic):
    cards = []
    stage_labels = {
        4: ("1. KADEME · EN KOLAY BAŞLANGIÇ", "Tahtadaki 4. Soru · 25 Puan"),
        3: ("2. KADEME · TEMEL ANALİZ", "Tahtadaki 3. Soru · 25 Puan"),
        2: ("3. KADEME · DEVRE SADELEŞTİRME", "Tahtadaki 2. Soru · 25 Puan"),
        1: ("4. KADEME · ZİRVE (SENTEZ)", "Tahtadaki 1. Soru · 25 Puan"),
    }
    for t in TOPIC_ORDER_EASY:
        _, long_ = TOPICS[t]
        st_lbl, pts_lbl = stage_labels[t]
        codes = ", ".join(p["code"] for p in by_topic[t][:5]) + (" …" if len(by_topic[t]) > 5 else "")
        cards.append(f'''
      <a class="exam-card" href="#soru{t}">
        <span class="pts">{pts_lbl}</span>
        <span class="n">{st_lbl}</span>
        <h3>{long_}</h3>
        <p>{len(by_topic[t])} soru (Kolay → Orta → Zor) · {esc(codes)}</p>
        <div class="bar"><span data-topic-bar="{t}"></span></div>
      </a>''')
    return f'''
<section class="hero" id="giris">
  <div class="eyebrow"><i></i>Tuna Göksu · Vize · Kolaydan zora adım adım öğrenme sistemi</div>
  <h1>Devre Analizi I vizesine<br><span class="grad">kolaydan zora, sıfırdan</span> hazırlan.</h1>
  <p class="lead">Hiç çalışmamış bir öğrencinin en rahat öğreneceği şekilde: önce <strong>genel tanımlar ve dikkat edilecek altın kurallar</strong>,
  ardından her konu içinde <strong>1. Aşama (Kolay) → 2. Aşama (Orta) → 3. Aşama (Zor)</strong> sırasıyla tek bir işlem basamağı bile atlanmadan çözülmüş 33 soru.</p>
  <div class="hero-actions">
    <a class="btn btn-primary btn-lg" href="#temel">1. Adım: Genel Tanımlar &amp; Kurallar</a>
    <a class="btn btn-ghost btn-lg" href="#soru4">2. Adım: En Kolay Sorudan Başla</a>
    <a class="btn btn-ghost btn-lg" href="#p4-87">Tahtadaki Soruya Git (P4.87)</a>
  </div>
  <div class="exam-map">{"".join(cards)}</div>
  <div class="board-photo">
    <img class="zoomable" src="img/WHITEBOARD_PHOTO.webp" alt="Sınıf tahtası: sınavın 4 sorusu">
    <p><strong>Sınıf Tahtası:</strong> “1- Maksimum güç transferi (bağımlı kaynak içeren devrede) · 2- Kaynak dönüşümü veya süperpozisyon sorusu ·
    3- Analiz sorusu, düğüm gerilimleri veya çevre akımları · 4- 1, 2 ve 3. bölümü içeren, güç hesapları da olan bir soru.”
    <br><em>Not:</em> Sınavda 1. soru Maksimum Güç olsa da, konuyu sıfırdan öğrenirken önce <strong>1. Kademe (Temel &amp; Güç) → 2. Kademe (Düğüm/Çevre) → 3. Kademe (Dönüşüm/Süperpozisyon) → 4. Kademe (Maksimum Güç)</strong> sırasıyla gitmek çok daha kolaydır. Aşağıdaki çubuktan istediğin an sıralamayı değiştirebilirsin.</p>
  </div>
</section>'''


def filter_bar(problems):
    c1 = sum(1 for p in problems if p.get("level", 2) == 1)
    c2 = sum(1 for p in problems if p.get("level", 2) == 2)
    c3 = sum(1 for p in problems if p.get("level", 2) == 3)
    return f'''
<div class="study-toolbar" id="studyToolbar">
  <div class="toolbar-group">
    <span class="toolbar-label">Zorluk filtresi:</span>
    <div class="seg seg-sm" id="levelFilter">
      <button class="seg-btn is-active" data-filter-level="all">Tümü ({len(problems)})</button>
      <button class="seg-btn" data-filter-level="1">🟢 1. Aşama: Kolay ({c1})</button>
      <button class="seg-btn" data-filter-level="2">🟡 2. Aşama: Orta ({c2})</button>
      <button class="seg-btn" data-filter-level="3">🔴 3. Aşama: Zor ({c3})</button>
    </div>
  </div>
  <div class="toolbar-group">
    <span class="toolbar-label">Konu sırası:</span>
    <div class="seg seg-sm" id="orderToggle">
      <button class="seg-btn is-active" data-order="easy">Kolaydan Zora (Önerilen)</button>
      <button class="seg-btn" data-order="exam">Tahtadaki Sıra (Soru 1→4)</button>
    </div>
  </div>
</div>'''


def mock_section(by_topic):
    mocks = []
    names = ["Isınma provası (Kolay–Orta)", "Tahta provası", "Klasik vize denemesi", "İleri seviye deneme", "Genel tekrar provası"]
    for k in range(5):
        items = []
        for t in (1, 2, 3, 4):
            lst = by_topic[t]
            if lst:
                items.append(lst[k % len(lst)]["id"])
        mocks.append(dict(title=f"Deneme {k + 1} — {names[k]}",
                          desc="4 soru · 90 dakika · her soru 25 puan", items=items))
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
    raw_problems, circuits = load_problems()
    render_all(circuits)
    render_all(SYMBOLS)
    by_topic = sort_by_topic(raw_problems)
    ordered_all = [p for t in TOPIC_ORDER_EASY for p in by_topic[t]]
    print(f"{len(ordered_all)} problem, {len(circuits)} şema")

    body = [header(), '<div class="layout">', sidebar(by_topic),
            '<main class="main"><div class="content">', hero(by_topic), FUNDAMENTALS,
            filter_bar(ordered_all), '<div id="topicsContainer">']
    n = 1
    for stage_idx, t in enumerate(TOPIC_ORDER_EASY, 1):
        body.append(topic_section(t, by_topic[t], n, stage_idx))
        n += len(by_topic[t])
    body.append('</div>')
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
