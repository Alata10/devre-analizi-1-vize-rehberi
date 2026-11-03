# -*- coding: utf-8 -*-
"""
SORU 1 (devam) — Bağımlı kaynaklı maksimum güç transferi / Thévenin.
P4.88, P5.119, P5.117, P4.79 (test kaynağı yöntemi).
İçerik şeması için bkz. build/CONTENT_SPEC.md ; sayılar build/verify/q1b_verify.py ile doğrulandı.
"""
from circuitkit import elm, ACCENT, NODE


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
def draw_p4_88(d):
    V = d.add(elm.SourceV().up().label('200 V', loc='top'))
    d.add(elm.Resistor().right().label('25 Ω'))
    d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down().label('100 Ω', loc='bottom'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Resistor().right().label('10 Ω')
          .label('$i_x \\rightarrow$', loc='bottom', color=ACCENT))
    d.add(elm.Dot().label('$V_2$', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down(d.unit * 0.45).label('20 Ω', loc='bottom'))
    d.add(elm.SourceControlledV().down(d.unit * 0.55).reverse().label('$30i_x$', loc='top'))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.pop()
    d.add(elm.Line().right(d.unit * 0.8))
    d.add(elm.Dot(open=True).label('a', loc='right'))
    d.add(elm.ResistorVar().down().label('$R_o$', loc='bottom'))
    d.add(elm.Dot(open=True).label('b', loc='right'))
    d.add(elm.Line().left().tox(V.start))


def draw_p5_119(d):
    h = d.unit * 1.5
    V = d.add(elm.SourceV().up(h).label('100 V', loc='top'))
    A = d.add(elm.Dot())
    # üst kol: (−+) 4Vx bağımlı kaynak + 4 Ω
    d.add(elm.Line().up(d.unit * 0.7))
    d.add(elm.SourceControlledV().right().label('$4V_x$', loc='top'))
    d.add(elm.Resistor().right().label('4 Ω', loc='top'))
    d.add(elm.Line().down(d.unit * 0.7))
    R = d.add(elm.Dot().label('$V_2$', loc='right', color=NODE, ofst=(0.1, 0.25)))
    # orta sıra
    d.add(elm.Resistor().at(A.center).right().label('4 Ω', loc='bottom'))
    M = d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.add(elm.Resistor().right().label('4 Ω', loc='bottom').to(R.center))
    # orta dikey kol: 4 Ω (Vx) + 20 V
    d.add(elm.Resistor().at(M.center).down(h / 2).label('4 Ω', loc='bottom')
          .label(('+', '$V_x$', '−'), loc='top', color=ACCENT))
    d.add(elm.SourceV().down(h / 2).reverse().label('20 V', loc='top'))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    # yük
    d.add(elm.Line().at(R.center).right(d.unit * 0.8))
    d.add(elm.Dot(open=True).label('a', loc='right'))
    d.add(elm.ResistorVar().down(h).label('$R_L$', loc='bottom'))
    d.add(elm.Dot(open=True).label('b', loc='right'))
    d.add(elm.Line().left().tox(V.start))


def draw_p5_117(d):
    h = d.unit * 2.2
    V = d.add(elm.SourceV().up(h).label('12 V', loc='top'))
    d.add(elm.Resistor().right(d.unit * 1.5).label('4 kΩ'))
    T = d.add(elm.Dot().label('$V_1$ (a)', loc='top', color=NODE))
    d.add(elm.Resistor().right(d.unit * 1.5).label('4 kΩ'))
    P = d.add(elm.Dot())
    # sağ kol: 2Ix bağımlı akım kaynağı (ok yukarı)
    d.add(elm.SourceControlledI().down(h).reverse().label('$2I_x$', loc='top'))
    BR = d.add(elm.Dot())
    # yük: üst düğüm ile iç düğüm arasında
    d.add(elm.ResistorVar().at(T.center).down(d.unit * 0.8).label('$R_L$', loc='bottom'))
    N = d.add(elm.Dot().label('$V_2$ (b)', loc='right', color=NODE, ofst=(0.05, -0.35)))
    d.add(elm.Line().left(d.unit * 0.5))
    d.add(elm.Resistor().down().toy(V.start).label('6 kΩ', loc='top')
          .label('$\\downarrow I_x$', loc='bottom', color=ACCENT))
    B1 = d.add(elm.Dot())
    d.add(elm.Line().at(N.center).right(d.unit * 0.5))
    d.add(elm.SourceI().down().toy(V.start).reverse().label('2 mA', loc='top'))
    B2 = d.add(elm.Dot())
    d.add(elm.Line().at(BR.center).left().tox(V.start))
    d.add(elm.Ground().at(B1.center))


def draw_p4_79(d):
    h = d.unit
    R100 = d.add(elm.Resistor().up(h).label('100 Ω', loc='top'))
    L = d.add(elm.Dot().label('$V_1$', loc='left', color=NODE, ofst=(-0.1, 0.25)))
    # üst kol: 150 Ω (iΔ ->)
    d.add(elm.Line().up(d.unit * 0.6))
    d.add(elm.Line().right(d.unit * 0.5)
          .label('$i_\\Delta \\rightarrow$', loc='top', color=ACCENT))
    d.add(elm.Resistor().right().label('150 Ω', loc='top'))
    d.add(elm.Line().right(d.unit * 0.5))
    d.add(elm.Line().down(d.unit * 0.6))
    J = d.add(elm.Dot())
    # orta sıra
    d.add(elm.Resistor().at(L.center).right().label('200 Ω', loc='bottom'))
    M = d.add(elm.Dot().label('$V_2$', loc='top', color=NODE))
    d.add(elm.Resistor().right().label('50 Ω', loc='bottom').to(J.center))
    d.add(elm.SourceControlledV().at(M.center).down(h).reverse().label('$250i_\\Delta$', loc='top'))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    # a-b terminalleri ve test kaynağı (mavi = bizim eklediğimiz)
    d.add(elm.Line().at(J.center).right(d.unit * 0.6))
    a = d.add(elm.Dot(open=True).label('a', loc='top'))
    d.add(elm.Line().right(d.unit * 0.7).color(ACCENT)
          .label('$I_T \\rightarrow$', loc='top', color=ACCENT))
    d.add(elm.SourceV().down(h).reverse().color(ACCENT).label('$V_T$', loc='bottom', color=ACCENT))
    d.add(elm.Line().left(d.unit * 0.7).color(ACCENT))
    d.add(elm.Dot(open=True).label('b', loc='bottom'))
    d.add(elm.Line().left().tox(R100.start))


CIRCUITS = {
    "p4-88": draw_p4_88,
    "p5-119": draw_p5_119,
    "p5-117": draw_p5_117,
    "p4-79": draw_p4_79,
}


# ---------------------------------------------------------------------------
# PROBLEMLER
# ---------------------------------------------------------------------------
PROBLEMS = [
    # =====================================================================
    # P4.88
    # =====================================================================
    dict(
        id="p4-88",
        topic=1,
        code="P4.88",
        title="$30i_x$ kaynaklı devrede $R_o$, $P_{max}$ ve güç yüzdesi",
        source="Çalışma Yaprağı 4 s.1",
        image="P4_88_ORIG.webp",
        circuit="p4-88",
        circuit_caption="Çözüm şeması: alt tel referans (0 V); üst düğümler $V_1$ ve $V_2$. $R_o$ a–b uçlarına bağlı.",
        level=2,
        question=(
            "Şekildeki devrede değişken direnç $R_o$, devreden <strong>maksimum güç</strong> çekecek şekilde ayarlanıyor. "
            "<br>a) $R_o$'nun değerini bulunuz."
            "<br>b) $R_o$'ya aktarılabilecek maksimum gücü bulunuz."
            "<br>c) Devrede üretilen toplam gücün yüzde kaçı $R_o$'ya aktarılır?"
        ),
        strategy=[
            r"Devrede bağımlı kaynak ($30i_x$) var → kaynakları öldürüp $R_{eq}$ <strong>aranmaz</strong>.",
            r"$R_o$'yu sök → açık devre gerilimi $V_{Th} = V_2$ (iki düğüm denklemi).",
            r"a–b'yi kısa devre et ($V_2 = 0$) → kısa devre akımı $I_{sc}$.",
            r"$R_o = R_{Th} = V_{Th}/I_{sc}$, &nbsp; $P_{max} = V_{Th}^2/(4R_{Th})$.",
            r"(c) için $R_o$ takılıyken devreyi tekrar çöz, kaynakların ürettiği gücü bul, oranla. $\sum p = 0$ ile sağla.",
        ],
        steps=[
            dict(
                title="Kontrol değişkenini ve bağımlı kaynağın düğümünü yaz (ek denklem)",
                body=(
                    r"Alt teli referans (0 V) seçelim. 25 Ω'dan sonraki düğüm $V_1$, sağ üst düğüm $V_2$ olsun.<br>"
                    r"• $i_x$: 10 Ω üzerindeki ok <strong>sağa</strong> bakıyor, yani akım $V_1$'den $V_2$'ye akıyor. "
                    r"Akım = (çıktığı düğüm − girdiği düğüm) / R.<br>"
                    r"• Sağdaki dikey kolda üstte 20 Ω, altta $30i_x$ kaynağı var. Kaynağın <em>+</em> ucu üstte, "
                    r"<em>−</em> ucu referansta. O hâlde 20 Ω ile kaynağın birleştiği noktanın gerilimi doğrudan $30i_x$'tir."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad i_x &= \frac{V_1 - V_2}{10} \\
\textbf{ek 2:}\quad V_{\text{ara}} &= 30\,i_x = 30\cdot\frac{V_1 - V_2}{10} = 3(V_1 - V_2)
\end{aligned}""",
                note="Bağımlı kaynağı gören ilk iş: kontrol değişkenini ($i_x$) düğüm gerilimleriyle yazmak.",
            ),
            dict(
                title="$V_1$ düğümünde KCL (açık devre, $R_o$ sökülü)",
                body=(
                    r"$V_1$ düğümüne üç kol bağlı: 25 Ω (sola, 200 V'a), 100 Ω (aşağı, referansa), 10 Ω (sağa, $V_2$'ye). "
                    r"Hepsini düğümden <strong>çıkan</strong> akım olarak (+) yazarız. Paydalar 25, 100, 10 → hepsini 100 ile çarparız."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - 200}{25} + \frac{V_1}{100} + \frac{V_1 - V_2}{10} &= 0 \qquad /\times 100 \\
4(V_1 - 200) + V_1 + 10(V_1 - V_2) &= 0 \\
4V_1 - 800 + V_1 + 10V_1 - 10V_2 &= 0 \\
15V_1 - 10V_2 &= 800 \qquad /\div 5 \\
\boxed{3V_1 - 2V_2 = 160} &\qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="$V_2$ düğümünde KCL",
                body=(
                    r"$V_2$ düğümünden iki akım çıkar: 10 Ω üzerinden sola $(V_2 - V_1)/10$ ve 20 Ω üzerinden aşağı "
                    r"$(V_2 - 30i_x)/20$. $R_o$ sökülü olduğu için üçüncü kol yok. Sonra ek 2'yi yerine koyarız."
                ),
                math=r"""\begin{aligned}
\frac{V_2 - V_1}{10} + \frac{V_2 - 30i_x}{20} &= 0 \\
\frac{V_2 - V_1}{10} + \frac{V_2 - 3(V_1 - V_2)}{20} &= 0 \qquad /\times 20 \\
2(V_2 - V_1) + V_2 - 3V_1 + 3V_2 &= 0 \\
2V_2 - 2V_1 + V_2 - 3V_1 + 3V_2 &= 0 \\
\boxed{-5V_1 + 6V_2 = 0} &\qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="Denklemleri çöz → $V_{Th}$",
                body=r"(II)'den $V_1$'i çekip (I)'de yerine koyarız.",
                math=r"""\begin{aligned}
\text{(II)}:\ 5V_1 = 6V_2 \;&\Rightarrow\; V_1 = 1.2\,V_2 \\
\text{(I)}:\ 3(1.2\,V_2) - 2V_2 &= 160 \\
3.6\,V_2 - 2V_2 &= 160 \\
1.6\,V_2 &= 160 \;\Rightarrow\; V_2 = 100\ \text{V} \\
V_1 &= 1.2\cdot 100 = 120\ \text{V} \\[4pt]
V_{Th} = V_{ab} = V_2 &= \boxed{100\ \text{V}}
\end{aligned}""",
                note=r"Hızlı kontrol: $i_x = (120-100)/10 = 2$ A, $30i_x = 60$ V, 20 Ω akımı $(100-60)/20 = 2$ A. Giren = çıkan, doğru.",
            ),
            dict(
                title="a–b kısa devre → $I_{sc}$",
                body=(
                    r"a ile b'yi düz telle birleştirince $V_2 = 0$ olur. $V_1$ düğümünün bağlantıları değişmediği için (I) aynen geçerlidir. "
                    r"(II) <strong>geçerli değildir</strong>, çünkü artık $V_2$ düğümünden kısa devre teline de akım gidiyor. "
                    r"Bu yüzden $I_{sc}$'yi kollardaki akımları tek tek bulup toplayarak hesaplarız."
                ),
                math=r"""\begin{aligned}
\text{(I)}:\ 3V_1 - 2(0) &= 160 \;\Rightarrow\; V_1 = \tfrac{160}{3} \approx 53.33\ \text{V} \\
i_x &= \frac{160/3 - 0}{10} = \frac{16}{3} \approx 5.333\ \text{A} \\
30\,i_x &= 30\cdot\frac{16}{3} = 160\ \text{V} \\
i_{20\Omega,\downarrow} &= \frac{0 - 160}{20} = -8\ \text{A} \quad (\text{yani 8 A yukarı}) \\[4pt]
I_{sc} &= \underbrace{\tfrac{16}{3}}_{10\,\Omega\text{'dan gelen}} + \underbrace{8}_{20\,\Omega\text{ kolundan gelen}} = \frac{40}{3} = \boxed{13.33\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="(a) ve (b): $R_o$ ve maksimum güç",
                body="Maksimum güç, yük direnci Thévenin direncine eşit olduğunda aktarılır.",
                math=r"""\begin{aligned}
R_o = R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{100}{40/3} = \frac{300}{40} = \boxed{7.5\ \Omega} \\[4pt]
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{100^2}{4\cdot 7.5} = \frac{10000}{30} = \boxed{333.33\ \text{W}}
\end{aligned}""",
            ),
            dict(
                title="(c) için: $R_o = 7.5\\ \\Omega$ takılıyken devreyi çöz",
                body=(
                    r"$R_o = R_{Th}$ olduğunda Thévenin gerilimi iki eşit dirence yarı yarıya bölünür, yani $V_2 = V_{Th}/2 = 50$ V. "
                    r"$V_1$ düğümü yine değişmediği için (I) geçerli. Buradan bütün akımları buluruz."
                ),
                math=r"""\begin{aligned}
V_2 &= \frac{100}{2} = 50\ \text{V} \\
\text{(I)}:\ 3V_1 - 2(50) = 160 \;&\Rightarrow\; 3V_1 = 260 \;\Rightarrow\; V_1 = \tfrac{260}{3} \approx 86.67\ \text{V} \\
i_x &= \frac{86.67 - 50}{10} = \frac{11}{3} \approx 3.667\ \text{A} \;\Rightarrow\; 30\,i_x = 110\ \text{V} \\
i_{20\Omega,\downarrow} &= \frac{50 - 110}{20} = -3\ \text{A} \quad (\text{yani 3 A yukarı}) \\
i_s &= \frac{200 - 86.67}{25} = \frac{68}{15} \approx 4.533\ \text{A} \quad (\text{200 V'un + ucundan çıkan})
\end{aligned}""",
                note=r"Kontrol ($V_2$ düğümü): $-3.667 + (-3) + 50/7.5 = -3.667 - 3 + 6.667 = 0$.",
            ),
            dict(
                title="(c): Güçler, $\\sum p = 0$ sağlaması ve yüzde",
                body=(
                    r"Pasif işaret kuralı: akım + uçtan giriyorsa $p = +vi$. 200 V kaynağında akım + uçtan <em>çıkıyor</em> → eksi. "
                    r"$30i_x$ kaynağında + uç üstte; üstten giren (aşağı) akım $-3$ A → $p = 110\cdot(-3)$. "
                    r"İki kaynak da negatif çıktı, yani ikisi de güç <strong>üretiyor</strong>."
                ),
                math=r"""\begin{aligned}
p_{200V} &= -200\cdot 4.533 = -906.67\ \text{W} \\
p_{30i_x} &= 110\cdot(-3) = -330\ \text{W} \\
p_{25\Omega} &= 4.533^2\cdot 25 = 513.78\ \text{W}, \qquad p_{100\Omega} = \frac{86.67^2}{100} = 75.11\ \text{W} \\
p_{10\Omega} &= 3.667^2\cdot 10 = 134.44\ \text{W}, \qquad p_{20\Omega} = 3^2\cdot 20 = 180\ \text{W} \\
p_{R_o} &= \frac{50^2}{7.5} = 333.33\ \text{W} \\[4pt]
\sum p_{\text{emilen}} &= 513.78 + 75.11 + 134.44 + 180 + 333.33 = 1236.67\ \text{W} \\
P_{\text{üretilen}} &= 906.67 + 330 = 1236.67\ \text{W} \quad \checkmark \\[4pt]
\%\ \text{yük} &= \frac{333.33}{1236.67}\times 100 = \boxed{\%\,26.95}
\end{aligned}""",
            ),
        ],
        answer=[
            r"V_{Th} = 100\ \text{V}",
            r"I_{sc} = 13.33\ \text{A}",
            r"R_o = R_{Th} = 7.5\ \Omega",
            r"P_{max} = 333.33\ \text{W}",
            r"\%\,26.95\ \text{yüke aktarılır}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } i_x = \tfrac{V_1 - V_2}{10},\qquad 30i_x = 3(V_1 - V_2) \\[2pt]
&\textbf{Açık devre:}\\
&V_1:\ \tfrac{V_1-200}{25} + \tfrac{V_1}{100} + \tfrac{V_1 - V_2}{10} = 0 \;\Rightarrow\; 3V_1 - 2V_2 = 160 \\
&V_2:\ \tfrac{V_2 - V_1}{10} + \tfrac{V_2 - 30i_x}{20} = 0 \;\Rightarrow\; -5V_1 + 6V_2 = 0 \\
&\Rightarrow V_1 = 120\ \text{V},\quad V_{Th} = V_2 = 100\ \text{V} \\[2pt]
&\textbf{Kısa devre } (V_2 = 0):\ V_1 = 53.33\ \text{V},\ i_x = 5.333\ \text{A},\ i_{20\Omega} = -8\ \text{A} \\
&I_{sc} = 5.333 + 8 = 13.33\ \text{A} \\[2pt]
&R_o = R_{Th} = 100/13.33 = 7.5\ \Omega,\qquad P_{max} = \tfrac{100^2}{4\cdot 7.5} = 333.33\ \text{W} \\[2pt]
&\textbf{(c) } V_2 = 50,\ V_1 = 86.67,\ i_x = 3.667,\ i_s = 4.533,\ i_{20\Omega} = -3 \\
&p_{200V} = -906.67,\ p_{dep} = -330,\ \textstyle\sum p_{\text{emilen}} = 1236.67\ \text{W} \\
&\% = 333.33/1236.67 = \%\,26.95
\end{aligned}""",
        traps=[
            r"$30i_x$ kaynağının <strong>+ ucu üstte</strong>: 20 Ω'un alt ucu $+30i_x$ olur. 20 Ω akımı $(V_2 - 30i_x)/20$, $(V_2 + 30i_x)/20$ değil.",
            r"Kısa devrede (II) denklemini kullanmak yanlıştır: $V_2$ düğümüne artık kısa devre teli de bağlı. $I_{sc}$'yi kol akımlarını toplayarak bul.",
            r"Kısa devrede 20 Ω akımı negatif çıkıyor ($-8$ A): bu akım <em>yukarı</em> akıp a ucuna gelir, yani $I_{sc}$'ye <strong>eklenir</strong>.",
            r"(c)'de yüzde, toplam <em>üretilen</em> güce göre alınır; bağımlı kaynağın ürettiği 330 W'ı da saymayı unutma.",
        ],
    ),

    # =====================================================================
    # P5.119
    # =====================================================================
    dict(
        id="p5-119",
        topic=1,
        code="P5.119",
        title="Üst kolda $4V_x$ bağımlı gerilim kaynağı: $R_L$ ve $P_{max}$",
        source="Çalışma Yaprağı 4 s.1",
        image="P5_119_ORIG.webp",
        circuit="p5-119",
        circuit_caption="Çözüm şeması: alt tel referans (0 V); sol üst düğüm 100 V, orta düğüm $V_1$, sağ düğüm $V_2$ (a ucu).",
        level=2,
        question=(
            "Şekildeki devrede $R_L$ direncine <strong>maksimum güç</strong> aktarılabilmesi için $R_L$ kaç ohm olmalıdır? "
            "Bu durumda $R_L$'ye aktarılabilecek maksimum güç kaç watt'tır?"
        ),
        strategy=[
            r"Bağımlı kaynak ($4V_x$) var → $V_{Th}$ ve $I_{sc}$ ile çalış.",
            r"Sol üst düğüm doğrudan 100 V'tur (kaynağa paralel); bilinmeyenler sadece $V_1$ (orta) ve $V_2$ (sağ).",
            r"$R_L$ sökülü: iki düğüm denklemi → $V_{Th} = V_2$.",
            r"$V_2 = 0$ (kısa devre): (I)'den $V_1$, sonra iki koldan a'ya gelen akımları topla → $I_{sc}$.",
            r"$R_L = V_{Th}/I_{sc}$, &nbsp; $P_{max} = V_{Th}^2/(4R_L)$.",
        ],
        steps=[
            dict(
                title="Bilinen düğümler ve kontrol değişkeni (ek denklemler)",
                body=(
                    r"Alt teli referans seçelim. 100 V kaynağı sol üst düğüm ile referans arasında olduğundan sol üst düğüm "
                    r"<strong>100 V</strong>'tur. Orta düğüm $V_1$, sağdaki düğüm $V_2$ olsun.<br>"
                    r"• $V_x$: orta dikey 4 Ω'un üst ucu (+) $V_1$'de, alt ucu (−) 20 V kaynağının + ucunda, yani 20 V'ta.<br>"
                    r"• Üst kol: 100 V düğümünden çıkınca önce $4V_x$ kaynağının <em>−</em> ucuna, sonra <em>+</em> ucuna geçeriz. "
                    r"− uçtan + uca geçerken gerilim $4V_x$ kadar <strong>artar</strong>. Kaynak ile üst 4 Ω arasındaki noktanın gerilimi bu yüzden $100 + 4V_x$'tir."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad V_x &= V_1 - 20 \\
\textbf{ek 2:}\quad V_{\text{üst}} &= 100 + 4V_x
\end{aligned}""",
            ),
            dict(
                title="$V_1$ düğümünde KCL (açık devre, $R_L$ sökülü)",
                body=(
                    r"$V_1$'den üç akım çıkar: sola 4 Ω üzerinden 100 V'a, aşağı 4 Ω üzerinden 20 V'a, sağa 4 Ω üzerinden $V_2$'ye. "
                    r"Paydaların hepsi 4 → 4 ile çarparız."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - 100}{4} + \frac{V_1 - 20}{4} + \frac{V_1 - V_2}{4} &= 0 \qquad /\times 4 \\
V_1 - 100 + V_1 - 20 + V_1 - V_2 &= 0 \\
\boxed{3V_1 - V_2 = 120} &\qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="$V_2$ düğümünde KCL",
                body=(
                    r"$V_2$'den iki akım çıkar: sola orta 4 Ω üzerinden $V_1$'e ve yukarı-sola üst 4 Ω üzerinden $V_{\text{üst}} = 100 + 4V_x$ noktasına. "
                    r"Sonra $V_x = V_1 - 20$ yazıp parantezleri açarız."
                ),
                math=r"""\begin{aligned}
\frac{V_2 - V_1}{4} + \frac{V_2 - (100 + 4V_x)}{4} &= 0 \qquad /\times 4 \\
V_2 - V_1 + V_2 - 100 - 4(V_1 - 20) &= 0 \\
V_2 - V_1 + V_2 - 100 - 4V_1 + 80 &= 0 \\
2V_2 - 5V_1 - 20 &= 0 \\
\boxed{-5V_1 + 2V_2 = 20} &\qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="Denklemleri çöz → $V_{Th}$",
                body=r"(I)'i 2 ile çarpıp (II) ile toplarsak $V_2$ yok olur.",
                math=r"""\begin{aligned}
2\times\text{(I)}:\quad 6V_1 - 2V_2 &= 240 \\
+\ \text{(II)}:\quad -5V_1 + 2V_2 &= 20 \\
\hline
V_1 &= 260\ \text{V} \\
V_2 &= 3V_1 - 120 = 3\cdot 260 - 120 = 660\ \text{V} \\[4pt]
V_{Th} = V_{ab} = V_2 &= \boxed{660\ \text{V}}
\end{aligned}""",
                note=(
                    r"Kontrol: $V_x = 240$ V, $4V_x = 960$ V, $V_{\text{üst}} = 1060$ V. "
                    r"Orta 4 Ω'dan $V_2$'ye gelen $(260-660)/4 = -100$ A, üst koldan gelen $(1060-660)/4 = 100$ A. Toplam 0, doğru."
                ),
            ),
            dict(
                title="a–b kısa devre → $I_{sc}$",
                body=(
                    r"$V_2 = 0$ yaparız. $V_1$ düğümünün bağlantıları değişmedi → (I) geçerli. (II) artık geçerli değil "
                    r"(kısa devre teli eklendi). a ucuna iki koldan akım gelir: orta 4 Ω ve üst kol. İkisini toplarız."
                ),
                math=r"""\begin{aligned}
\text{(I)}:\ 3V_1 - 0 &= 120 \;\Rightarrow\; V_1 = 40\ \text{V} \\
V_x &= 40 - 20 = 20\ \text{V} \;\Rightarrow\; V_{\text{üst}} = 100 + 4\cdot 20 = 180\ \text{V} \\
i_{\text{orta}} &= \frac{40 - 0}{4} = 10\ \text{A} \\
i_{\text{üst}} &= \frac{180 - 0}{4} = 45\ \text{A} \\[4pt]
I_{sc} &= 10 + 45 = \boxed{55\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="$R_L$ ve maksimum güç",
                body="Maksimum güç için $R_L = R_{Th}$ seçilir.",
                math=r"""\begin{aligned}
R_L = R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{660}{55} = \boxed{12\ \Omega} \\[4pt]
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{660^2}{4\cdot 12} = \frac{435600}{48} = \boxed{9075\ \text{W}}
\end{aligned}""",
                note=(
                    r"Sağlama (test kaynağı ile): bağımsız kaynakları sıfırla, a'ya $V_T$ uygula. (I) $\Rightarrow 3V_1 = V_T$, "
                    r"$I_T = \tfrac{V_T - V_1}{4} + \tfrac{V_T - 4V_1}{4} = \tfrac{V_T}{12}$ → $R_{Th} = 12\ \Omega$. Aynı sonuç."
                ),
            ),
        ],
        answer=[
            r"V_{Th} = 660\ \text{V}",
            r"I_{sc} = 55\ \text{A}",
            r"R_L = R_{Th} = 12\ \Omega",
            r"P_{max} = 9075\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } V_x = V_1 - 20,\qquad V_{\text{üst}} = 100 + 4V_x \\[2pt]
&\textbf{Açık devre:}\\
&V_1:\ \tfrac{V_1-100}{4} + \tfrac{V_1 - 20}{4} + \tfrac{V_1 - V_2}{4} = 0 \;\Rightarrow\; 3V_1 - V_2 = 120 \\
&V_2:\ \tfrac{V_2 - V_1}{4} + \tfrac{V_2 - 100 - 4V_x}{4} = 0 \;\Rightarrow\; -5V_1 + 2V_2 = 20 \\
&\Rightarrow V_1 = 260\ \text{V},\quad V_{Th} = V_2 = 660\ \text{V} \\[2pt]
&\textbf{Kısa devre } (V_2 = 0):\ V_1 = 40\ \text{V},\ V_x = 20\ \text{V},\ V_{\text{üst}} = 180\ \text{V} \\
&I_{sc} = \tfrac{40}{4} + \tfrac{180}{4} = 10 + 45 = 55\ \text{A} \\[2pt]
&R_L = R_{Th} = 660/55 = 12\ \Omega,\qquad P_{max} = \tfrac{660^2}{4\cdot 12} = 9075\ \text{W}
\end{aligned}""",
        traps=[
            r"$4V_x$ kaynağında <strong>− sol, + sağ</strong>: soldan sağa geçerken gerilim artar, $V_{\text{üst}} = 100 + 4V_x$. Ters okuyup $100 - 4V_x$ yazmak her şeyi bozar.",
            r"$V_x$ orta 4 Ω'un gerilimidir ve alt ucu 0 değil <strong>20 V</strong>'tur: $V_x = V_1 - 20$, $V_x = V_1$ değil.",
            r"Kısa devrede $V_x$ ve dolayısıyla $4V_x$ <strong>değişir</strong> (960 V → 80 V). Açık devredeki değeri taşımak yaygın bir hatadır.",
        ],
    ),

    # =====================================================================
    # P5.117
    # =====================================================================
    dict(
        id="p5-117",
        topic=1,
        code="P5.117",
        title="Yük devrenin içinde: iki düğüm arasındaki $R_L$ ve $2I_x$",
        source="Çalışma Yaprağı 4 s.1",
        image="P5_117_ORIG.webp",
        circuit="p5-117",
        circuit_caption="Çözüm şeması: alt tel referans (0 V). $R_L$, üst düğüm $V_1$ (a) ile iç düğüm $V_2$ (b) arasında; ikisi de referans değil.",
        level=3,
        question=(
            "Şekildeki devrede $R_L$ direncine <strong>maksimum güç</strong> aktarılabilmesi için $R_L$'nin değerini ve "
            "$R_L$'ye aktarılabilecek maksimum gücü bulunuz."
        ),
        strategy=[
            r"$R_L$ bir düğüm ile referans arasında değil, <strong>iki iç düğüm</strong> arasında: $V_{Th} = V_1 - V_2$ olacak.",
            r"Sağ kol: 4 kΩ, $2I_x$ akım kaynağıyla seri → bu 4 kΩ'dan geçen akım zorla $2I_x$'tir (ek denklem gerekmez).",
            r"$R_L$ sökülü: iki ayrı düğüm denklemi → $V_1$, $V_2$ → $V_{Th}$.",
            r"a–b kısa devre: $V_1 = V_2$ olur → <strong>süperdüğüm</strong>. Sonra kısa devre telindeki akımı KCL ile bul.",
            r"Birimler: kΩ, mA, V (kΩ · mA = V; V · mA = mW).",
        ],
        steps=[
            dict(
                title="Devreyi oku: düğümler, kontrol değişkeni, seri kol",
                body=(
                    r"Alt teli referans seçelim. Üstteki orta düğüm $V_1$ (a ucu), $R_L$'nin altındaki iç düğüm $V_2$ (b ucu) olsun. "
                    r"12 V kaynağın + ucu üstte olduğundan sol üst nokta 12 V'tur.<br>"
                    r"• $I_x$: 6 kΩ'da ok <strong>aşağı</strong>, yani $V_2$'den referansa akar.<br>"
                    r"• Sağdaki 4 kΩ ile $2I_x$ kaynağı seri bağlı (aralarındaki köşe başka hiçbir şeye bağlı değil). "
                    r"Kaynağın oku yukarı → $2I_x$ akımı yukarı çıkar, sağ 4 kΩ'dan sola geçerek $V_1$'e <strong>girer</strong>."
                ),
                math=r"""\begin{aligned}
\textbf{ek:}\quad I_x &= \frac{V_2}{6} \quad (\text{mA, } V_2 \text{ volt}) \\
i_{4k,\text{sağ}} &= 2I_x \quad (V_1 \text{ düğümüne giren})
\end{aligned}""",
                note="Akım kaynağıyla seri direnç akımı değiştirmez; düğüm denkleminde o kol doğrudan kaynak akımı olarak yazılır.",
            ),
            dict(
                title="Açık devre ($R_L$ sökülü): $V_2$ düğümü",
                body=(
                    r"$R_L$ sökülünce $V_2$ düğümünde sadece 6 kΩ (çıkan, +) ve 2 mA kaynağı (ok yukarı, düğüme <em>giren</em>, −) kalır."
                ),
                math=r"""\begin{aligned}
\frac{V_2}{6} - 2 &= 0 \;\Rightarrow\; V_2 = 12\ \text{V} \\
I_x &= \frac{12}{6} = 2\ \text{mA} \;\Rightarrow\; 2I_x = 4\ \text{mA}
\end{aligned}""",
            ),
            dict(
                title="Açık devre: $V_1$ düğümü → $V_{Th}$",
                body=(
                    r"$V_1$'den sol 4 kΩ üzerinden 12 V'a çıkan akım (+) ve sağ koldan giren $2I_x$ (−). $R_L$ sökülü."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - 12}{4} - 2I_x &= 0 \\
\frac{V_1 - 12}{4} - 4 &= 0 \qquad /\times 4 \\
V_1 - 12 &= 16 \;\Rightarrow\; V_1 = 28\ \text{V} \\[4pt]
V_{Th} = V_{ab} = V_1 - V_2 &= 28 - 12 = \boxed{16\ \text{V}}
\end{aligned}""",
                note=r"Burada $V_{Th}$ = $V_1$ değil! Yükün iki ucu da referanstan farklı, fark alınır.",
            ),
            dict(
                title="Kısa devre: a ile b birleşir → süperdüğüm",
                body=(
                    r"a–b'yi telle birleştirince $V_1 = V_2 = V$ olur. Kısa devre telindeki akımı bilmediğimiz için, iki düğümü "
                    r"tek bir <strong>süperdüğüm</strong> gibi düşünürüz: tel içeride kalır, denkleme girmez. "
                    r"Süperdüğümden çıkanlar: sol 4 kΩ ve 6 kΩ (+). Girenler: $2I_x$ ve 2 mA (−). Artık $I_x = V/6$."
                ),
                math=r"""\begin{aligned}
\frac{V - 12}{4} - 2I_x + \frac{V}{6} - 2 &= 0 \\
\frac{V - 12}{4} - \frac{2V}{6} + \frac{V}{6} - 2 &= 0 \\
\frac{V - 12}{4} - \frac{V}{6} - 2 &= 0 \qquad /\times 12 \\
3(V - 12) - 2V - 24 &= 0 \\
3V - 36 - 2V - 24 &= 0 \\
V &= 60\ \text{V} \;\Rightarrow\; I_x = \frac{60}{6} = 10\ \text{mA}
\end{aligned}""",
            ),
            dict(
                title="Kısa devre telindeki akım $I_{sc}$ (a'dan b'ye)",
                body=(
                    r"Telin akımını bulmak için sadece b düğümüne (eski $V_2$) KCL yazarız. "
                    r"b'den çıkan: 6 kΩ'a $I_x$. b'ye giren: 2 mA kaynağı ve telden gelen $I_{sc}$."
                ),
                math=r"""\begin{aligned}
I_x - 2 - I_{sc} &= 0 \\
I_{sc} &= 10 - 2 = \boxed{8\ \text{mA}}
\end{aligned}""",
                note=r"a tarafından sağlama: a'ya giren $2I_x = 20$ mA; a'dan çıkan sol 4 kΩ akımı $(60-12)/4 = 12$ mA ve $I_{sc} = 8$ mA. $20 = 12 + 8$, doğru.",
            ),
            dict(
                title="$R_L$ ve maksimum güç",
                body="Maksimum güç için $R_L = R_{Th}$. V / mA = kΩ ve V² / kΩ = mW olduğunu unutma.",
                math=r"""\begin{aligned}
R_L = R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{16\ \text{V}}{8\ \text{mA}} = \boxed{2\ \text{k}\Omega} \\[4pt]
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{16^2}{4\cdot 2000} = \frac{256}{8000} = 0.032\ \text{W} = \boxed{32\ \text{mW}}
\end{aligned}""",
                note=(
                    r"Sağlama (test kaynağı): 12 V kısa, 2 mA açık; a'ya $I_T$ sok, b'den çek. b: $V_2/6 + I_T = 0 \Rightarrow V_2 = -6I_T$, $I_x = -I_T$. "
                    r"a: $V_1/4 - 2I_x = I_T \Rightarrow V_1 = -4I_T$. $V_T = V_1 - V_2 = 2I_T$ → $R_{Th} = 2$ kΩ."
                ),
            ),
        ],
        answer=[
            r"V_{Th} = V_1 - V_2 = 16\ \text{V}",
            r"I_{sc} = 8\ \text{mA}",
            r"R_L = R_{Th} = 2\ \text{k}\Omega",
            r"P_{max} = 32\ \text{mW}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } I_x = V_2/6,\qquad \text{sağ 4 k}\Omega\text{ akımı} = 2I_x\ (V_1\text{'e giren}) \\[2pt]
&\textbf{Açık devre:}\\
&V_2:\ \tfrac{V_2}{6} - 2 = 0 \;\Rightarrow\; V_2 = 12\ \text{V},\ I_x = 2\ \text{mA} \\
&V_1:\ \tfrac{V_1 - 12}{4} - 2I_x = 0 \;\Rightarrow\; V_1 = 28\ \text{V} \\
&V_{Th} = V_1 - V_2 = 16\ \text{V} \\[2pt]
&\textbf{Kısa devre } (V_1 = V_2 = V,\ \text{süperdüğüm}):\\
&\tfrac{V - 12}{4} - 2\tfrac{V}{6} + \tfrac{V}{6} - 2 = 0 \;\Rightarrow\; V = 60\ \text{V},\ I_x = 10\ \text{mA} \\
&b:\ I_x - 2 - I_{sc} = 0 \;\Rightarrow\; I_{sc} = 8\ \text{mA} \\[2pt]
&R_L = R_{Th} = 16/8 = 2\ \text{k}\Omega,\qquad P_{max} = \tfrac{16^2}{4\cdot 2000} = 32\ \text{mW}
\end{aligned}""",
        traps=[
            r"$V_{Th}$'yi $V_1 = 28$ V sanmak: yük iki iç düğüm arasında, $V_{Th} = V_1 - V_2 = 16$ V.",
            r"Sağdaki 4 kΩ'u düğüm denklemine $(V_1 - V_3)/4$ diye yazıp yeni bilinmeyen açmak gereksiz: akım kaynağıyla seri olduğu için akımı zaten $2I_x$.",
            r"Kısa devrede $I_x$ değişir (2 mA → 10 mA). $2I_x$'i açık devre değeriyle (4 mA) bırakma.",
            r"Birim karışıklığı: kΩ ve mA ile çalışınca güç mW çıkar. $16^2/(4\cdot 2)$ = 32 <strong>mW</strong>, 32 W değil.",
        ],
    ),

    # =====================================================================
    # P4.79
    # =====================================================================
    dict(
        id="p4-79",
        topic=1,
        code="P4.79",
        title="Bağımsız kaynak yok: test kaynağı ile $R_{Th}$",
        source="Çalışma Yaprağı 3 s.3 (Thévenin)",
        image="P4_79_ORIG.webp",
        circuit="p4-79",
        circuit_caption="Çözüm şeması: alt tel (b) referans. Mavi $V_T$ kaynağı kitapta yok; $R_{Th}$'yi bulmak için a–b'ye bizim bağladığımız test kaynağıdır.",
        level=2,
        question=(
            "Şekildeki devrenin a–b uçlarına göre <strong>Thévenin eşdeğerini</strong> bulunuz. "
            "(Devrede hiç bağımsız kaynak yoktur; yalnızca dirençler ve $250i_\\Delta$ bağımlı gerilim kaynağı vardır.)"
        ),
        strategy=[
            r"Bağımsız kaynak yok → devre kendi başına hiçbir akım/gerilim üretemez: $V_{Th} = 0$, $I_{sc} = 0$.",
            r"$R_{Th} = V_{Th}/I_{sc} = 0/0$ <strong>belirsiz</strong> → bu yol çalışmaz.",
            r"Çözüm: a–b'ye dışarıdan bir <strong>test kaynağı</strong> $V_T$ bağla, çekilen $I_T$ akımını bul.",
            r"$R_{Th} = V_T / I_T$. Bilinmeyen sadece $V_1$ (orta düğüm $V_2$ bağımlı kaynakla belli).",
        ],
        steps=[
            dict(
                title="Neden $V_{Th}/I_{sc}$ burada işe yaramaz?",
                body=(
                    r"Bağımlı kaynak, kendisini kontrol eden akım ($i_\Delta$) sıfırsa sıfır üretir. Devrede onu başlatacak "
                    r"bağımsız bir kaynak olmadığı için bütün düğüm gerilimleri sıfır kalır. "
                    r"Yani a–b açıkken $V_{Th} = 0$, kısa devrede de $I_{sc} = 0$ çıkar. "
                    r"Oran $0/0$ olur ve hiçbir şey söylemez. Devreyi <strong>dışarıdan uyarmamız</strong> gerekir."
                ),
                math=r"""\begin{aligned}
V_{Th} &= 0, \qquad I_{sc} = 0 \\
R_{Th} &= \frac{V_{Th}}{I_{sc}} = \frac{0}{0} \;\;\Rightarrow\;\; \text{belirsiz}
\end{aligned}""",
                note="Sınav kuralı: bağımsız kaynak yok + bağımlı kaynak var = test kaynağı yöntemi.",
            ),
            dict(
                title="Test kaynağını bağla, ek denklemleri yaz",
                body=(
                    r"a–b'ye + ucu a'da olan bir $V_T$ gerilim kaynağı bağlarız; b referans (0 V). Kaynaktan a'ya giren akım $I_T$. "
                    r"Böylece a düğümünün gerilimi $V_T$ olur. Sol düğüm $V_1$, orta düğüm $V_2$.<br>"
                    r"• $i_\Delta$: 150 Ω'da ok <strong>sağa</strong>, yani $V_1$'den a'ya ($V_T$) akar.<br>"
                    r"• $250i_\Delta$ kaynağının + ucu üstte, − ucu referansta → orta düğüm doğrudan $V_2 = 250i_\Delta$."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad i_\Delta &= \frac{V_1 - V_T}{150} \\
\textbf{ek 2:}\quad V_2 &= 250\,i_\Delta = \frac{250}{150}(V_1 - V_T) = \frac{5}{3}(V_1 - V_T)
\end{aligned}""",
            ),
            dict(
                title="$V_1$ düğümünde KCL",
                body=(
                    r"$V_1$'den üç akım çıkar: aşağı 100 Ω, sağa 200 Ω ($V_2$'ye), yukarıdan 150 Ω (a'ya). "
                    r"Paydalar 100, 200, 150 → ortak kat 600. $V_2$ düğümüne denklem yazmayız, çünkü gerilimi bağımlı kaynakla zaten belli."
                ),
                math=r"""\begin{aligned}
\frac{V_1}{100} + \frac{V_1 - V_2}{200} + \frac{V_1 - V_T}{150} &= 0 \qquad /\times 600 \\
6V_1 + 3(V_1 - V_2) + 4(V_1 - V_T) &= 0 \\
6V_1 + 3V_1 - 3V_2 + 4V_1 - 4V_T &= 0 \\
13V_1 - 3V_2 - 4V_T &= 0 \\
13V_1 - 5(V_1 - V_T) - 4V_T &= 0 \qquad (3V_2 = 5(V_1 - V_T)) \\
13V_1 - 5V_1 + 5V_T - 4V_T &= 0 \\
8V_1 + V_T &= 0 \;\Rightarrow\; \boxed{V_1 = -\tfrac{V_T}{8}}
\end{aligned}""",
            ),
            dict(
                title="$i_\\Delta$ ve $V_2$'yi $V_T$ cinsinden bul",
                body=r"Bulduğumuz $V_1$'i ek denklemlere koyarız.",
                math=r"""\begin{aligned}
i_\Delta &= \frac{-\tfrac{V_T}{8} - V_T}{150} = \frac{-\tfrac{9V_T}{8}}{150} = -\frac{9V_T}{1200} = -\frac{3V_T}{400} \\
V_2 &= 250\cdot\left(-\frac{3V_T}{400}\right) = -\frac{750\,V_T}{400} = -\frac{15V_T}{8}
\end{aligned}""",
            ),
            dict(
                title="a düğümünde KCL → $I_T$ ve $R_{Th}$",
                body=(
                    r"Test kaynağından a'ya giren $I_T$, a'dan devreye iki koldan çıkar: 150 Ω üzerinden $V_1$'e ve 50 Ω üzerinden $V_2$'ye."
                ),
                math=r"""\begin{aligned}
I_T &= \frac{V_T - V_1}{150} + \frac{V_T - V_2}{50} \\
&= \frac{V_T + \tfrac{V_T}{8}}{150} + \frac{V_T + \tfrac{15V_T}{8}}{50} \\
&= \frac{\tfrac{9V_T}{8}}{150} + \frac{\tfrac{23V_T}{8}}{50} = \frac{3V_T}{400} + \frac{23V_T}{400} \\
&= \frac{26V_T}{400} = \frac{13V_T}{200} \\[4pt]
R_{Th} &= \frac{V_T}{I_T} = \frac{200}{13} \approx \boxed{15.38\ \Omega}
\end{aligned}""",
                note=(
                    r"Sayısal sağlama ($V_T = 1$ V): $V_1 = -0.125$ V, $i_\Delta = -7.5$ mA, $V_2 = -1.875$ V, "
                    r"$I_T = 7.5 + 57.5 = 65$ mA → $R_{Th} = 1/0.065 = 15.38\ \Omega$."
                ),
            ),
            dict(
                title="Thévenin eşdeğeri ve maksimum güç yorumu",
                body=(
                    r"Thévenin eşdeğeri: gerilimi sıfır olan bir kaynak (yani kısa devre) ile seri $15.38\ \Omega$. "
                    r"Dışarıdan bakınca bu devre <strong>sadece bir dirençtir</strong>. "
                    r"a–b'ye bir $R_L$ bağlasak eşleşme değeri $R_L = R_{Th} = 15.38\ \Omega$ olurdu, ama $V_{Th} = 0$ olduğu için "
                    r"aktarılacak güç de sıfırdır. Bu devre ancak başka bir kaynaklı devrenin parçası olduğunda anlam kazanır; "
                    r"o zaman yerine doğrudan $15.38\ \Omega$ yazılır."
                ),
                math=r"""\begin{aligned}
V_{Th} &= 0\ \text{V}, \qquad R_{Th} = \frac{200}{13} \approx 15.38\ \Omega \\
P_{max} &= \frac{V_{Th}^2}{4R_{Th}} = \frac{0^2}{4\cdot 15.38} = 0\ \text{W}
\end{aligned}""",
            ),
        ],
        answer=[
            r"V_{Th} = 0\ \text{V}",
            r"I_T = \tfrac{13}{200}V_T",
            r"R_{Th} = \tfrac{200}{13} \approx 15.38\ \Omega",
        ],
        exam=r"""\begin{aligned}
&\text{Bağımsız kaynak yok} \Rightarrow V_{Th} = 0,\ I_{sc} = 0 \Rightarrow \text{test kaynağı } V_T \text{ (a: +)} \\[2pt]
&\text{ek: } i_\Delta = \tfrac{V_1 - V_T}{150},\qquad V_2 = 250i_\Delta = \tfrac{5}{3}(V_1 - V_T) \\
&V_1:\ \tfrac{V_1}{100} + \tfrac{V_1 - V_2}{200} + \tfrac{V_1 - V_T}{150} = 0 \;\Rightarrow\; 13V_1 - 3V_2 - 4V_T = 0 \\
&\Rightarrow 8V_1 + V_T = 0,\quad V_1 = -V_T/8 \\
&i_\Delta = -\tfrac{3V_T}{400},\qquad V_2 = -\tfrac{15V_T}{8} \\
&I_T = \tfrac{V_T - V_1}{150} + \tfrac{V_T - V_2}{50} = \tfrac{3V_T}{400} + \tfrac{23V_T}{400} = \tfrac{13V_T}{200} \\[2pt]
&R_{Th} = V_T/I_T = 200/13 = 15.38\ \Omega,\qquad V_{Th} = 0
\end{aligned}""",
        traps=[
            r"$V_{Th}/I_{sc}$ ile uğraşmak: ikisi de 0 çıkar, oran $0/0$. Bağımsız kaynak yoksa doğrudan test kaynağına geç.",
            r"Bağımlı kaynağı da 'öldürüp' sadece dirençlerle $R_{eq}$ hesaplamak yanlıştır (öyle bulunan değer 15.38 Ω değildir). Bağımlı kaynak devrede <strong>kalır</strong>.",
            r"$i_\Delta$'nın tanımı $V_1$'den a'ya: test kaynağı bağlandığında a düğümü $V_T$ olur, $i_\Delta = (V_1 - V_T)/150$. a'yı 0 sanma.",
            r"$V_2$ için ayrıca KCL yazmaya çalışma: düğüm bir gerilim kaynağıyla referansa bağlı, gerilimi $250i_\Delta$ olarak zaten biliniyor.",
        ],
    ),
]
