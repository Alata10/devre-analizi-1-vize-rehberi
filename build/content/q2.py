# -*- coding: utf-8 -*-
"""
SORU 2 — Bağımlı kaynaklı süperpozisyon ve kaynak dönüşümü.
İçerik şeması için bkz. build/CONTENT_SPEC.md
"""
from circuitkit import elm, ACCENT, NODE


# ---------------------------------------------------------------------------
# YARDIMCILAR (mutlak koordinatla çizim)
# ---------------------------------------------------------------------------
def _w(d, a, b):
    """a noktasından b noktasına düz tel."""
    d.add(elm.Line().at(a).to(b))


def _dot(d, p, **kw):
    return d.add(elm.Dot(**kw).at(p))


def _img(name, w=520):
    """Adım gövdesine gömülen ara şema."""
    return (f'<img class="zoomable schematic" src="circuits/{name}.svg" alt="{name}" '
            f'style="width:100%;max-width:{w}px;margin:12px auto;filter:var(--img-filter);cursor:zoom-in">')


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
# ---- P4.97 ----------------------------------------------------------------
def _p4_97(d, v_on=True, i_on=True, vo='$v_o$'):
    if v_on:
        d.add(elm.SourceV().at((0, 0)).up(3).label('25 V', loc='bottom'))
    else:
        d.add(elm.Line().at((0, 0)).up(3).label('kısa devre', loc='bottom', color=ACCENT))
    _dot(d, (0, 3))
    _w(d, (0, 3), (0, 5.5))
    _w(d, (0, 5.5), (2, 5.5))
    d.add(elm.SourceControlledI().at((2, 5.5)).right(4).label('$2.2\\,i_\\phi$', loc='top'))
    _w(d, (6, 5.5), (8, 5.5))
    _w(d, (8, 5.5), (8, 3))
    d.add(elm.Resistor().at((0, 3)).right(4).label('4 kΩ', loc='top')
          .label('$\\leftarrow\\, i_\\phi$', loc='bottom', color=ACCENT))
    _dot(d, (4, 3))
    if i_on:
        d.add(elm.SourceI().at((4, 3)).down(3).label('5 mA', loc='bottom'))
    else:
        _dot(d, (4, 2.2), open=True)
        _dot(d, (4, 0.8), open=True)
        _w(d, (4, 3), (4, 2.2))
        _w(d, (4, 0.8), (4, 0))
        d.add(elm.Gap().at((4, 2.2)).down(1.4).label('açık devre', loc='bottom', color=ACCENT))
    _dot(d, (4, 0))
    _w(d, (4, 3), (8, 3))
    _dot(d, (8, 3))
    d.add(elm.Resistor().at((8, 3)).down(3).label('20 kΩ', loc='bottom'))
    _dot(d, (8, 0))
    _w(d, (8, 3), (10, 3))
    _dot(d, (10, 3), open=True)
    d.add(elm.Gap().at((10, 3)).down(3).label(('+', vo, '−'), loc='bottom', color=ACCENT))
    _dot(d, (10, 0), open=True)
    _w(d, (10, 0), (0, 0))
    d.add(elm.Ground().at((0, 0)))


def draw_p4_97(d):
    _p4_97(d)


def draw_p4_97_a(d):
    _p4_97(d, i_on=False, vo="$v_o'$")


def draw_p4_97_b(d):
    _p4_97(d, v_on=False, vo="$v_o''$")


# ---- P4.98 ----------------------------------------------------------------
def _p4_98(d, v90=True, v40=True, il='$i$'):
    if v90:
        d.add(elm.SourceV().at((0, 0)).up(3).label('90 V', loc='top'))
    else:
        d.add(elm.Line().at((0, 0)).up(3).label('kısa devre', loc='top', color=ACCENT))
    _dot(d, (0, 3))
    _w(d, (0, 3), (0, 5.2))
    d.add(elm.Resistor().at((0, 5.2)).right(7).label('1 kΩ', loc='top')
          .label(('+', '$v_b$', '−'), loc='bottom', color=ACCENT))
    _w(d, (7, 5.2), (7, 3))
    d.add(elm.Resistor().at((0, 3)).right(3.5).label('2 kΩ', loc='top'))
    _dot(d, (3.5, 3))
    d.add(elm.Resistor().at((3.5, 3)).right(3.5).label('4 kΩ', loc='top'))
    _dot(d, (7, 3))
    dep = d.add(elm.SourceControlledV().at((3.5, 0)).up(3).label('$2.5v_b$', loc='top'))
    d.add(elm.CurrentLabel(top=False, reverse=True, ofst=0.55, length=1.1).at(dep)
          .label(il, color=ACCENT).color(ACCENT))
    if v40:
        d.add(elm.SourceV().at((7, 0)).up(3).label('40 V', loc='bottom'))
    else:
        d.add(elm.Line().at((7, 0)).up(3).label('kısa devre', loc='bottom', color=ACCENT))
    d.add(elm.Resistor().at((7, 0)).left(3.5).label('2 kΩ', loc='top'))
    _dot(d, (3.5, 0))
    _w(d, (3.5, 0), (0, 0))
    d.add(elm.Ground().at((0, 0)))


def draw_p4_98(d):
    _p4_98(d)


def draw_p4_98_a(d):
    _p4_98(d, v40=False, il="$i'$")


def draw_p4_98_b(d):
    _p4_98(d, v90=False, il="$i''$")


# ---- P4.56 ----------------------------------------------------------------
def _p4_56_bottom(d):
    d.add(elm.Resistor().at((0, 3)).down(3).label('100 Ω', loc='bottom'))
    d.add(elm.Resistor().at((3, 3)).down(3).label('250 Ω', loc='bottom')
          .label(('+', '$v_a$', '−'), loc='top', color=ACCENT))
    d.add(elm.Resistor().at((6, 3)).down(3).label('500 Ω', loc='bottom')
          .label(('+', '$v_\\Delta$', '−'), loc='top', color=ACCENT))
    d.add(elm.Resistor().at((9, 3)).down(3).label('200 Ω', loc='bottom'))
    d.add(elm.SourceV().at((0, 3)).right(3).label('20 V', loc='top'))
    d.add(elm.SourceI().at((6, 3)).left(3).label('200 mA', loc='bottom'))
    d.add(elm.SourceControlledV().at((6, 3)).right(3).label('$0.4\\,v_a$', loc='top'))
    for x in (0, 3, 6, 9):
        _dot(d, (x, 3))
    for x in (3, 6):
        _dot(d, (x, 0))
    _w(d, (0, 0), (9, 0))
    d.add(elm.Ground().at((4.5, 0)))


def draw_p4_56(d):
    _p4_56_bottom(d)
    _w(d, (0, 3), (0, 5.5))
    _w(d, (0, 5.5), (2.5, 5.5))
    d.add(elm.SourceControlledI().at((2.5, 5.5)).right(4).label('$0.003\\,v_\\Delta$', loc='top'))
    _w(d, (6.5, 5.5), (9, 5.5))
    _w(d, (9, 5.5), (9, 3))
    d.add(elm.Label().at((0, 3.35)).label('$V_1$', color=NODE, halign='right', ofst=(-0.15, 0)))
    d.add(elm.Label().at((9, 3.35)).label('$V_4$', color=NODE, halign='left', ofst=(0.15, 0)))


