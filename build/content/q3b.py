# -*- coding: utf-8 -*-
"""
SORU 3 (b) — Bağımlı kaynaklı çevre akımları, süperçevre ve düğüm gerilimleri analizi.
Problemler: P4.42, P4.48, P4.52, P4.53, ÇY2 s.2 d.4.
İçerik şeması için bkz. build/CONTENT_SPEC.md ; doğrulama: build/verify/q3b_verify.py
"""
from circuitkit import elm, ACCENT, NODE


def _w(d, a, b):
    d.add(elm.Line().at(a).to(b))


def _dot(d, p, **kw):
    return d.add(elm.Dot(**kw).at(p))


def _cur(d, el, text, top=True, reverse=False, ofst=0.45, length=1.2):
    return d.add(elm.CurrentLabel(top=top, ofst=ofst, length=length, reverse=reverse)
                 .at(el).label(text, color=ACCENT).color(ACCENT))


def _mesh(d, pos, text):
    d.add(elm.LoopArrow(direction='cw', width=1.1, height=1.1).at(pos)
          .label(text, color=NODE).color(NODE))


# ---------------------------------------------------------------------------
# DEVRE ŞEMALARI
# ---------------------------------------------------------------------------
def draw_p4_42(d):
    # Alt-sol göz i1, alt-sağ göz i2, üst göz i3
    d.add(elm.SourceV().at((0, 0)).up(3.2).label('30 V', loc='top'))
    _dot(d, (0, 3.2))
    d.add(elm.Resistor().at((0, 3.2)).right(4).label('3 Ω', loc='top'))
    _dot(d, (4, 3.2))
    d.add(elm.Resistor().at((4, 3.2)).right(4).label('5 Ω', loc='top'))
    _dot(d, (8, 3.2))
    d.add(elm.SourceV().at((8, 0)).up(3.2).reverse().label('30 V', loc='bottom'))
    R20 = d.add(elm.Resistor().at((4, 3.2)).down(3.2).label('20 Ω', loc='bottom'))
    _cur(d, R20, '$i_\\Delta$', top=False, ofst=0.5)
    _dot(d, (4, 0))
    d.add(elm.Resistor().at((0, 0)).right(4).label('7 Ω', loc='top'))
    d.add(elm.Resistor().at((4, 0)).right(4).label('2 Ω', loc='top'))
    # Üst köprü: 53 i_Delta (+ solda, - sağda)
    _w(d, (0, 3.2), (0, 5.6))
    _w(d, (0, 5.6), (2.2, 5.6))
    d.add(elm.SourceControlledV().at((2.2, 5.6)).right(3.6).reverse().label('$53\\,i_\\Delta$', loc='top'))
    _w(d, (5.8, 5.6), (8, 5.6))
    _w(d, (8, 5.6), (8, 3.2))
    _mesh(d, (1.8, 1.5), '$i_1$')
    _mesh(d, (6.2, 1.5), '$i_2$')
    _mesh(d, (4.0, 4.4), '$i_3$')


def draw_p4_48(d):
    H = 4.2
    d.add(elm.SourceV().at((0, 0)).up(H).label('50 V', loc='top'))
    d.add(elm.Resistor().at((0, H)).right(3.6).label('2 Ω', loc='top')
          .label(('+', '$v_\\Delta$', '−'), loc='bottom', color=ACCENT))
    _dot(d, (3.6, H))
    R5 = d.add(elm.Resistor().at((3.6, H)).right(3.6).label('5 Ω', loc='top'))
    _cur(d, R5, '$i_\\Delta$', top=False, ofst=0.45)
    _dot(d, (7.2, H))
    _w(d, (7.2, H), (10.4, H))
    # Orta dikey kol: 4 Ω ve 9 i_Delta (+ üstte)
    d.add(elm.Resistor().at((3.6, H)).down(2.0).label('4 Ω', loc='bottom'))
    d.add(elm.SourceControlledV().at((3.6, 0)).up(2.2).label('$9\\,i_\\Delta$', loc='bottom'))
    _dot(d, (3.6, 0))
    # Sağ-orta dikey kol: 20 Ω
    d.add(elm.Resistor().at((7.2, H)).down(H).label('20 Ω', loc='bottom'))
    _dot(d, (7.2, 0))
    # En sağ dikey kol: 1.7 v_Delta (ok yukarı)
    d.add(elm.SourceControlledI().at((10.4, 0)).up(H).label('$1.7\\,v_\\Delta$', loc='bottom'))
    _w(d, (0, 0), (10.4, 0))
    _mesh(d, (1.7, 2.0), '$i_1$')
    _mesh(d, (5.4, 2.0), '$i_2$')
    _mesh(d, (8.8, 2.0), '$i_3$')


def draw_p4_52(d):
    # Sol alt göz i1, sol üst göz i2, sağ göz i3
    V = d.add(elm.SourceV().at((0, 0)).up(3.4).label('200 V', loc='top'))
    _cur(d, V, '$i_b$', top=False, ofst=0.45)
    _dot(d, (0, 3.4))
    R10t = d.add(elm.Resistor().at((0, 3.4)).up(3.0).label('10 Ω', loc='bottom'))
    _cur(d, R10t, '$i_a$', top=True, ofst=0.5)
    _w(d, (0, 6.4), (4.5, 6.4))
    _dot(d, (4.5, 6.4))
    _w(d, (4.5, 6.4), (8.6, 6.4))
    R25 = d.add(elm.Resistor().at((0, 3.4)).right(4.5).label('25 Ω', loc='top'))
    _cur(d, R25, '$i_d$', top=False, ofst=0.35)
    _dot(d, (4.5, 3.4))
    d.add(elm.SourceControlledI().at((4.5, 3.4)).up(3.0).label('$4.3\\,i_d$', loc='bottom'))
    R50 = d.add(elm.Resistor().at((4.5, 3.4)).down(3.4).label('50 Ω', loc='top'))
    _cur(d, R50, '$i_e$', top=False, ofst=0.45)
    _dot(d, (4.5, 0))
    d.add(elm.Resistor().at((0, 0)).right(4.5).label('10 Ω', loc='bottom'))
    _w(d, (4.5, 0), (8.6, 0))
    R100 = d.add(elm.Resistor().at((8.6, 6.4)).down(6.4).label('100 Ω', loc='top'))
    _cur(d, R100, '$i_c$', top=False, ofst=0.45)
    _mesh(d, (2.5, 1.4), '$i_1$')
    _mesh(d, (2.3, 4.9), '$i_2$')
    _mesh(d, (6.5, 3.2), '$i_3$')


