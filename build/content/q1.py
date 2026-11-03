# -*- coding: utf-8 -*-
"""
SORU 1 — Bağımlı kaynaklı maksimum güç transferi (Thévenin / Norton).
İçerik şeması için bkz. build/CONTENT_SPEC.md
"""
from circuitkit import elm, ACCENT, NODE


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
def draw_p4_87(d):
    V = d.add(elm.SourceV().up().label('110 V', loc='top'))
    d.add(elm.Resistor().right().label('15 Ω')
          .label(('+', '$v_\\Delta$', '−'), loc='bottom', color=ACCENT))
    d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.push()
    d.add(elm.SourceControlledI().down().reverse().label('$0.1v_\\Delta$', loc='bottom'))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.pop()
    d.add(elm.Resistor().right().label('5 Ω')
          .label('$\\leftarrow i_\\Delta$', loc='bottom', color=ACCENT))
    d.add(elm.Dot().label('$V_2$', loc='top', color=NODE))
    d.push()
    d.add(elm.SourceControlledV().down(d.unit * 0.55).label('$3i_\\Delta$', loc='bottom'))
    d.add(elm.Resistor().down(d.unit * 0.45).label('8 Ω', loc='bottom'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Line().right(d.unit * 0.8))
    d.add(elm.Dot(open=True).label('a', loc='right'))
    d.add(elm.ResistorVar().down().label('$R_o$', loc='bottom'))
    d.add(elm.Dot(open=True).label('b', loc='right'))
    d.add(elm.Line().left().tox(V.start))


CIRCUITS = {
    "p4-87": draw_p4_87,
}


# ---------------------------------------------------------------------------
# PROBLEMLER
# ---------------------------------------------------------------------------
PROBLEMS = [
    dict(
        id="p4-87",
        topic=1,
        code="P4.87",
        title="İki bağımlı kaynaklı devrede $R_o$ ve $P_{max}$",
        source="Çalışma Yaprağı 3 s.3 · ÇY4 s.1 · Tuna Hoca tahtada çözdü",
        image="P4_87_ORIG.webp",
        circuit="p4-87",
        circuit_caption="Çözüm şeması: alt tel referans (0 V); üst düğümler $V_1$ ve $V_2$.",
        level=2,
        featured=True,
        question=(
            "Şekildeki devrede değişken direnç $R_o$ ayarlanmaktadır. "
            "$R_o$'ya <strong>maksimum güç</strong> aktarılması için $R_o$ kaç ohm olmalıdır? "
            "Bu durumda $R_o$'ya aktarılan maksimum güç kaç watt'tır?"
        ),
        strategy=[
            "Devrede bağımlı kaynak var → kaynakları öldürüp $R_{eq}$ <strong>aranmaz</strong>.",
            "$R_o$'yu sök → açık devre gerilimi $V_{Th}$.",
            "a–b'yi kısa devre et → kısa devre akımı $I_{sc}$.",
            "$R_o = R_{Th} = V_{Th}/I_{sc}$, &nbsp; $P_{max} = V_{Th}^2 / (4R_{Th})$.",
        ],
        steps=[
            dict(
                title="Kontrol değişkenlerini düğüm gerilimleriyle yaz (ek denklemler)",
                body=(
                    "Alt teli referans (0 V) seçelim. 110 V kaynağın üst ucu bu yüzden 110 V'tur. "
                    "Ortadaki düğüme $V_1$, sağ üst düğüme $V_2$ diyelim.<br>"
                    "• $v_\\Delta$: 15 Ω'un <em>+</em> ucu 110 V'ta, <em>−</em> ucu $V_1$'de.<br>"
                    "• $i_\\Delta$: şekildeki ok <strong>sola</strong> bakıyor, yani akım $V_2$'den $V_1$'e akıyor. "
                    "Akım = (çıktığı düğüm − girdiği düğüm) / R."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad v_\Delta &= 110 - V_1 \\
\textbf{ek 2:}\quad i_\Delta &= \frac{V_2 - V_1}{5}
\end{aligned}""",
                note="Tahtada da aynı iki satır “ek 1 / ek 2” diye sağ üst köşeye yazıldı. Sınavda ilk iş budur.",
            ),
            dict(
                title="$V_1$ düğümünde KCL (açık devre, $R_o$ sökülü)",
                body=(
                    "Düğümden <strong>çıkan</strong> akımlar + , düğüme <strong>giren</strong> akımlar − yazılır. "
                    "$0.1v_\\Delta$ kaynağının oku yukarı, yani akım $V_1$'e <em>giriyor</em> → eksi işaretli."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - 110}{15} - 0.1\,v_\Delta + \frac{V_1 - V_2}{5} &= 0 \\
\frac{V_1 - 110}{15} - 0.1\,(110 - V_1) + \frac{V_1 - V_2}{5} &= 0 \qquad /\times 30 \\
2(V_1 - 110) - 3(110 - V_1) + 6(V_1 - V_2) &= 0 \\
2V_1 - 220 - 330 + 3V_1 + 6V_1 - 6V_2 &= 0 \\
\boxed{11V_1 - 6V_2 = 550} &\qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="$V_2$ düğümünde KCL",
                body=(
                    "Sağdaki dikey kolda $3i_\\Delta$ kaynağı ile 8 Ω seri. Kaynağın <em>+</em> ucu altta olduğundan "
                    "8 Ω'un üst ucunun gerilimi $V_2 + 3i_\\Delta$'dır. Bu koldan aşağı inen akım "
                    "$(V_2 + 3i_\\Delta)/8$ olur."
                ),
                math=r"""\begin{aligned}
\frac{V_2 - V_1}{5} + \frac{V_2 + 3i_\Delta}{8} &= 0 \\
\frac{V_2 - V_1}{5} + \frac{V_2 + \tfrac{3}{5}(V_2 - V_1)}{8} &= 0 \qquad /\times 40 \\
8(V_2 - V_1) + 5V_2 + 3(V_2 - V_1) &= 0 \\
8V_2 - 8V_1 + 5V_2 + 3V_2 - 3V_1 &= 0 \\
\boxed{-11V_1 + 16V_2 = 0} &\qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="Denklemleri çöz → $V_{Th}$",
                body="(I) ve (II)'yi alt alta toplarsak $V_1$ yok olur.",
                math=r"""\begin{aligned}
(11V_1 - 6V_2) + (-11V_1 + 16V_2) &= 550 + 0 \\
10V_2 &= 550 \;\Rightarrow\; V_2 = 55\ \text{V} \\
V_1 &= \tfrac{16}{11}\cdot 55 = 80\ \text{V} \\[4pt]
V_{Th} = V_{ab} = V_2 &= \boxed{55\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="a–b kısa devre → $I_{sc}$",
                body=(
                    "a ile b'yi düz telle birleştirince $V_2 = 0$ olur. (I) denklemi aynen geçerlidir "
                    "(çünkü $V_1$ düğümünün bağlantıları değişmedi). Sonra her koldaki akımı tek tek buluruz."
                ),
                math=r"""\begin{aligned}
11V_1 - 6(0) &= 550 \;\Rightarrow\; V_1 = 50\ \text{V} \\
i_\Delta &= \frac{0 - 50}{5} = -10\ \text{A} \quad (\text{yani 10 A soldan sağa}) \\
i_{8\Omega,\downarrow} &= \frac{0 + 3(-10)}{8} = -3.75\ \text{A} \quad (\text{yani 3.75 A yukarı}) \\[4pt]
I_{sc} &= \underbrace{10}_{5\,\Omega\text{'dan gelen}} + \underbrace{3.75}_{8\,\Omega\text{ kolundan gelen}} = \boxed{13.75\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="$R_o$ ve maksimum güç",
                body="Maksimum güç, yük direnci Thévenin direncine eşit olduğunda aktarılır.",
                math=r"""\begin{aligned}
R_o = R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{55}{13.75} = \boxed{4\ \Omega} \\[4pt]
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{55^2}{4\cdot 4} = \frac{3025}{16} = \boxed{189.06\ \text{W}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"V_{Th} = 55\ \text{V}",
            r"I_{sc} = 13.75\ \text{A}",
            r"R_o = R_{Th} = 4\ \Omega",
            r"P_{max} \approx 189.06\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&\text{ek 1: } v_\Delta = 110 - V_1, \qquad \text{ek 2: } i_\Delta = \tfrac{V_2 - V_1}{5} \\[2pt]
&\textbf{Açık devre:}\\
&V_1:\ \tfrac{V_1-110}{15} - 0.1(110 - V_1) + \tfrac{V_1 - V_2}{5} = 0 \;\Rightarrow\; 11V_1 - 6V_2 = 550 \\
&V_2:\ \tfrac{V_2 - V_1}{5} + \tfrac{V_2 + 3i_\Delta}{8} = 0 \;\Rightarrow\; -11V_1 + 16V_2 = 0 \\
&\Rightarrow V_1 = 80\ \text{V},\quad V_{Th} = V_2 = 55\ \text{V} \\[2pt]
&\textbf{Kısa devre } (V_2 = 0):\ V_1 = 50\ \text{V},\ i_\Delta = -10\ \text{A},\ i_{8\Omega} = -3.75\ \text{A} \\
&I_{sc} = 10 + 3.75 = 13.75\ \text{A} \\[2pt]
&R_o = R_{Th} = 55/13.75 = 4\ \Omega,\qquad P_{max} = \tfrac{55^2}{4\cdot 4} = 189.06\ \text{W}
\end{aligned}""",
        traps=[
            "$i_\\Delta$'nın oku <strong>sola</strong> bakıyor: $i_\\Delta = (V_2 - V_1)/5$. Ters yazarsan sonuç tamamen değişir.",
            "$3i_\\Delta$ kaynağının <strong>+ ucu altta</strong>: 8 Ω'un üst ucu $V_2 + 3i_\\Delta$ olur, $V_2 - 3i_\\Delta$ değil.",
            "Bağımlı kaynak varken 'kaynakları kapatıp' $R_{Th}$ hesaplamak yanlıştır; $V_{Th}/I_{sc}$ kullan.",
        ],
    ),
]
