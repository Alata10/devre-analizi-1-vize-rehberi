# -*- coding: utf-8 -*-
"""
SORU 1 (devam) — Bağımlı kaynaklı maksimum güç transferi: P4.89, P4.91, P4.90.
İçerik şeması için bkz. build/CONTENT_SPEC.md
Sayısal doğrulama: build/verify/q1c_verify.py
"""
from circuitkit import elm, ACCENT, NODE


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
def draw_p4_89(d):
    # x: 16Ω | 180 V | R_o | 10 Ω | 0.1v_Δ ;  y: üst kol / direnç sırası / alt tel
    x0, x1, x2, x3, x4 = 0, 3.2, 6.4, 9.6, 12.2
    yt, ym, yb = 2.3, 0, -3
    # direnç sırası
    d.add(elm.Resistor().endpoints((x0, ym), (x1, ym)).label('20 Ω'))
    d.add(elm.Resistor().endpoints((x1, ym), (x2, ym)).label('2 Ω')
          .label(('−', '$v_\\Delta$', '+'), loc='bottom', color=ACCENT))
    d.add(elm.Resistor().endpoints((x2, ym), (x3, ym)).label('8 Ω'))
    d.add(elm.Line().endpoints((x3, ym), (x4, ym)))
    # dikey kollar
    d.add(elm.Resistor().endpoints((x0, ym), (x0, yb)).label('16 Ω', loc='bottom'))
    d.add(elm.SourceV().endpoints((x1, yb), (x1, ym)).label('180 V', loc='bottom'))
    d.add(elm.ResistorVar().endpoints((x2, ym), (x2, yb)).label('$R_o$', loc='bottom')
          .label('$i_\\phi\\downarrow$', loc='top', color=ACCENT))
    d.add(elm.Resistor().endpoints((x3, ym), (x3, yb)).label('10 Ω', loc='bottom'))
    d.add(elm.SourceControlledI().endpoints((x4, yb), (x4, ym)).label('$0.1v_\\Delta$', loc='bottom'))
    # alt tel
    d.add(elm.Line().endpoints((x0, yb), (x4, yb)))
    for x in (x1, x2, x3):
        d.add(elm.Dot().at((x, yb)))
    d.add(elm.Ground().at((x2, yb)))
    # üst kol: 184 i_φ (+ solda)
    d.add(elm.Line().endpoints((x0, ym), (x0, yt)))
    d.add(elm.SourceControlledV().endpoints((x3, yt), (x0, yt)).label('$184i_\\phi$', loc='bottom'))
    d.add(elm.Line().endpoints((x3, yt), (x3, ym)))
    # düğümler
    d.add(elm.Dot().at((x0, ym)).label('$V_1$', loc='left', color=NODE))
    d.add(elm.Dot().at((x1, ym)).label('180 V', loc='top', color=NODE, ofst=0.15))
    d.add(elm.Dot().at((x2, ym)).label('$V_2$', loc='top', color=NODE))
    d.add(elm.Dot().at((x3, ym)).label('$V_3$', loc='right', color=NODE, ofst=(0.1, 0.35)))


def draw_p4_91(d):
    x0, x1, x2, x3 = 0, 3.6, 6.4, 10
    yt, ym, yb = 2.3, 0, -3
    # sol kol: 400 V (− üstte, + altta)
    d.add(elm.SourceV().endpoints((x0, ym), (x0, yb)).label('400 V', loc='bottom'))
    d.add(elm.Resistor().endpoints((x0, ym), (x1, ym)).label('16 Ω'))
    d.add(elm.Line().endpoints((x1, ym), (x2, ym)))
    d.add(elm.Resistor().endpoints((x2, ym), (x3, ym)).label('32 Ω'))
    # sağ kol: 200 V (− üstte, + altta)
    d.add(elm.SourceV().endpoints((x3, ym), (x3, yb)).label('200 V', loc='top'))
    # orta kollar
    d.add(elm.Resistor().endpoints((x1, ym), (x1, yb)).label('180 Ω', loc='bottom')
          .label('$i_\\Delta\\downarrow$', loc='top', color=ACCENT))
    d.add(elm.ResistorVar().endpoints((x2, ym), (x2, yb)).label('$R_o$', loc='bottom'))
    # alt tel
    d.add(elm.Resistor().endpoints((x0, yb), (x1, yb)).label('64 Ω'))
    d.add(elm.Line().endpoints((x1, yb), (x2, yb)))
    d.add(elm.Resistor().endpoints((x2, yb), (x3, yb)).label('48 Ω'))
    d.add(elm.Dot().at((x1, yb)))
    d.add(elm.Dot().at((x2, yb)))
    d.add(elm.Ground().at((x1, yb)))
    # üst kol: 316 i_Δ (+ solda)
    d.add(elm.Line().endpoints((x0, ym), (x0, yt)))
    d.add(elm.SourceControlledV().endpoints((x3, yt), (x0, yt)).label('$316i_\\Delta$', loc='bottom'))
    d.add(elm.Line().endpoints((x3, yt), (x3, ym)))
    # düğümler
    d.add(elm.Dot().at((x0, ym)).label('$V_1$', loc='right', color=NODE, ofst=(0.1, 0.35)))
    d.add(elm.Dot().at((x1, ym)).label('$V_2$', loc='top', color=NODE))
    d.add(elm.Dot().at((x2, ym)))
    d.add(elm.Dot().at((x3, ym)).label('$V_3$', loc='left', color=NODE, ofst=(-0.1, 0.35)))
    d.add(elm.Label().at((x0 - 0.2, yb - 0.45)).label('$V_1+400$', color=NODE))
    d.add(elm.Label().at((x3 + 0.2, yb - 0.45)).label('$V_3+200$', color=NODE))


def draw_p4_90(d):
    x0, x1, x2, x3 = 0, 3.6, 6.4, 10
    yt, ym, yb = 2.3, 0, -3
    # sol kol: 3.6 kV (+ üstte)
    d.add(elm.SourceV().endpoints((x0, yb), (x0, ym)).label('3.6 kV', loc='top'))
    d.add(elm.Resistor().endpoints((x0, ym), (x1, ym)).label('45 Ω')
          .label('$i_\\beta \\rightarrow$', loc='bottom', color=ACCENT))
    d.add(elm.Line().endpoints((x1, ym), (x2, ym)))
    d.add(elm.Resistor().endpoints((x2, ym), (x3, ym)).label('60 Ω'))
    # orta kollar
    d.add(elm.Resistor().endpoints((x1, ym), (x1, yb)).label('300 Ω', loc='bottom'))
    d.add(elm.ResistorVar().endpoints((x2, ym), (x2, yb)).label('$R_L$', loc='bottom'))
    # sağ kol: 150 i_β (− üstte, + altta)
    d.add(elm.SourceControlledV().endpoints((x3, ym), (x3, yb)).label('$150i_\\beta$', loc='bottom'))
    # alt tel
    d.add(elm.Resistor().endpoints((x0, yb), (x1, yb)).label('30 Ω'))
    d.add(elm.Line().endpoints((x1, yb), (x2, yb)))
    d.add(elm.Resistor().endpoints((x2, yb), (x3, yb)).label('15 Ω'))
    d.add(elm.Dot().at((x1, yb)))
    d.add(elm.Dot().at((x2, yb)))
    d.add(elm.Ground().at((x1, yb)))
    # üst kol: 30 Ω
    d.add(elm.Line().endpoints((x0, ym), (x0, yt)))
    d.add(elm.Resistor().endpoints((x0, yt), (x3, yt)).label('30 Ω'))
    d.add(elm.Line().endpoints((x3, yt), (x3, ym)))
    # düğümler
    d.add(elm.Dot().at((x0, ym)).label('$V_1$', loc='right', color=NODE, ofst=(0.1, 0.35)))
    d.add(elm.Dot().at((x1, ym)).label('$V_2$', loc='top', color=NODE))
    d.add(elm.Dot().at((x2, ym)))
    d.add(elm.Dot().at((x3, ym)).label('$V_3$', loc='left', color=NODE, ofst=(-0.1, 0.35)))
    d.add(elm.Label().at((x0 - 0.2, yb - 0.45)).label('$V_1-3600$', color=NODE))
    d.add(elm.Label().at((x3 + 0.2, yb - 0.45)).label('$V_3+150i_\\beta$', color=NODE))