def draw_p4_53(d):
    d.add(elm.SourceI().at((0, 0)).up(3.2).label('19 A', loc='top'))
    _w(d, (0, 3.2), (2.8, 3.2))
    _dot(d, (2.8, 3.2))
    d.add(elm.Label().at((2.8, 3.55)).label('$V_1$', color=NODE, halign='right', ofst=(-0.15, 0)))
    R40 = d.add(elm.Resistor().at((2.8, 3.2)).down(3.2).label('40 Ω', loc='bottom'))
    _cur(d, R40, '$i_a$', top=True, ofst=0.45)
    _dot(d, (2.8, 0))
    R5 = d.add(elm.Resistor().at((2.8, 3.2)).right(3.8).label('5 Ω', loc='top'))
    _cur(d, R5, '$i_b$', top=False, reverse=True, ofst=0.45)
    _dot(d, (6.6, 3.2))
    d.add(elm.Label().at((6.6, 3.55)).label('$V_2$', color=NODE))
    d.add(elm.SourceControlledI().at((6.6, 0)).up(3.2).label('$2\\,i_b$', loc='bottom'))
    _dot(d, (6.6, 0))
    R10 = d.add(elm.Resistor().at((6.6, 3.2)).right(3.8).label('10 Ω', loc='top'))
    _cur(d, R10, '$i_c$', top=False, reverse=True, ofst=0.45)
    _dot(d, (10.4, 3.2))
    d.add(elm.Label().at((10.4, 3.55)).label('$V_3$', color=NODE, halign='left', ofst=(0.15, 0)))
    V240 = d.add(elm.SourceV().at((10.4, 0)).up(3.2).reverse().label('240 V', loc='bottom'))
    _cur(d, V240, '$i_d$', top=True, reverse=True, ofst=0.5)
    # Üst köprü: 4 i_d (- solda, + sağda) ve i_e sağa doğru
    _w(d, (2.8, 3.2), (2.8, 5.6))
    _w(d, (2.8, 5.6), (4.8, 5.6))
    d.add(elm.SourceControlledV().at((4.8, 5.6)).right(3.4).label('$4\\,i_d$', loc='top'))
    W_ie = d.add(elm.Line().at((8.2, 5.6)).to((10.4, 5.6)))
    _cur(d, W_ie, '$i_e$', top=True, ofst=0.35, length=1.1)
    _w(d, (10.4, 5.6), (10.4, 3.2))
    _w(d, (0, 0), (10.4, 0))
    d.add(elm.Ground().at((6.6, 0)))


def draw_cy2_s2_d4(d):
    H = 3.6
    d.add(elm.SourceControlledI().at((0, 0)).up(H).label('$5\\,i_o$', loc='bottom'))
    _w(d, (0, H), (2.8, H))
    _dot(d, (2.8, H))
    d.add(elm.Label().at((2.8, H + 0.35)).label('$v_1$', color=NODE))
    d.add(elm.Resistor().at((2.8, H)).down(H).label('20 Ω', loc='bottom')
          .label(('+', '$v_1$', '−'), loc='top', color=ACCENT))
    _dot(d, (2.8, 0))
    d.add(elm.Resistor().at((2.8, H)).right(3.6).label('5 Ω', loc='top'))
    _dot(d, (6.4, H))
    d.add(elm.Label().at((6.4, H + 0.35)).label('$v_2$', color=NODE))
    R40 = d.add(elm.Resistor().at((6.4, H)).down(H).label('40 Ω', loc='bottom')
                .label(('+', '$v_2$', '−'), loc='top', color=ACCENT, ofst=0.55))
    _cur(d, R40, '$i_o$', top=True, ofst=0.45)
    _dot(d, (6.4, 0))
    d.add(elm.Resistor().at((6.4, H)).right(3.6).label('10 Ω', loc='top'))
    _dot(d, (10.0, H))
    d.add(elm.Label().at((10.0, H + 0.35)).label('$v_3$', color=NODE))
    d.add(elm.Resistor().at((10.0, H)).down(1.7).label('5 Ω', loc='bottom'))
    d.add(elm.SourceControlledV().at((10.0, 0)).up(1.9).label('$11.5\\,i_o$', loc='bottom'))
    _dot(d, (10.0, 0))
    d.add(elm.Resistor().at((10.0, H)).right(3.2).label('4 Ω', loc='top'))
    d.add(elm.SourceV().at((13.2, 0)).up(H).label('96 V', loc='bottom'))
    _w(d, (0, 0), (13.2, 0))
    d.add(elm.Ground().at((6.4, 0)))


CIRCUITS = {
    "p4-42": draw_p4_42,
    "p4-48": draw_p4_48,
    "p4-52": draw_p4_52,
    "p4-53": draw_p4_53,
    "cy2-s2-d4": draw_cy2_s2_d4,
}