def draw_p4_56_a(d):
    """0.003 v_Delta kaynağı ikiye bölünmüş hali."""
    _p4_56_bottom(d)
    _w(d, (0, 3), (-2.5, 3))
    d.add(elm.SourceControlledI().at((-2.5, 3)).down(3).label('$0.003\\,v_\\Delta$', loc='top'))
    _w(d, (-2.5, 0), (0, 0))
    _w(d, (9, 3), (11.5, 3))
    d.add(elm.SourceControlledI().at((11.5, 0)).up(3).label('$0.003\\,v_\\Delta$', loc='bottom'))
    _w(d, (9, 0), (11.5, 0))
    _dot(d, (0, 0))
    _dot(d, (9, 0))


def draw_p4_56_b(d):
    """Kaynak dönüşümünden sonra iki düğümlü devre."""
    H = 6
    # sol seri kol: 20 V (+ üstte), 100 Ω, 0.3 v_Delta (+ altta)
    d.add(elm.SourceV().at((0, H)).down(2).reverse().label('20 V', loc='top'))
    d.add(elm.Resistor().at((0, 4)).down(2).label('100 Ω', loc='top'))
    d.add(elm.SourceControlledV().at((0, 2)).down(2).label('$0.3\\,v_\\Delta$', loc='top'))
    _w(d, (0, H), (3, H))
    # v_a düğümü
    _dot(d, (3, H))
    _w(d, (3, H), (3, 4.5))
    d.add(elm.Resistor().at((3, 4.5)).down(3).label('250 Ω', loc='bottom')
          .label(('+', '$v_a$', '−'), loc='top', color=ACCENT))
    _w(d, (3, 1.5), (3, 0))
    # 200 mA
    d.add(elm.SourceI().at((6, H)).left(3).label('200 mA', loc='top'))
    _dot(d, (6, H))
    _w(d, (6, H), (6, 4.5))
    d.add(elm.Resistor().at((6, 4.5)).down(3).label('500 Ω', loc='bottom')
          .label(('+', '$v_\\Delta$', '−'), loc='top', color=ACCENT))
    _w(d, (6, 1.5), (6, 0))
    _w(d, (6, H), (9, H))
    # sağ seri kol: 0.4 v_a (− üstte), 200 Ω, 0.6 v_Delta (+ üstte)
    d.add(elm.SourceControlledV().at((9, H)).down(2).label('$0.4\\,v_a$', loc='bottom'))
    d.add(elm.Resistor().at((9, 4)).down(2).label('200 Ω', loc='bottom'))
    d.add(elm.SourceControlledV().at((9, 2)).down(2).reverse().label('$0.6\\,v_\\Delta$', loc='bottom'))
    _w(d, (0, 0), (9, 0))
    _dot(d, (3, 0))
    _dot(d, (6, 0))
    d.add(elm.Ground().at((4.5, 0)))


# ---- P4.59 ----------------------------------------------------------------
def _p4_59_right(d, x0):
    """x0: 15 kΩ'un sol ucu (düğüm). Sağda 25 kΩ (v_o) ve 1 mA."""
    d.add(elm.Resistor().at((x0, 3)).right(4).label('15 kΩ', loc='top'))
    _p4_59_out(d, x0 + 4)


def _p4_59_out(d, x):
    _dot(d, (x, 3))
    d.add(elm.Resistor().at((x, 3)).down(3).label('25 kΩ', loc='top')
          .label(('+', '$v_o$', '−'), loc='bottom', color=ACCENT))
    _dot(d, (x, 0))
    _w(d, (x, 3), (x + 2.5, 3))
    d.add(elm.SourceI().at((x + 2.5, 3)).down(3).label('1 mA', loc='bottom'))
    _w(d, (x + 2.5, 0), (0, 0))
    d.add(elm.Ground().at((x, 0)))


def draw_p4_59(d):
    d.add(elm.Resistor().at((0, 0)).up(3).label('5 kΩ', loc='top'))
    _w(d, (0, 3), (2.5, 3))
    d.add(elm.SourceI().at((2.5, 0)).up(3).label('8 mA', loc='top'))
    _dot(d, (2.5, 3))
    _dot(d, (2.5, 0))
    d.add(elm.Resistor().at((2.5, 3)).right(3).label('10 kΩ', loc='top'))
    d.add(elm.SourceV().at((5.5, 3)).right(3).label('35 V', loc='top'))
    _dot(d, (8.5, 3))
    d.add(elm.Resistor().at((8.5, 3)).down(3).label('30 kΩ', loc='top'))
    _dot(d, (8.5, 0))
    _p4_59_right(d, 8.5)


def draw_p4_59_a(d):
    d.add(elm.SourceV().at((0, 0)).up(3).label('75 V', loc='top'))
    d.add(elm.Resistor().at((0, 3)).right(3.5).label('15 kΩ', loc='top'))
    _dot(d, (3.5, 3))
    d.add(elm.Resistor().at((3.5, 3)).down(3).label('30 kΩ', loc='top'))
    _dot(d, (3.5, 0))
    _p4_59_right(d, 3.5)


def draw_p4_59_b(d):
    d.add(elm.SourceV().at((0, 0)).up(3).label('50 V', loc='top'))
    d.add(elm.Resistor().at((0, 3)).right(4).label('25 kΩ', loc='top'))
    _p4_59_out(d, 4)


def draw_p4_59_c(d):
    d.add(elm.SourceI().at((0, 0)).up(3).label('2 mA', loc='top'))
    _w(d, (0, 3), (2.5, 3))
    _dot(d, (2.5, 3))
    d.add(elm.Resistor().at((2.5, 3)).down(3).label('25 kΩ', loc='top'))
    _dot(d, (2.5, 0))
    _w(d, (2.5, 3), (5, 3))
    _p4_59_out(d, 5)


# ---- P4.60 ----------------------------------------------------------------
def _p4_60_right(d, x):
    """x: 1 mA kaynağının olduğu düğüm (B). Sağda 5 kΩ, 20 kΩ, 15 kΩ (i_o)."""
    _dot(d, (x, 3))
    d.add(elm.SourceI().at((x, 3)).down(3).label('1 mA', loc='bottom'))
    _dot(d, (x, 0))
    d.add(elm.Resistor().at((x, 3)).right(3.5).label('5 kΩ', loc='top'))
    _p4_60_out(d, x + 3.5)


def _p4_60_out(d, x):
    _dot(d, (x, 3))
    d.add(elm.Resistor().at((x, 3)).down(3).label('20 kΩ', loc='bottom'))
    _dot(d, (x, 0))
    _w(d, (x, 3), (x + 3, 3))
    r = d.add(elm.Resistor().at((x + 3, 3)).down(3).label('15 kΩ', loc='bottom'))
    d.add(elm.CurrentLabel(top=True, ofst=0.45, length=1.0).at(r)
          .label('$i_o$', color=ACCENT).color(ACCENT))
    _w(d, (x + 3, 0), (x, 0))
    d.add(elm.Ground().at((x, 0)))


def draw_p4_60(d):
    d.add(elm.SourceV().at((0, 0)).up(3).label('50 V', loc='bottom'))
    d.add(elm.Resistor().at((0, 3)).right(3.5).label('10 kΩ', loc='top'))
    _dot(d, (3.5, 3))
    d.add(elm.Resistor().at((3.5, 3)).down(3).label('15 kΩ', loc='bottom'))
    _dot(d, (3.5, 0))
    d.add(elm.Resistor().at((3.5, 3)).right(3.5).label('3 kΩ', loc='top'))
    _w(d, (0, 0), (3.5, 0))
    d.add(elm.Resistor().at((3.5, 0)).right(3.5).label('6 kΩ', loc='bottom'))
    _w(d, (7, 0), (10.5, 0))
    _p4_60_right(d, 7)


