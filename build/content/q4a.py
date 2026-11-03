# -*- coding: utf-8 -*-
"""
SORU 4 (a) — Güç hesabı / güç dengesi (pasif işaret kuralı, Σp = 0).
Çalışma Yaprağı 1: P2.10, P2.32, P2.36, P2.37, P2.9.
İçerik şeması için bkz. build/CONTENT_SPEC.md ; doğrulama: build/verify/q4a_verify.py
"""
from circuitkit import elm, ACCENT, NODE


def _cur(d, el, text, top=True, reverse=False, ofst=0.45, length=1.4):
    """Elemanın yanına (ACCENT renkli) akım oku + etiket koyar."""
    return d.add(elm.CurrentLabel(top=top, ofst=ofst, length=length, reverse=reverse)
                 .at(el).label(text).color(ACCENT))


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
def draw_p2_10(d):
    u = d.unit
    S = d.add(elm.SourceI().up().label('5 A', loc='top'))
    d.add(elm.Line().right(u * 1.1))
    d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.push()
    R30 = d.add(elm.Resistor().down().label('30 Ω', loc='bottom'))
    _cur(d, R30, '$i_\\phi$', top=True)
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Line().right(u * 0.35))
    d.add(elm.Dot())
    d.push()
    d.add(elm.Line().up(u * 0.75))
    d.add(elm.SourceControlledI().right(u * 1.6).label('$2i_\\phi$', loc='top'))
    d.add(elm.Line().down(u * 0.75))
    d.pop()
    R10 = d.add(elm.Resistor().right(u * 1.6).label('10 Ω', loc='bottom'))
    _cur(d, R10, '$i_{10}$', top=True, ofst=0.35, length=1.0)
    d.add(elm.Dot().label('$V_2$', loc='right', color=NODE))
    VS = d.add(elm.SourceV().down().reverse().label('$v_s$', loc='top'))
    _cur(d, VS, '$i_s$', top=False)
    d.add(elm.Line().left().tox(S.start))


def draw_p2_32(d):
    u = d.unit
    S = d.add(elm.SourceI().up().label('45 A', loc='top'))
    d.add(elm.Line().right(u * 1.1))
    d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.push()
    R6 = d.add(elm.Resistor().down().label('6 Ω', loc='bottom'))
    _cur(d, R6, '$i_x$', top=True)
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Resistor().right(u * 1.4).label('2 Ω', loc='top')
          .label(('+', '$v_o$', '−'), loc='bottom', color=ACCENT))
    d.add(elm.Line().right(u * 0.5))
    d.add(elm.Dot().label('$V_2$', loc='top', color=NODE))
    DV = d.add(elm.SourceControlledV().down().reverse().label('$2i_x$', loc='top'))
    _cur(d, DV, '$i_2$', top=False)
    d.add(elm.Line().left().tox(S.start))


def draw_p2_36(d):
    u = d.unit
    S = d.add(elm.SourceV().up().label('50 V', loc='top'))
    D20 = d.add(elm.SourceControlledV().right().label('$20i_\\sigma$', loc='top'))
    _cur(d, D20, '$i_a$', top=False, ofst=0.7)
    d.add(elm.Dot().label('$V_A$', loc='top', color=NODE))
    d.push()
    R18 = d.add(elm.Resistor().down().label('18 Ω', loc='bottom'))
    _cur(d, R18, '$i_\\Delta$', top=True)
    d.add(elm.Dot())
    d.pop()
    D5 = d.add(elm.SourceControlledV().right().reverse().label('$5i_\\sigma$', loc='top'))
    _cur(d, D5, '$i_b$', top=False, ofst=0.7)
    d.add(elm.Dot().label('$V_B$', loc='top', color=NODE))
    d.push()
    R40 = d.add(elm.Resistor().down().label('40 Ω', loc='bottom')
                .label(('+', '$v_o$', '−'), loc='top', color=ACCENT, ofst=0.9))
    _cur(d, R40, '$i_\\sigma$', top=True)
    d.add(elm.Dot())
    d.pop()
    d.add(elm.SourceControlledI().right().label('$8i_\\Delta$', loc='top'))
    d.add(elm.Line().right(u * 0.4))
    d.add(elm.Dot().label('$V_C$', loc='top', color=NODE))
    V20 = d.add(elm.SourceV().down().reverse().label('20 V', loc='top'))
    _cur(d, V20, '$i_c$', top=False)
    d.add(elm.Line().left().tox(S.start))