# ---------------------------------------------------------------------------
# PROBLEMLER
# ---------------------------------------------------------------------------
PROBLEMS = [
    dict(
        id="p4-42",
        topic=3,
        code="P4.42",
        title="Çevre akımları yöntemiyle $53\\,i_\\Delta$ bağımlı kaynaklı üç gözlü devrenin analizi",
        source="Çalışma Yaprağı 3 s.1",
        image="P4_42_ORIG.webp",
        circuit="p4-42",
        circuit_caption="Saat yönünde seçilen üç çevre akımı ($i_1, i_2, i_3$) ve orta koldaki kontrol akımı $i_\\Delta = i_1 - i_2$.",
        level=2,
        question=(
            "Şekildeki devrede <strong>çevre akımları (mesh-current) yöntemini</strong> kullanarak: "
            "<strong>(a)</strong> $i_1, i_2, i_3$ çevre akımlarını ve $i_\\Delta$ kontrol akımını bulunuz. "
            "<strong>(b)</strong> $20\\ \\Omega$ dirençte harcanan gücü ve $53\\,i_\\Delta$ bağımlı gerilim kaynağının gücünü hesaplayınız."
        ),
        strategy=[
            "Üç göz için saat yönünde $i_1$ (sol alt), $i_2$ (sağ alt) ve $i_3$ (üst) çevre akımlarını tanımlayalım.",
            "Orta dikey koldaki $20\\ \\Omega$ dirençten aşağı doğru geçen kontrol akımı $i_\\Delta = i_1 - i_2$ olarak çevre akımları cinsinden yazılır.",
            "Sağdaki $30\\ \\text{V}$ kaynağın $-$ ucunun üstte, $+$ ucunun altta olduğuna; üstteki $53\\,i_\\Delta$ kaynağın ise $+$ ucunun solda olduğuna dikkat ederek üç KVL denklemi kurulur.",
        ],
        steps=[
            dict(
                title="1. Aşama: Kontrol değişkeni ve 1. çevre ($i_1$) KVL denklemi",
                body=(
                    "Orta koldaki $20\\ \\Omega$ dirençten aşağı doğru inen akım $i_1$ ile aynı yönlü, $i_2$ ile ters yönlüdür. "
                    "Sol alt gözde saat yönünde KVL yazalım:"
                ),
                math=r"""\begin{aligned}
i_\Delta &= i_1 - i_2 \qquad \text{(ek denklem)} \\[6pt]
\textbf{Çevre 1 KVL:}\quad
&-30 + 3(i_1 - i_3) + 20(i_1 - i_2) + 7i_1 = 0 \\
&(3 + 20 + 7)i_1 - 20i_2 - 3i_3 = 30 \\
&30i_1 - 20i_2 - 3i_3 = 30 \qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: 2. çevre ($i_2$) ve 3. çevre ($i_3$) KVL denklemleri",
                body=(
                    "Sağ alt gözde ($i_2$) saat yönünde dolaşırken sağdaki $30\\ \\text{V}$ kaynağa üstten ($-$ uçtan) girilir. "
                    "Üst gözde ($i_3$) saat yönünde dolaşırken $53\\,i_\\Delta$ kaynağına soldan ($+$ uçtan) girilir:"
                ),
                math=r"""\begin{aligned}
\textbf{Çevre 2 KVL:}\quad
&20(i_2 - i_1) + 5(i_2 - i_3) - 30 + 2i_2 = 0 \\
&-20i_1 + 27i_2 - 5i_3 = 30 \qquad \text{(II)} \\[8pt]
\textbf{Çevre 3 KVL:}\quad
&53\,i_\Delta + 5(i_3 - i_2) + 3(i_3 - i_1) = 0 \\
&53(i_1 - i_2) - 3i_1 - 5i_2 + 8i_3 = 0 \\
&50i_1 - 58i_2 + 8i_3 = 0 \;\Longrightarrow\; 25i_1 - 29i_2 + 4i_3 = 0 \qquad \text{(III)}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Denklem sisteminin çözümü",
                body=(
                    "(I) ve (III) denklemlerinden $i_3$'ü yok edelim ($4 \\times \\text{(I)} + 3 \\times \\text{(III)}$), "
                    "ardından (II) ve (III) denklemlerinden $i_3$'ü yok edelim ($4 \\times \\text{(II)} + 5 \\times \\text{(III)}$):"
                ),
                math=r"""\begin{aligned}
4\text{(I)} + 3\text{(III)}:&\quad (120 + 75)i_1 + (-80 - 87)i_2 = 120 \;\Longrightarrow\; 195i_1 - 167i_2 = 120 \quad \text{(A)} \\[4pt]
4\text{(II)} + 5\text{(III)}:&\quad (-80 + 125)i_1 + (108 - 145)i_2 = 120 \;\Longrightarrow\; 45i_1 - 37i_2 = 120 \quad \text{(B)} \\[6pt]
\text{(A)} - \text{(B)}:&\quad 150i_1 - 130i_2 = 0 \;\Longrightarrow\; i_1 = \frac{13}{15}\,i_2 \\[6pt]
\text{(B)'de yerine koyarsak:}&\quad 45\left(\frac{13}{15}\,i_2\right) - 37i_2 = 120 \;\Longrightarrow\; (39 - 37)i_2 = 120 \;\Longrightarrow\; \boxed{i_2 = 60\ \text{A}} \\[4pt]
i_1 &= \frac{13}{15} \cdot 60 = \boxed{52\ \text{A}}, \qquad
i_3 = \frac{30(52) - 20(60) - 30}{3} = \frac{330}{3} = \boxed{110\ \text{A}} \\[4pt]
i_\Delta &= i_1 - i_2 = 52 - 60 = \boxed{-8\ \text{A}}
\end{aligned}""",
            ),
            dict(
                title="4. Aşama: $20\\ \\Omega$ direncin ve $53\\,i_\\Delta$ bağımlı kaynağın gücü",
                body="Bulunan akımlarla $20\\ \\Omega$ direncin harcadığı güç ve üstteki bağımlı kaynağın gücü:",
                math=r"""\begin{aligned}
p_{20\Omega} &= i_\Delta^2 \cdot 20 = (-8)^2 \cdot 20 = 64 \cdot 20 = \boxed{1280\ \text{W}} \\[6pt]
v_{\text{bağımlı}} &= 53\,i_\Delta = 53(-8) = -424\ \text{V} \\[4pt]
p_{53i_\Delta} &= (+53\,i_\Delta) \cdot i_3 = (-424) \cdot 110 = \boxed{-46640\ \text{W} = -46.64\ \text{kW (güç üretir)}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_1 = 52\ \text{A},\ i_2 = 60\ \text{A},\ i_3 = 110\ \text{A}",
            r"i_\Delta = -8\ \text{A}",
            r"p_{20\Omega} = 1280\ \text{W}",
            r"p_{53i_\Delta} = -46.64\ \text{kW}\ (\text{üretir})",
        ],
        exam=r"""\begin{aligned}
&i_\Delta = i_1 - i_2 \\[2pt]
&\text{Çevre 1: } -30 + 3(i_1 - i_3) + 20(i_1 - i_2) + 7i_1 = 0 \;\Longrightarrow\; 30i_1 - 20i_2 - 3i_3 = 30 \quad \text{(I)} \\
&\text{Çevre 2: } 20(i_2 - i_1) + 5(i_2 - i_3) - 30 + 2i_2 = 0 \;\Longrightarrow\; -20i_1 + 27i_2 - 5i_3 = 30 \quad \text{(II)} \\
&\text{Çevre 3: } 53(i_1 - i_2) + 5(i_3 - i_2) + 3(i_3 - i_1) = 0 \;\Longrightarrow\; 25i_1 - 29i_2 + 4i_3 = 0 \quad \text{(III)} \\[4pt]
&\Longrightarrow\; i_1 = 52\ \text{A},\qquad i_2 = 60\ \text{A},\qquad i_3 = 110\ \text{A},\qquad i_\Delta = -8\ \text{A} \\[2pt]
&p_{20\Omega} = (-8)^2 \times 20 = 1280\ \text{W},\qquad p_{53i_\Delta} = 53(-8)(110) = -46640\ \text{W (üretir)}
\end{aligned}""",
        traps=[
            "Sağdaki $30\\ \\text{V}$ kaynağın $-$ ucu üstte, $+$ ucu alttadır; $i_2$ saat yönünde dolaşırken bu kaynağa $-$ uçtan girer ($-30\\ \\text{V}$).",
            "Üstteki $53\\,i_\\Delta$ kaynağın $+$ ucu soldadır; $i_3$ saat yönünde dolaşırken $+$ uçtan girer ($+53\\,i_\\Delta$).",
        ],
    ),
    dict(
        id="p4-48",
        topic=3,
        code="P4.48",
        title="İki bağımlı kaynaklı ($9\\,i_\\Delta$ ve $1.7\\,v_\\Delta$) devrede çevre akımları analizi",
        source="Çalışma Yaprağı 3 s.1",
        image="P4_48_ORIG.webp",
        circuit="p4-48",
        circuit_caption="Sağ dış koldaki $1.7\\,v_\\Delta$ akım kaynağı, 3. çevre akımını doğrudan $i_3 = -1.7\\,v_\\Delta$ olarak kilitler.",
        level=2,
        question=(
            "Şekildeki devrede <strong>çevre akımları yöntemini</strong> kullanarak "
            "$i_1, i_2, i_3$ çevre akımlarını, $v_\\Delta$ ve $i_\\Delta$ kontrol büyüklüklerini "
            "ve $9\\,i_\\Delta$ bağımlı kaynağının gücünü bulunuz."
        ),
        strategy=[
            "Soldan sağa üç saat yönlü çevre akımı ($i_1, i_2, i_3$) seçelim.",
            "$2\\ \\Omega$ direnç yalnızca 1. çevrede olduğu için $v_\\Delta = 2i_1$; $5\\ \\Omega$ direnç yalnızca 2. çevrede olduğu için $i_\\Delta = i_2$ olur.",
            "En sağdaki $1.7\\,v_\\Delta$ bağımlı akım kaynağı dış kolda olduğu için 3. çevreye KVL yazılmaz; doğrudan $i_3 = -1.7\\,v_\\Delta = -3.4\\,i_1$ kısıtlaması kullanılır.",
        ],
        steps=[
            dict(
                title="1. Aşama: Kontrol değişkenleri ve 3. çevre kısıtlaması",
                body=(
                    "Üstteki $2\\ \\Omega$ ve $5\\ \\Omega$ dirençler dış kollarda yer aldığı için kontrol değişkenleri doğrudan çevre akımlarına bağlanır. "
                    "Sağ dış koldaki $1.7\\,v_\\Delta$ akım kaynağı yukarı doğru, $i_3$ ise sağ kolda aşağı doğru olduğu için $i_3 = -1.7\\,v_\\Delta$ olur:"
                ),
                math=r"""\begin{aligned}
v_\Delta &= 2\,i_1 \qquad (\text{ek 1}) \\[4pt]
i_\Delta &= i_2 \qquad (\text{ek 2}) \\[4pt]
i_3 &= -1.7\,v_\Delta = -1.7(2\,i_1) = -3.4\,i_1 \qquad (\text{3. çevre kısıtı})
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: 1. çevre ($i_1$) ve 2. çevre ($i_2$) KVL denklemleri",
                body="Sol ve orta gözlerde saat yönünde KVL yazıp $i_\\Delta = i_2$ ve $i_3 = -3.4\\,i_1$ ifadelerini yerine koyalım:",
                math=r"""\begin{aligned}
\textbf{Çevre 1 KVL:}\quad
&-50 + 2i_1 + 4(i_1 - i_2) + 9\,i_\Delta = 0 \\
&6i_1 - 4i_2 + 9i_2 = 50 \;\Longrightarrow\; 6i_1 + 5i_2 = 50 \qquad \text{(I)} \\[8pt]
\textbf{Çevre 2 KVL:}\quad
&-9\,i_\Delta + 4(i_2 - i_1) + 5i_2 + 20(i_2 - i_3) = 0 \\
&-4i_1 + (-9 + 4 + 5 + 20)i_2 - 20(-3.4\,i_1) = 0 \\
&64i_1 + 20i_2 = 0 \;\Longrightarrow\; 16i_1 + 5i_2 = 0 \qquad \text{(II)}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Denklem sisteminin çözümü ve $9\\,i_\\Delta$ kaynağın gücü",
                body="(II) denkleminden (I) denklemini çıkardığımızda $5i_2$ terimleri sadeleşir ve tüm akımlar tam sayı olarak bulunur:",
                math=r"""\begin{aligned}
\text{(II)} - \text{(I)}:\quad &(16 - 6)i_1 = 0 - 50 \;\Longrightarrow\; 10i_1 = -50 \;\Longrightarrow\; \boxed{i_1 = -5\ \text{A}} \\[4pt]
&5i_2 = -16(-5) = 80 \;\Longrightarrow\; \boxed{i_2 = i_\Delta = 16\ \text{A}} \\[4pt]
&i_3 = -3.4(-5) = \boxed{17\ \text{A}}, \qquad v_\Delta = 2(-5) = \boxed{-10\ \text{V}} \\[6pt]
&p_{9i_\Delta} = (9\,i_\Delta) \cdot (i_1 - i_2) = 144 \cdot (-5 - 16) = 144 \cdot (-21) = \boxed{-3024\ \text{W (güç üretir)}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_1 = -5\ \text{A},\ i_2 = 16\ \text{A},\ i_3 = 17\ \text{A}",
            r"v_\Delta = -10\ \text{V},\ i_\Delta = 16\ \text{A}",
            r"p_{9i_\Delta} = -3024\ \text{W}\ (\text{üretir})",
        ],
        exam=r"""\begin{aligned}
&v_\Delta = 2i_1,\qquad i_\Delta = i_2,\qquad i_3 = -1.7v_\Delta = -3.4i_1 \\[3pt]
&\text{Çevre 1: } -50 + 2i_1 + 4(i_1 - i_2) + 9i_2 = 0 \;\Longrightarrow\; 6i_1 + 5i_2 = 50 \quad \text{(I)} \\
&\text{Çevre 2: } -9i_2 + 4(i_2 - i_1) + 5i_2 + 20(i_2 - (-3.4i_1)) = 0 \;\Longrightarrow\; 16i_1 + 5i_2 = 0 \quad \text{(II)} \\[3pt]
&\text{(II)} - \text{(I)}:\ 10i_1 = -50 \;\Longrightarrow\; i_1 = -5\ \text{A},\quad i_2 = i_\Delta = 16\ \text{A},\quad i_3 = 17\ \text{A},\quad v_\Delta = -10\ \text{V} \\[3pt]
&p_{9i_\Delta} = (9 \times 16)(i_1 - i_2) = 144(-21) = -3024\ \text{W (üretir)}
\end{aligned}""",
        traps=[
            "Sağdaki $1.7\\,v_\\Delta$ akım kaynağının bulunduğu 3. göze KVL yazılmaz; akım kaynağının uç gerilimi bilinmediği için doğrudan $i_3 = -1.7\\,v_\\Delta$ kısıtlaması kullanılır.",
            "Orta koldaki $9\\,i_\\Delta$ kaynağının $+$ ucu üsttedir; 1. çevrede $+9\\,i_\\Delta$, 2. çevrede $-9\\,i_\\Delta$ olarak denkleme girer.",
        ],
    ),
    dict(
        id="p4-52",
        topic=3,
        code="P4.52",
        title="Süperçevre (Supermesh) yöntemiyle $4.3\\,i_d$ bağımlı akım kaynaklı devrede kol akımları",
        source="Çalışma Yaprağı 3 s.1",
        image="P4_52_ORIG.webp",
        circuit="p4-52",
        circuit_caption="Üst-sol ($i_2$) ve sağ ($i_3$) çevreler arasındaki $4.3\\,i_d$ bağımlı akım kaynağı bir süperçevre oluşturur.",
        level=3,
        question=(
            "Şekildeki devrede <strong>çevre akımları (süperçevre) yöntemini</strong> kullanarak "
            "$i_a, i_b, i_c, i_d$ ve $i_e$ kol akımlarını bulunuz."
        ),
        strategy=[
            "Sol alt göze $i_1$, sol üst göze $i_2$, sağ göze $i_3$ çevre akımlarını (saat yönünde) atayalım.",
            "Ortadaki $4.3\\,i_d$ bağımlı akım kaynağı $i_2$ ve $i_3$ gözlerinin ortak kolundadır; bu iki göz birleştirilerek <strong>süperçevre (supermesh)</strong> KVL denklemi yazılır.",
            "Akım kaynağının kısıtlama denklemi: yukarı yönlü $4.3\\,i_d$ akımı $i_3$ ile aynı, $i_2$ ile zıt yönlü olduğundan $i_3 - i_2 = 4.3\\,i_d = 4.3(i_1 - i_2)$ olur.",
        ],
        steps=[
            dict(
                title="1. Aşama: Kol akımlarının çevre akımları cinsinden ifadesi ve süperçevre kısıtı",
                body=(
                    "Dış kollardaki $i_a, i_b, i_c$ akımları doğrudan çevre akımlarına eşittir; iç kollardaki $i_d$ ve $i_e$ ise iki çevre akımının farkıdır:"
                ),
                math=r"""\begin{aligned}
i_a &= i_2, \qquad i_b = i_1, \qquad i_c = i_3 \\[4pt]
i_d &= i_1 - i_2, \qquad i_e = i_1 - i_3 \\[6pt]
\textbf{Süperçevre kısıt denklemi (} 4.3\,i_d \textbf{ kolu):}& \\
i_3 - i_2 &= 4.3\,i_d = 4.3(i_1 - i_2) \\
-4.3\,i_1 + 3.3\,i_2 + i_3 &= 0 \;\xrightarrow{\times 10}\; -43i_1 + 33i_2 + 10i_3 = 0 \qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: 1. çevre KVL ve Süperçevre ($i_2 + i_3$) KVL denklemleri",
                body=(
                    "Sol alt gözde ($i_1$) normal KVL, $i_2$ ve $i_3$ gözlerini birleştiren dış sınırda ise $4.3\\,i_d$ koluna uğramadan süperçevre KVL yazalım:"
                ),
                math=r"""\begin{aligned}
\textbf{Çevre 1 KVL:}\quad
&-200 + 25(i_1 - i_2) + 50(i_1 - i_3) + 10i_1 = 0 \\
&85i_1 - 25i_2 - 50i_3 = 200 \;\xrightarrow{\div 5}\; 17i_1 - 5i_2 - 10i_3 = 40 \qquad \text{(II)} \\[8pt]
\textbf{Süperçevre (2 + 3) KVL:}\quad
&10i_2 + 100i_3 + 50(i_3 - i_1) + 25(i_2 - i_1) = 0 \\
&-75i_1 + 35i_2 + 150i_3 = 0 \;\xrightarrow{\div 5}\; -15i_1 + 7i_2 + 30i_3 = 0 \qquad \text{(III)}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Denklem sisteminin çözümü ve 5 kol akımı",
                body=(
                    "(I) ve (II) denklemlerini taraf tarafa topladığımızda $+10i_3$ ve $-10i_3$ hemen birbirini götürür:"
                ),
                math=r"""\begin{aligned}
\text{(I)} + \text{(II)}:&\quad (-43 + 17)i_1 + (33 - 5)i_2 = 40 \\
&\quad -26i_1 + 28i_2 = 40 \;\Longrightarrow\; -13i_1 + 14i_2 = 20 \qquad \text{(A)} \\[6pt]
3 \times \text{(II)} + \text{(III)}:&\quad (51 - 15)i_1 + (-15 + 7)i_2 = 120 \\
&\quad 36i_1 - 8i_2 = 120 \;\Longrightarrow\; 9i_1 - 2i_2 = 30 \qquad \text{(B)} \\[6pt]
\text{(A)} + 7 \times \text{(B)}:&\quad (-13 + 63)i_1 = 20 + 210 \;\Longrightarrow\; 50i_1 = 230 \;\Longrightarrow\; \boxed{i_1 = i_b = 4.6\ \text{A}} \\[4pt]
2i_2 &= 9(4.6) - 30 = 11.4 \;\Longrightarrow\; \boxed{i_2 = i_a = 5.7\ \text{A}} \\[4pt]
10i_3 &= 43(4.6) - 33(5.7) = 197.8 - 188.1 = 9.7 \;\Longrightarrow\; \boxed{i_3 = i_c = 0.97\ \text{A}} \\[6pt]
i_d &= i_1 - i_2 = 4.6 - 5.7 = \boxed{-1.1\ \text{A}}, \qquad
i_e = i_1 - i_3 = 4.6 - 0.97 = \boxed{3.63\ \text{A}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_a = 5.7\ \text{A}",
            r"i_b = 4.6\ \text{A}",
            r"i_c = 0.97\ \text{A}",
            r"i_d = -1.1\ \text{A}",
            r"i_e = 3.63\ \text{A}",
        ],
        exam=r"""\begin{aligned}
&i_a = i_2,\quad i_b = i_1,\quad i_c = i_3,\quad i_d = i_1 - i_2,\quad i_e = i_1 - i_3 \\[2pt]
&\text{Kısıt: } i_3 - i_2 = 4.3(i_1 - i_2) \;\Longrightarrow\; -43i_1 + 33i_2 + 10i_3 = 0 \quad \text{(I)} \\
&\text{Çevre 1: } -200 + 25(i_1 - i_2) + 50(i_1 - i_3) + 10i_1 = 0 \;\Longrightarrow\; 17i_1 - 5i_2 - 10i_3 = 40 \quad \text{(II)} \\
&\text{Süperçevre (2+3): } 10i_2 + 100i_3 + 50(i_3 - i_1) + 25(i_2 - i_1) = 0 \;\Longrightarrow\; -15i_1 + 7i_2 + 30i_3 = 0 \quad \text{(III)} \\[3pt]
&\text{(I)+(II)}: -13i_1 + 14i_2 = 20,\qquad 3\text{(II)+(III)}: 9i_1 - 2i_2 = 30 \\
&\Longrightarrow\; i_1 = i_b = 4.6\ \text{A},\quad i_2 = i_a = 5.7\ \text{A},\quad i_3 = i_c = 0.97\ \text{A},\quad i_d = -1.1\ \text{A},\quad i_e = 3.63\ \text{A}
\end{aligned}""",
        traps=[
            "İki çevre arasında akım kaynağı ($4.3\\,i_d$) varken her iki çevreye ayrı ayrı KVL yazılamaz; ortak kol atlanarak tek bir <strong>süperçevre KVL</strong> denklemi yazılır.",
            "Süperçevre KVL'de $25\\ \\Omega$ dirençten geçerken $25(i_2 - i_1)$, $50\\ \\Omega$ dirençten geçerken $50(i_3 - i_1)$ yazılır.",
        ],
    ),
    dict(
        id="p4-53",
        topic=3,
        code="P4.53",
        title="Süperdüğüm / Süperçevre ile $2\\,i_b$ ve $4\\,i_d$ bağımlı kaynaklı devrenin tam analizi",
        source="Çalışma Yaprağı 3 s.1",
        image="P4_53_ORIG.webp",
        circuit="p4-53",
        circuit_caption="Sağdaki 240 V kaynak $V_3 = -240\\ \\text{V}$ düğümünü sabitler; üstteki $4\\,i_d$ kaynak $V_3 - V_1 = 4\\,i_d$ kısıtını kurar.",
        level=3,
        question=(
            "Şekildeki devrede: <strong>(a)</strong> $i_a, i_b, i_c, i_d$ ve $i_e$ kol akımlarını bulunuz. "
            "<strong>(b)</strong> Devredeki tüm elemanların güçlerini hesaplayarak $\\sum p = 0$ güç dengesini doğrulayınız."
        ),
        strategy=[
            "Alt teli referans ($0\\ \\text{V}$) seçelim; sağdaki $240\\ \\text{V}$ kaynağın $-$ ucu üstte olduğu için sağ üst düğüm doğrudan $V_3 = -240\\ \\text{V}$ olur!",
            "Üstteki $4\\,i_d$ bağımlı gerilim kaynağının $-$ ucu solda ($V_1$), $+$ ucu sağda ($V_3$) olduğu için $V_3 - V_1 = 4\\,i_d \\implies V_1 = -240 - 4\\,i_d$ olur.",
            "Orta düğümde ($V_2$) KCL ve tüm devreyi saran dış KCL (referans düğümde KCL) ile tüm düğüm gerilimleri ve kol akımları tam sayı olarak bulunur.",
        ],
        steps=[
            dict(
                title="1. Aşama: Düğüm gerilimleri ve orta düğüm ($V_2$) KCL bağıntısı",
                body=(
                    "Alt teli $0\\ \\text{V}$ referans aldığımızda sağ üst düğüm $V_3 = -240\\ \\text{V}$'tur. "
                    "Şekilde $i_b$ ve $i_c$ oklarının <strong>sağdan sola</strong> baktığına dikkat ederek Ohm kanunu ve düğüm $V_2$'de KCL yazalım:"
                ),
                math=r"""\begin{aligned}
V_3 &= -240\ \text{V}, \qquad V_3 - V_1 = 4\,i_d \;\Longrightarrow\; i_d = \frac{-240 - V_1}{4} \\[6pt]
i_a &= \frac{V_1}{40}, \qquad i_b = \frac{V_2 - V_1}{5}, \qquad i_c = \frac{V_3 - V_2}{10} = \frac{-240 - V_2}{10} \\[6pt]
\text{Düğüm } V_2 \text{ KCL (çıkanlar } + \text{):}\quad
&i_b - i_c - 2\,i_b = 0 \;\Longrightarrow\; -i_b - i_c = 0 \;\Longrightarrow\; i_c = -i_b \\[4pt]
\frac{-240 - V_2}{10} &= -\frac{V_2 - V_1}{5} \qquad (\times 10) \\[4pt]
-240 - V_2 &= -2V_2 + 2V_1 \;\Longrightarrow\; V_2 = 2V_1 + 240 \qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: ($V_1, V_3$) süperdüğüm / referans KCL denklemi ve çözüm",
                body=(
                    "Alt referans düğümüne yukarıdan inen ve çıkan dikey kol akımlarının toplamı sıfır olmalıdır ($-19 + i_a - 2\\,i_b + i_d = 0$):"
                ),
                math=r"""\begin{aligned}
i_b &= \frac{V_2 - V_1}{5} = \frac{(2V_1 + 240) - V_1}{5} = \frac{V_1 + 240}{5} \\[6pt]
\text{Dikey kollar KCL:}\quad
&-19 + i_a - 2\,i_b + i_d = 0 \\[4pt]
&-19 + \frac{V_1}{40} - 2\left(\frac{V_1 + 240}{5}\right) + \frac{-240 - V_1}{4} = 0 \qquad (\times 40) \\[4pt]
&-760 + V_1 - 16(V_1 + 240) + 10(-240 - V_1) = 0 \\
&-760 + V_1 - 16V_1 - 3840 - 2400 - 10V_1 = 0 \\
&-25V_1 = 7000 \;\Longrightarrow\; \boxed{V_1 = -280\ \text{V}} \\[4pt]
&V_2 = 2(-280) + 240 = \boxed{-320\ \text{V}}, \qquad V_3 = \boxed{-240\ \text{V}}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Kol akımları ($i_a, i_b, i_c, i_d, i_e$) ve güç dengesi ($\\sum p = 0$)",
                body="Bulunan düğüm gerilimlerinden 5 kol akımını ve 7 elemanın gücünü hesaplayalım:",
                math=r"""\begin{aligned}
i_a &= \frac{-280}{40} = \boxed{-7\ \text{A}}, \qquad
i_b = \frac{-320 - (-280)}{5} = \boxed{-8\ \text{A}}, \qquad
i_c = -i_b = \boxed{8\ \text{A}} \\[4pt]
i_d &= \frac{-240 - (-280)}{4} = \boxed{10\ \text{A}}, \qquad
i_e = i_c + i_d = 8 + 10 = \boxed{18\ \text{A}} \\[8pt]
p_{40\Omega} &= (-7)^2(40) = +1960\ \text{W}, \quad
p_{5\Omega} = (-8)^2(5) = +320\ \text{W}, \quad
p_{10\Omega} = 8^2(10) = +640\ \text{W} \\
p_{19\text{A}} &= -V_1 \cdot 19 = -(-280)(19) = +5320\ \text{W (emer)} \\[4pt]
p_{2i_b} &= -V_2 \cdot (2i_b) = -(-320)(-16) = -5120\ \text{W (üretir)} \\
p_{4i_d} &= (V_1 - V_3) \cdot i_e = (-40)(18) = -720\ \text{W (üretir)} \\
p_{240\text{V}} &= V_3 \cdot i_d = (-240)(10) = -2400\ \text{W (üretir)} \\[4pt]
\sum P_{\text{harcanan}} &= 1960 + 320 + 640 + 5320 = \boxed{8240\ \text{W}} = \sum P_{\text{üretilen}} = 5120 + 720 + 2400
\end{aligned}""",
            ),
        ],
        answer=[
            r"i_a = -7\ \text{A},\ i_b = -8\ \text{A},\ i_c = 8\ \text{A}",
            r"i_d = 10\ \text{A},\ i_e = 18\ \text{A}",
            r"\sum P_{\text{üretilen}} = \sum P_{\text{harcanan}} = 8240\ \text{W}",
        ],
        exam=r"""\begin{aligned}
&V_3 = -240\ \text{V},\qquad V_3 - V_1 = 4i_d \;\Longrightarrow\; i_d = \frac{-240 - V_1}{4} \\
&\text{KCL } (V_2):\ i_b - i_c - 2i_b = 0 \;\Longrightarrow\; i_c = -i_b \;\Longrightarrow\; \frac{-240 - V_2}{10} = -\frac{V_2 - V_1}{5} \;\Longrightarrow\; V_2 = 2V_1 + 240 \\
&\text{Dikey KCL: } -19 + \frac{V_1}{40} - 2\left(\frac{V_1+240}{5}\right) + \frac{-240-V_1}{4} = 0 \xrightarrow{\times 40} -25V_1 = 7000 \;\Longrightarrow\; V_1 = -280\ \text{V} \\
&\Longrightarrow\; V_2 = -320\ \text{V},\quad i_a = -7\ \text{A},\quad i_b = -8\ \text{A},\quad i_c = 8\ \text{A},\quad i_d = 10\ \text{A},\quad i_e = 18\ \text{A} \\
&\sum P_{\text{üretilen}} = 5120 + 720 + 2400 = 8240\ \text{W} = \sum P_{\text{harcanan}}
\end{aligned}""",
        traps=[
            "Sağdaki $240\\ \\text{V}$ kaynağın $-$ ucu üsttedir; bu nedenle $V_3 = +240\\ \\text{V}$ değil, $V_3 = -240\\ \\text{V}$ olur.",
            "$i_b$ ve $i_c$ oklarının yönü sağdan sola doğrudur: $i_b = (V_2 - V_1)/5$ ve $i_c = (V_3 - V_2)/10$.",
        ],
    ),
    dict(
        id="cy2-s2-d4",
        topic=3,
        code="ÇY2 · s.2 · 4",
        title="İki bağımlı kaynaklı ($5\\,i_o$ ve $11.5\\,i_o$) üç düğümlü devrede $v_1, v_2, v_3$ gerilimleri",
        source="Çalışma Yaprağı 2 s.2 (4. devre)",
        image="CY2_S2_D4_ORIG.webp",
        circuit="cy2-s2-d4",
        circuit_caption="Kontrol akımı $i_o = v_2 / 40$ orta düğüm gerilimine bağlıdır; üç düğümde KCL ile $v_1, v_2, v_3$ bulunur.",
        level=2,
        question=(
            "Şekildeki devrede <strong>düğüm gerilimleri yöntemini</strong> kullanarak "
            "$v_1, v_2, v_3$ düğüm gerilimlerini ve $i_o$ kontrol akımını bulunuz."
        ),
        strategy=[
            "Alt teli referans ($0\\ \\text{V}$) seçtiğimizde üç temel düğümün gerilimleri doğrudan $v_1, v_2, v_3$ olur.",
            "Orta koldaki $40\\ \\Omega$ dirençten aşağı inen kontrol akımı $i_o = v_2 / 40$ olarak yazılır.",
            "Üç düğümde KCL yazılıp $i_o = v_2 / 40$ yerine konulduğunda $v_1, v_2, v_3$ tam sayı olarak elde edilir.",
        ],
        steps=[
            dict(
                title="1. Aşama: Kontrol denklemi ve 1. düğüm ($v_1$) KCL denklemi",
                body="Orta koldaki $40\\ \\Omega$ direnç üzerinde $v_2$ gerilimi tanımlı olduğundan $i_o = v_2 / 40$ olur. Düğüm 1'de KCL yazalım:",
                math=r"""\begin{aligned}
i_o &= \frac{v_2}{40} \qquad \text{(ek denklem)} \\[6pt]
\textbf{Düğüm 1 KCL:}\quad
&-5\,i_o + \frac{v_1}{20} + \frac{v_1 - v_2}{5} = 0 \\[4pt]
&-5\left(\frac{v_2}{40}\right) + \frac{v_1}{20} + \frac{v_1 - v_2}{5} = 0 \qquad (\times 40) \\[4pt]
&-5v_2 + 2v_1 + 8(v_1 - v_2) = 0 \\
&10v_1 - 13v_2 = 0 \;\Longrightarrow\; v_1 = 1.3\,v_2 \qquad \text{(I)}
\end{aligned}""",
            ),
            dict(
                title="2. Aşama: 2. düğüm ($v_2$) ve 3. düğüm ($v_3$) KCL denklemleri",
                body="Düğüm 2 ve Düğüm 3 için KCL (çıkan akımlar $+$) denklemlerini kuralım:",
                math=r"""\begin{aligned}
\textbf{Düğüm 2 KCL:}\quad
&\frac{v_2 - v_1}{5} + \frac{v_2}{40} + \frac{v_2 - v_3}{10} = 0 \qquad (\times 40) \\[4pt]
&8(v_2 - v_1) + v_2 + 4(v_2 - v_3) = 0 \\
&-8v_1 + 13v_2 - 4v_3 = 0 \qquad \text{(II)} \\[8pt]
\textbf{Düğüm 3 KCL:}\quad
&\frac{v_3 - v_2}{10} + \frac{v_3 - 11.5\,i_o}{5} + \frac{v_3 - 96}{4} = 0 \\[4pt]
&i_o = \frac{v_2}{40} \text{ yazılıp } 40 \text{ ile çarpılırsa:} \\
&4(v_3 - v_2) + 8v_3 - 2.3\,v_2 + 10(v_3 - 96) = 0 \\
&-6.3\,v_2 + 22v_3 = 960 \qquad \text{(III)}
\end{aligned}""",
            ),
            dict(
                title="3. Aşama: Denklem sisteminin çözümü",
                body="(I) ve (II) denklemlerini taraf tarafa topladığımızda $-13v_2$ ve $+13v_2$ terimleri birbirini götürür:",
                math=r"""\begin{aligned}
\text{(I)} + \text{(II)}:&\quad 2v_1 - 4v_3 = 0 \;\Longrightarrow\; v_1 = 2v_3 \\[4pt]
\text{(I)}'den:&\quad 1.3\,v_2 = 2v_3 \;\Longrightarrow\; v_3 = 0.65\,v_2 \\[6pt]
\text{(III)}'te yerine koyarsak:&\quad -6.3\,v_2 + 22(0.65\,v_2) = 960 \\
&\quad (-6.3 + 14.3)\,v_2 = 960 \;\Longrightarrow\; 8v_2 = 960 \;\Longrightarrow\; \boxed{v_2 = 120\ \text{V}} \\[4pt]
v_1 &= 1.3 \times 120 = \boxed{156\ \text{V}}, \qquad
v_3 = 0.65 \times 120 = \boxed{78\ \text{V}} \\[4pt]
i_o &= \frac{v_2}{40} = \frac{120}{40} = \boxed{3\ \text{A}}
\end{aligned}""",
            ),
        ],
        answer=[
            r"v_1 = 156\ \text{V}",
            r"v_2 = 120\ \text{V}",
            r"v_3 = 78\ \text{V}",
            r"i_o = 3\ \text{A}",
        ],
        exam=r"""\begin{aligned}
&i_o = \frac{v_2}{40} \\[2pt]
&\text{Düğüm 1: } -5\left(\frac{v_2}{40}\right) + \frac{v_1}{20} + \frac{v_1 - v_2}{5} = 0 \xrightarrow{\times 40} 10v_1 - 13v_2 = 0 \quad \text{(I)} \\
&\text{Düğüm 2: } \frac{v_2 - v_1}{5} + \frac{v_2}{40} + \frac{v_2 - v_3}{10} = 0 \xrightarrow{\times 40} -8v_1 + 13v_2 - 4v_3 = 0 \quad \text{(II)} \\
&\text{Düğüm 3: } \frac{v_3 - v_2}{10} + \frac{v_3 - 11.5(v_2/40)}{5} + \frac{v_3 - 96}{4} = 0 \xrightarrow{\times 40} -6.3v_2 + 22v_3 = 960 \quad \text{(III)} \\[3pt]
&\text{(I)+(II)}:\ 2v_1 = 4v_3 \;\Rightarrow\; v_1 = 2v_3,\quad v_3 = 0.65v_2 \;\xrightarrow{\text{(III)}}\; 8v_2 = 960 \\
&\Longrightarrow\; v_2 = 120\ \text{V},\qquad v_1 = 156\ \text{V},\qquad v_3 = 78\ \text{V},\qquad i_o = 3\ \text{A}
\end{aligned}""",
        traps=[
            "3. düğümün alt kolunda $5\\ \\Omega$ direnç ile $11.5\\,i_o$ bağımlı gerilim kaynağı seri bağlıdır; bu koldan aşağı inen akım $(v_3 - 11.5\\,i_o)/5$ olarak yazılır.",
            "Sağdaki $96\\ \\text{V}$ kaynak $4\\ \\Omega$ dirençle seri bağlı olduğu için $v_3$ düğümünü doğrudan $96\\ \\text{V}$ yapmaz; KCL terimi $(v_3 - 96)/4$ olur.",
        ],
    ),
]