def draw_p4_60_a(d):
    d.add(elm.SourceV().at((0, 0)).up(3).label('30 V', loc='top'))
    d.add(elm.Resistor().at((0, 3)).right(3.5).label('6 kΩ', loc='top'))
    d.add(elm.Resistor().at((3.5, 3)).right(3.5).label('3 kΩ', loc='top'))
    _w(d, (0, 0), (3.5, 0))
    d.add(elm.Resistor().at((3.5, 0)).right(3.5).label('6 kΩ', loc='bottom'))
    _w(d, (7, 0), (10.5, 0))
    _p4_60_right(d, 7)


def draw_p4_60_b(d):
    d.add(elm.SourceI().at((0, 0)).up(3).label('2 mA', loc='top'))
    _w(d, (0, 3), (2.5, 3))
    _dot(d, (2.5, 3))
    d.add(elm.Resistor().at((2.5, 3)).down(3).label('15 kΩ', loc='bottom'))
    _dot(d, (2.5, 0))
    _w(d, (2.5, 3), (5, 3))
    _w(d, (0, 0), (5, 0))
    _w(d, (5, 0), (8.5, 0))
    _p4_60_right(d, 5)


def draw_p4_60_c(d):
    d.add(elm.SourceI().at((0, 0)).up(3).label('0.75 mA', loc='top'))
    _w(d, (0, 3), (2.5, 3))
    _dot(d, (2.5, 3))
    d.add(elm.Resistor().at((2.5, 3)).down(3).label('20 kΩ', loc='bottom'))
    _dot(d, (2.5, 0))
    _w(d, (2.5, 3), (5.5, 3))
    _w(d, (0, 0), (5.5, 0))
    _p4_60_out(d, 5.5)


CIRCUITS = {
    "p4-97": draw_p4_97,
    "p4-97-a": draw_p4_97_a,
    "p4-97-b": draw_p4_97_b,
    "p4-98": draw_p4_98,
    "p4-98-a": draw_p4_98_a,
    "p4-98-b": draw_p4_98_b,
    "p4-56": draw_p4_56,
    "p4-56-a": draw_p4_56_a,
    "p4-56-b": draw_p4_56_b,
    "p4-59": draw_p4_59,
    "p4-59-a": draw_p4_59_a,
    "p4-59-b": draw_p4_59_b,
    "p4-59-c": draw_p4_59_c,
    "p4-60": draw_p4_60,
    "p4-60-a": draw_p4_60_a,
    "p4-60-b": draw_p4_60_b,
    "p4-60-c": draw_p4_60_c,
}