def draw_p2_37(d):
    u = d.unit
    # --- sol bölüm: v_g, 60 Ω, 260 Ω (seri) ---
    Vg = d.add(elm.SourceV().up().label('$v_g$', loc='top', color=ACCENT))
    R60 = d.add(elm.Resistor().right().label('60 Ω', loc='top'))
    _cur(d, R60, '$i_1$', top=False, ofst=0.4)
    d.add(elm.Resistor().down().label('260 Ω', loc='bottom'))
    B1 = d.add(elm.Dot())
    d.add(elm.Line().left().tox(Vg.start))
    # --- orta bölüm: 25 i_1 || 20 Ω || 80 Ω ---
    d.add(elm.Line().right(u * 1.0).at(B1.center))
    B2 = d.add(elm.Dot())
    d.add(elm.SourceControlledI().up().reverse().label('$25i_1$', loc='bottom'))
    d.add(elm.Line().right(u * 0.9))
    T2 = d.add(elm.Dot())
    d.add(elm.Resistor().down().label('20 Ω', loc='top')
          .label(('+', '$v_1$', '−'), loc='bottom', color=ACCENT))
    B3 = d.add(elm.Dot())
    d.add(elm.Line().right(u * 1.0).at(T2.center).label('$i_2$  →', loc='top', color=ACCENT))
    d.add(elm.Resistor().down().label('80 Ω', loc='bottom'))
    B4 = d.add(elm.Dot())
    d.add(elm.Line().left().at(B4.center).tox(B2.center))
    # --- sağ bölüm: 40 i_2 || 40 Ω || 10 Ω ---
    d.add(elm.Line().right(u * 1.0).at(B4.center))
    B5 = d.add(elm.Dot())
    d.add(elm.SourceControlledI().up().reverse().label('$40i_2$', loc='bottom'))
    d.add(elm.Line().right(u * 0.9))
    T5 = d.add(elm.Dot())
    d.add(elm.Resistor().down().label('40 Ω', loc='top')
          .label(('+', '$v_o$', '−'), loc='bottom', color=ACCENT))
    B6 = d.add(elm.Dot())
    d.add(elm.Line().right(u * 1.0).at(T5.center))
    d.add(elm.Resistor().down().label('10 Ω', loc='bottom'))
    d.add(elm.Line().left().tox(B5.center))


