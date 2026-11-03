# -*- coding: utf-8 -*-
"""
circuitkit — tek tip, ders kitabı kalitesinde devre şeması üretimi (schemdraw tabanlı).

Kullanım (içerik modüllerinde):

    from circuitkit import elm, ACCENT, NODE

    def draw_p4_87(d):
        V = d.add(elm.SourceV().up().label('110 V', loc='left'))
        d.add(elm.Resistor().right().label('15 Ω').label(('+', '$v_\\Delta$', '−'), loc='bottom'))
        ...

    CIRCUITS = {"p4-87": draw_p4_87}

Kurallar:
  * Renk verme: varsayılan çizgi rengi siyah (#111). Vurgu gerekiyorsa sadece
    ACCENT (mavi, kontrol değişkeni / ölçülen büyüklük) ve NODE (kırmızı, düğüm adı) kullan.
  * Etiketlerde matematik için $...$ (LaTeX/mathtext) kullan: '$v_\\Delta$', '$0.1v_\\Delta$', '$R_o$'.
  * Birimler düz metin: '15 Ω', '3.6 kV', '5 mA'.
  * Yönler (schemdraw):
      - SourceV().up()  -> + ucu ÜSTTE.    .down() -> + ucu ALTTA.   (.reverse() kutbu çevirir)
      - SourceI().up()  -> ok YUKARI.      .down() -> ok AŞAĞI.
      - SourceControlledV / SourceControlledI aynı kurala uyar (baklava sembolü).
      - Resistor, ResistorVar (yük direnci R_L/R_o için ResistorVar kullan).
  * Düğüm noktaları için elm.Dot(); açık uç (a, b terminali) için elm.Dot(open=True).
  * Akım oku: elm.CurrentLabelInline(direction='in'/'out').at(eleman).label('$i_x$')
    veya basitçe eleman.label('$i_\\Delta$ →', loc='bottom').
"""
import os
import schemdraw
import schemdraw.elements as elm  # noqa: F401  (içerik modülleri buradan import eder)

schemdraw.svgconfig.text = 'path'   # metin -> vektör yol (her yerde aynı görünür)
schemdraw.svgconfig.svg2 = True
schemdraw.svgconfig.precision = 2

INK = '#111111'
ACCENT = '#1d4ed8'   # kontrol değişkeni / ölçülen akım-gerilim
NODE = '#c2410c'     # düğüm isimleri (V1, V2 ...)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, '..', 'circuits'))


def render(name, fn, out_dir=OUT_DIR):
    """fn(d) çizimi yapar; circuits/<name>.svg dosyasına yazar ve yolu döndürür."""
    os.makedirs(out_dir, exist_ok=True)
    with schemdraw.Drawing(show=False) as d:
        d.config(unit=3, fontsize=13, color=INK, lw=1.5, font='serif')
        fn(d)
        data = d.get_imagedata('svg')
    svg = data.decode('utf-8') if isinstance(data, bytes) else data
    path = os.path.join(out_dir, f'{name}.svg')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    return path


def render_all(circuits, out_dir=OUT_DIR):
    paths = {}
    for name, fn in circuits.items():
        paths[name] = render(name, fn, out_dir)
    return paths