CIRCUITS = {
    "p4-89": draw_p4_89,
    "p4-91": draw_p4_91,
    "p4-90": draw_p4_90,
}


# ---------------------------------------------------------------------------
# PROBLEMLER
# ---------------------------------------------------------------------------
PROBLEMS = [
    # =======================================================================
    # P4.89
    # =======================================================================
    dict(
        id="p4-89",
        topic=1,
        code="P4.89",
        title="Yük akımına bağlı $184i_\\phi$ kaynağı: $R_o$, $P_{max}$ ve 180 V kaynağın gücü",
        source="Çalışma Yaprağı 3 s.4 · Çalışma Yaprağı 4 s.1",
        image="P4_89_ORIG.webp",
        circuit="p4-89",
        circuit_caption="Çözüm şeması: alt tel referans (0 V). Üst düğümler soldan sağa $V_1$, 180 V (kaynak sabitliyor), $V_2$, $V_3$.",
        level=3,
        question=(
            "Şekildeki devrede değişken direnç $R_o$, kendisine <strong>maksimum güç</strong> aktarılacak şekilde ayarlanmaktadır.<br>"
            "a) $R_o$ kaç ohm olmalıdır?<br>"
            "b) $R_o$'ya aktarılabilecek maksimum güç kaç watt'tır?<br>"
            "c) (Kitaptaki ek soru) $R_o$ (a)'daki değere ayarlıyken 180 V'luk kaynak devreye ne kadar güç verir?"
        ),
        strategy=[
            "Kontrol akımı $i_\\phi$ doğrudan $R_o$'nun akımı. $R_o$ sökülünce $i_\\phi = 0$ olur → $184i_\\phi$ kaynağı 0 V'luk bir <strong>tel</strong> gibi davranır.",
            "Açık devre ($R_o$ sökülü): düğüm gerilimleriyle $V_{Th} = V_2$'yi bul.",
            "Kısa devre ($R_o$ yerine tel): $V_2 = 0$, $i_\\phi = I_{sc}$; süper düğümle $I_{sc}$'yi bul.",
            "$R_o = R_{Th} = V_{Th}/I_{sc}$, &nbsp; $P_{max} = V_{Th}^2/(4R_{Th})$.",
            "(c) için $R_o = R_{Th}$ iken $V_2 = V_{Th}/2$ kısayolunu kullan; kaynağın akımını bul, $\\sum p = 0$ ile sağla.",
        ],
        steps=[
            dict(
                title="Düğümleri adlandır ve ek denklemleri yaz",
                body=(
                    r"Alt teli referans (0 V) seçiyoruz. 180 V kaynağın + ucu üstte, yani o düğüm doğrudan <strong>180 V</strong>; "
                    r"bilinmeyen değil. Kalan üst düğümler: en sol $V_1$, $R_o$'nun üstü $V_2$, sağdaki $V_3$.<br>"
                    r"• $v_\Delta$: 2 Ω'un <em>−</em> ucu solda (180 V), <em>+</em> ucu sağda ($V_2$). Gerilim = (+ uç) − (− uç).<br>"
                    r"• $i_\phi$: $R_o$'dan <strong>aşağı</strong> akan akım.<br>"
                    r"• Üstteki $184i_\phi$ kaynağının + ucu solda ($V_1$), − ucu sağda ($V_3$)."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad v_\Delta &= V_2 - 180 \\
\textbf{ek 2:}\quad i_\phi &= \text{(R}_o\text{'dan aşağı akan akım)} \\
\textbf{ek 3:}\quad V_1 - V_3 &= 184\, i_\phi
\end{aligned}""",
                note="$V_1$ ile $V_3$ arasında gerilim kaynağı var → bu iki düğüm birlikte bir süper düğüm oluşturur.",
            ),
            dict(
                title="Açık devre: $R_o$ sökülünce $i_\\phi = 0$",
                body=(
                    r"$R_o$'yu çıkardığımızda o koldan akım akamaz: $i_\phi = 0$. O zaman $184i_\phi = 0$ V olur; "
                    r"0 V'luk gerilim kaynağı bir teldir. Yani $V_1 = V_3$. Bu ortak gerilime $V$ diyelim."
                ),
                math=r"""\begin{aligned}
i_\phi &= 0 \;\Rightarrow\; V_1 - V_3 = 184\cdot 0 = 0 \\
V_1 &= V_3 = V
\end{aligned}""",
            ),
            dict(
                title="Açık devre: $V_2$ düğümünde KCL",
                body=(
                    r"$V_2$ düğümüne bağlı iki direnç var (2 Ω ve 8 Ω); $R_o$ sökülü. Çıkan akımlar + yazılır."
                ),
                math=r"""\begin{aligned}
\frac{V_2 - 180}{2} + \frac{V_2 - V}{8} &= 0 \qquad /\times 8 \\
4(V_2 - 180) + (V_2 - V) &= 0 \\
4V_2 - 720 + V_2 - V &= 0 \\
\boxed{5V_2 - V = 720} &\qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="Açık devre: süper düğümde ($V_1$ + $V_3$) KCL",
                body=(
                    r"Süper düğümden çıkan akımlar: 16 Ω'dan aşağı, 20 Ω'dan sağa (180 V düğümüne), 8 Ω'dan sola ($V_2$'ye), "
                    r"10 Ω'dan aşağı. $0.1v_\Delta$ kaynağının oku yukarı, yani akım $V_3$'e <em>giriyor</em> → eksi işaretli. "
                    r"Paydalar 16, 20, 8, 10 → ortak payda 80."
                ),
                math=r"""\begin{aligned}
\frac{V}{16} + \frac{V - 180}{20} + \frac{V - V_2}{8} + \frac{V}{10} - 0.1\,v_\Delta &= 0 \\
\frac{V}{16} + \frac{V - 180}{20} + \frac{V - V_2}{8} + \frac{V}{10} - 0.1\,(V_2 - 180) &= 0 \qquad /\times 80 \\
5V + 4(V - 180) + 10(V - V_2) + 8V - 8(V_2 - 180) &= 0 \\
5V + 4V - 720 + 10V - 10V_2 + 8V - 8V_2 + 1440 &= 0 \\
27V - 18V_2 + 720 &= 0 \qquad /\div 9 \\
\boxed{3V - 2V_2 = -80} &\qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="Denklemleri çöz → $V_{Th}$",
                body=r"(I)'den $V = 5V_2 - 720$ çekip (II)'ye koyalım.",
                math=r"""\begin{aligned}
3(5V_2 - 720) - 2V_2 &= -80 \\
15V_2 - 2160 - 2V_2 &= -80 \\
13V_2 &= 2080 \;\Rightarrow\; V_2 = 160\ \text{V} \\
V &= 5(160) - 720 = 80\ \text{V} \quad (V_1 = V_3 = 80\ \text{V}) \\[4pt]
V_{Th} = V_2 &= \boxed{160\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre: $R_o$ yerine tel → $V_2 = 0$, $i_\\phi = I_{sc}$",
                body=(
                    r"Şimdi $R_o$'nun yerine düz tel koyuyoruz. $V_2 = 0$ olur ve telden aşağı akan akım $i_\phi = I_{sc}$'dir. "
                    r"Artık $i_\phi \neq 0$, yani $184i_\phi$ kaynağı devrede gerçekten var. Önce ek denklemler sayıya döner:"
                ),
                math=r"""\begin{aligned}
v_\Delta &= 0 - 180 = -180\ \text{V} \;\Rightarrow\; 0.1\,v_\Delta = -18\ \text{A} \\
V_1 - V_3 &= 184\, I_{sc} \qquad \text{(ek 3)}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre: $V_2$ düğümünde KCL → $I_{sc}$'yi $V_3$ cinsinden yaz",
                body=(
                    r"$V_2 = 0$ düğümünden çıkan akımlar: 2 Ω'dan sola, 8 Ω'dan sağa ve telden aşağı ($I_{sc}$)."
                ),
                math=r"""\begin{aligned}
\frac{0 - 180}{2} + \frac{0 - V_3}{8} + I_{sc} &= 0 \\
-90 - \frac{V_3}{8} + I_{sc} &= 0 \\
\boxed{I_{sc} = 90 + \frac{V_3}{8}} &\qquad \text{(III)}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre: süper düğümde KCL",
                body=(
                    r"Aynı süper düğüm, ama şimdi $V_1$ ile $V_3$ farklı ve $V_2 = 0$. "
                    r"$0.1v_\Delta = -18$ A girdiği için $-(-18) = +18$ yazılır. Yine $\times 80$."
                ),
                math=r"""\begin{aligned}
\frac{V_1}{16} + \frac{V_1 - 180}{20} + \frac{V_3 - 0}{8} + \frac{V_3}{10} - (-18) &= 0 \qquad /\times 80 \\
5V_1 + 4(V_1 - 180) + 10V_3 + 8V_3 + 1440 &= 0 \\
5V_1 + 4V_1 - 720 + 18V_3 + 1440 &= 0 \\
9V_1 + 18V_3 &= -720 \qquad /\div 9 \\
\boxed{V_1 + 2V_3 = -80} &\qquad \text{(IV)}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre denklemlerini çöz → $I_{sc}$",
                body=r"Ek 3'te $I_{sc}$ yerine (III)'ü koyup $V_1$'i $V_3$ cinsinden yazalım, sonra (IV)'e yerleştirelim.",
                math=r"""\begin{aligned}
V_1 &= V_3 + 184\, I_{sc} = V_3 + 184\left(90 + \frac{V_3}{8}\right) \\
V_1 &= V_3 + 16560 + 23V_3 = 24V_3 + 16560 \\[4pt]
(24V_3 + 16560) + 2V_3 &= -80 \\
26V_3 &= -16640 \;\Rightarrow\; V_3 = -640\ \text{V} \\
V_1 &= 24(-640) + 16560 = 1200\ \text{V} \\[4pt]
I_{sc} &= 90 + \frac{-640}{8} = 90 - 80 = \boxed{10\ \text{A}}
\end{aligned}""",
                note="Sağlama: $V_1 - V_3 = 1200 - (-640) = 1840 = 184 \\cdot 10$ ✓",
            ),
            dict(
                title="(a) ve (b): $R_o$ ve maksimum güç",
                body="Yük direnci Thévenin direncine eşit olunca maksimum güç aktarılır.",
                math=r"""\begin{aligned}
R_o = R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{160}{10} = \boxed{16\ \Omega} \\[4pt]
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{160^2}{4\cdot 16} = \frac{25600}{64} = \boxed{400\ \text{W}}
\end{aligned}""",
            ),
            dict(
                title="(c) $R_o = 16\\ \\Omega$ iken düğüm gerilimleri",
                body=(
                    r"Kısayol: $R_o = R_{Th}$ olduğunda Thévenin eşdeğeri bir gerilim bölücüdür, yük gerilimi $V_{Th}$'nin tam yarısıdır. "
                    r"Yani $V_2 = 80$ V, $i_\phi = 80/16 = 5$ A. Sonra $V_2$ düğümünde KCL ile $V_3$'ü, ek 3 ile $V_1$'i buluruz."
                ),
                math=r"""\begin{aligned}
V_2 &= \frac{V_{Th}}{2} = 80\ \text{V}, \qquad i_\phi = \frac{80}{16} = 5\ \text{A} \\[4pt]
\frac{80 - 180}{2} + 5 + \frac{80 - V_3}{8} &= 0 \\
-50 + 5 + 10 - \frac{V_3}{8} &= 0 \;\Rightarrow\; \frac{V_3}{8} = -35 \;\Rightarrow\; V_3 = -280\ \text{V} \\
V_1 &= V_3 + 184\, i_\phi = -280 + 920 = 640\ \text{V}
\end{aligned}""",
                note="Sağlama (süper düğüm): $\\tfrac{640}{16} + \\tfrac{460}{20} + \\tfrac{-360}{8} + \\tfrac{-280}{10} - 0.1(-100) = 40 + 23 - 45 - 28 + 10 = 0$ ✓",
            ),
            dict(
                title="(c) 180 V kaynağın verdiği güç",
                body=(
                    r"Kaynağın + ucundan (180 V düğümü) dışarı çıkan akım, o düğümden 20 Ω'a ve 2 Ω'a giden akımların toplamıdır. "
                    r"Akım + uçtan <em>çıktığı</em> için kaynak güç üretir."
                ),
                math=r"""\begin{aligned}
i_{180} &= \frac{180 - V_1}{20} + \frac{180 - V_2}{2} = \frac{180 - 640}{20} + \frac{180 - 80}{2} \\
&= -23 + 50 = 27\ \text{A} \\[4pt]
p_{180\text{V}} &= -180 \cdot 27 = -4860\ \text{W} \quad \Rightarrow \quad \boxed{4860\ \text{W verir}}
\end{aligned}""",
            ),
            dict(
                title="Güç dengesi sağlaması: $\\sum p = 0$",
                body=(
                    r"Pasif işaret kuralıyla her elemanın gücü. Bağımlı gerilim kaynağından geçen akım, $V_1$ düğümündeki KCL'den: "
                    r"$\tfrac{640}{16} + \tfrac{460}{20} + i_{13} = 0 \Rightarrow i_{13} = -63$ A (yani 63 A $V_3$'ten $V_1$'e, + uçtan çıkıyor). "
                    r"$0.1v_\Delta = 0.1(80-180) = -10$ A, yani 10 A <em>aşağı</em>, + uçtan ($V_3$) giriyor."
                ),
                math=r"""\begin{aligned}
&p_{16} = \tfrac{640^2}{16} = 25600, \quad p_{20} = \tfrac{460^2}{20} = 10580, \quad p_{2} = \tfrac{100^2}{2} = 5000 \\
&p_{8} = \tfrac{360^2}{8} = 16200, \quad p_{10} = \tfrac{280^2}{10} = 7840, \quad p_{R_o} = \tfrac{80^2}{16} = 400 \\
&p_{180\text{V}} = -4860, \quad p_{0.1v_\Delta} = (-280)(10) = -2800, \quad p_{184i_\phi} = 920\cdot(-63) = -57960 \\[4pt]
&\text{emilen} = 65620\ \text{W}, \qquad \text{üretilen} = 4860 + 2800 + 57960 = 65620\ \text{W} \;\Rightarrow\; \sum p = 0\ \checkmark
\end{aligned}""",
            ),
        ],
        answer=[
            r"V_{Th} = 160\ \text{V}",
            r"I_{sc} = 10\ \text{A}",
            r"R_o = R_{Th} = 16\ \Omega",
            r"P_{max} = 400\ \text{W}",
            r"p_{180\text{V}} = 4860\ \text{W (verir)}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } v_\Delta = V_2 - 180, \qquad V_1 - V_3 = 184\, i_\phi \\[2pt]
&\textbf{Açık devre } (i_\phi = 0 \Rightarrow V_1 = V_3 = V):\\
&V_2:\ \tfrac{V_2 - 180}{2} + \tfrac{V_2 - V}{8} = 0 \;\Rightarrow\; 5V_2 - V = 720 \\
&\text{SD}:\ \tfrac{V}{16} + \tfrac{V-180}{20} + \tfrac{V - V_2}{8} + \tfrac{V}{10} - 0.1(V_2 - 180) = 0 \;\Rightarrow\; 3V - 2V_2 = -80 \\
&\Rightarrow V_2 = 160\ \text{V},\ V = 80\ \text{V},\quad V_{Th} = 160\ \text{V} \\[2pt]
&\textbf{Kısa devre } (V_2 = 0,\ i_\phi = I_{sc}):\ 0.1v_\Delta = -18\ \text{A} \\
&V_2:\ -90 - \tfrac{V_3}{8} + I_{sc} = 0, \qquad \text{SD}:\ V_1 + 2V_3 = -80, \qquad V_1 - V_3 = 184 I_{sc} \\
&\Rightarrow V_3 = -640\ \text{V},\ V_1 = 1200\ \text{V},\ I_{sc} = 10\ \text{A} \\[2pt]
&R_o = R_{Th} = 160/10 = 16\ \Omega,\qquad P_{max} = \tfrac{160^2}{4\cdot 16} = 400\ \text{W} \\[2pt]
&\textbf{(c)}\ V_2 = 80,\ i_\phi = 5,\ V_3 = -280,\ V_1 = 640 \\
&i_{180} = \tfrac{180-640}{20} + \tfrac{180-80}{2} = 27\ \text{A},\quad p_{180\text{V}} = -4860\ \text{W (4860 W verir)}
\end{aligned}""",
        traps=[
            "Açık devrede $i_\\phi = 0$ olduğunu görmemek: $184i_\\phi$ kaynağı o anda <strong>tel</strong>dir, $V_1 = V_3$ olur. Bunu kullanmazsan bilinmeyen sayısı boşuna artar.",
            "Kısa devrede ise $i_\\phi = I_{sc} \\neq 0$; kaynağı yine tel sanıp $V_1 = V_3$ yazmak yanlıştır.",
            "$v_\\Delta$'nın + ucu <strong>sağda</strong> ($V_2$ tarafı): $v_\\Delta = V_2 - 180$, $180 - V_2$ değil.",
            "$P_{max}$ formülünde $V_{Th}^2/(4R_{Th})$ yerine $V_{Th}^2/R_{Th}$ yazmak — 4 kat fazla çıkar.",
        ],
    ),

    # =======================================================================
    # P4.91
    # =======================================================================
    dict(
        id="p4-91",
        topic=1,
        code="P4.91",
        title="İki bağımsız, bir bağımlı kaynak: $R_o$, $P_{max}$ ve güç yüzdesi",
        source="Çalışma Yaprağı 3 s.4 · Çalışma Yaprağı 4 s.1",
        image="P4_91_ORIG.webp",
        circuit="p4-91",
        circuit_caption="Çözüm şeması: orta alt düğüm referans (0 V). Alt köşe düğümleri kaynaklar yüzünden $V_1+400$ ve $V_3+200$.",
        level=3,
        question=(
            "Şekildeki devrede değişken direnç $R_o$, devreden <strong>maksimum güç</strong> çekecek şekilde ayarlanmaktadır.<br>"
            "a) $R_o$ kaç ohm olmalıdır?<br>"
            "b) $R_o$'ya aktarılan maksimum güç kaç watt'tır?<br>"
            "c) (Kitaptaki ek soru) Devrede üretilen toplam gücün yüzde kaçı $R_o$'ya aktarılır?"
        ),
        strategy=[
            "Orta alt düğümü referans seç. Her gerilim kaynağı bir direnç düğümünü diğerine 'bağlar' → sol ve sağ köşeler tek bir <strong>süper düğüm</strong> olur.",
            "Açık devre: $i_\\Delta = V_2/180$; üç denklem (süper düğüm, $V_2$ düğümü, bağımlı kaynak) → $V_{Th} = V_2$.",
            "Kısa devre: $V_2 = 0 \\Rightarrow i_\\Delta = 0 \\Rightarrow 316i_\\Delta$ tel olur → $I_{sc}$.",
            "$R_o = V_{Th}/I_{sc}$, $P_{max} = V_{Th}^2/(4R_{Th})$.",
            "(c): $R_o = R_{Th}$ iken $V_2 = V_{Th}/2$; tüm güçleri bul, $\\sum p = 0$ ile sağla.",
        ],
        steps=[
            dict(
                title="Düğümleri adlandır, kaynakların verdiği bilgileri yaz",
                body=(
                    r"Orta alttaki düğüm (180 Ω ve $R_o$'nun altı) referans: 0 V. Üstte $V_1$ (sol), $V_2$ (orta, $R_o$'nun üstü), $V_3$ (sağ).<br>"
                    r"• 400 V kaynağın <strong>− ucu üstte</strong>, + ucu altta: alt sol köşe $V_1 + 400$.<br>"
                    r"• 200 V kaynağın da − ucu üstte: alt sağ köşe $V_3 + 200$.<br>"
                    r"• $i_\Delta$: 180 Ω'dan aşağı akan akım.<br>"
                    r"• $316i_\Delta$: + ucu solda ($V_1$), − ucu sağda ($V_3$)."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad i_\Delta &= \frac{V_2 - 0}{180} \\
\textbf{ek 2:}\quad V_1 - V_3 &= 316\, i_\Delta
\end{aligned}""",
                note="$V_1$, $V_1+400$, $V_3$, $V_3+200$ düğümleri gerilim kaynaklarıyla birbirine bağlı → hepsi tek süper düğüm.",
            ),
            dict(
                title="Süper düğümde KCL (açık ve kısa devrede aynı)",
                body=(
                    r"Süper düğümden dışarı çıkan dört akım var: 16 Ω'dan $V_2$'ye, 64 Ω'dan referansa, 32 Ω'dan $V_2$'ye, 48 Ω'dan referansa. "
                    r"Paydalar 16, 64, 32, 48 → ortak payda 192."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - V_2}{16} + \frac{V_1 + 400}{64} + \frac{V_3 - V_2}{32} + \frac{V_3 + 200}{48} &= 0 \qquad /\times 192 \\
12(V_1 - V_2) + 3(V_1 + 400) + 6(V_3 - V_2) + 4(V_3 + 200) &= 0 \\
12V_1 - 12V_2 + 3V_1 + 1200 + 6V_3 - 6V_2 + 4V_3 + 800 &= 0 \\
\boxed{15V_1 - 18V_2 + 10V_3 = -2000} &\qquad \text{(S)}
\end{aligned}""",
            ),
            dict(
                title="Açık devre: $V_2$ düğümünde KCL",
                body=r"$R_o$ sökülü. $V_2$'den çıkan akımlar: 16 Ω'dan sola, 180 Ω'dan aşağı, 32 Ω'dan sağa. Ortak payda 1440.",
                math=r"""\begin{aligned}
\frac{V_2 - V_1}{16} + \frac{V_2}{180} + \frac{V_2 - V_3}{32} &= 0 \qquad /\times 1440 \\
90(V_2 - V_1) + 8V_2 + 45(V_2 - V_3) &= 0 \\
\boxed{-90V_1 + 143V_2 - 45V_3 = 0} &\qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="Açık devre: bağımlı kaynak denklemi",
                body=r"Ek 2'de $i_\Delta = V_2/180$ yaz, paydadan kurtulmak için 45 ile çarp ($316/180 = 79/45$).",
                math=r"""\begin{aligned}
V_1 - V_3 &= 316\cdot\frac{V_2}{180} = \frac{79}{45}V_2 \qquad /\times 45 \\
\boxed{45V_1 - 45V_3 = 79V_2} &\qquad \text{(III)}
\end{aligned}""",
            ),
            dict(
                title="Açık devre denklemlerini çöz → $V_{Th}$",
                body=(
                    r"(III)'ten $45V_3 = 45V_1 - 79V_2$. Bunu (II)'de yerine koyunca $V_3$ gider; "
                    r"sonra hepsini $V_2$ cinsinden (S)'ye yerleştiririz."
                ),
                math=r"""\begin{aligned}
-90V_1 + 143V_2 - (45V_1 - 79V_2) &= 0 \\
-135V_1 + 222V_2 &= 0 \;\Rightarrow\; V_1 = \frac{222}{135}V_2 = \frac{74}{45}V_2 \\
V_3 &= V_1 - \frac{79}{45}V_2 = \frac{74 - 79}{45}V_2 = -\frac{V_2}{9} \\[4pt]
15\cdot\frac{74}{45}V_2 - 18V_2 + 10\left(-\frac{V_2}{9}\right) &= -2000 \\
\frac{74}{3}V_2 - 18V_2 - \frac{10}{9}V_2 &= -2000 \qquad /\times 9 \\
222V_2 - 162V_2 - 10V_2 &= -18000 \\
50V_2 &= -18000 \;\Rightarrow\; V_2 = -360\ \text{V} \\
V_1 &= \tfrac{74}{45}(-360) = -592\ \text{V}, \qquad V_3 = -\tfrac{-360}{9} = 40\ \text{V} \\[4pt]
V_{Th} = V_2 &= \boxed{-360\ \text{V}}
\end{aligned}""",
                note="Eksi işaret sadece $R_o$'nun üst ucunun alt ucundan daha düşük gerilimde olduğunu söyler. Güç için işaret önemli değil, $V_{Th}^2$ kullanılır.",
            ),
            dict(
                title="Kısa devre: $V_2 = 0$ → $i_\\Delta = 0$",
                body=(
                    r"$R_o$ yerine tel koyunca $V_2 = 0$. 180 Ω'un iki ucu da 0 V'ta, akım geçmez: $i_\Delta = 0$. "
                    r"Dolayısıyla $316i_\Delta = 0$ → bağımlı kaynak tel olur, $V_1 = V_3 = V$. (S) denklemi aynen geçerli:"
                ),
                math=r"""\begin{aligned}
15V - 18(0) + 10V &= -2000 \\
25V &= -2000 \;\Rightarrow\; V = V_1 = V_3 = -80\ \text{V}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre akımı $I_{sc}$",
                body=(
                    r"Teldeki akım (yukarıdan aşağı), $V_2$ düğümüne 16 Ω ve 32 Ω'dan <em>gelen</em> akımların toplamıdır "
                    r"(180 Ω'dan akım geçmiyor)."
                ),
                math=r"""\begin{aligned}
I_{sc} &= \frac{V_1 - 0}{16} + \frac{V_3 - 0}{32} = \frac{-80}{16} + \frac{-80}{32} \\
&= -5 - 2.5 = \boxed{-7.5\ \text{A}}
\end{aligned}""",
                note="$V_{Th}$ ile aynı yönde (üstten alta) tanımladık; ikisi de eksi çıktı, oranları pozitif olacak.",
            ),
            dict(
                title="(a) ve (b): $R_o$ ve maksimum güç",
                body="Maksimum güç koşulu: $R_o = R_{Th}$.",
                math=r"""\begin{aligned}
R_o = R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{-360}{-7.5} = \boxed{48\ \Omega} \\[4pt]
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{(-360)^2}{4\cdot 48} = \frac{129600}{192} = \boxed{675\ \text{W}}
\end{aligned}""",
            ),
            dict(
                title="(c) $R_o = 48\\ \\Omega$ iken düğüm gerilimleri",
                body=(
                    r"$R_o = R_{Th}$ olduğunda yük gerilimi $V_{Th}$'nin yarısıdır: $V_2 = -180$ V. "
                    r"O zaman $i_\Delta = -180/180 = -1$ A ve ek 2'den $V_1 - V_3 = -316$ V. Süper düğüm (S) ile $V_3$'ü buluruz."
                ),
                math=r"""\begin{aligned}
V_2 &= -180\ \text{V}, \qquad i_\Delta = -1\ \text{A}, \qquad V_1 = V_3 - 316 \\[4pt]
15(V_3 - 316) - 18(-180) + 10V_3 &= -2000 \\
15V_3 - 4740 + 3240 + 10V_3 &= -2000 \\
25V_3 &= -500 \;\Rightarrow\; V_3 = -20\ \text{V}, \qquad V_1 = -336\ \text{V}
\end{aligned}""",
            ),
            dict(
                title="(c) Kol akımları",
                body=(
                    r"Alt sol köşe $V_1 + 400 = 64$ V, alt sağ köşe $V_3 + 200 = 180$ V. "
                    r"400 V kaynaktan geçen akım, 64 Ω'un akımıyla aynıdır (seri). Bağımlı kaynağın akımı $V_1$ düğümündeki KCL'den gelir."
                ),
                math=r"""\begin{aligned}
i_{16} &= \frac{V_1 - V_2}{16} = \frac{-336 + 180}{16} = -9.75\ \text{A} \quad (V_1 \to V_2) \\
i_{32} &= \frac{V_3 - V_2}{32} = \frac{-20 + 180}{32} = 5\ \text{A} \quad (V_3 \to V_2) \\
i_{64} &= \frac{64 - 0}{64} = 1\ \text{A}, \qquad i_{48} = \frac{180 - 0}{48} = 3.75\ \text{A} \\
V_1:\ i_{16} + i_{dep} + i_{64} &= 0 \;\Rightarrow\; i_{dep} = 9.75 - 1 = 8.75\ \text{A} \quad (V_1 \to V_3)
\end{aligned}""",
            ),
            dict(
                title="(c) Güçler, $\\sum p = 0$ ve yüzde",
                body=(
                    r"400 V ve 200 V kaynaklarında akım <strong>− uçtan girip</strong> + uçtan çıkıyor → güç üretiyorlar. "
                    r"Bağımlı kaynakta 8.75 A + uçtan giriyor ama gerilimi $316(-1) = -316$ V, yani o da güç üretiyor."
                ),
                math=r"""\begin{aligned}
&p_{400\text{V}} = -400\cdot 1 = -400, \quad p_{200\text{V}} = -200\cdot 3.75 = -750, \quad p_{316i_\Delta} = (-316)(8.75) = -2765 \\
&p_{16} = 9.75^2\cdot 16 = 1521, \quad p_{32} = 5^2\cdot 32 = 800, \quad p_{64} = 1^2\cdot 64 = 64 \\
&p_{48} = 3.75^2\cdot 48 = 675, \quad p_{180} = \tfrac{180^2}{180} = 180, \quad p_{R_o} = \tfrac{180^2}{48} = 675 \\[4pt]
&\text{üretilen} = 400 + 750 + 2765 = 3915\ \text{W}, \qquad \text{emilen} = 3915\ \text{W} \;\Rightarrow\; \sum p = 0\ \checkmark \\[4pt]
&\%\,= \frac{675}{3915}\times 100 = \boxed{17.24\ \%}
\end{aligned}""",
            ),
        ],
        answer=[
            r"V_{Th} = -360\ \text{V}",
            r"I_{sc} = -7.5\ \text{A}",
            r"R_o = R_{Th} = 48\ \Omega",
            r"P_{max} = 675\ \text{W}",
            r"\%\ \text{aktarılan} = 675/3915 \approx 17.24\ \%",
        ],
        exam=r"""\begin{aligned}
&\text{ref: orta alt. } \text{Alt köşeler: } V_1 + 400,\ V_3 + 200;\quad i_\Delta = \tfrac{V_2}{180},\quad V_1 - V_3 = 316 i_\Delta \\
&\text{SD}:\ \tfrac{V_1 - V_2}{16} + \tfrac{V_1 + 400}{64} + \tfrac{V_3 - V_2}{32} + \tfrac{V_3 + 200}{48} = 0 \;\Rightarrow\; 15V_1 - 18V_2 + 10V_3 = -2000 \\[2pt]
&\textbf{Açık devre:}\ V_2:\ -90V_1 + 143V_2 - 45V_3 = 0, \qquad 45V_1 - 45V_3 = 79V_2 \\
&\Rightarrow V_1 = -592,\ V_2 = -360,\ V_3 = 40\ \text{V},\quad V_{Th} = -360\ \text{V} \\[2pt]
&\textbf{Kısa devre:}\ V_2 = 0 \Rightarrow i_\Delta = 0 \Rightarrow V_1 = V_3 = V,\ 25V = -2000,\ V = -80\ \text{V} \\
&I_{sc} = \tfrac{-80}{16} + \tfrac{-80}{32} = -7.5\ \text{A} \\[2pt]
&R_o = R_{Th} = \tfrac{-360}{-7.5} = 48\ \Omega,\qquad P_{max} = \tfrac{360^2}{4\cdot 48} = 675\ \text{W} \\[2pt]
&\textbf{(c)}\ V_2 = -180,\ i_\Delta = -1,\ V_3 = -20,\ V_1 = -336 \\
&p_{400} = -400,\ p_{200} = -750,\ p_{dep} = -2765 \Rightarrow \text{üretilen} = 3915\ \text{W},\quad \% = \tfrac{675}{3915} = 17.24\%
\end{aligned}""",
        traps=[
            "Her iki bağımsız kaynakta da <strong>− uç üstte</strong>: alt köşe $V_1 - 400$ değil $V_1 + 400$'dür.",
            "Kısa devrede 180 Ω da kısa devre olur → $i_\\Delta = 0$ ve $316i_\\Delta$ tel gibi davranır. Bunu fark etmek işi çok kısaltır.",
            "$V_{Th}$ ve $I_{sc}$'yi <strong>aynı yönde</strong> tanımla (ikisi de üstten alta). Yönler karışırsa $R_{Th}$ eksi çıkar.",
            "Yüzdeyi bağımsız kaynakların gücüne göre değil, <strong>üretilen toplam güce</strong> (bağımlı kaynak dahil) göre hesapla.",
        ],
    ),

    # =======================================================================
    # P4.90
    # =======================================================================
    dict(
        id="p4-90",
        topic=1,
        code="P4.90",
        title="3.6 kV kaynak ve $150i_\\beta$: $R_L$, $P_{max}$ ve kaynak gücünün yüzdesi",
        source="Çalışma Yaprağı 4 s.1",
        image="P4_90_ORIG.webp",
        circuit="p4-90",
        circuit_caption="Çözüm şeması: orta alt düğüm referans (0 V). Alt köşe düğümleri $V_1-3600$ ve $V_3+150i_\\beta$.",
        level=3,
        question=(
            "Şekildeki devrede değişken direnç $R_L$, kendisine <strong>maksimum güç</strong> aktarılacak şekilde ayarlanmaktadır.<br>"
            "a) $R_L$ kaç ohm olmalıdır?<br>"
            "b) $R_L$'ye aktarılan maksimum güç kaç watt'tır?<br>"
            "c) (Kitaptaki ek soru) $R_L$ bu değerdeyken 3.6 kV'luk kaynağın verdiği gücün yüzde kaçı $R_L$'ye ulaşır?"
        ),
        strategy=[
            "Orta alt düğümü referans seç. 3.6 kV kaynak sol köşeleri, $150i_\\beta$ kaynağı sağ köşeleri birer <strong>süper düğüm</strong> yapar.",
            "Açık devre: üç bilinmeyen ($V_1, V_2, V_3$), üç denklem → $V_{Th} = V_2$.",
            "Kısa devre: $V_2 = 0$; iki denklem → $V_1, V_3$ → $I_{sc} = i_\\beta + i_{60}$.",
            "$R_L = V_{Th}/I_{sc}$, $P_{max} = V_{Th}^2/(4R_{Th})$.",
            "(c): $R_L = R_{Th}$ iken $V_2 = V_{Th}/2$; kaynak akımını bul, oranla. $\\sum p = 0$ sağlaması yap.",
        ],
        steps=[
            dict(
                title="Düğümleri adlandır, ek denklemleri yaz",
                body=(
                    r"Orta alttaki düğüm (300 Ω ve $R_L$'nin altı) referans. Üstte $V_1$ (sol), $V_2$ ($R_L$'nin üstü), $V_3$ (sağ).<br>"
                    r"• 3.6 kV kaynağın + ucu üstte ($V_1$) → alt sol köşe $V_1 - 3600$.<br>"
                    r"• $150i_\beta$ kaynağının <strong>− ucu üstte</strong> ($V_3$), + ucu altta → alt sağ köşe $V_3 + 150i_\beta$.<br>"
                    r"• $i_\beta$: 45 Ω'dan sağa, yani $V_1$'den $V_2$'ye akan akım."
                ),
                math=r"""\begin{aligned}
\textbf{ek:}\quad i_\beta &= \frac{V_1 - V_2}{45} \;\Rightarrow\; 150\, i_\beta = \frac{150}{45}(V_1 - V_2) = \frac{10}{3}(V_1 - V_2)
\end{aligned}""",
            ),
            dict(
                title="Sol süper düğüm ($V_1$ ve $V_1 - 3600$)",
                body=(
                    r"Bu süper düğümden çıkan akımlar: üst 30 Ω'dan $V_3$'e, 45 Ω'dan $V_2$'ye, alt 30 Ω'dan referansa. "
                    r"$R_L$ bu denkleme girmez, yani denklem açık ve kısa devrede <em>aynı</em>dır (sadece $V_2$ değişir). Ortak payda 90."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - V_3}{30} + \frac{V_1 - V_2}{45} + \frac{V_1 - 3600}{30} &= 0 \qquad /\times 90 \\
3(V_1 - V_3) + 2(V_1 - V_2) + 3(V_1 - 3600) &= 0 \\
3V_1 - 3V_3 + 2V_1 - 2V_2 + 3V_1 - 10800 &= 0 \\
\boxed{8V_1 - 2V_2 - 3V_3 = 10800} &\qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="Sağ süper düğüm ($V_3$ ve $V_3 + 150i_\\beta$)",
                body=(
                    r"Çıkan akımlar: üst 30 Ω'dan $V_1$'e, 60 Ω'dan $V_2$'ye, 15 Ω'dan referansa. 15 Ω'un sağ ucu $V_3 + 150i_\beta$'dır. "
                    r"Bu denklem de $R_L$'den bağımsız. Ortak payda 60, sonra kesirden kurtulmak için $\times 3$."
                ),
                math=r"""\begin{aligned}
\frac{V_3 - V_1}{30} + \frac{V_3 - V_2}{60} + \frac{V_3 + 150i_\beta}{15} &= 0 \qquad /\times 60 \\
2(V_3 - V_1) + (V_3 - V_2) + 4\left(V_3 + \tfrac{10}{3}(V_1 - V_2)\right) &= 0 \\
2V_3 - 2V_1 + V_3 - V_2 + 4V_3 + \tfrac{40}{3}V_1 - \tfrac{40}{3}V_2 &= 0 \qquad /\times 3 \\
6V_3 - 6V_1 + 3V_3 - 3V_2 + 12V_3 + 40V_1 - 40V_2 &= 0 \\
\boxed{34V_1 - 43V_2 + 21V_3 = 0} &\qquad \text{(III)}
\end{aligned}""",
            ),
            dict(
                title="Açık devre: $V_2$ düğümünde KCL",
                body=r"$R_L$ sökülü. $V_2$'den çıkan akımlar: 45 Ω'dan sola, 300 Ω'dan aşağı, 60 Ω'dan sağa. Ortak payda 900.",
                math=r"""\begin{aligned}
\frac{V_2 - V_1}{45} + \frac{V_2}{300} + \frac{V_2 - V_3}{60} &= 0 \qquad /\times 900 \\
20(V_2 - V_1) + 3V_2 + 15(V_2 - V_3) &= 0 \\
\boxed{-20V_1 + 38V_2 - 15V_3 = 0} &\qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="Açık devre denklemlerini çöz → $V_{Th}$",
                body=(
                    r"Önce $V_3$'ü yok edelim: (I)$\times 5$ − (II) ve (I)$\times 7$ + (III). Sonra kalan iki denklemden $V_1$'i yok ederiz."
                ),
                math=r"""\begin{aligned}
\text{(I)}\times 5 - \text{(II)}:\quad (40 + 20)V_1 + (-10 - 38)V_2 &= 54000 \;\Rightarrow\; 60V_1 - 48V_2 = 54000 \;\Rightarrow\; 5V_1 - 4V_2 = 4500 \\
\text{(I)}\times 7 + \text{(III)}:\quad (56 + 34)V_1 + (-14 - 43)V_2 &= 75600 \;\Rightarrow\; 90V_1 - 57V_2 = 75600 \;\Rightarrow\; 30V_1 - 19V_2 = 25200 \\[4pt]
(30V_1 - 19V_2) - 6(5V_1 - 4V_2) &= 25200 - 27000 \\
5V_2 &= -1800 \;\Rightarrow\; V_2 = -360\ \text{V} \\
V_1 &= \frac{4500 + 4(-360)}{5} = \frac{3060}{5} = 612\ \text{V} \\
3V_3 &= 8(612) - 2(-360) - 10800 = -5184 \;\Rightarrow\; V_3 = -1728\ \text{V} \\[4pt]
V_{Th} = V_2 &= \boxed{-360\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre: $V_2 = 0$",
                body=(
                    r"$R_L$ yerine tel → $V_2 = 0$. (I) ve (III) aynen geçerli; sadece $V_2 = 0$ koyarız. "
                    r"(I)$\times 7$ + (III) yine $V_3$'ü yok eder."
                ),
                math=r"""\begin{aligned}
\text{(I)}:\ 8V_1 - 3V_3 &= 10800, \qquad \text{(III)}:\ 34V_1 + 21V_3 = 0 \\
56V_1 - 21V_3 + 34V_1 + 21V_3 &= 75600 \\
90V_1 &= 75600 \;\Rightarrow\; V_1 = 840\ \text{V} \\
V_3 &= -\frac{34}{21}(840) = -1360\ \text{V}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre akımı $I_{sc}$",
                body=(
                    r"Teldeki akım (yukarıdan aşağı) = $V_2$ düğümüne 45 Ω'dan ve 60 Ω'dan <em>gelen</em> akımlar "
                    r"(300 Ω'un iki ucu da 0 V, akım taşımaz)."
                ),
                math=r"""\begin{aligned}
i_\beta &= \frac{840 - 0}{45} = \frac{56}{3}\ \text{A}, \qquad i_{60} = \frac{V_3 - 0}{60} = \frac{-1360}{60} = -\frac{68}{3}\ \text{A} \\
I_{sc} &= \frac{56}{3} - \frac{68}{3} = -\frac{12}{3} = \boxed{-4\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="(a) ve (b): $R_L$ ve maksimum güç",
                body="Maksimum güç için $R_L = R_{Th}$.",
                math=r"""\begin{aligned}
R_L = R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{-360}{-4} = \boxed{90\ \Omega} \\[4pt]
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{360^2}{4\cdot 90} = \frac{129600}{360} = \boxed{360\ \text{W}}
\end{aligned}""",
            ),
            dict(
                title="(c) $R_L = 90\\ \\Omega$ iken düğüm gerilimleri",
                body=(
                    r"Yük Thévenin direncine eşitken $V_2 = V_{Th}/2 = -180$ V. (I) ve (III)'te $V_2 = -180$ koyup çözelim."
                ),
                math=r"""\begin{aligned}
\text{(I)}:\ 8V_1 - 3V_3 &= 10800 + 2(-180) = 10440 \\
\text{(III)}:\ 34V_1 + 21V_3 &= 43(-180) = -7740 \\
\text{(I)}\times 7 + \text{(III)}:\ 90V_1 &= 73080 - 7740 = 65340 \;\Rightarrow\; V_1 = 726\ \text{V} \\
3V_3 &= 8(726) - 10440 = -4632 \;\Rightarrow\; V_3 = -1544\ \text{V}
\end{aligned}""",
            ),
            dict(
                title="(c) Kaynağın gücü ve yüzde",
                body=(
                    r"3.6 kV kaynağın + ucundan ($V_1$) çıkan akım, $V_1$'den üst 30 Ω'a ve 45 Ω'a giden akımların toplamıdır. "
                    r"(Sağlama: aynı akım alt 30 Ω'dan geçer: $(0 - (726 - 3600))/30 = 2874/30 = 95.8$ A.)"
                ),
                math=r"""\begin{aligned}
i_\beta &= \frac{726 - (-180)}{45} = \frac{906}{45} \approx 20.133\ \text{A}, \qquad i_{30} = \frac{726 - (-1544)}{30} = \frac{2270}{30} \approx 75.667\ \text{A} \\
i_{kaynak} &= i_\beta + i_{30} = 95.8\ \text{A} \\
p_{3.6\text{kV}} &= -3600 \cdot 95.8 = -344880\ \text{W} \quad (344.88\ \text{kW verir}) \\[4pt]
\% &= \frac{360}{344880}\times 100 \approx \boxed{0.104\ \%}
\end{aligned}""",
                note="Kaynağın gücünün binde birinden azı yüke gidiyor: maksimum güç transferi 'en verimli' çalışma demek değildir.",
            ),
            dict(
                title="Güç dengesi sağlaması: $\\sum p = 0$",
                body=(
                    r"Alt sağ köşe: $V_3 + 150i_\beta = -1544 + 3020 = 1476$ V. 15 Ω'dan referansa $1476/15 = 98.4$ A akar; "
                    r"bu akım bağımlı kaynaktan aşağı doğru, − uçtan girip + uçtan çıkarak geçer → kaynak güç üretir."
                ),
                math=r"""\begin{aligned}
&p_{150i_\beta} = -(3020)(98.4) = -297168\ \text{W}, \qquad p_{3.6\text{kV}} = -344880\ \text{W} \\
&p_{45} = \tfrac{906^2}{45} = 18240.8, \quad p_{30,\text{üst}} = \tfrac{2270^2}{30} \approx 171763.33, \quad p_{30,\text{alt}} = \tfrac{2874^2}{30} = 275329.2 \\
&p_{300} = \tfrac{180^2}{300} = 108, \quad p_{R_L} = 360, \quad p_{60} = \tfrac{1364^2}{60} \approx 31008.27, \quad p_{15} = \tfrac{1476^2}{15} = 145238.4 \\[4pt]
&\text{emilen} = 642048\ \text{W}, \qquad \text{üretilen} = 344880 + 297168 = 642048\ \text{W} \;\Rightarrow\; \sum p = 0\ \checkmark
\end{aligned}""",
                note="Bağımlı kaynak da dahil edilirse toplam üretilen güç 642 048 W olur ve $R_L$'nin payı $360/642048 \\approx \\%0.056$'ya düşer.",
            ),
        ],
        answer=[
            r"V_{Th} = -360\ \text{V}",
            r"I_{sc} = -4\ \text{A}",
            r"R_L = R_{Th} = 90\ \Omega",
            r"P_{max} = 360\ \text{W}",
            r"p_{3.6\text{kV}} = 344.88\ \text{kW (verir)},\quad \% = 0.104\ \%",
        ],
        exam=r"""\begin{aligned}
&\text{ref: orta alt. Alt köşeler: } V_1 - 3600,\ V_3 + 150 i_\beta;\quad i_\beta = \tfrac{V_1 - V_2}{45} \\
&\text{SD}_\text{sol}:\ \tfrac{V_1 - V_3}{30} + \tfrac{V_1 - V_2}{45} + \tfrac{V_1 - 3600}{30} = 0 \;\Rightarrow\; 8V_1 - 2V_2 - 3V_3 = 10800 \\
&\text{SD}_\text{sağ}:\ \tfrac{V_3 - V_1}{30} + \tfrac{V_3 - V_2}{60} + \tfrac{V_3 + 150i_\beta}{15} = 0 \;\Rightarrow\; 34V_1 - 43V_2 + 21V_3 = 0 \\[2pt]
&\textbf{Açık devre:}\ V_2:\ -20V_1 + 38V_2 - 15V_3 = 0 \\
&\Rightarrow V_1 = 612,\ V_2 = -360,\ V_3 = -1728\ \text{V},\quad V_{Th} = -360\ \text{V} \\[2pt]
&\textbf{Kısa devre } (V_2 = 0):\ V_1 = 840,\ V_3 = -1360\ \text{V} \\
&I_{sc} = \tfrac{840}{45} + \tfrac{-1360}{60} = \tfrac{56}{3} - \tfrac{68}{3} = -4\ \text{A} \\[2pt]
&R_L = R_{Th} = \tfrac{-360}{-4} = 90\ \Omega,\qquad P_{max} = \tfrac{360^2}{4\cdot 90} = 360\ \text{W} \\[2pt]
&\textbf{(c)}\ V_2 = -180,\ V_1 = 726,\ V_3 = -1544\ \text{V} \\
&i_{kaynak} = \tfrac{906}{45} + \tfrac{2270}{30} = 95.8\ \text{A},\quad p_{3.6\text{kV}} = -344880\ \text{W},\quad \% = \tfrac{360}{344880} = 0.104\%
\end{aligned}""",
        traps=[
            "$150i_\\beta$ kaynağının <strong>− ucu üstte</strong>: alt sağ köşe $V_3 + 150i_\\beta$'dır, $V_3 - 150i_\\beta$ değil.",
            "$i_\\beta$ 45 Ω'un akımıdır ve oku <strong>sağa</strong> bakar: $i_\\beta = (V_1 - V_2)/45$. Kısa devrede de $V_2 = 0$ ile $i_\\beta = V_1/45$ olur, sıfır olmaz.",
            "Sol köşedeki 30 Ω ile üstteki 30 Ω farklı dirençlerdir; ikisini paralel sanma (aralarında 3.6 kV kaynak var).",
            "Kısa devre akımına 300 Ω'u katma: iki ucu da 0 V olduğu için akım taşımaz.",
        ],
    ),
]