def draw_p2_9(d):
    u = d.unit
    S5 = d.add(elm.SourceV().up().label('5 V', loc='top'))
    R54 = d.add(elm.Resistor().right().label('54 kΩ', loc='top'))
    _cur(d, R54, '$i_1$', top=False, ofst=0.4)
    d.add(elm.SourceV().right(u * 0.9).label('1 V', loc='top'))
    d.add(elm.Dot().label('$V_A$', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down().label('6 kΩ', loc='bottom'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.SourceControlledI().right().reverse().label('$30i_1$', loc='bottom')
          .label(('+', '$v$', '−'), loc='top', color=ACCENT))
    d.add(elm.Dot().label('$V_R$', loc='top', color=NODE))
    R18 = d.add(elm.Resistor().right().label('1.8 kΩ', loc='top'))
    _cur(d, R18, '$30i_1$', top=False, reverse=True, ofst=0.4)
    V8 = d.add(elm.SourceV().down().reverse().label('8 V', loc='top'))
    d.add(elm.Line().left().tox(S5.start))


CIRCUITS = {
    "p2-10": draw_p2_10,
    "p2-32": draw_p2_32,
    "p2-36": draw_p2_36,
    "p2-37": draw_p2_37,
    "p2-9": draw_p2_9,
}

PROBLEMS = [
    dict(
        id="p2-10",
        topic=4,
        code="P2.10",
        title="Kontrol akımı $i_\\phi = 2\\ \\text{A}$ verildiğinde $v_s$ gerilimini ve güç dengesini bulma",
        source="Çalışma Yaprağı 1 s.7",
        image="PROB_2_10_ORIG.webp",
        circuit="p2-10",
        circuit_caption="Alt düğüm 0 V referans seçildiğinde sol üst düğüm $V_1 = 60\\ \\text{V}$, sağ üst düğüm $V_2 = v_s = 70\\ \\text{V}$ olur.",
        level=1,
        question=(
            "Şekildeki devrede $30\\ \\Omega$ dirençten geçen kontrol akımı $i_\\phi = 2\\ \\text{A}$ olarak verilmiştir. "
            "<strong>(a)</strong> $v_s$ gerilimini bulunuz. "
            "<strong>(b)</strong> Dirençlerde harcanan toplam gücü hesaplayınız. "
            "<strong>(c)</strong> Devredeki tüm elemanların güçlerini bularak $\\sum p = 0$ güç dengesini doğrulayınız."
        ),
        strategy=[
            "Alt teli $0\\ \\text{V}$ referans seçelim; $30\\ \\Omega$ dirençten aşağı doğru $i_\\phi = 2\\ \\text{A}$ geçtiğinden sol üst düğüm gerilimi doğrudan $V_1 = 30 \\cdot i_\\phi$ olur.",
            "Sol üst düğümde ($V_1$) KCL uygulayarak $10\\ \\Omega$ dirençten geçen $i_{10}$ akımını buluruz.",
            "$V_2 = V_1 - 10\\,i_{10}$ bağıntısından $v_s = V_2$ bulunur; ardından her eleman için pasif işaret kuralı ($+$ uçtan giren akım $\\to p = +vi$) ile güçler hesaplanır.",
        ],
        steps=[
            dict(
                title="Sol üst düğüm gerilimi $V_1$ ve bağımlı kaynak akımı",
                body=(
                    "$30\\ \\Omega$ dirençten aşağı doğru $i_\\phi = 2\\ \\text{A}$ geçtiği için Ohm kanunuyla sol üst düğüm gerilimi $V_1$ ve üstteki bağımlı akım kaynağının değeri hemen bulunur:"
                ),
                math=r"""\begin{aligned}
V_1 &= 30 \cdot i_\phi = 30 \cdot 2 = \boxed{60\ \text{V}} \\[4pt]
2i_\phi &= 2 \cdot 2 = 4\ \text{A} \quad (\text{soldan sağa})
\end{aligned}""",
            ),
            dict(
                title="Düğüm $V_1$'de KCL ve $v_s$ geriliminin hesabı",
                body=(
                    "$10\\ \\Omega$ dirençten soldan sağa ($V_1 \\to V_2$) geçen akıma $i_{10}$ diyelim. "
                    "Düğüm $V_1$'de KCL (çıkan akımlar $+$, girenler $-$) yazıp $V_2 = v_s$ gerilimini bulalım:"
                ),
                math=r"""\begin{aligned}
-5 + i_\phi + 2i_\phi + i_{10} &= 0 \\
-5 + 2 + 4 + i_{10} &= 0 \;\Longrightarrow\; i_{10} = -1\ \text{A} \quad (\text{yani sağdan sola } 1\ \text{A}) \\[6pt]
v_s = V_2 &= V_1 - 10\,i_{10} = 60 - 10(-1) = \boxed{70\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="Sağ düğümde KCL ve tüm elemanların güç tablosu ($\\sum p = 0$)",
                body=(
                    "Sağ üst düğüm $V_2$'ye soldan gelen toplam akım $i_{10} + 2i_\\phi$, aşağı doğru $v_s$ kaynağının $+$ ucundan içeri giren $i_s$ akımına eşittir:"
                ),
                math=r"""\begin{aligned}
i_s &= i_{10} + 2i_\phi = -1 + 4 = 3\ \text{A} \quad (v_s\text{'nin } + \text{ ucundan girer}) \\[6pt]
p_{30\Omega} &= i_\phi^2 \cdot 30 = 2^2 \cdot 30 = +120\ \text{W}, \qquad
p_{10\Omega} = i_{10}^2 \cdot 10 = (-1)^2 \cdot 10 = +10\ \text{W} \\
P_{\text{direnç}} &= 120 + 10 = \boxed{130\ \text{W}} \\[6pt]
p_{5\text{A}} &= -V_1 \cdot 5 = -60 \cdot 5 = -300\ \text{W} \quad (\text{akım } + \text{ uçtan çıkar, üretir}) \\
p_{2i_\phi} &= (V_1 - V_2) \cdot (2i_\phi) = (60 - 70) \cdot 4 = -40\ \text{W} \quad (\text{üretir}) \\
p_{v_s} &= +v_s \cdot i_s = 70 \cdot 3 = +210\ \text{W} \quad (\text{harcar}) \\[6pt]
\sum p &= (-300 - 40) + (120 + 10 + 210) = -340 + 340 = \boxed{0\ \text{W}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_s = 70\ \text{V}",
            r"P_{\text{direnç}} = 130\ \text{W}",
            r"\sum P_{\text{üretilen}} = \sum P_{\text{harcanan}} = 340\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&i_\phi = 2\ \text{A} \;\Longrightarrow\; V_1 = 30 \times 2 = 60\ \text{V}, \qquad 2i_\phi = 4\ \text{A} \\
&\text{KCL } (V_1):\ -5 + 2 + 4 + i_{10} = 0 \;\Longrightarrow\; i_{10} = -1\ \text{A} \\
&v_s = V_2 = V_1 - 10\,i_{10} = 60 - 10(-1) = 70\ \text{V} \\
&\text{KCL } (V_2):\ i_s = i_{10} + 2i_\phi = -1 + 4 = 3\ \text{A} \\[4pt]
&p_{30\Omega} = 2^2(30) = 120\ \text{W},\quad p_{10\Omega} = (-1)^2(10) = 10\ \text{W} \;\Rightarrow\; P_R = 130\ \text{W} \\
&p_{5\text{A}} = -60(5) = -300\ \text{W},\quad p_{2i_\phi} = (60-70)(4) = -40\ \text{W},\quad p_{v_s} = 70(3) = +210\ \text{W} \\
&\sum p = -300 - 40 + 120 + 10 + 210 = 0
\end{aligned}""",
        traps=[
            "$2i_\\phi$ bağımlı akım kaynağının üzerinde sıfır gerilim olduğu sanılmamalıdır; uçları arasındaki gerilim $V_1 - V_2 = 60 - 70 = -10\\ \\text{V}$'tur.",
            "$i_{10} = -1\\ \\text{A}$ negatif çıktığı için $V_2$ düğümü $V_1$'den daha yüksek potansiyeldedir ($70\\ \\text{V} > 60\\ \\text{V}$).",
        ],
    ),
    dict(
        id="p2-32",
        topic=4,
        code="P2.32",
        title="$45\\ \\text{A}$ ve $2i_x$ bağımlı kaynaklı devrede $v_o$ ve güç dengesi",
        source="Çalışma Yaprağı 1 s.8",
        image="PROB_2_32_ORIG.webp",
        circuit="p2-32",
        circuit_caption="Sol düğüm $V_1 = 6i_x = 90\\ \\text{V}$, sağ düğüm $V_2 = 2i_x = 30\\ \\text{V}$ ve $v_o = V_1 - V_2 = 60\\ \\text{V}$.",
        level=1,
        question=(
            "Şekildeki devrede: <strong>(a)</strong> $2\\ \\Omega$ direnç üzerindeki $v_o$ gerilimini bulunuz. "
            "<strong>(b)</strong> Her bir elemanın gücünü hesaplayarak devrede üretilen toplam gücü ve $\\sum p = 0$ dengesini gösteriniz."
        ),
        strategy=[
            "Alt düğümü referans ($0\\ \\text{V}$) seçtiğimizde sol düğüm gerilimi $V_1 = 6i_x$, sağ düğüm gerilimi ise bağımlı gerilim kaynağından dolayı doğrudan $V_2 = 2i_x$ olur.",
            "$2\\ \\Omega$ dirençten soldan sağa geçen akım $i_2 = (V_1 - V_2)/2 = (6i_x - 2i_x)/2 = 2i_x$ olarak $i_x$ cinsinden yazılır.",
            "Sol düğümde KCL ($-45 + i_x + 2i_x = 0$) ile $i_x = 15\\ \\text{A}$ bulunur ve tüm güçler hesaplanır.",
        ],
        steps=[
            dict(
                title="Düğüm gerilimlerini $i_x$ cinsinden yazma ve KCL",
                body=(
                    "Alt teli $0\\ \\text{V}$ referans alalım. Sol koldaki $6\\ \\Omega$ dirençten aşağı $i_x$ geçtiği için $V_1 = 6i_x$, "
                    "sağ koldaki bağımlı gerilim kaynağından dolayı $V_2 = 2i_x$ olur:"
                ),
                math=r"""\begin{aligned}
V_1 &= 6i_x, \qquad V_2 = 2i_x \\[4pt]
v_o &= V_1 - V_2 = 6i_x - 2i_x = 4i_x \\[4pt]
i_{2\Omega} &= \frac{v_o}{2} = \frac{4i_x}{2} = 2i_x \\[6pt]
\text{Düğüm } V_1 \text{ için KCL:}\quad
&-45 + i_x + i_{2\Omega} = 0 \\
&-45 + i_x + 2i_x = 0 \;\Longrightarrow\; 3i_x = 45 \;\Longrightarrow\; \boxed{i_x = 15\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="$v_o$ gerilimi ve düğüm potansiyelleri",
                body="$i_x = 15\\ \\text{A}$ değerini yerine koyduğumuzda:",
                math=r"""\begin{aligned}
V_1 &= 6 \cdot 15 = 90\ \text{V}, \qquad V_2 = 2 \cdot 15 = 30\ \text{V} \\[4pt]
v_o &= V_1 - V_2 = 90 - 30 = \boxed{60\ \text{V}}, \qquad i_2 = 2i_x = 30\ \text{A}
\end{aligned}""",
            ),
            dict(
                title="Güç hesabı ve $\\sum p = 0$ sağlaması",
                body=(
                    "$45\\ \\text{A}$ kaynağın akımı $V_1 = 90\\ \\text{V}$ düğümüne ($+$ uca) alttan girip üstten çıktığı için güç üretir. "
                    "Sağdaki $2i_x = 30\\ \\text{V}$ bağımlı kaynağın $+$ (üst) ucundan $i_2 = 30\\ \\text{A}$ akımı içeri girdiği için bu kaynak güç harcar (emer):"
                ),
                math=r"""\begin{aligned}
p_{45\text{A}} &= -V_1 \cdot 45 = -90 \cdot 45 = \boxed{-4050\ \text{W}\ (\text{üretir})} \\[4pt]
p_{6\Omega} &= i_x^2 \cdot 6 = 15^2 \cdot 6 = +1350\ \text{W} \\
p_{2\Omega} &= i_2^2 \cdot 2 = 30^2 \cdot 2 = +1800\ \text{W} \\
p_{2i_x} &= +(2i_x) \cdot i_2 = 30 \cdot 30 = +900\ \text{W}\ (\text{emer}) \\[6pt]
\sum p &= -4050 + 1350 + 1800 + 900 = \boxed{0\ \text{W}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_x = 15\ \text{A}",
            r"v_o = 60\ \text{V}",
            r"P_{\text{üretilen}} = 4050\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&V_1 = 6i_x,\qquad V_2 = 2i_x,\qquad v_o = V_1 - V_2 = 4i_x,\qquad i_2 = \frac{v_o}{2} = 2i_x \\
&\text{KCL } (V_1):\ -45 + i_x + 2i_x = 0 \;\Longrightarrow\; i_x = 15\ \text{A} \\
&\Longrightarrow\; V_1 = 90\ \text{V},\quad V_2 = 30\ \text{V},\quad v_o = 60\ \text{V},\quad i_2 = 30\ \text{A} \\[4pt]
&p_{45\text{A}} = -90 \times 45 = -4050\ \text{W},\quad p_{6\Omega} = 15^2(6) = 1350\ \text{W},\quad p_{2\Omega} = 30^2(2) = 1800\ \text{W} \\
&p_{2i_x} = +30 \times 30 = +900\ \text{W} \;\Longrightarrow\; \sum p = -4050 + 1350 + 1800 + 900 = 0
\end{aligned}""",
        traps=[
            "Bağımlı kaynak her zaman güç üretmez: burada $2i_x$ kaynağının $+$ (üst) ucundan $30\\ \\text{A}$ akım içeri girdiği için $p_{2i_x} = +900\\ \\text{W} > 0$'dır, yani güç emer.",
        ],
    ),
    dict(
        id="p2-36",
        topic=4,
        code="P2.36",
        title="Üç bağımlı kaynaklı ($20i_\\sigma$, $5i_\\sigma$, $8i_\\Delta$) devrede analiz ve tam güç tablosu",
        source="Çalışma Yaprağı 1 s.9",
        image="PROB_2_36_ORIG.webp",
        circuit="p2-36",
        circuit_caption="Düğüm gerilimleri $V_A$, $V_B = v_o$ ve $V_C = 20\\ \\text{V}$ tek bilinmeyen $i_\\sigma$ cinsinden yazılarak çözülür.",
        level=3,
        question=(
            "Şekildeki devrede: <strong>(a)</strong> $i_\\Delta$ akımını ve $v_o$ gerilimini bulunuz. "
            "<strong>(b)</strong> Devredeki 7 elemanın tamamı için güçleri hesaplayarak $\\sum p = 0$ güç dengesini doğrulayınız."
        ),
        strategy=[
            "Alt tel referans ($0\\ \\text{V}$) seçildiğinde sol üst köşe $50\\ \\text{V}$ olur. Üstteki $20i_\\sigma$ kaynağının $-$ ucu solda, $+$ ucu sağda olduğu için $V_A = 50 + 20i_\\sigma$ bulunur.",
            "$5i_\\sigma$ kaynağının $+$ ucu solda ($V_A$), $-$ ucu sağda ($V_B$) olduğundan $V_B = V_A - 5i_\\sigma = 50 + 15i_\\sigma$ olur.",
            "Aynı zamanda $V_B$ düğümü $40\\ \\Omega$ direnç üzerindedir ($V_B = 40i_\\sigma$); bu eşitlikten $i_\\sigma = 2\\ \\text{A}$ tek adımda bulunur!",
        ],
        steps=[
            dict(
                title="1. Aşama: $V_A$ ve $V_B$ düğüm gerilimlerini $i_\\sigma$ cinsinden yazma",
                body=(
                    "Alt teli $0\\ \\text{V}$ referans alalım. Soldaki $50\\ \\text{V}$ kaynak ve üstteki iki bağımlı gerilim kaynağının ($20i_\\sigma$ ve $5i_\\sigma$) kutuplarına dikkat ederek $V_A$ ve $V_B$ gerilimlerini $i_\\sigma$ cinsinden ifade edelim:"
                ),
                math=r"""\begin{aligned}
V_A &= 50 + 20i_\sigma \quad (\text{çünkü } 20i_\sigma \text{ kaynağının } + \text{ ucu } A \text{ tarafında}) \\[4pt]
V_B &= V_A - 5i_\sigma = (50 + 20i_\sigma) - 5i_\sigma = 50 + 15i_\sigma \\[6pt]
\text{Ayrıca } 40\ \Omega \text{ dirençte Ohm kanunu:}\quad
V_B &= 40i_\sigma \\[6pt]
50 + 15i_\sigma &= 40i_\sigma \;\Longrightarrow\; 25i_\sigma = 50 \;\Longrightarrow\; \boxed{i_\sigma = 2\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: $v_o$, $i_\\Delta$ ve kol akımlarının hesabı",
                body="$i_\\sigma = 2\\ \\text{A}$ bulunduğuna göre düğüm gerilimlerini ve kol akımlarını sırayla hesaplayalım:",
                math=r"""\begin{aligned}
v_o = V_B &= 40 \cdot 2 = \boxed{80\ \text{V}} \\[4pt]
V_A &= 50 + 20(2) = \boxed{90\ \text{V}} \\[4pt]
i_\Delta &= \frac{V_A}{18} = \frac{90}{18} = \boxed{5\ \text{A}}, \qquad
8i_\Delta = 8 \cdot 5 = 40\ \text{A} \quad (\text{sağa doğru}) \\[6pt]
\text{Düğüm } B \text{ KCL (soldan gelen } i_b \text{ akımı):}\quad
i_b &= i_\sigma + 8i_\Delta = 2 + 40 = 42\ \text{A} \\[4pt]
\text{Düğüm } A \text{ KCL (soldan gelen } i_a \text{ akımı):}\quad
i_a &= i_\Delta + i_b = 5 + 42 = 47\ \text{A}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: 7 elemanın güç tablosu ve $\\sum p = 0$ sağlaması",
                body=(
                    "Sağdaki $20\\ \\text{V}$ kaynağından dolayı $V_C = 20\\ \\text{V}$'tur; dolayısıyla $8i_\\Delta = 40\\ \\text{A}$ bağımlı akım kaynağının sol ucu $V_B = 80\\ \\text{V}$, sağ ucu $V_C = 20\\ \\text{V}$'tur:"
                ),
                math=r"""\begin{aligned}
p_{50\text{V}} &= -50 \cdot i_a = -50 \cdot 47 = -2350\ \text{W} \quad (\text{üretir}) \\
p_{20i_\sigma} &= -(20i_\sigma) \cdot i_a = -40 \cdot 47 = -1880\ \text{W} \quad (\text{akım } - \text{ uçtan girer, üretir}) \\
p_{18\Omega} &= i_\Delta^2 \cdot 18 = 5^2 \cdot 18 = +450\ \text{W} \\
p_{5i_\sigma} &= +(5i_\sigma) \cdot i_b = +10 \cdot 42 = +420\ \text{W} \quad (\text{akım } + \text{ uçtan girer, emer}) \\
p_{40\Omega} &= i_\sigma^2 \cdot 40 = 2^2 \cdot 40 = +160\ \text{W} \\
p_{8i_\Delta} &= (V_B - V_C) \cdot (8i_\Delta) = (80 - 20) \cdot 40 = +2400\ \text{W} \quad (\text{emer}) \\
p_{20\text{V}} &= +20 \cdot (8i_\Delta) = +20 \cdot 40 = +800\ \text{W} \quad (\text{emer}) \\[6pt]
\sum P_{\text{üretilen}} &= 2350 + 1880 = \boxed{4230\ \text{W}} \\
\sum P_{\text{harcanan}} &= 450 + 420 + 160 + 2400 + 800 = \boxed{4230\ \text{W}} \;\Longrightarrow\; \sum p = 0
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_\sigma = 2\ \text{A}",
            r"i_\Delta = 5\ \text{A}",
            r"v_o = 80\ \text{V}",
            r"\sum P_{\text{üretilen}} = \sum P_{\text{harcanan}} = 4230\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&V_A = 50 + 20i_\sigma,\qquad V_B = V_A - 5i_\sigma = 50 + 15i_\sigma,\qquad V_B = 40i_\sigma \\
&\Longrightarrow\; 50 + 15i_\sigma = 40i_\sigma \;\Longrightarrow\; i_\sigma = 2\ \text{A},\quad v_o = V_B = 80\ \text{V},\quad V_A = 90\ \text{V} \\
&i_\Delta = \frac{90}{18} = 5\ \text{A},\qquad 8i_\Delta = 40\ \text{A},\qquad i_b = 2 + 40 = 42\ \text{A},\qquad i_a = 5 + 42 = 47\ \text{A} \\[4pt]
&p_{50\text{V}} = -50(47) = -2350\ \text{W},\quad p_{20i_\sigma} = -40(47) = -1880\ \text{W},\quad p_{18\Omega} = 5^2(18) = 450\ \text{W} \\
&p_{5i_\sigma} = +10(42) = 420\ \text{W},\quad p_{40\Omega} = 2^2(40) = 160\ \text{W},\quad p_{8i_\Delta} = (80-20)(40) = 2400\ \text{W},\quad p_{20\text{V}} = 20(40) = 800\ \text{W} \\
&\sum p = -(2350 + 1880) + (450 + 420 + 160 + 2400 + 800) = -4230 + 4230 = 0
\end{aligned}""",
        traps=[
            "$20i_\\sigma$ kaynağının $-$ ucu solda, $+$ ucu sağda olduğu için potansiyeli yükseltir ($50 + 20i_\\sigma$); $5i_\\sigma$ kaynağının ise $+$ ucu solda olduğu için potansiyeli düşürür ($V_A - 5i_\\sigma$).",
            "$8i_\\Delta$ akım kaynağının gücü hesaplanırken iki ucu arasındaki gerilim farkı $V_B - V_C = 80 - 20 = 60\\ \\text{V}$ alınmalıdır.",
        ],
    ),
    dict(
        id="p2-37",
        topic=4,
        code="P2.37",
        title="Üç kademeli bağımlı kaynaklı devrede sondan başa ($v_o = 5\\ \\text{V} \\to v_g$) analiz",
        source="Çalışma Yaprağı 1 s.10",
        image="PROB_2_37_ORIG.webp",
        circuit="p2-37",
        circuit_caption="Sağ kademede $v_o = 5\\ \\text{V}$ bilindiğinden geriye doğru $i_2 \\to v_1 \\to i_1 \\to v_g = 1\\ \\text{V}$ sırasıyla bulunur.",
        level=2,
        question=(
            "Şekildeki üç kademeli devrede çıkış gerilimi $v_o = 5\\ \\text{V}$ olarak verilmiştir. "
            "<strong>(a)</strong> Orta kademedeki $v_1$ gerilimini ve girişteki $v_g$ kaynak gerilimini bulunuz. "
            "<strong>(b)</strong> Devrede üretilen/harcanan toplam gücü hesaplayınız."
        ),
        strategy=[
            "Üç kademe birbirine yalnızca alt referans teliyle (ve bağımlı kaynakların kontrol değişkenleriyle) bağlıdır; kademeler arasındaki tek alt telden akım geçmez.",
            "En sağdaki kademede $v_o = 5\\ \\text{V}$ bilindiğinden $40\\ \\Omega$ ve $10\\ \\Omega$ direnç akımları toplanarak $40i_2$ bulunur $\\to i_2$ elde edilir.",
            "Orta kademede $i_2$ akımı doğrudan $80\\ \\Omega$ dirençten geçtiği için $v_1 = 80i_2$ bulunur; buradan $25i_1 \\to i_1$ ve sol kademede $v_g = (60+260)i_1$ hesaplanır.",
        ],
        steps=[
            dict(
                title="1. Aşama: Sağ kademeden $i_2$ akımını bulma ($v_o = 5\\ \\text{V}$)",
                body=(
                    "Sağ kademede $40\\ \\Omega$ ve $10\\ \\Omega$ dirençler paraleldir ve üzerlerindeki gerilim $v_o = 5\\ \\text{V}$'tur. "
                    "Üst düğümde KCL (aşağı inen tüm kolların toplamı $= 0$) yazalım:"
                ),
                math=r"""\begin{aligned}
40i_2 + \frac{v_o}{40} + \frac{v_o}{10} &= 0 \\[4pt]
40i_2 + \frac{5}{40} + \frac{5}{10} &= 0 \;\Longrightarrow\; 40i_2 + 0.125 + 0.5 = 0 \\[4pt]
40i_2 &= -0.625 = -\frac{5}{8}\ \text{A} \;\Longrightarrow\; \boxed{i_2 = -\frac{1}{64}\ \text{A} = -15.625\ \text{mA}}
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: Orta kademeden $v_1$ gerilimini ve $i_1$ akımını bulma",
                body=(
                    "Orta kademede sağ üstten $80\\ \\Omega$ dirence giren akım $i_2$ olduğundan Ohm kanunuyla $v_1 = 80i_2$ bulunur. "
                    "Ardından orta üst düğümde KCL ile $25i_1$ ve $i_1$ hesaplanır:"
                ),
                math=r"""\begin{aligned}
v_1 &= 80\,i_2 = 80 \cdot \left(-\frac{1}{64}\right) = -\frac{5}{4}\ \text{V} = \boxed{-1.25\ \text{V}} \\[6pt]
\text{Orta üst düğümde KCL:}\quad
&25i_1 + \frac{v_1}{20} + i_2 = 0 \\[4pt]
&25i_1 + \frac{-1.25}{20} + (-0.015625) = 0 \\
&25i_1 - 0.0625 - 0.015625 = 0 \;\Longrightarrow\; 25i_1 = 0.078125 = \frac{5}{64}\ \text{A} \\[4pt]
&\Longrightarrow\; \boxed{i_1 = \frac{1}{320}\ \text{A} = 3.125\ \text{mA}}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Sol kademeden $v_g$ gerilimini ve toplam gücü bulma",
                body=(
                    "Sol kademede $v_g$ kaynağı, $60\\ \\Omega$ ve $260\\ \\Omega$ dirençlerle tek bir seri göz oluşturur:"
                ),
                math=r"""\begin{aligned}
v_g &= (60 + 260)\,i_1 = 320 \cdot \frac{1}{320} = \boxed{1\ \text{V}} \\[8pt]
\text{Her kademede dirençlerin harcadığı (= kaynakların ürettiği) güç:}& \\
P_{\text{sol}} &= v_g \cdot i_1 = 1 \cdot 3.125\ \text{mA} = 3.125\ \text{mW} \\
P_{\text{orta}} &= \frac{v_1^2}{20} + \frac{v_1^2}{80} = 78.125 + 19.53125 = 97.65625\ \text{mW} \\
P_{\text{sağ}} &= \frac{v_o^2}{40} + \frac{v_o^2}{10} = 625 + 2500 = 3125\ \text{mW} \\[4pt]
P_{\text{toplam}} &= 3.125 + 97.65625 + 3125 = \boxed{3225.78125\ \text{mW} \approx 3.226\ \text{W}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_2 = -15.625\ \text{mA}",
            r"v_1 = -1.25\ \text{V}",
            r"i_1 = 3.125\ \text{mA}",
            r"v_g = 1\ \text{V}",
            r"P_{\text{toplam}} \approx 3.226\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&\textbf{Sağ kademe } (v_o = 5\ \text{V}):\quad 40i_2 + \frac{5}{40} + \frac{5}{10} = 0 \;\Longrightarrow\; 40i_2 = -\frac{5}{8}\ \text{A} \;\Longrightarrow\; i_2 = -\frac{1}{64}\ \text{A} = -15.625\ \text{mA} \\[3pt]
&\textbf{Orta kademe:}\quad v_1 = 80\,i_2 = 80\left(-\frac{1}{64}\right) = -1.25\ \text{V} \\
&25i_1 + \frac{-1.25}{20} + \left(-\frac{1}{64}\right) = 0 \;\Longrightarrow\; 25i_1 = \frac{5}{64}\ \text{A} \;\Longrightarrow\; i_1 = \frac{1}{320}\ \text{A} = 3.125\ \text{mA} \\[3pt]
&\textbf{Sol kademe:}\quad v_g = (60 + 260)\,i_1 = 320 \times \frac{1}{320} = 1\ \text{V} \\[3pt]
&P_{\text{toplam}} = 3.125\ \text{mW} + 97.65625\ \text{mW} + 3125\ \text{mW} = 3225.78\ \text{mW}
\end{aligned}""",
        traps=[
            "$40i_2$ kaynağının oku <strong>aşağı</strong> doğru olduğu için direnç akımlarıyla aynı yöndedir; bu nedenle $40i_2 = -0.625\\ \\text{A}$ negatif çıkar.",
            "Orta ve sağ kademeler yalnızca alt telle birbirine bağlıdır; üstten bir dönüş yolu olmadığı için alt telden kademeler arası akım geçmez.",
        ],
    ),
    dict(
        id="p2-9",
        topic=4,
        code="P2.9",
        title="$30i_1$ bağımlı akım kaynaklı devrede $i_1$, $v$ ve mikro-watt düzeyinde güç dengesi",
        source="Çalışma Yaprağı 1 s.7",
        image="PROB_2_9_ORIG.webp",
        circuit="p2-9",
        circuit_caption="Düğüm $V_A$'ya soldan $i_1$, sağdan $30i_1$ girer; $6\\ \\text{k}\\Omega$ dirençten aşağı $31i_1$ iner.",
        level=2,
        question=(
            "Şekildeki devrede: <strong>(a)</strong> $i_1$ akımını ve bağımlı akım kaynağı üzerindeki $v$ gerilimini bulunuz. "
            "<strong>(b)</strong> Tüm elemanların güçlerini hesaplayarak $\\sum p = 0$ dengesini gösteriniz."
        ),
        strategy=[
            "Orta düğüm $V_A$'ya soldan $i_1$ ve sağdaki bağımlı kaynaktan $30i_1$ akımı girdiği için, $6\\ \\text{k}\\Omega$ dirençten aşağı inen akım $i_1 + 30i_1 = 31i_1$ olur.",
            "Dolayısıyla orta düğüm gerilimi $V_A = 6\\ \\text{k}\\Omega \\times 31i_1 = 186\\ \\text{k}\\Omega \\cdot i_1$ olarak doğrudan $i_1$'e bağlanır.",
            "Sol koldaki KVL ($5 - 54\\,\\text{k}\\Omega \\cdot i_1 + 1 = V_A$) ile $i_1 = 25\\ \\mu\\text{A}$ bulunur; sağ koldan $V_R$ bulunup $v = V_A - V_R$ hesaplanır.",
        ],
        steps=[
            dict(
                title="1. Aşama: Orta düğümde KCL ve sol kolda KVL ile $i_1$'in hesabı",
                body=(
                    "Alt teli $0\\ \\text{V}$ referans alalım. Orta düğüm $V_A$'ya soldan $i_1$, sağdan $30i_1$ akımı girdiği için $6\\ \\text{k}\\Omega$ dirençten aşağı inen akım $31i_1$ olur:"
                ),
                math=r"""\begin{aligned}
i_{6\text{k}\Omega} &= i_1 + 30i_1 = 31i_1 \\[4pt]
V_A &= 6000 \cdot (31i_1) = 186000\,i_1 \\[6pt]
\text{Sol koldan } V_A \text{ potansiyeli (1 V kaynağın } + \text{ ucu sağda):}& \\
V_A &= 5 - 54000\,i_1 + 1 = 6 - 54000\,i_1 \\[6pt]
186000\,i_1 &= 6 - 54000\,i_1 \;\Longrightarrow\; 240000\,i_1 = 6 \\[4pt]
i_1 &= \frac{6}{240000} = \boxed{25\ \mu\text{A} = 0.025\ \text{mA}}
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: $V_A$, $V_R$ ve bağımlı kaynak gerilimi $v$",
                body=(
                    "Sağ koldaki $8\\ \\text{V}$ kaynaktan sola doğru $30i_1$ akımı $1.8\\ \\text{k}\\Omega$ direnç üzerinden geçerek bağımlı kaynağa ulaşır:"
                ),
                math=r"""\begin{aligned}
V_A &= 186000 \cdot (25 \times 10^{-6}) = \boxed{4.65\ \text{V}} \\[4pt]
30i_1 &= 30 \cdot (25\ \mu\text{A}) = 750\ \mu\text{A} = 0.75\ \text{mA} \\[4pt]
V_R &= 8 - 1800 \cdot (0.75 \times 10^{-3}) = 8 - 1.35 = \boxed{6.65\ \text{V}} \\[6pt]
v &= V_A - V_R = 4.65 - 6.65 = \boxed{-2\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Tüm elemanların güçleri ($\\mu\\text{W}$) ve $\\sum p = 0$",
                body=(
                    "Bağımlı akım kaynağında $30i_1 = 750\\ \\mu\\text{A}$ akımı sağdan sola, yani $-$ uçtan girip $+$ (sol) uçtan çıktığı için $p_{30i_1} = -v \\cdot (30i_1)$ formülü uygulanır:"
                ),
                math=r"""\begin{aligned}
p_{5\text{V}} &= -5 \cdot 25\ \mu\text{A} = -125\ \mu\text{W} \quad (\text{üretir}) \\
p_{1\text{V}} &= -1 \cdot 25\ \mu\text{A} = -25\ \mu\text{W} \quad (\text{akım } - \text{ uçtan girer, üretir}) \\
p_{8\text{V}} &= -8 \cdot 750\ \mu\text{A} = -6000\ \mu\text{W} \quad (\text{üretir}) \\[4pt]
p_{54\text{k}\Omega} &= (25\ \mu\text{A})^2 \cdot 54000 = +33.75\ \mu\text{W} \\
p_{6\text{k}\Omega} &= (775\ \mu\text{A})^2 \cdot 6000 = +3603.75\ \mu\text{W} \\
p_{1.8\text{k}\Omega} &= (750\ \mu\text{A})^2 \cdot 1800 = +1012.5\ \mu\text{W} \\
p_{30i_1} &= -v \cdot (30i_1) = -(-2\ \text{V}) \cdot 750\ \mu\text{A} = +1500\ \mu\text{W} \quad (\text{emer}) \\[6pt]
\sum P_{\text{üretilen}} &= 125 + 25 + 6000 = \boxed{6150\ \mu\text{W} = 6.15\ \text{mW}} \\
\sum P_{\text{harcanan}} &= 33.75 + 3603.75 + 1012.5 + 1500 = \boxed{6150\ \mu\text{W} = 6.15\ \text{mW}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_1 = 25\ \mu\text{A}",
            r"v = -2\ \text{V}",
            r"\sum P_{\text{üretilen}} = \sum P_{\text{harcanan}} = 6.15\ \text{mW}",
        ],
        exam=r"""\begin{aligned}
&\text{KCL } (V_A):\ i_{6\text{k}} = i_1 + 30i_1 = 31i_1 \;\Longrightarrow\; V_A = 6\ \text{k}\Omega \times 31i_1 = 186\ \text{k}\Omega \cdot i_1 \\
&\text{Sol kol: } 5 - 54\ \text{k}\Omega \cdot i_1 + 1 = 186\ \text{k}\Omega \cdot i_1 \;\Longrightarrow\; 240\ \text{k}\Omega \cdot i_1 = 6 \;\Longrightarrow\; i_1 = 25\ \mu\text{A} \\
&V_A = 4.65\ \text{V},\qquad 30i_1 = 0.75\ \text{mA},\qquad V_R = 8 - 1.8\ \text{k}\Omega \times 0.75\ \text{mA} = 6.65\ \text{V} \\
&v = V_A - V_R = 4.65 - 6.65 = -2\ \text{V} \\[3pt]
&\sum P_{\text{üretilen}} = 125 + 25 + 6000 = 6150\ \mu\text{W} = \sum P_{\text{harcanan}}
\end{aligned}""",
        traps=[
            "Üstteki $1\\ \\text{V}$ kaynağının $-$ ucu solda, $+$ ucu sağda olduğu için $5\\ \\text{V}$ kaynakla aynı yönde potansiyel ekler ($5 + 1 = 6\\ \\text{V}$).",
            "$30i_1$ kaynağında akım $+$ (sol) uçtan dışarı çıktığı için $p = -v \\cdot (30i_1)$ olur; ancak $v = -2\\ \\text{V}$ negatif çıktığından $p = -(-2)(750\\ \\mu\\text{A}) = +1500\\ \\mu\\text{W} > 0$ (güç emer).",
        ],
    ),
]
