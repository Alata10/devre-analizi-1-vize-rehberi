# -*- coding: utf-8 -*-
"""
SORU 3 (A) — Bağımlı kaynaklı düğüm gerilimleri: Çalışma Yaprağı 2 devreleri.
İçerik şeması için bkz. build/CONTENT_SPEC.md
Doğrulama: build/verify/q3a_verify.py
"""
from circuitkit import elm, ACCENT, NODE


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
def draw_cy2_s2_d1(d):
    I = d.add(elm.SourceI().up().label('3 A', loc='top'))
    d.add(elm.Line().right(d.unit * 0.9))
    d.add(elm.Dot().label('$v_o$', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down().label('200 Ω', loc='top')
          .label(('+', '$v_o$', '−'), loc='bottom', color=ACCENT))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.pop()
    d.add(elm.Line().right(d.unit * 1.1))
    d.add(elm.Dot())
    d.push()
    d.add(elm.Resistor().down(d.unit * 0.5).label('10 Ω', loc='top'))
    d.add(elm.Dot().label('$V_x$', loc='left', color=NODE))
    d.add(elm.SourceControlledV().down(d.unit * 0.5).label('$5i_\\Delta$', loc='top'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Resistor().right().label('20 Ω')
          .label('$i_\\Delta \\rightarrow$', loc='bottom', color=ACCENT))
    d.add(elm.SourceV().down().reverse().label('80 V', loc='bottom'))
    d.add(elm.Line().left().tox(I.start))


def draw_cy2_s2_d2(d):
    V = d.add(elm.SourceV().up().label('160 V', loc='top'))
    d.add(elm.Resistor().right().label('10 Ω'))
    d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.push()
    R = d.add(elm.Resistor().down().label('100 Ω', loc='top'))
    d.add(elm.CurrentLabel(top=False, reverse=True, length=0.9, ofst=0.45).at(R)
          .label('$i_\\sigma$').color(ACCENT))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.pop()
    d.add(elm.Resistor().right().label('30 Ω'))
    d.add(elm.SourceControlledV().down().reverse().label('$150i_\\sigma$', loc='bottom'))
    d.add(elm.Resistor().left().label('20 Ω', loc='bottom'))
    d.add(elm.Line().left().tox(V.start))


def draw_cy2_s2_d3(d):
    V = d.add(elm.SourceV().up().label('50 V', loc='top'))
    d.add(elm.Resistor().right().label('500 Ω'))
    d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down().label('1 kΩ', loc='top')
          .label(('+', '$v_\\Delta$', '−'), loc='bottom', color=ACCENT))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.pop()
    d.add(elm.Resistor().right().label('2 kΩ'))
    d.add(elm.Dot().label('$V_2$', loc='top', color=NODE))
    d.push()
    d.add(elm.SourceControlledI().down().reverse().label('$v_\\Delta/750$', loc='top'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Line().right(d.unit * 1.1))
    d.add(elm.Dot())
    d.add(elm.Resistor().down().label('200 Ω', loc='top')
          .label(('+', '$v_o$', '−'), loc='bottom', color=ACCENT))
    d.add(elm.Line().left().tox(V.start))


def draw_cy2_s2_d5(d):
    V = d.add(elm.SourceV().up().label('15 V', loc='top'))
    d.add(elm.Line().right(d.unit * 0.8))
    d.add(elm.Dot().label('15 V', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down().label('33 Ω', loc='top'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Resistor().right().label('10 Ω'))
    N1 = d.add(elm.Dot().label('$V_1$', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down().label('2 Ω', loc='top')
          .label(('+', '$v_\\Delta$', '−'), loc='bottom', color=ACCENT))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.pop()
    S = d.add(elm.SourceControlledV().right().reverse().label('$5v_\\Delta$', loc='top'))
    N2 = d.add(elm.Dot().label('$V_2$', loc='top', color=NODE))
    d.push()
    d.add(elm.Resistor().down().label('20 Ω', loc='top'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Line().right(d.unit * 1.1))
    d.add(elm.Resistor().down().label('40 Ω', loc='top')
          .label(('+', '$v_o$', '−'), loc='bottom', color=ACCENT))
    d.add(elm.Line().left().tox(V.start))
    d.add(elm.EncircleBox([N1, S, N2], padx=0.35, pady=0.55)
          .linestyle('--').color(ACCENT))


def draw_cy2_s1_d6(d):
    I = d.add(elm.SourceI().up().label('3 mA', loc='top'))
    N1 = d.add(elm.Dot().label('$v_1$', loc='left', color=NODE))
    d.add(elm.Line().up(d.unit * 0.8))
    d.add(elm.Resistor().right(d.unit * 2).label('4 kΩ'))
    d.add(elm.Line().down(d.unit * 0.8))
    N2 = d.add(elm.Dot().label('$v_2$', loc='right', color=NODE))
    d.add(elm.Resistor().down().label('1 kΩ', loc='bottom')
          .label(('+', '$v_o$', '−'), loc='top', color=ACCENT))
    G = d.add(elm.Dot())
    d.add(elm.Ground().at(G.center))
    d.add(elm.Line().left().tox(I.start))
    d.add(elm.Resistor().at(N1.center).right().label('2 kΩ'))
    d.add(elm.Dot().label('$v_x$', loc='bottom', color=NODE))
    d.add(elm.SourceControlledV().right().to(N2.center).label('$3v_o$', loc='top'))


CIRCUITS = {
    "cy2-s2-d1": draw_cy2_s2_d1,
    "cy2-s2-d2": draw_cy2_s2_d2,
    "cy2-s2-d3": draw_cy2_s2_d3,
    "cy2-s2-d5": draw_cy2_s2_d5,
    "cy2-s1-d6": draw_cy2_s1_d6,
}


# ---------------------------------------------------------------------------
# PROBLEMLER
# ---------------------------------------------------------------------------
PROBLEMS = [
    # =======================================================================
    # 1) ÇY2 s.2 · 1
    # =======================================================================
    dict(
        id="cy2-s2-d1",
        topic=3,
        code="ÇY2 · s.2 · 1",
        title=r"Tek bilinmeyenli düğüm: $v_o$ ve $5i_\Delta$ kaynağının gücü",
        source="Çalışma Yaprağı 2 s.2",
        image="CY2_S2_D1_ORIG.webp",
        circuit="cy2-s2-d1",
        circuit_caption=r"Çözüm şeması: alt tel referans (0 V); üst düğüm $v_o$; 10 Ω ile bağımlı kaynak arasındaki nokta $V_x$.",
        level=2,
        question=(
            r"Şekildeki devrede <strong>(a)</strong> düğüm gerilimi yöntemiyle $v_o$'yu bulunuz. "
            r"<strong>(b)</strong> Bağımlı kaynağın ($5i_\Delta$) emdiği gücü bulunuz. "
            r"<strong>(c)</strong> Bağımsız kaynakların ürettiği toplam gücü bulunuz ve $\sum p = 0$ sağlamasını yapınız."
        ),
        strategy=[
            r"Alt teli referans (0 V) seç. Üst tel tek parça → tek bilinmeyen: $v_o$. 80 V kaynağın üst ucu zaten 80 V.",
            r"Kontrol değişkeni $i_\Delta$'yı ve 10 Ω'un alt ucunu ($V_x$) $v_o$ cinsinden yaz (ek denklemler).",
            r"$v_o$ düğümünde KCL yaz, tek denklemi çöz.",
            r"Kol akımlarını bul; pasif işaret kuralıyla güç tablosu yap, $\sum p = 0$ kontrol et.",
        ],
        steps=[
            dict(
                title="Referans, bilinen gerilimler ve ek denklemler",
                body=(
                    r"Alt teli referans (0 V) alalım. Üstteki uzun tel tek bir düğümdür ve gerilimi tam olarak "
                    r"200 Ω'un üstündeki $v_o$'dur — yani bilinmeyenimiz doğrudan $v_o$.<br>"
                    r"• 80 V kaynağın + ucu üstte, alt ucu referansta → 20 Ω'un sağ ucu <strong>80 V</strong> (bilinen).<br>"
                    r"• $i_\Delta$: ok <strong>sağa</strong> bakıyor, akım $v_o$'dan 80 V'a gidiyor. Akım = (çıktığı düğüm − girdiği düğüm)/R.<br>"
                    r"• Bağımlı kaynağın <em>+</em> ucu <strong>altta</strong> (0 V), <em>−</em> ucu üstte ($V_x$). "
                    r"Kaynak gerilimi her zaman (+ uç) − (− uç) olduğundan $0 - V_x = 5i_\Delta$."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad i_\Delta &= \frac{v_o - 80}{20} \\
\textbf{ek 2:}\quad 0 - V_x &= 5i_\Delta \;\Rightarrow\; V_x = -5i_\Delta
\end{aligned}""",
                note="10 Ω ile bağımlı kaynak seri; aradaki $V_x$ noktası esas düğüm değil, bu yüzden ayrı KCL yazmaya gerek yok.",
            ),
            dict(
                title="$v_o$ düğümünde KCL",
                body=(
                    r"Düğümden <strong>çıkan</strong> akımlar +, <strong>giren</strong> akımlar −. "
                    r"3 A kaynağın oku yukarı, akımı düğüme <em>sokuyor</em> → $-3$. "
                    r"200 Ω'dan aşağı $v_o/200$; 10 Ω'dan aşağı $(v_o - V_x)/10 = (v_o + 5i_\Delta)/10$; "
                    r"20 Ω'dan sağa $i_\Delta = (v_o - 80)/20$ çıkar."
                ),
                math=r"""\begin{aligned}
-3 + \frac{v_o}{200} + \frac{v_o + 5i_\Delta}{10} + \frac{v_o - 80}{20} &= 0 \qquad /\times 200 \\
-600 + v_o + 20(v_o + 5i_\Delta) + 10(v_o - 80) &= 0 \\
-600 + v_o + 20v_o + 100i_\Delta + 10v_o - 800 &= 0 \\
100i_\Delta = 100\cdot\frac{v_o - 80}{20} &= 5v_o - 400 \qquad (\text{ek 1'den}) \\
-600 + v_o + 20v_o + 5v_o - 400 + 10v_o - 800 &= 0 \\
36v_o - 1800 &= 0 \\
v_o = \frac{1800}{36} &= \boxed{50\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="Kontrol değişkeni ve kol akımları",
                body=(
                    r"$v_o$'yu ek denklemlere geri koyup her koldaki akımı buluruz. "
                    r"Sonunda KCL'yi sayılarla kontrol etmek, işaret hatasını hemen yakalar."
                ),
                math=r"""\begin{aligned}
i_\Delta &= \frac{50 - 80}{20} = -1.5\ \text{A} \quad (\text{yani 1.5 A sağdan sola}) \\
V_x &= -5(-1.5) = 7.5\ \text{V} \\
i_{10\Omega,\downarrow} &= \frac{50 - 7.5}{10} = 4.25\ \text{A} \\
i_{200\Omega,\downarrow} &= \frac{50}{200} = 0.25\ \text{A} \\[4pt]
\text{kontrol: }\ 0.25 + 4.25 + (-1.5) &= 3\ \text{A} \;\checkmark
\end{aligned}""",
            ),
            dict(
                title=r"(b) Bağımlı kaynağın gücü",
                body=(
                    r"Kaynak gerilimi $5i_\Delta = 5(-1.5) = -7.5$ V (+ ucu altta). 10 Ω'dan gelen 4.25 A kaynağın içinden "
                    r"<strong>aşağı</strong> akıyor: üstteki − uçtan girip alttaki + uçtan çıkıyor. "
                    r"Pasif işaret kuralında + uçtan giren akımı kullanırız: $i_{+} = -4.25$ A."
                ),
                math=r"""\begin{aligned}
p_{5i_\Delta} &= (5i_\Delta)\cdot i_{+} \\
&= (-7.5)\cdot(-4.25) \\
&= \boxed{+31.875\ \text{W}} \quad (\text{pozitif} \Rightarrow \text{güç emer})
\end{aligned}""",
                note="Gerilim de akım da 'ters' çıktı; iki eksi birbirini götürür ve kaynak güç emer.",
            ),
            dict(
                title=r"(c) Güç tablosu ve $\sum p = 0$",
                body=(
                    r"• 3 A kaynak: akım üstteki + uçtan <em>çıkıyor</em> → $p = -v_o\cdot 3$.<br>"
                    r"• 80 V kaynak: $i_\Delta$ şekilde + uca (üste) giriyor → $p = +80\cdot i_\Delta$.<br>"
                    r"• Dirençler her zaman $p = i^2R$ veya $v^2/R$ (daima pozitif)."
                ),
                math=r"""\begin{aligned}
p_{3\text{A}} &= -50\cdot 3 = -150\ \text{W} \\
p_{80\text{V}} &= 80\cdot(-1.5) = -120\ \text{W} \\
p_{200\Omega} &= \frac{50^2}{200} = 12.5\ \text{W} \\
p_{10\Omega} &= 4.25^2\cdot 10 = 180.625\ \text{W} \\
p_{20\Omega} &= (-1.5)^2\cdot 20 = 45\ \text{W} \\
p_{5i_\Delta} &= 31.875\ \text{W} \\[4pt]
\sum p &= -150 - 120 + 12.5 + 180.625 + 45 + 31.875 = 0 \;\checkmark \\[4pt]
P_{\text{bağımsız, üretilen}} &= 150 + 120 = \boxed{270\ \text{W}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_o = 50\ \text{V}",
            r"i_\Delta = -1.5\ \text{A}",
            r"p_{5i_\Delta} = 31.875\ \text{W (emer)}",
            r"P_{\text{bağımsız}} = 270\ \text{W (üretilen)}",
        ],
        exam=r"""\begin{aligned}
&\text{ek 1: } i_\Delta = \tfrac{v_o - 80}{20}, \qquad \text{ek 2: } V_x = -5i_\Delta \\[2pt]
&v_o:\ -3 + \tfrac{v_o}{200} + \tfrac{v_o + 5i_\Delta}{10} + \tfrac{v_o - 80}{20} = 0 \quad /\times 200 \\
&-600 + v_o + 20v_o + 5v_o - 400 + 10v_o - 800 = 0 \;\Rightarrow\; 36v_o = 1800 \;\Rightarrow\; v_o = 50\ \text{V} \\[2pt]
&i_\Delta = -1.5\ \text{A},\quad V_x = 7.5\ \text{V},\quad i_{10\Omega} = 4.25\ \text{A} \downarrow \\
&p_{5i_\Delta} = (-7.5)(-4.25) = 31.875\ \text{W (emer)} \\
&p_{3A} = -150\ \text{W},\ p_{80V} = -120\ \text{W} \;\Rightarrow\; P_{\text{üretilen}} = 270\ \text{W} \\
&\sum p = -150 - 120 + 12.5 + 180.625 + 45 + 31.875 = 0
\end{aligned}""",
        traps=[
            r"Bağımlı kaynağın <strong>+ ucu altta</strong>: 10 Ω'un alt ucu $V_x = -5i_\Delta$ olur, $+5i_\Delta$ değil.",
            r"3 A kaynağı akımı düğüme <em>sokuyor</em>; KCL'de (çıkan + kuralıyla) $-3$ yazılır.",
            r"Güçte akımın hangi uçtan girdiğine bak: 4.25 A bağımlı kaynağa − uçtan giriyor, yani $i_{+} = -4.25$ A.",
            r"$i_\Delta$ negatif çıktı: akım aslında 80 V kaynağın + ucundan <em>çıkıyor</em>, bu yüzden 80 V kaynak 120 W üretir.",
        ],
    ),

    # =======================================================================
    # 2) ÇY2 s.2 · 2
    # =======================================================================
    dict(
        id="cy2-s2-d2",
        topic=3,
        code="ÇY2 · s.2 · 2",
        title=r"Seri kollu tek düğüm: $i_\sigma$ ve $150i_\sigma$ kaynağının gücü",
        source="Çalışma Yaprağı 2 s.2",
        image="CY2_S2_D2_ORIG.webp",
        circuit="cy2-s2-d2",
        circuit_caption=r"Çözüm şeması: 100 Ω'un alt ucu referans (0 V); tek esas düğüm $V_1$. 30 Ω, $150i_\sigma$ ve 20 Ω seri bir koldur.",
        level=2,
        question=(
            r"Şekildeki devrede düğüm gerilimi yöntemiyle $i_\sigma$'yı bulunuz. "
            r"Bağımlı gerilim kaynağının ($150i_\sigma$) gücünü hesaplayınız (emiyor mu, üretiyor mu?) "
            r"ve tüm elemanlar için $\sum p = 0$ sağlamasını yapınız."
        ),
        strategy=[
            r"100 Ω'un alt ucunu referans al; 160 V kaynağın üst ucu 160 V olur.",
            r"30 Ω, $150i_\sigma$ ve 20 Ω <strong>seri</strong> → aynı akım; aradaki noktalar esas düğüm değil. Tek bilinmeyen $V_1$.",
            r"Ek denklem: $i_\sigma$'yı $V_1$ cinsinden yaz (ok yukarı!).",
            r"Seri kolun akımını KVL ile $V_1$ cinsinden bul, $V_1$'de KCL yaz.",
            r"Akımlar → güç tablosu → $\sum p = 0$.",
        ],
        steps=[
            dict(
                title="Referans, esas düğüm ve ek denklem",
                body=(
                    r"Alt tel (100 Ω'un alt ucu ve 160 V'un − ucu) referans: 0 V. 160 V kaynağın üst ucu 160 V'tur.<br>"
                    r"Sağdaki 30 Ω → $150i_\sigma$ → 20 Ω yolu dallanmadan devam eder; aynı akım $i_k$ hepsinden geçer. "
                    r"Bu yüzden tek esas bilinmeyen düğüm $V_1$'dir.<br>"
                    r"$i_\sigma$'nın oku 100 Ω üzerinde <strong>yukarı</strong>: akım alttan (0 V) üste ($V_1$) gidiyor."
                ),
                math=r"""\begin{aligned}
\textbf{ek:}\quad i_\sigma = \frac{0 - V_1}{100} = -\frac{V_1}{100}
\end{aligned}""",
            ),
            dict(
                title="Seri kolun akımı $i_k$ (KVL ile)",
                body=(
                    r"$i_k$, $V_1$'den sağa çıkıp 30 Ω, kaynak ve 20 Ω üzerinden referansa dönen akım olsun. "
                    r"$V_1$'den başlayıp gerilim düşümlerini çıkararak 0 V'a ulaşırız. Kaynağa üstteki + uçtan girdiğimiz için "
                    r"gerilim $150i_\sigma$ kadar <em>düşer</em>."
                ),
                math=r"""\begin{aligned}
V_1 - 30i_k - 150i_\sigma - 20i_k &= 0 \\
i_k &= \frac{V_1 - 150i_\sigma}{50} \\
150i_\sigma = 150\cdot\left(-\frac{V_1}{100}\right) &= -1.5V_1 \\
i_k = \frac{V_1 + 1.5V_1}{50} = \frac{2.5V_1}{50} &= \frac{V_1}{20}
\end{aligned}""",
                note="Seri dirençleri kaynakla birlikte tek kol gibi düşün: 30 + 20 = 50 Ω ve araya bir gerilim kaynağı.",
            ),
            dict(
                title="$V_1$ düğümünde KCL",
                body=(
                    r"Çıkan akımlar +: 10 Ω'dan sola $(V_1 - 160)/10$, 100 Ω'dan aşağı $V_1/100$, sağ koldan $i_k = V_1/20$."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - 160}{10} + \frac{V_1}{100} + \frac{V_1}{20} &= 0 \qquad /\times 100 \\
10(V_1 - 160) + V_1 + 5V_1 &= 0 \\
10V_1 - 1600 + V_1 + 5V_1 &= 0 \\
16V_1 &= 1600 \\
V_1 &= \boxed{100\ \text{V}}
\end{aligned}""",
                note=r"100 Ω'un akımını KCL'de 'çıkan' yönde $V_1/100$ yazdık. $i_\sigma$ yukarı tanımlı olduğu için $i_\sigma = -V_1/100$ — ikisini karıştırma.",
            ),
            dict(
                title=r"$i_\sigma$ ve diğer akımlar",
                body=r"Bulduğumuz $V_1$'i yerine koyalım ve KCL'yi sayılarla kontrol edelim.",
                math=r"""\begin{aligned}
i_\sigma &= -\frac{100}{100} = \boxed{-1\ \text{A}} \quad (\text{yani 1 A aşağı}) \\
150i_\sigma &= -150\ \text{V} \\
i_k &= \frac{100}{20} = 5\ \text{A} \\
i_{10\Omega} &= \frac{160 - 100}{10} = 6\ \text{A} \quad (\text{sağa}) \\[4pt]
\text{kontrol: }\ 6 &= 1 + 5 \;\checkmark \\
V_{\text{sağ üst}} = 100 - 30\cdot 5 = -50\ \text{V}, &\quad V_{\text{sağ alt}} = 20\cdot 5 = 100\ \text{V} \\
-50 - 100 &= -150 = 150i_\sigma \;\checkmark
\end{aligned}""",
            ),
            dict(
                title=r"Bağımlı kaynağın gücü",
                body=(
                    r"$i_k = 5$ A kaynağın içinden <strong>yukarıdan aşağı</strong> akıyor, yani + uçtan giriyor. "
                    r"Pasif işaret kuralı: $p = v\cdot i_{+}$."
                ),
                math=r"""\begin{aligned}
p_{150i_\sigma} &= (150i_\sigma)\cdot i_k \\
&= (-150)\cdot 5 \\
&= \boxed{-750\ \text{W}} \quad (\text{negatif} \Rightarrow 750\ \text{W üretir})
\end{aligned}""",
            ),
            dict(
                title=r"Güç tablosu ve $\sum p = 0$",
                body=r"160 V kaynakta 6 A akım + uçtan <em>çıkıyor</em> → $p = -160\cdot 6$. Dirençler $i^2R$.",
                math=r"""\begin{aligned}
p_{160\text{V}} &= -160\cdot 6 = -960\ \text{W} \\
p_{10\Omega} &= 6^2\cdot 10 = 360\ \text{W} \\
p_{100\Omega} &= (-1)^2\cdot 100 = 100\ \text{W} \\
p_{30\Omega} &= 5^2\cdot 30 = 750\ \text{W} \\
p_{20\Omega} &= 5^2\cdot 20 = 500\ \text{W} \\
p_{150i_\sigma} &= -750\ \text{W} \\[4pt]
\sum p &= -960 + 360 + 100 + 750 + 500 - 750 = 0 \;\checkmark
\end{aligned}""",
                note="Üretilen: 960 + 750 = 1710 W. Harcanan: 360 + 100 + 750 + 500 = 1710 W.",
            ),
        ],
        answer=[
            r"V_1 = 100\ \text{V}",
            r"i_\sigma = -1\ \text{A}",
            r"p_{150i_\sigma} = -750\ \text{W (750 W üretir)}",
            r"\textstyle\sum p = 0",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } i_\sigma = -\tfrac{V_1}{100}, \qquad i_k = \tfrac{V_1 - 150i_\sigma}{50} = \tfrac{V_1 + 1.5V_1}{50} = \tfrac{V_1}{20} \\[2pt]
&V_1:\ \tfrac{V_1 - 160}{10} + \tfrac{V_1}{100} + \tfrac{V_1}{20} = 0 \quad /\times 100 \\
&10V_1 - 1600 + V_1 + 5V_1 = 0 \;\Rightarrow\; V_1 = 100\ \text{V} \\[2pt]
&i_\sigma = -1\ \text{A},\quad 150i_\sigma = -150\ \text{V},\quad i_k = 5\ \text{A},\quad i_{10\Omega} = 6\ \text{A} \\
&p_{150i_\sigma} = (-150)(5) = -750\ \text{W (üretir)} \\
&\sum p = -960 + 360 + 100 + 750 + 500 - 750 = 0
\end{aligned}""",
        traps=[
            r"$i_\sigma$'nın oku <strong>yukarı</strong>: $i_\sigma = -V_1/100$. İşareti kaçırırsan $150i_\sigma$'nın işareti ve tüm sonuç değişir.",
            r"30 Ω ile 20 Ω arasındaki noktaları ayrı bilinmeyen yapma; seri kolda tek akım vardır.",
            r"Akım + uçtan giriyor diye kaynağın güç emdiğini sanma: kaynak gerilimi $-150$ V olduğundan $p<0$, kaynak <strong>üretir</strong>.",
        ],
    ),

    # =======================================================================
    # 3) ÇY2 s.2 · 3
    # =======================================================================
    dict(
        id="cy2-s2-d3",
        topic=3,
        code="ÇY2 · s.2 · 3",
        title=r"İki düğüm, gerilim kontrollü akım kaynağı: $v_\Delta/750$",
        source="Çalışma Yaprağı 2 s.2",
        image="CY2_S2_D3_ORIG.webp",
        circuit="cy2-s2-d3",
        circuit_caption=r"Çözüm şeması: alt tel referans (0 V); $V_1 = v_\Delta$, $V_2 = v_o$.",
        level=2,
        question=(
            r"Şekildeki devrede düğüm gerilimi yöntemiyle $v_\Delta$ ve $v_o$ gerilimlerini bulunuz. "
            r"Bağımlı akım kaynağının gücünü hesaplayınız ve $\sum p = 0$ sağlamasını yapınız."
        ),
        strategy=[
            r"Alt tel referans; 50 V'un üst ucu 50 V. Bilinmeyenler $V_1$ (= $v_\Delta$) ve $V_2$ (= $v_o$).",
            r"Ek denklem: kaynak akımı $v_\Delta/750 = V_1/750$, oku yukarı → $V_2$'ye <strong>giriyor</strong>.",
            r"$V_1$ ve $V_2$'de KCL yaz; paydaları eşitle (×2000 ve ×6000).",
            r"İki denklemi çöz; akımlar → güç tablosu.",
        ],
        steps=[
            dict(
                title="Referans, bilinmeyenler ve ek denklem",
                body=(
                    r"Alt tel referans (0 V). 1 kΩ'un üstü $V_1$, 200 Ω'un üstü $V_2$.<br>"
                    r"• $v_\Delta$: 1 kΩ'un + ucu $V_1$'de, − ucu referansta → $v_\Delta = V_1$.<br>"
                    r"• $v_o$: 200 Ω'un + ucu $V_2$'de → $v_o = V_2$.<br>"
                    r"• Bağımlı kaynağın oku yukarı: $V_1/750$ akımını $V_2$ düğümüne <em>sokuyor</em>."
                ),
                math=r"""\begin{aligned}
\textbf{ek:}\quad v_\Delta = V_1, \qquad v_o = V_2, \qquad i_{\text{kaynak}} = \frac{v_\Delta}{750} = \frac{V_1}{750}
\end{aligned}""",
            ),
            dict(
                title="$V_1$ düğümünde KCL",
                body=(
                    r"Çıkan akımlar +: 500 Ω'dan sola, 1 kΩ'dan aşağı, 2 kΩ'dan sağa. "
                    r"Paydalar 500, 1000, 2000 → hepsini 2000 ile çarparız."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - 50}{500} + \frac{V_1}{1000} + \frac{V_1 - V_2}{2000} &= 0 \qquad /\times 2000 \\
4(V_1 - 50) + 2V_1 + (V_1 - V_2) &= 0 \\
4V_1 - 200 + 2V_1 + V_1 - V_2 &= 0 \\
\boxed{7V_1 - V_2 = 200} &\qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="$V_2$ düğümünde KCL",
                body=(
                    r"2 kΩ'dan sola $(V_2 - V_1)/2000$ çıkar; bağımlı kaynak $V_1/750$ akımını <em>sokar</em> → eksi; "
                    r"200 Ω'dan aşağı $V_2/200$ çıkar. 2000, 750 ve 200'ün EKOK'u 6000'dir."
                ),
                math=r"""\begin{aligned}
\frac{V_2 - V_1}{2000} - \frac{V_1}{750} + \frac{V_2}{200} &= 0 \qquad /\times 6000 \\
3(V_2 - V_1) - 8V_1 + 30V_2 &= 0 \\
3V_2 - 3V_1 - 8V_1 + 30V_2 &= 0 \\
-11V_1 + 33V_2 &= 0 \\
\boxed{V_1 = 3V_2} &\qquad \text{(II)}
\end{aligned}""",
                note="6000/2000 = 3, 6000/750 = 8, 6000/200 = 30. Katsayıları ayrı ayrı hesapla, kafadan yapma.",
            ),
            dict(
                title="Denklemleri çöz",
                body=r"(II)'yi (I)'de yerine koyarız.",
                math=r"""\begin{aligned}
7(3V_2) - V_2 &= 200 \\
21V_2 - V_2 &= 200 \\
20V_2 &= 200 \;\Rightarrow\; V_2 = 10\ \text{V} \\
V_1 &= 3\cdot 10 = 30\ \text{V} \\[4pt]
v_\Delta = V_1 = \boxed{30\ \text{V}}, &\qquad v_o = V_2 = \boxed{10\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="Kol akımları ve bağımlı kaynağın gücü",
                body=(
                    r"Bağımlı kaynağın üst ucu $V_2 = 10$ V, alt ucu 0 V; üst ucu + kabul ederiz. "
                    r"Kaynak akımı yukarı akıp <strong>+ uçtan çıkıyor</strong> → pasif işaret kuralında $p = -v\cdot i$."
                ),
                math=r"""\begin{aligned}
i_{\text{kaynak}} &= \frac{30}{750} = 0.04\ \text{A} = 40\ \text{mA} \\
i_{500\Omega} &= \frac{50 - 30}{500} = 0.04\ \text{A}, \qquad i_{1\text{k}} = \frac{30}{1000} = 0.03\ \text{A} \\
i_{2\text{k}} &= \frac{30 - 10}{2000} = 0.01\ \text{A}, \qquad i_{200\Omega} = \frac{10}{200} = 0.05\ \text{A} \\
\text{kontrol: }\ 0.04 &= 0.03 + 0.01 \;\checkmark, \qquad 0.01 + 0.04 = 0.05 \;\checkmark \\[4pt]
p_{\text{kaynak}} &= -V_2\cdot i_{\text{kaynak}} = -10\cdot 0.04 = \boxed{-0.4\ \text{W}} \quad (\text{üretir})
\end{aligned}""",
            ),
            dict(
                title=r"Güç tablosu ve $\sum p = 0$",
                body=r"50 V kaynakta 0.04 A akım + uçtan çıkıyor → $p = -50\cdot 0.04$.",
                math=r"""\begin{aligned}
p_{50\text{V}} &= -50\cdot 0.04 = -2\ \text{W} \\
p_{500\Omega} &= 0.04^2\cdot 500 = 0.8\ \text{W} \\
p_{1\text{k}} &= \frac{30^2}{1000} = 0.9\ \text{W} \\
p_{2\text{k}} &= \frac{20^2}{2000} = 0.2\ \text{W} \\
p_{200\Omega} &= \frac{10^2}{200} = 0.5\ \text{W} \\
p_{\text{kaynak}} &= -0.4\ \text{W} \\[4pt]
\sum p &= -2 + 0.8 + 0.9 + 0.2 + 0.5 - 0.4 = 0 \;\checkmark
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_\Delta = 30\ \text{V}",
            r"v_o = 10\ \text{V}",
            r"i_{\text{kaynak}} = 40\ \text{mA}",
            r"p_{\text{kaynak}} = -0.4\ \text{W (üretir)}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } v_\Delta = V_1,\ v_o = V_2 \\[2pt]
&V_1:\ \tfrac{V_1 - 50}{500} + \tfrac{V_1}{1000} + \tfrac{V_1 - V_2}{2000} = 0 \;/\times 2000 \;\Rightarrow\; 7V_1 - V_2 = 200 \\
&V_2:\ \tfrac{V_2 - V_1}{2000} - \tfrac{V_1}{750} + \tfrac{V_2}{200} = 0 \;/\times 6000 \;\Rightarrow\; -11V_1 + 33V_2 = 0 \Rightarrow V_1 = 3V_2 \\
&21V_2 - V_2 = 200 \;\Rightarrow\; V_2 = 10\ \text{V},\quad V_1 = 30\ \text{V} \\[2pt]
&v_\Delta = 30\ \text{V},\quad v_o = 10\ \text{V},\quad i_k = 30/750 = 0.04\ \text{A} \\
&p_k = -10\cdot 0.04 = -0.4\ \text{W};\quad \sum p = -2 + 0.8 + 0.9 + 0.2 + 0.5 - 0.4 = 0
\end{aligned}""",
        traps=[
            r"Kaynağın oku yukarı → akım $V_2$'ye <strong>giriyor</strong>; KCL'de $-V_1/750$ yazılır.",
            r"Kontrol değişkeni $v_\Delta$, 1 kΩ'un gerilimidir: $v_\Delta = V_1$, $V_2$ değil.",
            r"$\times 6000$ yaparken her terimin katsayısını ayrı hesapla (3, 8, 30). Bir katsayı hatası tüm sonucu bozar.",
        ],
    ),

    # =======================================================================
    # 4) ÇY2 s.2 · 5  (süperdüğüm)
    # =======================================================================
    dict(
        id="cy2-s2-d5",
        topic=3,
        code="ÇY2 · s.2 · 5",
        title=r"Süperdüğüm: iki düğüm arasında $5v_\Delta$ gerilim kaynağı",
        source="Çalışma Yaprağı 2 s.2",
        image="CY2_S2_D5_ORIG.webp",
        circuit="cy2-s2-d5",
        circuit_caption=r"Çözüm şeması: alt tel referans; $V_1 = v_\Delta$, $V_2 = v_o$. Kesikli kutu: süperdüğüm ($V_1$ + kaynak + $V_2$).",
        level=3,
        question=(
            r"Şekildeki devrede düğüm gerilimi yöntemiyle $v_o$'yu bulunuz. "
            r"Bağımlı gerilim kaynağının ($5v_\Delta$) gücünü hesaplayınız ve $\sum p = 0$ sağlamasını yapınız."
        ),
        strategy=[
            r"Alt tel referans; 15 V'un üst ucu 15 V. 33 Ω kaynağa paralel → düğüm denklemine girmez.",
            r"$V_1$ ile $V_2$ arasında <strong>yalnızca</strong> gerilim kaynağı var → ikisini tek bir <strong>süperdüğüm</strong> yap.",
            r"Kısıt denklemi: $V_1 - V_2 = 5v_\Delta$, ve $v_\Delta = V_1$.",
            r"Süperdüğümden çıkan tüm akımlar için tek KCL yaz; kısıtla birlikte çöz.",
            r"Kaynak akımını tek düğüm KCL'sinden bul → güç tablosu.",
        ],
        steps=[
            dict(
                title="Referans, bilinen düğüm ve 33 Ω",
                body=(
                    r"Alt tel referans (0 V). 15 V kaynağın + ucu üstte → sol üst düğüm <strong>15 V</strong> (bilinen).<br>"
                    r"33 Ω doğrudan bu düğüm ile referans arasında, yani 15 V kaynağa <strong>paralel</strong>: gerilimi ne olursa olsun 15 V'tur. "
                    r"$V_1$ ve $V_2$'yi hiç etkilemez; sadece 15 V kaynağın vermesi gereken akımı artırır (güç tablosunda lazım olacak).<br>"
                    r"Bilinmeyenler: $V_1$ (2 Ω'un üstü, $= v_\Delta$) ve $V_2$ (20 Ω / 40 Ω'un üstü, $= v_o$)."
                ),
                math=r"""\begin{aligned}
\textbf{ek:}\quad v_\Delta = V_1, \qquad v_o = V_2
\end{aligned}""",
            ),
            dict(
                title="Neden süperdüğüm? Kısıt denklemi",
                body=(
                    r"$V_1$'de normal KCL yazmak istesek, bağımlı kaynaktan geçen akımı yazmamız gerekir. Ama gerilim kaynağının akımı "
                    r"Ohm yasasıyla bulunamaz (direnç yok, akım her değeri alabilir). Çözüm: $V_1$, kaynak ve $V_2$'yi "
                    r"<strong>tek bir kapalı yüzeyle</strong> çevirmek (şemadaki kesikli kutu). Kaynağın akımı kutunun <em>içinde</em> kalır ve KCL'de hiç görünmez.<br>"
                    r"İki düğümü birleştirince bir denklem kaybederiz; onu kaynağın kendisi verir: <strong>kısıt denklemi</strong>. "
                    r"Kaynağın + ucu solda ($V_1$), − ucu sağda ($V_2$)."
                ),
                math=r"""\begin{aligned}
\textbf{kısıt:}\quad V_1 - V_2 &= 5v_\Delta \\
V_1 - V_2 &= 5V_1 \\
\boxed{V_2 = -4V_1} &\qquad \text{(K)}
\end{aligned}""",
            ),
            dict(
                title="Süperdüğümde KCL",
                body=(
                    r"Kutudan <strong>dışarı çıkan</strong> akımları + yazarız: 10 Ω'dan sola $(V_1 - 15)/10$, 2 Ω'dan aşağı $V_1/2$, "
                    r"20 Ω'dan aşağı $V_2/20$, 40 Ω'dan aşağı $V_2/40$. Paydalar 10, 2, 20, 40 → ×40."
                ),
                math=r"""\begin{aligned}
\frac{V_1 - 15}{10} + \frac{V_1}{2} + \frac{V_2}{20} + \frac{V_2}{40} &= 0 \qquad /\times 40 \\
4(V_1 - 15) + 20V_1 + 2V_2 + V_2 &= 0 \\
4V_1 - 60 + 20V_1 + 3V_2 &= 0 \\
\boxed{24V_1 + 3V_2 = 60} &\qquad \text{(I)}
\end{aligned}""",
                note="Süperdüğüm KCL'sinde kaynağın akımı yoktur — bu yöntemin bütün amacı budur.",
            ),
            dict(
                title="Kısıtla birlikte çöz",
                body=r"(K)'yı (I)'de yerine koyarız.",
                math=r"""\begin{aligned}
24V_1 + 3(-4V_1) &= 60 \\
24V_1 - 12V_1 &= 60 \\
12V_1 &= 60 \;\Rightarrow\; V_1 = 5\ \text{V} \\
V_2 &= -4\cdot 5 = -20\ \text{V} \\[4pt]
v_\Delta = \boxed{5\ \text{V}}, &\qquad v_o = \boxed{-20\ \text{V}} \\
\text{kontrol: }\ V_1 - V_2 = 5 - (-20) &= 25 = 5v_\Delta \;\checkmark
\end{aligned}""",
            ),
            dict(
                title="Bağımlı kaynağın akımı ve gücü",
                body=(
                    r"Kaynak akımını bulmak için şimdi <em>tek başına</em> $V_1$ düğümüne bakarız. $i_s$: kaynağın içinden soldan sağa "
                    r"(yani + uçtan giren) akım olsun. $V_1$'e 10 Ω'dan giren akım, 2 Ω'dan ve kaynaktan çıkanların toplamına eşittir."
                ),
                math=r"""\begin{aligned}
i_{10\Omega} &= \frac{15 - 5}{10} = 1\ \text{A} \quad (V_1\text{'e giren}) \\
i_{2\Omega} &= \frac{5}{2} = 2.5\ \text{A} \\
i_s &= 1 - 2.5 = -1.5\ \text{A} \quad (\text{yani 1.5 A sağdan sola}) \\
\text{kontrol: }\ \frac{-20}{20} + \frac{-20}{40} &= -1 - 0.5 = -1.5\ \text{A} \;\checkmark \\[4pt]
p_{5v_\Delta} &= (5v_\Delta)\cdot i_s = 25\cdot(-1.5) = \boxed{-37.5\ \text{W}} \quad (\text{üretir})
\end{aligned}""",
            ),
            dict(
                title=r"Güç tablosu ve $\sum p = 0$",
                body=(
                    r"15 V kaynağın akımı = 33 Ω'un akımı + 10 Ω'un akımı; bu akım + uçtan çıkar → $p<0$."
                ),
                math=r"""\begin{aligned}
i_{15\text{V}} &= \frac{15}{33} + 1 = \frac{48}{33} = \frac{16}{11} \approx 1.4545\ \text{A} \\
p_{15\text{V}} &= -15\cdot\frac{16}{11} = -\frac{240}{11} \approx -21.82\ \text{W} \\
p_{33\Omega} &= \frac{15^2}{33} = \frac{75}{11} \approx 6.82\ \text{W} \\
p_{10\Omega} &= 1^2\cdot 10 = 10\ \text{W}, \qquad p_{2\Omega} = \frac{5^2}{2} = 12.5\ \text{W} \\
p_{20\Omega} &= \frac{(-20)^2}{20} = 20\ \text{W}, \qquad p_{40\Omega} = \frac{(-20)^2}{40} = 10\ \text{W} \\
p_{5v_\Delta} &= -37.5\ \text{W} \\[4pt]
\sum p &= -\frac{240}{11} + \frac{75}{11} + 10 + 12.5 + 20 + 10 - 37.5 \\
&= -15 + 15 = 0 \;\checkmark
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_\Delta = 5\ \text{V}",
            r"v_o = -20\ \text{V}",
            r"i_s = -1.5\ \text{A}",
            r"p_{5v_\Delta} = -37.5\ \text{W (üretir)}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } v_\Delta = V_1,\ v_o = V_2 \qquad \text{kısıt: } V_1 - V_2 = 5V_1 \Rightarrow V_2 = -4V_1 \\[2pt]
&\text{SD: } \tfrac{V_1 - 15}{10} + \tfrac{V_1}{2} + \tfrac{V_2}{20} + \tfrac{V_2}{40} = 0 \;/\times 40 \;\Rightarrow\; 24V_1 + 3V_2 = 60 \\
&24V_1 - 12V_1 = 60 \;\Rightarrow\; V_1 = 5\ \text{V},\quad V_2 = -20\ \text{V} \\[2pt]
&v_o = -20\ \text{V},\quad i_s = 1 - 2.5 = -1.5\ \text{A},\quad p_{5v_\Delta} = 25(-1.5) = -37.5\ \text{W} \\
&\sum p = -\tfrac{240}{11} + \tfrac{75}{11} + 10 + 12.5 + 20 + 10 - 37.5 = 0
\end{aligned}""",
        traps=[
            r"Süperdüğüm KCL'sine kaynağın akımını <strong>yazma</strong>; ama kısıt denklemini de <strong>unutma</strong> — yoksa bir denklem eksik kalır.",
            r"Kısıtın işareti: + uç solda ($V_1$) → $V_1 - V_2 = 5v_\Delta$. Ters yazarsan $V_2 = 6V_1$ gibi yanlış bir ilişki çıkar.",
            r"33 Ω, 15 V kaynağa paralel: düğüm denklemine girmez, ama güç tablosuna <strong>girer</strong>.",
            r"$v_o$'nun negatif çıkması hata değildir; bağımlı kaynak $V_2$'yi referansın altına çekiyor.",
        ],
    ),

    # =======================================================================
    # 5) ÇY2 s.1 · 6
    # =======================================================================
    dict(
        id="cy2-s1-d6",
        topic=3,
        code="ÇY2 · s.1 · 6",
        title=r"Dirençle seri bağımlı kaynak: $v_1$, $v_2$ ve $3v_o$'nun gücü",
        source="Çalışma Yaprağı 2 s.1",
        image="CY2_S1_D6_ORIG.webp",
        circuit="cy2-s1-d6",
        circuit_caption=r"Çözüm şeması: toprak referans; esas düğümler $v_1$, $v_2$. $v_x$: 2 kΩ ile $3v_o$ arasındaki (esas olmayan) nokta.",
        level=2,
        question=(
            r"Şekildeki devrede düğüm gerilimi yöntemiyle $v_1$ ve $v_2$ düğüm gerilimlerini (dolayısıyla $v_o$'yu) bulunuz. "
            r"Tüm elemanların gücünü hesaplayıp $\sum p = 0$ olduğunu gösteriniz."
        ),
        strategy=[
            r"Toprak referans. Esas düğümler $v_1$ ve $v_2$; $v_o = v_2$.",
            r"2 kΩ ile $3v_o$ kaynağı <strong>seri</strong>: aradaki $v_x$ noktasını kaynak üzerinden $v_2$ cinsinden yaz.",
            r"Birimler: kΩ ve mA kullan (V = kΩ·mA, güç mW).",
            r"$v_1$ ve $v_2$'de KCL → iki denklem → çöz → güç tablosu.",
        ],
        steps=[
            dict(
                title="Referans ve ek denklemler",
                body=(
                    r"Alt tel toprak (0 V). Esas düğümler $v_1$ (sol) ve $v_2$ (sağ).<br>"
                    r"• $v_o$: 1 kΩ'un + ucu $v_2$'de, − ucu toprakta → $v_o = v_2$.<br>"
                    r"• Bağımlı kaynağın + ucu <strong>sağda</strong> ($v_2$'ye bağlı), − ucu solda ($v_x$). "
                    r"(+ uç) − (− uç) = kaynak gerilimi: $v_2 - v_x = 3v_o$."
                ),
                math=r"""\begin{aligned}
\textbf{ek 1:}\quad v_o &= v_2 \\
\textbf{ek 2:}\quad v_x &= v_2 - 3v_o = v_2 - 3v_2 = -2v_2
\end{aligned}""",
                note=r"Kaynak $v_1$–$v_2$ arasında tek başına değil, 2 kΩ ile seri; bu yüzden süperdüğüm gerekmez. 2 kΩ'un akımını $(v_1 - v_x)/2$ ile yazarız.",
            ),
            dict(
                title="Orta kolun akımı",
                body=(
                    r"Orta koldan $v_1$'den $v_2$'ye akan akım, 2 kΩ'un akımıdır: (sol uç − sağ uç)/R. "
                    r"2 kΩ'un sağ ucu $v_2$ <strong>değil</strong>, $v_x$'tir."
                ),
                math=r"""\begin{aligned}
i_m &= \frac{v_1 - v_x}{2} = \frac{v_1 - (-2v_2)}{2} = \frac{v_1 + 2v_2}{2}\ \text{mA}
\end{aligned}""",
            ),
            dict(
                title="$v_1$ düğümünde KCL",
                body=(
                    r"Çıkan +, giren −. 3 mA kaynağı akımı $v_1$'e <em>sokuyor</em> → $-3$. 4 kΩ'dan $v_2$'ye $(v_1 - v_2)/4$, "
                    r"orta koldan $i_m$ çıkar."
                ),
                math=r"""\begin{aligned}
-3 + \frac{v_1 - v_2}{4} + \frac{v_1 + 2v_2}{2} &= 0 \qquad /\times 4 \\
-12 + (v_1 - v_2) + 2(v_1 + 2v_2) &= 0 \\
-12 + v_1 - v_2 + 2v_1 + 4v_2 &= 0 \\
3v_1 + 3v_2 &= 12 \\
\boxed{v_1 + v_2 = 4} &\qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="$v_2$ düğümünde KCL",
                body=(
                    r"4 kΩ'dan $(v_2 - v_1)/4$ çıkar. Orta kolun akımı $i_m$ $v_2$'ye <em>giriyor</em> → $-i_m$. "
                    r"1 kΩ'dan toprağa $v_2/1$ çıkar."
                ),
                math=r"""\begin{aligned}
\frac{v_2 - v_1}{4} - \frac{v_1 + 2v_2}{2} + \frac{v_2}{1} &= 0 \qquad /\times 4 \\
(v_2 - v_1) - 2(v_1 + 2v_2) + 4v_2 &= 0 \\
v_2 - v_1 - 2v_1 - 4v_2 + 4v_2 &= 0 \\
-3v_1 + v_2 &= 0 \\
\boxed{v_2 = 3v_1} &\qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="Denklemleri çöz",
                body=r"(II)'yi (I)'de yerine koy.",
                math=r"""\begin{aligned}
v_1 + 3v_1 &= 4 \;\Rightarrow\; 4v_1 = 4 \\
v_1 &= \boxed{1\ \text{V}} \\
v_2 &= 3\cdot 1 = \boxed{3\ \text{V}} = v_o \\
v_x &= -2\cdot 3 = -6\ \text{V}
\end{aligned}""",
                note=r"Hızlı sağlama: 3 mA'nın tamamı sonunda 1 kΩ üzerinden toprağa döner, yani $v_2 = 3\ \text{mA}\cdot 1\ \text{k}\Omega = 3$ V. Tutuyor.",
            ),
            dict(
                title="Kol akımları",
                body=r"Her kolun akımını hesaplayıp $v_1$'de KCL'yi sayılarla kontrol edelim.",
                math=r"""\begin{aligned}
i_{4\text{k}} &= \frac{1 - 3}{4} = -0.5\ \text{mA} \quad (\text{yani 0.5 mA } v_2\text{'den } v_1\text{'e}) \\
i_m &= \frac{1 + 2\cdot 3}{2} = 3.5\ \text{mA} \quad (v_1 \rightarrow v_2) \\
i_{1\text{k}} &= \frac{3}{1} = 3\ \text{mA} \\[4pt]
\text{kontrol: }\ -0.5 + 3.5 &= 3\ \text{mA} \;\checkmark
\end{aligned}""",
            ),
            dict(
                title=r"Güç tablosu ve $\sum p = 0$",
                body=(
                    r"• 3 mA kaynak: akım üstten ($v_1$, + uç) çıkıyor → $p = -1\cdot 3$.<br>"
                    r"• $3v_o = 9$ V kaynak: $i_m = 3.5$ mA soldan sağa akıyor; − uçtan girip + uçtan <em>çıkıyor</em> → $p = -9\cdot 3.5$.<br>"
                    r"• V·mA = mW."
                ),
                math=r"""\begin{aligned}
p_{3\text{mA}} &= -1\cdot 3 = -3\ \text{mW} \\
p_{4\text{k}} &= \frac{(1 - 3)^2}{4} = 1\ \text{mW} \\
p_{2\text{k}} &= 3.5^2\cdot 2 = 24.5\ \text{mW} \\
p_{3v_o} &= -9\cdot 3.5 = -31.5\ \text{mW} \\
p_{1\text{k}} &= \frac{3^2}{1} = 9\ \text{mW} \\[4pt]
\sum p &= -3 + 1 + 24.5 - 31.5 + 9 = 0 \;\checkmark
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_1 = 1\ \text{V}",
            r"v_2 = v_o = 3\ \text{V}",
            r"p_{3v_o} = -31.5\ \text{mW (üretir)}",
            r"p_{3\text{mA}} = -3\ \text{mW (üretir)}",
        ],
        exam=r"""\begin{aligned}
&\text{ek: } v_o = v_2,\quad v_x = v_2 - 3v_o = -2v_2,\quad i_m = \tfrac{v_1 + 2v_2}{2}\ \text{mA} \\[2pt]
&v_1:\ -3 + \tfrac{v_1 - v_2}{4} + \tfrac{v_1 + 2v_2}{2} = 0 \;/\times 4 \;\Rightarrow\; v_1 + v_2 = 4 \\
&v_2:\ \tfrac{v_2 - v_1}{4} - \tfrac{v_1 + 2v_2}{2} + v_2 = 0 \;/\times 4 \;\Rightarrow\; -3v_1 + v_2 = 0 \\
&v_1 = 1\ \text{V},\quad v_2 = v_o = 3\ \text{V},\quad i_m = 3.5\ \text{mA},\quad i_{4k} = -0.5\ \text{mA} \\[2pt]
&\sum p = -3 + 1 + 24.5 - 31.5 + 9 = 0\ \text{mW}
\end{aligned}""",
        traps=[
            r"2 kΩ'un akımını $(v_1 - v_2)/2$ yazmak en sık hatadır; sağ ucu $v_x = v_2 - 3v_o$'dır.",
            r"Kaynağın + ucu <strong>sağda</strong>: $v_x = v_2 - 3v_o$. + ucu solda sanırsan $v_x = v_2 + 3v_o$ olur ve sonuç değişir.",
            r"Birimleri karıştırma: kΩ ile mA kullanıyorsan gerilim V, güç mW çıkar.",
        ],
    ),
]
