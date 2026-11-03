# -*- coding: utf-8 -*-
"""
SORU 4 (b) — Güç hesabı / güç dengesi (pasif işaret kuralı, Σp = 0, kaynak bağlantılarının geçerliliği).
Çalışma Yaprağı 1 problemleri: Şekil 2.23, P2.1, P2.2, P2.15, P2.18.
İçerik şeması için bkz. build/CONTENT_SPEC.md — doğrulama: build/verify/q4b_verify.py
"""
from circuitkit import elm, ACCENT, NODE


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
def draw_fig2_23(d):
    # Sol göz: 10 V (+ üstte) ve 6 Ω
    V = d.add(elm.SourceV().up().label('10 V', loc='top'))
    d.add(elm.Line().right(d.unit * 0.9).label('$i_s \\rightarrow$', loc='top', color=ACCENT))
    d.add(elm.Resistor().down().label('6 Ω', loc='bottom'))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.add(elm.Line().left().tox(V.start))
    # Sağ göz: 3 i_s (+ üstte) → 2 Ω → 3 Ω ; yalnız alt telden ortak
    d.add(elm.Line().right(d.unit * 0.7).at(G.center))
    B2 = d.add(elm.Dot())
    d.add(elm.SourceControlledV().up().label('$3i_s$', loc='bottom'))
    d.add(elm.Resistor().right().label('2 Ω')
          .label('$i_o \\rightarrow$', loc='bottom', color=ACCENT))
    d.add(elm.Resistor().down().label('3 Ω', loc='top')
          .label(('+', '$v_o$', '−'), loc='bottom', color=ACCENT))
    d.add(elm.Line().left().tox(B2.center))


def draw_p2_1(d):
    D = d.add(elm.SourceControlledV().up().label('$i_b/4$', loc='top'))
    d.add(elm.Line().right(d.unit * 1.1))
    T = d.add(elm.Dot().label('üst', loc='top', color=NODE))
    d.add(elm.Line().right(d.unit * 1.1)
          .label('$\\leftarrow i_b$', loc='top', color=ACCENT))
    d.add(elm.SourceI().down().label('8 A', loc='bottom'))
    d.add(elm.Line().left(d.unit * 1.1))
    B = d.add(elm.Dot())
    d.add(elm.Ground().at(B.center))
    d.add(elm.Line().left().tox(D.start))
    d.add(elm.SourceV().up().at(B.center).label('$v_g$', loc='bottom', color=ACCENT))


def draw_p2_2(d):
    S = d.add(elm.SourceI().down().label('15 A', loc='bottom'))
    d.add(elm.Line().right(d.unit * 1.6)
          .label('15 A $\\rightarrow$', loc='bottom', color=ACCENT))
    R = d.add(elm.Dot())
    d.add(elm.Ground().at(S.end))
    d.add(elm.SourceControlledI().right(d.unit * 1.6).at(S.start)
          .label('$\\alpha v_x$', loc='top'))
    d.add(elm.SourceV().down().label('25 V', loc='bottom')
          .label(('+', '$v_x$', '−'), loc='top', color=ACCENT))
    del R


def draw_p2_15(d):
    s = d.unit * 0.85
    L = d.unit
    xs = [i * s for i in range(6)]
    # üst ve alt raylar
    d.add(elm.Line().at((xs[0], 0)).to((xs[-1], 0)))
    d.add(elm.Line().at((xs[0], -L)).to((xs[-1], -L)))
    d.add(elm.Resistor().down().at((xs[0], 0)).label('6 kΩ', loc='bottom'))
    d.add(elm.SourceI().up().at((xs[1], -L)).label('6 mA', loc='top'))
    d.add(elm.SourceControlledI().down().at((xs[2], 0)).label('$3I_x$', loc='bottom'))
    d.add(elm.SourceI().down().at((xs[3], 0)).label('3 mA', loc='bottom'))
    d.add(elm.Resistor().down().at((xs[4], 0)).label('2 kΩ', loc='bottom')
          .label('$I_x \\downarrow$', loc='top', color=ACCENT))
    d.add(elm.Resistor().down().at((xs[5], 0)).label('3 kΩ', loc='bottom')
          .label('$I_L \\downarrow$', loc='top', color=ACCENT))
    for x in xs[1:-1]:
        d.add(elm.Dot().at((x, 0)))
        d.add(elm.Dot().at((x, -L)))
    d.add(elm.Dot().at((xs[3] + s / 2, 0)).label('$V$', loc='top', color=NODE))
    d.add(elm.Ground().at((xs[3] + s / 2, -L)))


def draw_p2_18(d):
    V = d.add(elm.SourceV().up().label('45 V', loc='top'))
    d.add(elm.Resistor().right().label('1 Ω')
          .label(('+', '$V_o$', '−'), loc='bottom', color=ACCENT))
    d.add(elm.SourceControlledV().down().label('$3V_o$', loc='bottom'))
    d.add(elm.Resistor().left().tox(V.start).label('5 Ω', loc='bottom')
          .label('$\\leftarrow i$', loc='top', color=ACCENT))
    d.add(elm.Ground().at(V.start))