PROBLEMS = [
    dict(
        id="p4-97",
        topic=2,
        code="P4.97",
        title="Süperpozisyon ile $v_o$ gerilimini bulma ($2.2\\,i_\\phi$ bağımlı kaynaklı)",
        source="Çalışma Yaprağı 3 s.4 · Çalışma Yaprağı 4 s.2",
        image="P4_97_ORIG.webp",
        circuit="p4-97",
        circuit_caption="25 V ve 5 mA bağımsız kaynaklar sırayla tek başına bırakılır; $2.2\\,i_\\phi$ bağımlı kaynağı her iki alt devrede de devrede kalır.",
        level=2,
        question=(
            "Şekildeki devrede <strong>süperpozisyon (toplamsallık) yöntemini</strong> kullanarak "
            "$20\\ \\text{k}\\Omega$ direnç üzerindeki $v_o$ çıkış gerilimini bulunuz."
        ),
        strategy=[
            "Süperpozisyonda her adımda yalnızca <strong>bir bağımsız kaynak</strong> aktif bırakılır; diğer bağımsız gerilim kaynakları <strong>kısa devre</strong> (düz tel), bağımsız akım kaynakları <strong>açık devre</strong> (kopuk tel) yapılır.",
            "<strong>Altın kural:</strong> Bağımlı kaynak ($2.2\\,i_\\phi$) <strong>asla kapatılmaz</strong>; her iki alt devrede de kendi kontrol değişkeni ($i_\\phi'$ ve $i_\\phi''$) ile çalışmaya devam eder.",
            "1. Alt devre: $25\\ \\text{V}$ aktif, $5\\ \\text{mA}$ açık devre $\\to v_o'$ bulunur.",
            "2. Alt devre: $5\\ \\text{mA}$ aktif, $25\\ \\text{V}$ kısa devre $\\to v_o''$ bulunur ve $v_o = v_o' + v_o''$ toplanır.",
        ],
        steps=[
            dict(
                title="1. Alt devre: Yalnızca $25\\ \\text{V}$ kaynağı aktif ($5\\ \\text{mA}$ açık devre)",
                body=(
                    "Ortadaki $5\\ \\text{mA}$ bağımsız akım kaynağını <strong>açık devre</strong> yapıp devreden çıkarıyoruz. "
                    "Sol üst düğüm $25\\ \\text{V}$ kaynağından dolayı doğrudan $25\\ \\text{V}$ potansiyelindedir; sağ üst düğümün gerilimi ise $v_o'$ olur. "
                    "$4\\ \\text{k}\\Omega$ direncin altındaki $i_\\phi'$ okunun <strong>sağdan sola</strong> ($v_o'$ düğümünden $25\\ \\text{V}$ düğümüne) baktığına dikkat edelim:"
                    + _img("p4-97-a")
                ),
                math=r"""\begin{aligned}
i_\phi' &= \frac{v_o' - 25}{4000} \\[6pt]
\text{Düğüm } v_o' \text{ için KCL (çıkanlar } + \text{):}\quad
&\frac{v_o' - 25}{4000} - 2.2\,i_\phi' + \frac{v_o'}{20000} = 0 \\[4pt]
i_\phi' \text{ yerine yazılırsa:}\quad
&-1.2\,\frac{v_o' - 25}{4000} + \frac{v_o'}{20000} = 0 \qquad (\times 20000) \\[4pt]
-6(v_o' - 25) + v_o' &= 0 \\
-6v_o' + 150 + v_o' &= 0 \\
-5v_o' &= -150 \;\Longrightarrow\; \boxed{v_o' = 30\ \text{V}}
\end{aligned}""",
                note="Kontrol akımı $i_\\phi' = (30 - 25)/4000 = 1.25\\ \\text{mA}$ (sağdan sola).",
            ),
            dict(
                title="2. Alt devre: Yalnızca $5\\ \\text{mA}$ kaynağı aktif ($25\\ \\text{V}$ kısa devre)",
                body=(
                    "Şimdi $25\\ \\text{V}$ gerilim kaynağını <strong>kısa devre</strong> (düz tel) yapıyoruz ve $5\\ \\text{mA}$ akım kaynağını geri takıyoruz. "
                    "Sol üst düğüm doğrudan toprağa ($0\\ \\text{V}$) bağlandığı için $4\\ \\text{k}\\Omega$ direncin sol ucu $0\\ \\text{V}$ olur:"
                    + _img("p4-97-b")
                ),
                math=r"""\begin{aligned}
i_\phi'' &= \frac{v_o'' - 0}{4000} = \frac{v_o''}{4000} \\[6pt]
\text{Düğüm } v_o'' \text{ için KCL:}\quad
&\frac{v_o''}{4000} - 2.2\,i_\phi'' + 0.005 + \frac{v_o''}{20000} = 0 \\[4pt]
&-1.2\,\frac{v_o''}{4000} + \frac{v_o''}{20000} + 0.005 = 0 \qquad (\times 20000) \\[4pt]
-6v_o'' + v_o'' + 100 &= 0 \\
-5v_o'' &= -100 \;\Longrightarrow\; \boxed{v_o'' = 20\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="Süperpozisyon toplamı",
                body="İki bağımsız kaynağın ayrı ayrı ürettiği çıkış gerilimlerini cebirsel olarak topluyoruz:",
                math=r"""\begin{aligned}
v_o &= v_o' + v_o'' = 30 + 20 = \boxed{50\ \text{V}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_o' = 30\ \text{V}",
            r"v_o'' = 20\ \text{V}",
            r"v_o = 50\ \text{V}",
        ],
        exam=r"""\begin{aligned}
&\textbf{1) } 25\ \text{V aktif, } 5\ \text{mA açık devre:}\quad i_\phi' = \frac{v_o' - 25}{4000} \\
&\text{KCL: } \frac{v_o'-25}{4000} - 2.2\,\frac{v_o'-25}{4000} + \frac{v_o'}{20000} = 0 \xrightarrow{\times 20000} -6(v_o'-25) + v_o' = 0 \;\Rightarrow\; v_o' = 30\ \text{V} \\[4pt]
&\textbf{2) } 5\ \text{mA aktif, } 25\ \text{V kısa devre:}\quad i_\phi'' = \frac{v_o''}{4000} \\
&\text{KCL: } \frac{v_o''}{4000} - 2.2\,\frac{v_o''}{4000} + 0.005 + \frac{v_o''}{20000} = 0 \xrightarrow{\times 20000} -5v_o'' + 100 = 0 \;\Rightarrow\; v_o'' = 20\ \text{V} \\[4pt]
&\textbf{Toplam: } v_o = v_o' + v_o'' = 30 + 20 = 50\ \text{V}
\end{aligned}""",
        traps=[
            "$4\\ \\text{k}\\Omega$ üzerindeki $i_\\phi$ oku <strong>sağdan sola</strong> ($v_o \\to 25\\ \\text{V}$) yönündedir; $i_\\phi = (v_o - 25)/4000$ yazılmalıdır.",
            "Bağımlı akım kaynağı $2.2\\,i_\\phi$ hiçbir adımda açık devre yapılmaz.",
            "$25\\ \\text{V}$ kaynağı kısa devre edildiğinde sol üst düğüm $0\\ \\text{V}$ olur; $4\\ \\text{k}\\Omega$ direnç silinmez, toprağa bağlı kalır.",
        ],
    ),
    dict(
        id="p4-98",
        topic=2,
        code="P4.98",
        title="Süperpozisyon ile bağımlı kaynak akımı $i$'yi bulma ($2.5\\,v_b$)",
        source="Çalışma Yaprağı 4 s.2",
        image="P4_98_ORIG.webp",
        circuit="p4-98",
        circuit_caption="90 V ve 40 V bağımsız gerilim kaynakları sırayla kısa devre edilir; ortadaki $2.5\\,v_b$ bağımlı gerilim kaynağı korunur.",
        level=2,
        question=(
            "Şekildeki devrede <strong>süperpozisyon yöntemini</strong> kullanarak "
            "$2.5\\,v_b$ bağımlı gerilim kaynağından aşağı doğru geçen $i$ akımını bulunuz."
        ),
        strategy=[
            "Alt orta düğümü (orta kolun altı) referans ($0\\ \\text{V}$) seçelim. Sağ koldaki $40\\ \\text{V}$ kaynak ile alttaki $2\\ \\text{k}\\Omega$ direnç aynı dış kolda <strong>seri</strong> bağlıdır.",
            "Orta düğüm doğrudan bağımlı gerilim kaynağına bağlı olduğu için potansiyeli $V_B = 2.5\\,v_b$ olur.",
            "1. Alt devre: $90\\ \\text{V}$ aktif, $40\\ \\text{V}$ kısa devre $\\to i'$ hesaplanır.",
            "2. Alt devre: $40\\ \\text{V}$ aktif, $90\\ \\text{V}$ kısa devre $\\to i''$ hesaplanır ve $i = i' + i''$ toplanır.",
        ],
        steps=[
            dict(
                title="Düğüm bağıntıları ve kontrol değişkeni $v_b$",
                body=(
                    "Sol üst düğüme $V_A$, orta düğüme $V_B$, sağ üst düğüme $V_C$ diyelim (dirençler $\\text{k}\\Omega$, akımlar $\\text{mA}$). "
                    "Üstteki $1\\ \\text{k}\\Omega$ direnç üzerindeki gerilim $v_b = V_A - V_C$ olduğundan orta düğüm gerilimi:"
                ),
                math=r"""\begin{aligned}
v_b &= V_A - V_C, \qquad V_B = 2.5\,v_b = 2.5(V_A - V_C) \\[4pt]
i &= \frac{V_A - V_B}{2} + \frac{V_C - V_B}{4} \quad (\text{mA, orta düğüme giren akımlar toplamı})
\end{aligned}""",
            ),
            dict(
                title="1. Alt devre: $90\\ \\text{V}$ aktif, $40\\ \\text{V}$ kısa devre ($i'$)",
                body=(
                    "$40\\ \\text{V}$ kaynağını kısa devre yaptığımızda $V_A' = 90\\ \\text{V}$ olur ve sağ dış kol yalnızca $2\\ \\text{k}\\Omega$ direnç üzerinden toprağa iner:"
                    + _img("p4-98-a")
                ),
                math=r"""\begin{aligned}
v_b' &= 90 - V_C', \qquad V_B' = 2.5(90 - V_C') = 225 - 2.5V_C' \\[6pt]
\text{Düğüm } V_C' \text{ için KCL:}\quad
&\frac{V_C' - 90}{1} + \frac{V_C' - V_B'}{4} + \frac{V_C' - 0}{2} = 0 \qquad (\times 4) \\[4pt]
4(V_C' - 90) + \bigl(V_C' - (225 - 2.5V_C')\bigr) + 2V_C' &= 0 \\
4V_C' - 360 + 3.5V_C' - 225 + 2V_C' &= 0 \\
9.5V_C' &= 585 \;\Longrightarrow\; V_C' = \frac{1170}{19}\ \text{V} \approx 61.58\ \text{V} \\[6pt]
v_b' &= 90 - \frac{1170}{19} = \frac{540}{19}\ \text{V}, \qquad V_B' = 2.5 \cdot \frac{540}{19} = \frac{1350}{19}\ \text{V} \\[6pt]
i' &= \frac{90 - V_B'}{2} + \frac{V_C' - V_B'}{4}
= \frac{360/19}{2} + \frac{-180/19}{4}
= \frac{180}{19} - \frac{45}{19} = \boxed{\frac{135}{19}\ \text{mA} \approx 7.105\ \text{mA}}
\end{aligned}""",
            ),
            dict(
                title="2. Alt devre: $40\\ \\text{V}$ aktif, $90\\ \\text{V}$ kısa devre ($i''$)",
                body=(
                    "$90\\ \\text{V}$ kaynağını kısa devre yaptığımızda sol üst düğüm toprağa iner ($V_A'' = 0\\ \\text{V}$). "
                    "Sağ dış kolda $40\\ \\text{V}$ kaynak ile $2\\ \\text{k}\\Omega$ direnç seri bağlıdır:"
                    + _img("p4-98-b")
                ),
                math=r"""\begin{aligned}
v_b'' &= 0 - V_C'' = -V_C'', \qquad V_B'' = 2.5\,v_b'' = -2.5V_C'' \\[6pt]
\text{Düğüm } V_C'' \text{ için KCL:}\quad
&\frac{V_C'' - 0}{1} + \frac{V_C'' - (-2.5V_C'')}{4} + \frac{V_C'' - 40}{2} = 0 \qquad (\times 4) \\[4pt]
4V_C'' + 3.5V_C'' + 2(V_C'' - 40) &= 0 \\
9.5V_C'' &= 80 \;\Longrightarrow\; V_C'' = \frac{160}{19}\ \text{V} \approx 8.42\ \text{V} \\[6pt]
V_B'' &= -2.5 \cdot \frac{160}{19} = -\frac{400}{19}\ \text{V} \\[6pt]
i'' &= \frac{0 - V_B''}{2} + \frac{V_C'' - V_B''}{4}
= \frac{400/19}{2} + \frac{560/19}{4}
= \frac{200}{19} + \frac{140}{19} = \boxed{\frac{340}{19}\ \text{mA} \approx 17.895\ \text{mA}}
\end{aligned}""",
            ),
            dict(
                title="Süperpozisyon toplamı",
                body="İki alt devreden gelen akımları topladığımızda paydalar sadeleşir ve tam sayı sonuç elde edilir:",
                math=r"""\begin{aligned}
i &= i' + i'' = \frac{135}{19} + \frac{340}{19} = \frac{475}{19} = \boxed{25\ \text{mA}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i' = \frac{135}{19}\ \text{mA} \approx 7.11\ \text{mA}",
            r"i'' = \frac{340}{19}\ \text{mA} \approx 17.89\ \text{mA}",
            r"i = 25\ \text{mA}",
        ],
        exam=r"""\begin{aligned}
&v_b = V_A - V_C,\quad V_B = 2.5(V_A - V_C),\quad i = \frac{V_A - V_B}{2} + \frac{V_C - V_B}{4}\ (\text{mA}) \\[4pt]
&\textbf{1) } 90\ \text{V aktif } (V_A'=90,\ 40\ \text{V kısa devre}): \\
&\frac{V_C'-90}{1} + \frac{V_C' - 2.5(90-V_C')}{4} + \frac{V_C'}{2} = 0 \;\Rightarrow\; 9.5V_C' = 585 \;\Rightarrow\; V_C' = \frac{1170}{19}\ \text{V},\ V_B' = \frac{1350}{19}\ \text{V} \\
&i' = \frac{90 - 1350/19}{2} + \frac{1170/19 - 1350/19}{4} = \frac{135}{19}\ \text{mA} \\[4pt]
&\textbf{2) } 40\ \text{V aktif } (V_A''=0,\ 90\ \text{V kısa devre}): \\
&\frac{V_C''}{1} + \frac{3.5V_C''}{4} + \frac{V_C''-40}{2} = 0 \;\Rightarrow\; 9.5V_C'' = 80 \;\Rightarrow\; V_C'' = \frac{160}{19}\ \text{V},\ V_B'' = -\frac{400}{19}\ \text{V} \\
&i'' = \frac{400/19}{2} + \frac{560/19}{4} = \frac{340}{19}\ \text{mA} \\[4pt]
&\textbf{Toplam: } i = \frac{135}{19} + \frac{340}{19} = \frac{475}{19} = 25\ \text{mA}
\end{aligned}""",
        traps=[
            "Sağ alttaki $2\\ \\text{k}\\Omega$ direnç $40\\ \\text{V}$ kaynakla seri bağlıdır; $40\\ \\text{V}$ kaynağı kısa devre edildiğinde bu $2\\ \\text{k}\\Omega$ direnç silinmez.",
            "Orta koldaki $i$ akımı bir dirençten değil, $2.5\\,v_b$ gerilim kaynağından geçer; bu yüzden $V_B$'ye üstten giren iki direnç akımının toplamından ($KCL$) bulunur.",
        ],
    ),
    dict(
        id="p4-56",
        topic=2,
        code="P4.56",
        title="Kaynak dönüşümü ve düğüm analizi ile $20\\ \\text{V}$ kaynağın gücünü bulma",
        source="Çalışma Yaprağı 3 s.2",
        image="P4_56_ORIG.webp",
        circuit="p4-56",
        circuit_caption="Kontrol değişkenleri $v_a$ (250 Ω) ve $v_\\Delta$ (500 Ω) dallarına dokunmadan yan kollar sadeleştirilir.",
        level=3,
        question=(
            "Şekildeki devrede $20\\ \\text{V}$ bağımsız gerilim kaynağının "
            "<strong>ürettiği veya harcadığı gücü</strong> bulunuz."
        ),
        strategy=[
            "Kontrol değişkenleri $v_a$ ($250\\ \\Omega$ üzerinde) ve $v_\\Delta$ ($500\\ \\Omega$ üzerinde) olduğu için bu iki dikey dirence <strong>kesinlikle dokunulmaz</strong>.",
            "Üstteki $0.003\\,v_\\Delta$ akım kaynağı $V_1$ düğümünden çıkıp $V_4$ düğümüne girdiği için, $V_1$'den toprağa inen ve topraktan $V_4$'e çıkan iki eşdeğer akım kaynağı gibi düşünülebilir.",
            "Sol koldaki ($100\\ \\Omega \\parallel 0.003\\,v_\\Delta$) ve sağ koldaki ($200\\ \\Omega \\parallel 0.003\\,v_\\Delta$) Norton çiftleri Thévenin seri kollarına dönüştürülerek devre yalnızca $v_a$ ve $v_\\Delta$ düğümlerine indirgenir.",
        ],
        steps=[
            dict(
                title="1. Aşama: Yan kolların kaynak dönüşümü ile iki düğüme indirgenmesi",
                body=(
                    "Üstteki $0.003\\,v_\\Delta$ kaynağı $V_1$'den akım çekip $V_4$'e akım basar:"
                    + _img("p4-56-a")
                    + "Solda $100\\ \\Omega$ ile paralel olan $0.003\\,v_\\Delta$ (aşağı yönlü) kaynağı, $100 \\cdot 0.003\\,v_\\Delta = 0.3\\,v_\\Delta$ (+ ucu altta) seri gerilim kaynağına dönüşür. "
                    "Sağda ise $200\\ \\Omega$ ile paralel olan $0.003\\,v_\\Delta$ (yukarı yönlü) kaynağı, $200 \\cdot 0.003\\,v_\\Delta = 0.6\\,v_\\Delta$ (+ ucu üstte) seri gerilim kaynağına dönüşür:"
                    + _img("p4-56-b")
                ),
                math=r"""\begin{aligned}
V_1 &= v_a - 20, \qquad V_4 = v_\Delta + 0.4\,v_a \\[4pt]
\text{Sol seri kol gerilimi (toprağa göre):}\quad &v_a - 20 + 0.3\,v_\Delta \quad (\text{100 }\Omega\text{ üzerinden}) \\
\text{Sağ seri kol gerilimi (toprağa göre):}\quad &v_\Delta + 0.4\,v_a - 0.6\,v_\Delta = 0.4\,v_a + 0.4\,v_\Delta \quad (\text{200 }\Omega\text{ üzerinden})
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: $v_a$ ve $v_\\Delta$ düğümlerinde KCL denklemleri",
                body="İndirgenmiş devrede $v_a$ ve $v_\\Delta$ düğümleri için KCL (çıkan akımlar $+$) yazalım:",
                math=r"""\begin{aligned}
\textbf{Düğüm } v_a:&\quad \frac{v_a - 20 + 0.3\,v_\Delta}{100} + \frac{v_a}{250} - 0.2 = 0 \qquad (\times 500) \\[4pt]
&5(v_a - 20 + 0.3\,v_\Delta) + 2v_a - 100 = 0 \\
&7v_a + 1.5\,v_\Delta = 200 \;\Longrightarrow\; 14v_a + 3v_\Delta = 400 \qquad \text{(I)} \\[8pt]
\textbf{Düğüm } v_\Delta:&\quad 0.2 + \frac{v_\Delta}{500} + \frac{v_\Delta + 0.4\,v_a - 0.6\,v_\Delta}{200} = 0 \qquad (\times 1000) \\[4pt]
&200 + 2v_\Delta + 5(0.4\,v_a + 0.4\,v_\Delta) = 0 \\
&2v_a + 4v_\Delta = -200 \;\Longrightarrow\; v_a + 2v_\Delta = -100 \qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Denklem sisteminin çözümü",
                body="(II) denkleminden $v_a = -100 - 2v_\\Delta$ çekip (I) denkleminde yerine koyalım:",
                math=r"""\begin{aligned}
14(-100 - 2v_\Delta) + 3v_\Delta &= 400 \\
-1400 - 28v_\Delta + 3v_\Delta &= 400 \\
-25v_\Delta &= 1800 \;\Longrightarrow\; \boxed{v_\Delta = -72\ \text{V}} \\[6pt]
v_a &= -100 - 2(-72) = -100 + 144 = \boxed{44\ \text{V}} \\[4pt]
V_1 &= v_a - 20 = 44 - 20 = \boxed{24\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="4. Aşama: $20\\ \\text{V}$ kaynağın akımı ve gücü",
                body=(
                    "$v_a$ düğümünde $250\\ \\Omega$ dirençten aşağı inen akım $v_a/250$ ve sağdan gelen $200\\ \\text{mA}$ kaynak akımı bilindiğine göre, "
                    "$20\\ \\text{V}$ kaynağın $+$ (sağ) ucundan içeri giren $i_{20\\text{V}}$ akımını KCL ile buluruz:"
                ),
                math=r"""\begin{aligned}
i_{20\text{V}\ (\text{+ uçtan giren})} &= 0.2 - \frac{v_a}{250} = 0.2 - \frac{44}{250} = 0.2 - 0.176 = \boxed{0.024\ \text{A} = 24\ \text{mA}} \\[6pt]
p_{20\text{V}} &= (+20\ \text{V}) \cdot (0.024\ \text{A}) = \boxed{+0.48\ \text{W} = 480\ \text{mW (güç harcar / emer)}}
\end{aligned}""",
                note="Kontrol: Sol düğüm $V_1$'den $100\\ \\Omega$'a inen akım $24/100 = 0.24\\ \\text{A}$ ve üstten gelen $-0.003(-72) = 0.216\\ \\text{A}$ olduğundan $0.24 - 0.216 = 0.024\\ \\text{A}$ birebir doğrulanır.",
            ),
        ],
        answer=[
            r"v_a = 44\ \text{V}",
            r"v_\Delta = -72\ \text{V}",
            r"i_{20\text{V}} = 24\ \text{mA}",
            r"p_{20\text{V}} = +0.48\ \text{W}\ (\text{emer})",
        ],
        exam=r"""\begin{aligned}
&V_1 = v_a - 20, \qquad V_4 = v_\Delta + 0.4\,v_a \\[3pt]
&\text{Süperdüğüm } (V_1, v_a):\quad \frac{v_a - 20}{100} + 0.003\,v_\Delta + \frac{v_a}{250} - 0.2 = 0 \xrightarrow{\times 500} 14v_a + 3v_\Delta = 400 \quad \text{(I)} \\[3pt]
&\text{Süperdüğüm } (v_\Delta, V_4):\quad 0.2 + \frac{v_\Delta}{500} + \frac{v_\Delta + 0.4\,v_a}{200} - 0.003\,v_\Delta = 0 \xrightarrow{\times 1000} v_a + 2v_\Delta = -100 \quad \text{(II)} \\[3pt]
&\text{(I) ve (II)}'den:\quad v_\Delta = -72\ \text{V},\qquad v_a = 44\ \text{V},\qquad V_1 = 24\ \text{V} \\[3pt]
&i_{20\text{V}\ (\text{+ uçtan giren})} = 0.2 - \frac{44}{250} = 0.024\ \text{A} \;\Longrightarrow\; p_{20\text{V}} = 20 \times 0.024 = +0.48\ \text{W (güç emer)}
\end{aligned}""",
        traps=[
            "$250\\ \\Omega$ ($v_a$) ve $500\\ \\Omega$ ($v_\\Delta$) kontrol değişkeni dallarıdır; kaynak dönüşümü sırasında başka dirençlerle birleştirilmez.",
            "$20\\ \\text{V}$ kaynağının $+$ ucu sağda ($v_a$ tarafında), $-$ ucu solda ($V_1$ tarafında) olduğundan $V_1 = v_a - 20$ olur.",
            "Akım $20\\ \\text{V}$ kaynağının $+$ ucundan içeri girdiği için pasif işaret kuralına göre $p = +0.48\\ \\text{W} > 0$'dır (kaynak güç emer).",
        ],
    ),
    dict(
        id="p4-59",
        topic=2,
        code="P4.59",
        title="Ardışık kaynak dönüşümleri ile $v_o$ gerilimini bulma",
        source="Çalışma Yaprağı 3 s.2",
        image="P4_59_ORIG.webp",
        circuit="p4-59",
        circuit_caption="Soldan sağa doğru Norton ↔ Thévenin dönüşümleriyle devre tek düğümlü paralel devreye indirgenir.",
        level=1,
        question=(
            "Şekildeki devrede <strong>kaynak dönüşümü yöntemini</strong> kullanarak "
            "$25\\ \\text{k}\\Omega$ direnç üzerindeki $v_o$ gerilimini bulunuz."
        ),
        strategy=[
            "Aranan $v_o$ gerilimi sağdaki $25\\ \\text{k}\\Omega$ direnç üzerinde tanımlı olduğu için bu dirence dokunmadan soldan sağa doğru sadeleştirme yapılır.",
            "1. Adım: Soldaki $8\\ \\text{mA} \\parallel 5\\ \\text{k}\\Omega$ Norton çifti $\\to 40\\ \\text{V} + 5\\ \\text{k}\\Omega$ Thévenin koluna dönüştürülür ve seri $10\\ \\text{k}\\Omega$, $35\\ \\text{V}$ ile toplanır.",
            "2. Adım: Elde edilen $75\\ \\text{V} + 15\\ \\text{k}\\Omega$ kolu tekrar Norton'a çevrilip paralel $30\\ \\text{k}\\Omega$ ile birleştirilir.",
            "3. Adım: Tekrar Thévenin'e geçilip üstteki seri $15\\ \\text{k}\\Omega$ eklendikten sonra son kez Norton'a çevrilerek $v_o$ tek adımda bulunur.",
        ],
        steps=[
            dict(
                title="1. Dönüşüm: Sol kolu Thévenin'e çevirip seri elemanları toplama",
                body=(
                    "En soldaki $8\\ \\text{mA}$ (yukarı yönlü) akım kaynağı ile paralel $5\\ \\text{k}\\Omega$ direnci Thévenin eşdeğerine çevirelim: "
                    "$V_1 = 8\\ \\text{mA} \\times 5\\ \\text{k}\\Omega = 40\\ \\text{V}$ (+ üstte) ve seri $5\\ \\text{k}\\Omega$. "
                    "Üst koldaki seri $10\\ \\text{k}\\Omega$ direnç ve aynı yönlü $35\\ \\text{V}$ (+ sağda) kaynak ile toplandığında:"
                    + _img("p4-59-a")
                ),
                math=r"""\begin{aligned}
V_{s1} &= 40 + 35 = 75\ \text{V} \quad (\text{+ üstte}) \\
R_{s1} &= 5 + 10 = 15\ \text{k}\Omega
\end{aligned}""",
            ),
            dict(
                title="2. Dönüşüm: Norton'a geçiş, $30\\ \\text{k}\\Omega$ ile paralel birleştirme ve tekrar Thévenin",
                body=(
                    "$75\\ \\text{V}$ ve seri $15\\ \\text{k}\\Omega$ kolunu Norton'a çevirirsek yukarı yönlü $I_{N1} = 75 / 15 = 5\\ \\text{mA}$ ve paralel $15\\ \\text{k}\\Omega$ elde ederiz. "
                    "Bunu ortadaki $30\\ \\text{k}\\Omega$ ile paralel birleştirip tekrar Thévenin'e çevirelim ve sağ üstteki seri $15\\ \\text{k}\\Omega$ ile toplayalım:"
                    + _img("p4-59-b")
                ),
                math=r"""\begin{aligned}
R_{p1} &= 15\ \text{k}\Omega \parallel 30\ \text{k}\Omega = \frac{15 \times 30}{15 + 30} = 10\ \text{k}\Omega \\[4pt]
V_{s2} &= 5\ \text{mA} \times 10\ \text{k}\Omega = 50\ \text{V} \quad (\text{+ üstte}) \\[4pt]
R_{s2} &= 10\ \text{k}\Omega + 15\ \text{k}\Omega = 25\ \text{k}\Omega
\end{aligned}""",
            ),
            dict(
                title="3. Dönüşüm: Son Norton eşdeğeri ve $v_o$'nun hesabı",
                body=(
                    "$50\\ \\text{V}$ ve seri $25\\ \\text{k}\\Omega$ kolunu son kez Norton'a çevirdiğimizde yukarı yönlü $2\\ \\text{mA}$ kaynak ve paralel $25\\ \\text{k}\\Omega$ direnç oluşur:"
                    + _img("p4-59-c")
                ),
                math=r"""\begin{aligned}
I_{N2} &= \frac{50\ \text{V}}{25\ \text{k}\Omega} = 2\ \text{mA} \quad (\text{yukarı}) \\[4pt]
I_{\text{toplam}} &= 2\ \text{mA} - 1\ \text{mA} = 1\ \text{mA} \quad (\text{yukarı}), \qquad
R_{\text{eş}} = 25\ \text{k}\Omega \parallel 25\ \text{k}\Omega = 12.5\ \text{k}\Omega \\[4pt]
v_o &= I_{\text{toplam}} \times R_{\text{eş}} = 1\ \text{mA} \times 12.5\ \text{k}\Omega = \boxed{12.5\ \text{V}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_o = 12.5\ \text{V}",
        ],
        exam=r"""\begin{aligned}
&8\ \text{mA} \parallel 5\ \text{k}\Omega \;\longrightarrow\; 40\ \text{V} + 5\ \text{k}\Omega \\
&\text{Seri toplam: } (40 + 35)\ \text{V} = 75\ \text{V}, \quad (5 + 10)\ \text{k}\Omega = 15\ \text{k}\Omega \\
&75\ \text{V} + 15\ \text{k}\Omega \;\longrightarrow\; 5\ \text{mA} \parallel 15\ \text{k}\Omega \\
&15\ \text{k}\Omega \parallel 30\ \text{k}\Omega = 10\ \text{k}\Omega \;\Longrightarrow\; 5\ \text{mA} \parallel 10\ \text{k}\Omega \;\longrightarrow\; 50\ \text{V} + 10\ \text{k}\Omega \\
&\text{Seri } 15\ \text{k}\Omega \text{ ile: } 50\ \text{V} + 25\ \text{k}\Omega \;\longrightarrow\; 2\ \text{mA} \parallel 25\ \text{k}\Omega \\
&v_o = (2 - 1)\ \text{mA} \times (25\ \text{k}\Omega \parallel 25\ \text{k}\Omega) = 1\ \text{mA} \times 12.5\ \text{k}\Omega = 12.5\ \text{V}
\end{aligned}""",
        traps=[
            "$35\\ \\text{V}$ kaynağının $+$ ucu sağda olduğu için soldaki $40\\ \\text{V}$ (+ üstte) kaynakla aynı yönde akım sürer; gerilimler çıkarılmaz, $40 + 35 = 75\\ \\text{V}$ toplanır.",
            "Sağdaki $1\\ \\text{mA}$ kaynak aşağı doğru olduğu için yukarı yönlü $2\\ \\text{mA}$ kaynaktan çıkarılır ($2 - 1 = 1\\ \\text{mA}$).",
        ],
    ),
    dict(
        id="p4-60",
        topic=2,
        code="P4.60",
        title="Merdiven devrede kaynak dönüşümü ile $i_o$ akımını bulma (alt koldaki $6\\ \\text{k}\\Omega$ detayı)",
        source="Çalışma Yaprağı 3 s.2",
        image="P4_60_ORIG.webp",
        circuit="p4-60",
        circuit_caption="Alt koldaki 6 kΩ direnç, üstteki 6 kΩ ve 3 kΩ dirençlerle aynı seri koldadır ($6+3+6 = 15\\ \\text{k}\\Omega$).",
        level=2,
        question=(
            "Şekildeki devrede <strong>kaynak dönüşümü yöntemini</strong> kullanarak "
            "en sağdaki $15\\ \\text{k}\\Omega$ dirençten geçen $i_o$ akımını bulunuz."
        ),
        strategy=[
            "En sağdaki $15\\ \\text{k}\\Omega$ ($i_o$) direncine dokunmadan soldan sağa doğru sadeleştirme yapılır.",
            "Soldaki $50\\ \\text{V} + 10\\ \\text{k}\\Omega$ kolu Norton'a çevrilip paralel $15\\ \\text{k}\\Omega$ ile birleştirilir ($10 \\parallel 15 = 6\\ \\text{k}\\Omega$) ve tekrar Thévenin'e ($30\\ \\text{V} + 6\\ \\text{k}\\Omega$) dönüştürülür.",
            "<strong>Kritik adım:</strong> Bu $6\\ \\text{k}\\Omega$, üstteki $3\\ \\text{k}\\Omega$ ve alt teldeki $6\\ \\text{k}\\Omega$ dirençlerin üçü de aynı tek gözün içinde <strong>seri</strong> bağlıdır ($R = 6 + 3 + 6 = 15\\ \\text{k}\\Omega$).",
        ],
        steps=[
            dict(
                title="1. Dönüşüm: Sol gözün Thévenin eşdeğeri ve alt koldaki $6\\ \\text{k}\\Omega$",
                body=(
                    "$50\\ \\text{V}$ (+ altta, $-$ üstte) gerilim kaynağı ve seri $10\\ \\text{k}\\Omega$ direnci Norton'a çevirelim: "
                    "aşağı yönlü $50 / 10 = 5\\ \\text{mA}$ akım kaynağı ve paralel $10\\ \\text{k}\\Omega$. "
                    "Paralel $15\\ \\text{k}\\Omega$ ile birleştirip tekrar Thévenin'e çevirdiğimizde (+ altta $30\\ \\text{V}$ ve $6\\ \\text{k}\\Omega$) "
                    "üstteki $3\\ \\text{k}\\Omega$ ve alttaki $6\\ \\text{k}\\Omega$ ile seri hale gelir:"
                    + _img("p4-60-a")
                ),
                math=r"""\begin{aligned}
R_{p1} &= 10\ \text{k}\Omega \parallel 15\ \text{k}\Omega = \frac{10 \times 15}{10 + 15} = 6\ \text{k}\Omega \\[4pt]
V_{s1} &= 5\ \text{mA} \times 6\ \text{k}\Omega = 30\ \text{V} \quad (\text{+ altta, } - \text{ üstte}) \\[4pt]
R_{s1} &= 6 + 3 + 6 = 15\ \text{k}\Omega
\end{aligned}""",
            ),
            dict(
                title="2. Dönüşüm: $1\\ \\text{mA}$ kaynak ile birleştirme ve $5\\ \\text{k}\\Omega$ serisi",
                body=(
                    "$30\\ \\text{V}$ (+ altta) ve seri $15\\ \\text{k}\\Omega$ kolunu Norton'a çevirirsek <strong>aşağı yönlü</strong> $30 / 15 = 2\\ \\text{mA}$ kaynak ve paralel $15\\ \\text{k}\\Omega$ elde ederiz:"
                    + _img("p4-60-b")
                    + "Aynı düğümdeki aşağı yönlü $1\\ \\text{mA}$ kaynak ile aynı yönde olduklarından toplanırlar ($2 + 1 = 3\\ \\text{mA}$ aşağı). "
                    "Bunu tekrar Thévenin'e çevirip ($3\\ \\text{mA} \\times 15\\ \\text{k}\\Omega = 45\\ \\text{V}$, + altta) sağ üstteki seri $5\\ \\text{k}\\Omega$ ile toplarız:"
                ),
                math=r"""\begin{aligned}
I_{N2} &= 2\ \text{mA} + 1\ \text{mA} = 3\ \text{mA} \quad (\text{aşağı}) \\[4pt]
V_{s2} &= 3\ \text{mA} \times 15\ \text{k}\Omega = 45\ \text{V} \quad (\text{+ altta}), \qquad
R_{s2} = 15 + 5 = 20\ \text{k}\Omega
\end{aligned}""",
            ),
            dict(
                title="3. Dönüşüm: Son Norton eşdeğeri ve akım bölme",
                body=(
                    "$45\\ \\text{V}$ (+ altta) ve $20\\ \\text{k}\\Omega$ kolunu Norton'a çevirdiğimizde aşağı yönlü $I_{N3} = 45 / 20 = 2.25\\ \\text{mA}$ ve paralel $20\\ \\text{k}\\Omega$ oluşur. "
                    "Sağda iki adet $20\\ \\text{k}\\Omega$ ($20 \\parallel 20 = 10\\ \\text{k}\\Omega$) ve aranan $15\\ \\text{k}\\Omega$ paralel kalır:"
                ),
                math=r"""\begin{aligned}
I_{N3} &= \frac{45\ \text{V}}{20\ \text{k}\Omega} = 2.25\ \text{mA} \quad (\text{aşağı, yani üst düğümden çekilen akım}) \\[4pt]
R_p &= 20\ \text{k}\Omega \parallel 20\ \text{k}\Omega = 10\ \text{k}\Omega \\[6pt]
\text{Akım bölme (} i_o \text{ yukarıdan aşağı tanımlı olduğu için işaret } - \text{ olur):}& \\
i_o &= -I_{N3} \cdot \frac{R_p}{R_p + 15\ \text{k}\Omega}
= -2.25 \cdot \frac{10}{10 + 15} = -2.25 \cdot \frac{2}{5} = \boxed{-0.9\ \text{mA}}
\end{aligned}""",
                note="Eğer $50\\ \\text{V}$ kaynağın $+$ ucu üstte okunursa $2 - 1 = 1\\ \\text{mA} \\to 15\\ \\text{V} / 20\\ \\text{k}\\Omega = 0.75\\ \\text{mA} \\to i_o = 0.75 \\times (10/25) = +0.3\\ \\text{mA}$ bulunur. Şekilde $50\\ \\text{V}$ kaynağın $+$ ucu üstte ise $i_o = 0.3\\ \\text{mA}$, altta ise $-0.9\\ \\text{mA}$'dir; her iki durumda da direnç indirgemesi $6+3+6=15\\ \\text{k}\\Omega$ ve $10/(10+15)=2/5$ oranı aynıdır.",
            ),
        ],
        answer=[
            r"R_{\text{ara}} = 6 + 3 + 6 = 15\ \text{k}\Omega",
            r"i_o = 0.3\ \text{mA}\ (\text{veya kutba göre } -0.9\ \text{mA})",
        ],
        exam=r"""\begin{aligned}
&50\ \text{V} + 10\ \text{k}\Omega \;\longrightarrow\; 5\ \text{mA} \parallel 10\ \text{k}\Omega,\qquad 10\ \text{k}\Omega \parallel 15\ \text{k}\Omega = 6\ \text{k}\Omega \\
&5\ \text{mA} \parallel 6\ \text{k}\Omega \;\longrightarrow\; 30\ \text{V} + 6\ \text{k}\Omega \\
&\text{Üst } 3\ \text{k}\Omega \text{ ve alt } 6\ \text{k}\Omega \text{ ile seri: } R = 6 + 3 + 6 = 15\ \text{k}\Omega \;\longrightarrow\; 2\ \text{mA} \parallel 15\ \text{k}\Omega \\
&(+50\ \text{V üstte ise}):\ (2 - 1)\ \text{mA} = 1\ \text{mA} \parallel 15\ \text{k}\Omega \;\longrightarrow\; 15\ \text{V} + 15\ \text{k}\Omega \\
&\text{Seri } 5\ \text{k}\Omega \text{ ile: } 15\ \text{V} + 20\ \text{k}\Omega \;\longrightarrow\; 0.75\ \text{mA} \parallel 20\ \text{k}\Omega \\
&20\ \text{k}\Omega \parallel 20\ \text{k}\Omega = 10\ \text{k}\Omega \;\Longrightarrow\; i_o = 0.75\ \text{mA} \times \frac{10}{10 + 15} = 0.3\ \text{mA}
\end{aligned}""",
        traps=[
            "Alt teldeki $6\\ \\text{k}\\Omega$ direnci görmezden gelmek en yaygın hatadır; sol kısım tek bir Thévenin koluna dönüştüğünde üstteki $3\\ \\text{k}\\Omega$ ve alttaki $6\\ \\text{k}\\Omega$ aynı seri akımı taşır ($6 + 3 + 6 = 15\\ \\text{k}\\Omega$).",
            "Son adımda iki adet $20\\ \\text{k}\\Omega$ direnç paraleldir ($10\\ \\text{k}\\Omega$); akım bölme formülünde paydaya $10 + 15 = 25\\ \\text{k}\\Omega$ yazılır.",
        ],
    ),
]