CIRCUITS = {
    "fig2-23": draw_fig2_23,
    "p2-1": draw_p2_1,
    "p2-2": draw_p2_2,
    "p2-15": draw_p2_15,
    "p2-18": draw_p2_18,
}


# ---------------------------------------------------------------------------
# PROBLEMLER
# ---------------------------------------------------------------------------
PROBLEMS = [
    # ------------------------------------------------------------------ Şekil 2.23
    dict(
        id="fig2-23",
        topic=4,
        code="Şekil 2.23",
        title="Bağımlı kaynaklı iki gözlü devrede $v_o$ ve güç dengesi",
        source="Çalışma Yaprağı 1 s.7 · Örnek 2.10",
        image="FIG_2_23_ORIG.webp",
        circuit="fig2-23",
        circuit_caption="Çözüm şeması: alt tel referans (0 V). $i_s$ ve $i_o$ şekildeki yönlerde; $v_o$'nun + ucu üstte.",
        level=1,
        question=(
            "a) Kirchhoff yasalarını ve Ohm yasasını kullanarak Şekil 2.23'te gösterilen $v_o$ gerilimini bulunuz.<br>"
            "b) Çözümünüzün, devrede <strong>üretilen toplam gücün harcanan toplam güce eşit</strong> olması "
            "koşuluyla tutarlı olduğunu gösteriniz."
        ),
        strategy=[
            "İki göz yalnızca alt telden birleşiyor → gözler arasında akım geçmez, her göz ayrı çözülür.",
            "Sol göz: 10 V doğrudan 6 Ω'un uçlarında → $i_s$ Ohm yasasından.",
            "Sağ göz: $3i_s$ artık bilinen bir sayı; KVL ile $i_o$, sonra $v_o = 3\\,i_o$.",
            "Her eleman için pasif işaret kuralıyla $p$ yaz ve $\\sum p = 0$ olduğunu göster.",
        ],
        steps=[
            dict(
                title="Topolojiyi oku: gözler neden birbirinden bağımsız?",
                body=(
                    "Sol gözün etrafına kapalı bir çizgi çizdiğini düşün. Bu çizgiyi kesen <strong>tek</strong> tel, "
                    "alt teldeki bağlantı. KCL'ye göre kapalı bir bölgeye giren toplam akım sıfırdır; "
                    "tek telden giren akım başka yoldan çıkamayacağı için o telin akımı sıfır olmak zorunda.<br>"
                    "Sonuç: 10 V kaynağından çıkan $i_s$ akımının tamamı 6 Ω'dan geçer; sağ gözün akımı ise $i_o$'dır."
                ),
                math=r"""i_{\text{alt tel (gözler arası)}} = 0 \;\Rightarrow\; i_{6\Omega} = i_s,\qquad i_{3\Omega} = i_o""",
            ),
            dict(
                title="Sol göz: KVL ile $i_s$",
                body=(
                    "Sol alttan başlayıp saat yönünde dolaşalım. 10 V kaynağında önce <em>−</em> ucuyla karşılaşırız → $-10$. "
                    "6 Ω'da akım $i_s$ yukarıdan aşağı akıyor, yani üst ucu +; önce + ile karşılaşırız → $+6i_s$."
                ),
                math=r"""\begin{aligned}
-10 + 6\,i_s &= 0 \\
6\,i_s &= 10 \\
i_s &= \frac{10}{6} = \frac{5}{3} \;\Rightarrow\; \boxed{i_s \approx 1.667\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="Bağımlı kaynağın değerini hesapla",
                body="Bağımlı kaynak, $i_s$ bilindiği anda sıradan bir gerilim kaynağı gibi davranır.",
                math=r"""3\,i_s = 3\cdot\frac{5}{3} = \boxed{5\ \text{V}}""",
            ),
            dict(
                title="Sağ göz: KVL ile $i_o$ ve $v_o$",
                body=(
                    "Sağ gözün sol alt köşesinden saat yönünde: $3i_s$ kaynağında önce <em>−</em> → $-3i_s$. "
                    "2 Ω'da $i_o$ sağa akıyor, önce + → $+2i_o$. 3 Ω'da $i_o$ aşağı akıyor, önce + → $+3i_o$.<br>"
                    "$v_o$'nun + ucu üstte ve akım üstten giriyor, bu yüzden $v_o = +3\\,i_o$."
                ),
                math=r"""\begin{aligned}
-3i_s + 2\,i_o + 3\,i_o &= 0 \\
-5 + 5\,i_o &= 0 \\
i_o &= \frac{5}{5} = \boxed{1\ \text{A}} \\[4pt]
v_o &= 3\,\Omega \cdot i_o = 3\cdot 1 = \boxed{3\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="Her elemanın gücü (pasif işaret kuralı)",
                body=(
                    "Kural: akım elemanın <strong>+ ucundan giriyorsa</strong> $p = +vi$, + ucundan çıkıyorsa $p = -vi$. "
                    "Dirençlerde akım her zaman + uçtan girer, bu yüzden $p = i^2R > 0$.<br>"
                    "• 10 V: $i_s$ kaynağın + (üst) ucundan <em>çıkıyor</em> → eksi.<br>"
                    "• $3i_s$: $i_o$ kaynağın + (üst) ucundan <em>çıkıyor</em> → eksi."
                ),
                math=r"""\begin{aligned}
p_{10\text{V}} &= -10\cdot i_s = -10\cdot\frac{5}{3} = -16.67\ \text{W} &&\text{(üretir)} \\
p_{6\Omega} &= i_s^2\cdot 6 = \frac{25}{9}\cdot 6 = 16.67\ \text{W} &&\text{(emer)} \\
p_{3i_s} &= -(3i_s)\cdot i_o = -5\cdot 1 = -5\ \text{W} &&\text{(üretir)} \\
p_{2\Omega} &= i_o^2\cdot 2 = 1\cdot 2 = 2\ \text{W} &&\text{(emer)} \\
p_{3\Omega} &= i_o^2\cdot 3 = 1\cdot 3 = 3\ \text{W} &&\text{(emer)}
\end{aligned}""",
            ),
            dict(
                title="Güç dengesi: $\\sum p = 0$",
                body="Tüm güçleri işaretleriyle topla. Sıfır çıkıyorsa üretilen güç = harcanan güç demektir.",
                math=r"""\begin{aligned}
\sum p &= -16.67 + 16.67 - 5 + 2 + 3 = \boxed{0} \\[4pt]
P_{\text{üretilen}} &= 16.67 + 5 = 21.67\ \text{W} \\
P_{\text{harcanan}} &= 16.67 + 2 + 3 = 21.67\ \text{W}
\end{aligned}""",
                note="Kesirle çalışırsan yuvarlama hatası olmaz: $-\\tfrac{50}{3} + \\tfrac{50}{3} - 5 + 2 + 3 = 0$.",
            ),
        ],
        answer=[
            r"i_s = \tfrac{5}{3} \approx 1.667\ \text{A}",
            r"i_o = 1\ \text{A}",
            r"v_o = 3\ \text{V}",
            r"P_{\text{üretilen}} = P_{\text{harcanan}} = 21.67\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&\text{Sol göz: } -10 + 6i_s = 0 \;\Rightarrow\; i_s = 5/3\ \text{A} \\
&3i_s = 5\ \text{V} \\
&\text{Sağ göz: } -3i_s + 2i_o + 3i_o = 0 \;\Rightarrow\; i_o = 1\ \text{A},\quad v_o = 3i_o = 3\ \text{V} \\[2pt]
&p_{10V} = -10(5/3) = -16.67\ \text{W},\quad p_{6\Omega} = (5/3)^2\cdot 6 = 16.67\ \text{W} \\
&p_{3i_s} = -5\cdot 1 = -5\ \text{W},\quad p_{2\Omega} = 2\ \text{W},\quad p_{3\Omega} = 3\ \text{W} \\
&\textstyle\sum p = -16.67 + 16.67 - 5 + 2 + 3 = 0 \;\Rightarrow\; P_{\text{ür}} = P_{\text{har}} = 21.67\ \text{W}
\end{aligned}""",
        traps=[
            "Bağımlı kaynak da güç üretebilir: $3i_s$ kaynağı burada 5 W <strong>üretiyor</strong>. "
            "Onu hesaba katmazsan $\\sum p \\neq 0$ çıkar.",
            "Pasif işaret kuralında bakılan tek şey akımın <strong>+ uçtan girip girmediğidir</strong>; "
            "kaynağın bağımlı ya da bağımsız olması işareti değiştirmez.",
            "6 Ω'un akımının $i_s$'e eşit olduğunu söylerken gerekçeyi yaz: iki göz arasında tek tel var, o telden akım geçmez.",
        ],
    ),

    # ------------------------------------------------------------------ P2.1
    dict(
        id="p2-1",
        topic=4,
        code="P2.1",
        title="Paralel gerilim kaynakları: geçerli bağlantı için $v_g$ ve 8 A kaynağının gücü",
        source="Çalışma Yaprağı 1 s.5",
        image="PROB_2_1_ORIG.webp",
        circuit="p2-1",
        circuit_caption="Çözüm şeması: alt tel referans (0 V). Üç eleman da üst ve alt düğüm arasında, yani paralel; $i_b$ oku sola.",
        level=1,
        question=(
            "Şekildeki devre için:<br>"
            "a) Bağlantının <strong>geçerli</strong> olması için $v_g$ ne olmalıdır?<br>"
            "b) Bu $v_g$ değeri için 8 A kaynağına ait gücü bulunuz."
        ),
        strategy=[
            "Üç eleman da aynı iki düğüm (üst–alt) arasında → hepsi paralel, hepsinin gerilimi aynı.",
            "Paralel gerilim kaynakları ancak <strong>aynı polarite ve aynı değerde</strong> ise geçerlidir (KVL).",
            "$i_b$'yi 8 A kaynağından KCL ile bul (ok sola bakıyor, dikkat).",
            "8 A kaynağının gücü: akım + uçtan giriyor mu? → $p = \\pm vi$.",
        ],
        steps=[
            dict(
                title="$i_b$'yi bul (sağ üst köşede KCL)",
                body=(
                    "8 A kaynağının oku aşağı: kaynak, üst telden 8 A çekip alt tele basıyor. "
                    "$i_b$ ise sağ üst köşeden <strong>sola</strong> doğru tanımlı. Sağ üst köşe düğümünde "
                    "çıkan akımlar + : kaynaktan aşağı çıkan 8 A ve sola çıkan $i_b$."
                ),
                math=r"""\begin{aligned}
8 + i_b &= 0 \\
\boxed{i_b = -8\ \text{A}} &\qquad (\text{yani üst telde 8 A sağa akıyor})
\end{aligned}""",
            ),
            dict(
                title="Geçerlilik: iki paralel gerilim kaynağında KVL",
                body=(
                    "$i_b/4$ kaynağı ile $v_g$ kaynağının oluşturduğu sol gözü saat yönünde dolaşalım (sol alttan başla). "
                    "$i_b/4$ kaynağında önce <em>−</em> → $-\\tfrac{i_b}{4}$; $v_g$ kaynağında aşağı inerken önce <em>+</em> → $+v_g$. "
                    "KVL'nin sağlanması için iki gerilim eşit olmalı; aksi halde bağlantı <strong>geçersizdir</strong> "
                    "(ideal kaynaklar sonsuz akım isterdi)."
                ),
                math=r"""\begin{aligned}
-\frac{i_b}{4} + v_g &= 0 \\
v_g &= \frac{i_b}{4} = \frac{-8}{4} \\
\boxed{v_g = -2\ \text{V}} &
\end{aligned}""",
                note="Kural (ÇY1): paralel gerilim kaynaklarının polariteleri ve büyüklükleri aynı olmalı; seri akım kaynaklarının yönü ve büyüklüğü aynı olmalı.",
            ),
            dict(
                title="8 A kaynağının gerilimi",
                body=(
                    "8 A kaynağı da aynı iki düğüme bağlı, bu yüzden üzerindeki gerilim (üst − alt) $v_g$'dir. "
                    "Kaynağın + ucunu üstte kabul edelim: $v = -2$ V (üst düğüm alttan 2 V daha düşük)."
                ),
                math=r"""v_{8\text{A}} = v_{\text{üst}} - v_{\text{alt}} = v_g = -2\ \text{V}""",
            ),
            dict(
                title="8 A kaynağının gücü (pasif işaret kuralı)",
                body=(
                    "8 A akım kaynağın içinden yukarıdan aşağı akıyor, yani + kabul ettiğimiz <strong>üst uçtan giriyor</strong> "
                    "→ $p = +v\\,i$. Sonuç negatif çıkarsa kaynak güç üretir."
                ),
                math=r"""\begin{aligned}
p_{8\text{A}} &= +v_{8\text{A}}\cdot 8 = (-2)(8) \\
&= \boxed{-16\ \text{W}} \qquad (\text{16 W üretir / verir})
\end{aligned}""",
            ),
            dict(
                title="Kontrol: $\\sum p = 0$",
                body=(
                    "Paralel iki gerilim kaynağının akımlarını ayrı ayrı bulamayız (8 A'yı aralarında nasıl paylaştıkları belirsiz); "
                    "soru da bu yüzden yalnız 8 A kaynağını soruyor. Ama <em>toplamlarını</em> bulabiliriz. "
                    "$i_1$, $i_2$: $i_b/4$ ve $v_g$ kaynaklarında aşağı akan akımlar olsun. Üst düğümde KCL (çıkan +):"
                ),
                math=r"""\begin{aligned}
i_1 + i_2 + 8 &= 0 \;\Rightarrow\; i_1 + i_2 = -8\ \text{A} \\
p_1 + p_2 &= v_g\,i_1 + v_g\,i_2 = v_g\,(i_1 + i_2) = (-2)(-8) = +16\ \text{W} \\[4pt]
\sum p &= -16 + 16 = \boxed{0}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_b = -8\ \text{A}",
            r"v_g = -2\ \text{V}",
            r"p_{8\text{A}} = -16\ \text{W}\ (\text{16 W üretir})",
        ],
        exam=r"""\begin{aligned}
&\text{KCL (sağ üst): } 8 + i_b = 0 \;\Rightarrow\; i_b = -8\ \text{A} \\
&\text{a) Paralel V kaynakları: KVL } -\tfrac{i_b}{4} + v_g = 0 \;\Rightarrow\; v_g = \tfrac{-8}{4} = -2\ \text{V} \\
&\text{b) } v_{8A} = v_g = -2\ \text{V},\ \text{akım + uçtan giriyor:} \\
&\quad p_{8A} = (-2)(8) = -16\ \text{W} \;\;(\text{16 W üretir}) \\
&\text{Kontrol: } p_1 + p_2 = (-2)(-8) = 16\ \text{W},\quad \textstyle\sum p = 0
\end{aligned}""",
        traps=[
            "$i_b$'nin oku <strong>sola</strong> bakıyor: $i_b = -8$ A. $+8$ alırsan $v_g = +2$ V ve 8 A kaynağı "
            "'16 W emiyor' çıkar — ikisi de yanlış.",
            "Akım kaynağının gerilimini kaynak belirlemez; paralel bağlı elemanlar belirler (burada $v_g$).",
            "Paralel gerilim kaynaklarının tek tek akımları ve güçleri belirsizdir; yalnız toplamları bulunur.",
        ],
    ),

    # ------------------------------------------------------------------ P2.2
    dict(
        id="p2-2",
        topic=4,
        code="P2.2",
        title="Seri akım kaynakları: geçerli bağlantı için $\\alpha$ ve 25 V kaynağının gücü",
        source="Çalışma Yaprağı 1 s.5",
        image="PROB_2_2_ORIG.webp",
        circuit="p2-2",
        circuit_caption="Çözüm şeması: tek göz. 25 V kaynağının − ucu üstte, $v_x$'in + ucu üstte. Mavi ok gerçek akım yönü (15 A, saatin tersi).",
        level=1,
        question=(
            "Şekildeki devre için:<br>"
            "a) Bağlantının <strong>geçerli</strong> olması için $\\alpha$ ne olmalıdır?<br>"
            "b) (a)'da bulunan $\\alpha$ değeri için 25 V kaynağına ait gücü bulunuz."
        ),
        strategy=[
            "Dört bağlantı tek bir göz oluşturuyor → hepsi seri, hepsinden aynı akım geçer.",
            "Seri akım kaynakları <strong>aynı yön ve aynı büyüklükte</strong> akım vermeli (KCL).",
            "$v_x$'i polariteden oku: $v_x$'in + ucu kaynağın − ucunda.",
            "25 V kaynağının gücü: akım + uçtan giriyor mu?",
        ],
        steps=[
            dict(
                title="$v_x$'i oku",
                body=(
                    "$v_x$'in + işareti üstte, − işareti altta. 25 V kaynağının ise − ucu üstte, + ucu altta. "
                    "Yani üst nokta alttan 25 V <em>düşük</em>."
                ),
                math=r"""v_x = v_{\text{üst}} - v_{\text{alt}} = \boxed{-25\ \text{V}}""",
            ),
            dict(
                title="Geçerlilik: sol üst köşede KCL",
                body=(
                    "Sol üst köşeye iki eleman bağlı: aşağı bakan 15 A kaynağı ve sağa bakan $\\alpha v_x$ kaynağı. "
                    "Çıkan akımlar + : 15 A aşağı çıkıyor, $\\alpha v_x$ sağa çıkıyor. "
                    "Seri iki akım kaynağının verdiği akımlar bu denklemi sağlamazsa bağlantı geçersizdir."
                ),
                math=r"""\begin{aligned}
15 + \alpha v_x &= 0 \\
15 + \alpha(-25) &= 0 \\
25\,\alpha &= 15 \\
\alpha &= \frac{15}{25} = \boxed{0.6\ \text{A/V}}
\end{aligned}""",
            ),
            dict(
                title="Akımın gerçek yönü",
                body=(
                    "$\\alpha v_x = 0.6\\cdot(-25) = -15$ A: yani üst telde 15 A <strong>sola</strong> akıyor. "
                    "Bu, 15 A kaynağının sol kolda aşağı bastığı akımla aynı: göz akımı 15 A, <strong>saatin tersi</strong> "
                    "(sol kolda aşağı, alt telde sağa, sağ kolda yukarı, üst telde sola)."
                ),
                math=r"""\alpha v_x = 0.6\cdot(-25) = -15\ \text{A} \;\Rightarrow\; 15\ \text{A (saatin tersi)}""",
            ),
            dict(
                title="25 V kaynağının gücü (pasif işaret kuralı)",
                body=(
                    "Sağ kolda akım aşağıdan yukarı çıkıyor; kaynağın <strong>+ ucu altta</strong>. "
                    "Akım + uçtan <strong>giriyor</strong> → $p = +vi$. Sonuç pozitif: bu kaynak güç <em>emer</em> "
                    "(şarj edilen bir akü gibi)."
                ),
                math=r"""p_{25\text{V}} = +25\cdot 15 = \boxed{375\ \text{W}} \qquad (\text{emer})""",
            ),
            dict(
                title="Kontrol: $\\sum p = 0$",
                body=(
                    "Seri iki akım kaynağının gerilimlerini ayrı ayrı bulamayız (25 V'u aralarında nasıl paylaştıkları belirsiz), "
                    "ama toplam güçlerini bulabiliriz. Alt tel 0 V, sağ üst nokta $-25$ V, sol üst nokta $V_a$ (bilinmiyor) olsun.<br>"
                    "• 15 A: akım üstten girip aşağı iniyor, + üstte → $p = V_a\\cdot 15$.<br>"
                    "• $\\alpha v_x$: 15 A sağdan sola geçiyor, + ucu sağda kabul edersek akım + uçtan girer → $p = (-25 - V_a)\\cdot 15$."
                ),
                math=r"""\begin{aligned}
p_{15\text{A}} + p_{\alpha v_x} &= 15V_a + 15(-25 - V_a) \\
&= 15V_a - 375 - 15V_a = -375\ \text{W} \\[4pt]
\sum p &= -375 + 375 = \boxed{0}
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_x = -25\ \text{V}",
            r"\alpha = 0.6\ \text{A/V}",
            r"p_{25\text{V}} = +375\ \text{W}\ (\text{emer})",
        ],
        exam=r"""\begin{aligned}
&v_x = -25\ \text{V}\ (v_x\text{'in + ucu kaynağın − ucunda}) \\
&\text{a) KCL (sol üst): } 15 + \alpha v_x = 0 \;\Rightarrow\; 15 - 25\alpha = 0 \;\Rightarrow\; \alpha = 0.6\ \text{A/V} \\
&\text{Göz akımı: 15 A saatin tersi; 25 V'ta akım + (alt) uçtan giriyor} \\
&\text{b) } p_{25V} = +25\cdot 15 = 375\ \text{W}\ (\text{emer}) \\
&\text{Kontrol: } p_{15A} + p_{\alpha v_x} = 15V_a + 15(-25 - V_a) = -375\ \text{W},\ \ \textstyle\sum p = 0
\end{aligned}""",
        traps=[
            "$v_x$'in + ucu 25 V kaynağının <strong>− ucunda</strong>: $v_x = -25$ V. $+25$ alırsan $\\alpha = -0.6$ çıkar.",
            "\"Kaynak\" adı güç ürettiği anlamına gelmez: 25 V kaynağında akım + uçtan girdiği için $p = +375$ W, güç emer.",
            "Seri akım kaynaklarının tek tek gerilimleri (ve güçleri) belirsizdir; $\\sum p$ kontrolünde ikisinin toplamı kullanılır.",
        ],
    ),

    # ------------------------------------------------------------------ P2.15
    dict(
        id="p2-15",
        topic=4,
        code="P2.15",
        title="Paralel akım kaynakları ve bağımlı kaynak: $I_L$ ve güç dengesi",
        source="Çalışma Yaprağı 1 s.10",
        image="PROB_2_15_ORIG.webp",
        circuit="p2-15",
        circuit_caption="Çözüm şeması: alt ray referans (0 V), üst ray $V$. Altı eleman da paralel.",
        level=1,
        question=(
            "Şekil P2.15'teki devrede $I_L$ akımını bulunuz.<br>"
            "<em>(Soru 4 hazırlığı için ek: her elemanın gücünü bulup $\\sum p = 0$ olduğunu gösteriniz.)</em>"
        ),
        strategy=[
            "Bütün elemanlar üst ve alt ray arasında → hepsi paralel, tek bilinmeyen üst rayın gerilimi $V$.",
            "Kontrol akımını $V$ cinsinden yaz: $I_x = V/2\\ \\text{k}\\Omega$ (ek denklem).",
            "Üst rayda tek KCL → $V$; sonra $I_L = V/3\\ \\text{k}\\Omega$.",
            "Birim kolaylığı: V, mA, kΩ kullan → güçler mW çıkar.",
        ],
        steps=[
            dict(
                title="Referans ve ek denklem",
                body=(
                    "Alt rayı 0 V seçelim, üst rayın gerilimi $V$ olsun. kΩ ve mA ile çalışınca V/kΩ = mA olur, "
                    "kesir yazmaya gerek kalmaz.<br>"
                    "$I_x$, 2 kΩ'dan yukarıdan aşağı akıyor; $I_L$, 3 kΩ'dan yukarıdan aşağı akıyor."
                ),
                math=r"""\begin{aligned}
\textbf{ek:}\quad I_x &= \frac{V}{2} \ \text{(mA)},\qquad I_L = \frac{V}{3}\ \text{(mA)}
\end{aligned}""",
            ),
            dict(
                title="Üst rayda KCL",
                body=(
                    "Çıkan akımlar +, giren akımlar −. Dirençlerden aşağı akanlar çıkan (+). "
                    "6 mA kaynağının oku <strong>yukarı</strong> → üst raya giriyor (−). "
                    "$3I_x$ ve 3 mA kaynaklarının okları <strong>aşağı</strong> → üst raydan çıkıyor (+)."
                ),
                math=r"""\begin{aligned}
\frac{V}{6} - 6 + 3I_x + 3 + \frac{V}{2} + \frac{V}{3} &= 0 \\
\frac{V}{6} - 6 + 3\cdot\frac{V}{2} + 3 + \frac{V}{2} + \frac{V}{3} &= 0 \qquad /\times 6 \\
V - 36 + 9V + 18 + 3V + 2V &= 0 \\
15V - 18 &= 0 \\
V &= \frac{18}{15} = \boxed{1.2\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="$I_x$ ve $I_L$",
                body="Ek denklemlere $V = 1.2$ V koy.",
                math=r"""\begin{aligned}
I_x &= \frac{1.2}{2} = 0.6\ \text{mA} \qquad 3I_x = 1.8\ \text{mA} \\
I_L &= \frac{1.2}{3} = \boxed{0.4\ \text{mA}}
\end{aligned}""",
            ),
            dict(
                title="Her elemanın gücü (ek)",
                body=(
                    "Hepsinin uçlarında $V = 1.2$ V var, + üstte. Akımı aşağı akan (üstten giren) elemanlarda $p = +V\\,i$; "
                    "6 mA kaynağında akım + uçtan <em>çıkıyor</em> → $p = -V\\,i$. V × mA = mW."
                ),
                math=r"""\begin{aligned}
p_{6\text{k}} &= \frac{V^2}{6} = \frac{1.44}{6} = 0.24\ \text{mW} &&\text{(emer)} \\
p_{6\text{mA}} &= -V\cdot 6 = -1.2\cdot 6 = -7.2\ \text{mW} &&\text{(üretir)} \\
p_{3I_x} &= +V\cdot 3I_x = 1.2\cdot 1.8 = 2.16\ \text{mW} &&\text{(emer)} \\
p_{3\text{mA}} &= +V\cdot 3 = 1.2\cdot 3 = 3.6\ \text{mW} &&\text{(emer)} \\
p_{2\text{k}} &= \frac{V^2}{2} = \frac{1.44}{2} = 0.72\ \text{mW} &&\text{(emer)} \\
p_{3\text{k}} &= \frac{V^2}{3} = \frac{1.44}{3} = 0.48\ \text{mW} &&\text{(emer)}
\end{aligned}""",
            ),
            dict(
                title="Güç dengesi: $\\sum p = 0$",
                body="Tek güç üreten eleman 6 mA kaynağı; geri kalan herkes (bağımlı kaynak ve 3 mA kaynağı dahil) güç emiyor.",
                math=r"""\begin{aligned}
\sum p &= 0.24 - 7.2 + 2.16 + 3.6 + 0.72 + 0.48 = \boxed{0} \\[4pt]
P_{\text{üretilen}} &= 7.2\ \text{mW} \\
P_{\text{emilen}} &= 0.24 + 2.16 + 3.6 + 0.72 + 0.48 = 7.2\ \text{mW}
\end{aligned}""",
            ),
        ],
        answer=[
            r"V = 1.2\ \text{V}",
            r"I_x = 0.6\ \text{mA}",
            r"I_L = 0.4\ \text{mA}",
            r"P_{\text{üretilen}} = P_{\text{emilen}} = 7.2\ \text{mW}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } I_x = V/2,\quad I_L = V/3 \quad (\text{V, mA, k}\Omega) \\
&\text{KCL (üst ray): } \tfrac{V}{6} - 6 + 3\tfrac{V}{2} + 3 + \tfrac{V}{2} + \tfrac{V}{3} = 0 \;\;/\times 6 \\
&V - 36 + 9V + 18 + 3V + 2V = 0 \;\Rightarrow\; 15V = 18 \;\Rightarrow\; V = 1.2\ \text{V} \\
&I_x = 0.6\ \text{mA},\qquad I_L = 1.2/3 = 0.4\ \text{mA} \\[2pt]
&p:\ 0.24,\ -7.2,\ 2.16,\ 3.6,\ 0.72,\ 0.48\ \text{mW} \;\Rightarrow\; \textstyle\sum p = 0
\end{aligned}""",
        traps=[
            "Okun yönü KCL işaretini belirler: aşağı bakan $3I_x$ ve 3 mA <strong>çıkan</strong> (+), yukarı bakan 6 mA <strong>giren</strong> (−).",
            "$3I_x$'i KCL'ye koymadan önce $I_x = V/2$ ek denklemini yaz; $3V$ yazmak sık yapılan hata.",
            "kΩ ve mA ile çalışınca güç birimi <strong>mW</strong> olur, W değil.",
        ],
    ),

    # ------------------------------------------------------------------ P2.18
    dict(
        id="p2-18",
        topic=4,
        code="P2.18",
        title="Tek gözlü devrede bağımlı gerilim kaynağı: 5 Ω'un gücü",
        source="Çalışma Yaprağı 1 s.10",
        image="PROB_2_18_ORIG.webp",
        circuit="p2-18",
        circuit_caption="Çözüm şeması: göz akımı $i$ saat yönünde (alt telde sola). $3V_o$ kaynağının + ucu altta.",
        level=1,
        question=(
            "Şekil 2.82'deki devrede 5 Ω'luk dirençte harcanan gücü hesaplayınız.<br>"
            "<em>(Ek: tüm elemanların güçleriyle $\\sum p = 0$ kontrolü yapınız.)</em>"
        ),
        strategy=[
            "Tek göz → tek akım $i$ (saat yönü seçelim).",
            "Kontrol değişkeni: $V_o = 1\\cdot i$ (akım 1 Ω'a + uçtan giriyor).",
            "KVL → $i$; sonra $P_{5\\Omega} = i^2\\cdot 5$.",
            "Kaynakların gücü pasif işaret kuralıyla, ardından $\\sum p = 0$.",
        ],
        steps=[
            dict(
                title="Göz akımı ve ek denklem",
                body=(
                    "Saat yönünde $i$: 45 V'tan yukarı, 1 Ω'dan sağa, $3V_o$'dan aşağı, 5 Ω'dan sola. "
                    "1 Ω'da akım soldan sağa akıyor ve $V_o$'nun + ucu solda: akım + uçtan giriyor, Ohm yasası doğrudan uygulanır."
                ),
                math=r"""\textbf{ek:}\quad V_o = 1\cdot i = i""",
            ),
            dict(
                title="KVL (saat yönü)",
                body=(
                    "Sol alttan başla. 45 V'ta önce <em>−</em> → $-45$. 1 Ω'da önce + → $+V_o$. "
                    "$3V_o$ kaynağına üstten giriyoruz, üst uç <em>−</em> → $-3V_o$. "
                    "5 Ω'da akımla aynı yönde (sağdan sola) gidiyoruz, önce + → $+5i$."
                ),
                math=r"""\begin{aligned}
-45 + V_o - 3V_o + 5i &= 0 \\
-45 + i - 3i + 5i &= 0 \\
3i &= 45 \\
\boxed{i = 15\ \text{A}} &\qquad V_o = 15\ \text{V},\quad 3V_o = 45\ \text{V}
\end{aligned}""",
            ),
            dict(
                title="5 Ω'da harcanan güç",
                body="Dirençte akım her zaman + uçtan girer, güç her zaman pozitiftir.",
                math=r"""P_{5\Omega} = i^2\cdot 5 = 15^2\cdot 5 = 225\cdot 5 = \boxed{1125\ \text{W}}""",
            ),
            dict(
                title="Tüm elemanların gücü (pasif işaret kuralı)",
                body=(
                    "• 45 V: akım + (üst) uçtan <em>çıkıyor</em> → $p = -45\\,i$.<br>"
                    "• $3V_o$: akım − (üst) uçtan girip + (alt) uçtan <em>çıkıyor</em> → $p = -(3V_o)\\,i$. "
                    "Bu bağımlı kaynak da güç üretiyor."
                ),
                math=r"""\begin{aligned}
p_{45\text{V}} &= -45\cdot 15 = -675\ \text{W} &&\text{(üretir)} \\
p_{1\Omega} &= 15^2\cdot 1 = 225\ \text{W} &&\text{(emer)} \\
p_{3V_o} &= -45\cdot 15 = -675\ \text{W} &&\text{(üretir)} \\
p_{5\Omega} &= 15^2\cdot 5 = 1125\ \text{W} &&\text{(emer)}
\end{aligned}""",
            ),
            dict(
                title="Güç dengesi: $\\sum p = 0$",
                body="İki kaynağın ürettiği toplam güç, iki direncin harcadığı toplam güce eşit olmalı.",
                math=r"""\begin{aligned}
\sum p &= -675 + 225 - 675 + 1125 = \boxed{0} \\[4pt]
P_{\text{üretilen}} &= 675 + 675 = 1350\ \text{W} = P_{\text{harcanan}} = 225 + 1125
\end{aligned}""",
            ),
        ],
        answer=[
            r"i = 15\ \text{A}",
            r"V_o = 15\ \text{V}",
            r"P_{5\Omega} = 1125\ \text{W} = 1.125\ \text{kW}",
        ],
        exam=r"""\begin{aligned}
&i \text{ saat yönü, ek: } V_o = 1\cdot i \\
&\text{KVL: } -45 + V_o - 3V_o + 5i = 0 \;\Rightarrow\; -45 + 3i = 0 \;\Rightarrow\; i = 15\ \text{A} \\
&P_{5\Omega} = 15^2\cdot 5 = 1125\ \text{W} \\[2pt]
&p_{45V} = -675\ \text{W},\ p_{1\Omega} = 225\ \text{W},\ p_{3V_o} = -675\ \text{W},\ p_{5\Omega} = 1125\ \text{W} \\
&\textstyle\sum p = -675 + 225 - 675 + 1125 = 0
\end{aligned}""",
        traps=[
            "$3V_o$ kaynağının <strong>+ ucu altta</strong>: saat yönünde dolaşırken önce − ile karşılaşırsın → $-3V_o$. "
            "$+3V_o$ yazarsan $7i = 45$ çıkar, yanlış.",
            "Bağımlı kaynak burada 45 V kaynağı kadar (675 W) güç üretiyor; 'bağımlı kaynak güç üretmez' diye bir kural yok.",
            "$V_o$'nun işareti akım yönüyle tutarlı olmalı: + uç solda ve akım soldan giriyorsa $V_o = +1\\cdot i$.",
        ],
    ),
]
