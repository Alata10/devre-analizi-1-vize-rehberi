# -*- coding: utf-8 -*-
"""
q3a doğrulama — ÇY2 düğüm gerilimi problemleri (bağımlı kaynaklı).
Her problem iki yoldan çözülür:
  (1) adımlarda yazılan sadeleştirilmiş denklemler (Fraction ile, tam sayısal),
  (2) bağımsız genel MNA (modified nodal analysis) çözümü — numpy ile.
Adımlarda geçen her ara ve son sayı assert edilir. Çalıştır:  python build/verify/q3a_verify.py
"""
import sys
from fractions import Fraction as F
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TOL = 1e-9


def close(a, b, tol=TOL):
    return abs(float(a) - float(b)) < tol


def solve2(a11, a12, b1, a21, a22, b2):
    det = a11 * a22 - a12 * a21
    return (b1 * a22 - a12 * b2) / det, (a11 * b2 - a21 * b1) / det


# ---------------------------------------------------------------------------
# MNA çözücü: düğümler 0 (referans), 1..n. Elemanlar:
#  ('R', a, b, R)          direnç a-b
#  ('I', a, b, I)          bağımsız akım kaynağı: akım a'dan çıkıp kaynağın içinden b'ye gider  (a -> b)
#  ('V', p, m, V)          bağımsız gerilim kaynağı: v_p - v_m = V
#  ('VCVS', p, m, k, cp, cm)   v_p - v_m = k (v_cp - v_cm)
#  ('CCVS', p, m, k, ctrl)     v_p - v_m = k * i_ctrl  (ctrl: ('R', a, b, R) yönlü akım a->b)
#  ('VCCS', a, b, k, cp, cm)   kaynak içinden a -> b akım = k (v_cp - v_cm)
# ---------------------------------------------------------------------------
def mna(n, elems):
    vs = [e for e in elems if e[0] in ('V', 'VCVS', 'CCVS')]
    N = n + len(vs)
    A = np.zeros((N, N))
    z = np.zeros(N)

    def idx(k):
        return k - 1

    def stamp_G(a, b, g):
        if a: A[idx(a), idx(a)] += g
        if b: A[idx(b), idx(b)] += g
        if a and b:
            A[idx(a), idx(b)] -= g
            A[idx(b), idx(a)] -= g

    for e in elems:
        t = e[0]
        if t == 'R':
            stamp_G(e[1], e[2], 1.0 / e[3])
        elif t == 'I':
            a, b, I = e[1], e[2], e[3]
            # akım a'dan çıkar (kaynak içinden) b'ye girer: a düğümünden dışarı... kaynak a->b iç akım:
            # a düğümünden kaynağa giren akım I => a için "çıkan" +I ; b'ye kaynaktan çıkan I => b için giren
            if a: z[idx(a)] -= I
            if b: z[idx(b)] += I
        elif t == 'VCCS':
            a, b, k, cp, cm = e[1:]
            # a'dan çıkan (kaynağa giren) akım k(vcp-vcm)
            for node, sgn in ((a, 1), (b, -1)):
                if node:
                    if cp: A[idx(node), idx(cp)] += sgn * k
                    if cm: A[idx(node), idx(cm)] -= sgn * k
    for j, e in enumerate(vs):
        r = n + j
        p, m = e[1], e[2]
        # akım değişkeni: kaynağın içinden p -> m yönünde (p'den kaynağa giren)
        if p:
            A[idx(p), r] += 1
            A[r, idx(p)] += 1
        if m:
            A[idx(m), r] -= 1
            A[r, idx(m)] -= 1
        if e[0] == 'V':
            z[r] = e[3]
        elif e[0] == 'VCVS':
            k, cp, cm = e[3], e[4], e[5]
            if cp: A[r, idx(cp)] -= k
            if cm: A[r, idx(cm)] += k
        elif e[0] == 'CCVS':
            k, (_, a, b, R) = e[3], e[4]
            if a: A[r, idx(a)] -= k / R
            if b: A[r, idx(b)] += k / R
    x = np.linalg.solve(A, z)
    v = [0.0] + list(x[:n])
    return v, list(x[n:])


report = []


def ok(label, val):
    report.append(f"  {label} = {val}")


# ===========================================================================
# 1) ÇY2 s.2 · 1   (3 A, 200 Ω, 10 Ω + 5iΔ, 20 Ω, 80 V)
# ===========================================================================
print("cy2-s2-d1")
# ek: iΔ = (vo - 80)/20 ; 10Ω'un alt ucu = -5iΔ
# KCL ×200: -600 + vo + 20(vo + 5iΔ) + 10(vo - 80) = 0, 100 iΔ = 5vo - 400
# => 36 vo - 1800 = 0
coef_vo = 1 + 20 + 10 + 5
const = -600 - 800 - 400
assert coef_vo == 36 and const == -1800
vo = F(1800, 36)
assert vo == 50
iD = (vo - 80) / 20
assert iD == F(-3, 2)
v_bottom = -5 * iD           # 10Ω'un alt ucu (bağımlı kaynağın üst ucu)
assert v_bottom == F(15, 2)
i10 = (vo - v_bottom) / 10   # 10Ω'dan aşağı
assert i10 == F(17, 4)       # 4.25 A
# KCL kontrol
assert -3 + vo / 200 + i10 + iD == 0
i200 = vo / 200
assert i200 == F(1, 4)
# güçler (pasif işaret)
p3A = -vo * 3
p200 = vo ** 2 / 200
p10 = i10 ** 2 * 10
p20 = iD ** 2 * 20
p80 = 80 * iD              # iΔ 80 V'un + ucundan giriyor
vdep = 5 * iD              # alt(+) - üst(-) = 5iΔ = -7.5
assert vdep == F(-15, 2)
p_dep = vdep * (-i10)      # + uca (alta) giren akım = -i10
assert p3A == -150 and p200 == F(25, 2) and p10 == F(1445, 8) and p20 == 45
assert p80 == -120 and p_dep == F(255, 8)          # 31.875 W
assert close(p10, 180.625) and close(p_dep, 31.875)
assert p3A + p200 + p10 + p20 + p80 + p_dep == 0
assert p200 + p10 + p20 + p_dep == 270 and -(p3A + p80) == 270
# MNA: nodes 1=vo, 2=80V üst, 3=10Ω alt ucu
v, _ = mna(3, [('I', 0, 1, 3.0), ('R', 1, 0, 200), ('R', 1, 2, 20), ('V', 2, 0, 80),
               ('R', 1, 3, 10), ('CCVS', 0, 3, 5, ('R', 1, 2, 20))])
assert close(v[1], 50) and close(v[3], 7.5)
ok("vo", vo); ok("iΔ", iD); ok("p_dep", p_dep)

# ===========================================================================
# 2) ÇY2 s.2 · 2   (160 V, 10 Ω, 100 Ω, 30 Ω, 150iσ, 20 Ω)
# ===========================================================================
print("cy2-s2-d2")
# iσ = -V1/100 ; seri kol akımı i_k = (V1 - 150 iσ)/50 = V1/20
# ×100: 10(V1-160) + V1 + 5V1 = 0 -> 16 V1 = 1600
assert 10 + 1 + 5 == 16
V1 = F(1600, 16)
assert V1 == 100
isg = -V1 / 100
assert isg == -1
vdep = 150 * isg
assert vdep == -150
ik = (V1 - vdep) / 50
assert ik == 5 and ik == V1 / 20
i10 = (160 - V1) / 10
assert i10 == 6
assert i10 == V1 / 100 + ik       # KCL
v_rt = V1 - 30 * ik               # sağ üst (kaynağın + ucu)
v_rb = 20 * ik                    # sağ alt (kaynağın - ucu)
assert v_rt == -50 and v_rb == 100 and v_rt - v_rb == vdep
p160 = -160 * i10
p10 = i10 ** 2 * 10
p100 = V1 ** 2 / 100
p30 = ik ** 2 * 30
p20 = ik ** 2 * 20
p_dep = vdep * ik                 # ik + uçtan (üstten) giriyor
assert (p160, p10, p100, p30, p20, p_dep) == (-960, 360, 100, 750, 500, -750)
assert p160 + p10 + p100 + p30 + p20 + p_dep == 0
v, _ = mna(4, [('V', 1, 0, 160), ('R', 1, 2, 10), ('R', 2, 0, 100), ('R', 2, 3, 30),
               ('CCVS', 3, 4, 150, ('R', 0, 2, 100)), ('R', 4, 0, 20)])
assert close(v[2], 100) and close(v[3], -50) and close(v[4], 100)
ok("V1", V1); ok("iσ", isg); ok("p_dep", p_dep)

# ===========================================================================
# 3) ÇY2 s.2 · 3   (50 V, 500 Ω, 1 kΩ, 2 kΩ, vΔ/750, 200 Ω)
# ===========================================================================
print("cy2-s2-d3")
# (I) ×2000: 4(V1-50) + 2V1 + (V1 - V2) = 0 -> 7V1 - V2 = 200
# (II) ×6000: 3(V2 - V1) - 8V1 + 30V2 = 0 -> -11V1 + 33V2 = 0 -> V1 = 3V2
assert (4 + 2 + 1, 4 * 50) == (7, 200)
assert (-3 - 8, 3 + 30) == (-11, 33)
V1, V2 = solve2(F(7), F(-1), F(200), F(-11), F(33), F(0))
assert V1 == 30 and V2 == 10
assert 7 * 3 - 1 == 20 and F(200, 20) == 10
vD, vo = V1, V2
idep = vD / 750
assert idep == F(1, 25)            # 0.04 A = 40 mA
i500 = (50 - V1) / 500
i1k = V1 / 1000
i2k = (V1 - V2) / 2000
i200 = V2 / 200
assert (i500, i1k, i2k, i200) == (F(1, 25), F(3, 100), F(1, 100), F(1, 20))
assert i500 == i1k + i2k and i2k + idep == i200
p50 = -50 * i500
p500 = i500 ** 2 * 500
p1k = V1 ** 2 / 1000
p2k = (V1 - V2) ** 2 / 2000
p200 = V2 ** 2 / 200
p_dep = -V2 * idep                 # akım + uçtan (üstten) çıkıyor
assert (p50, p500, p1k, p2k, p200, p_dep) == (-2, F(4, 5), F(9, 10), F(1, 5), F(1, 2), F(-2, 5))
assert p50 + p500 + p1k + p2k + p200 + p_dep == 0
v, _ = mna(3, [('V', 1, 0, 50), ('R', 1, 2, 500), ('R', 2, 0, 1000), ('R', 2, 3, 2000),
               ('VCCS', 0, 3, 1 / 750, 2, 0), ('R', 3, 0, 200)])
assert close(v[2], 30) and close(v[3], 10)
ok("vΔ", vD); ok("vo", vo); ok("p_dep", p_dep)

# ===========================================================================
# 4) ÇY2 s.2 · 5   (15 V, 33 Ω, 10 Ω, 2 Ω, 5vΔ süperdüğüm, 20 Ω, 40 Ω)
# ===========================================================================
print("cy2-s2-d5")
# kısıt: V1 - V2 = 5vΔ = 5V1 -> V2 = -4V1
# süperdüğüm ×40: 4(V1-15) + 20V1 + 2V2 + V2 = 0 -> 24V1 + 3V2 = 60
assert (4 + 20, 2 + 1, 4 * 15) == (24, 3, 60)
# yerine koy: 24V1 - 12V1 = 60 -> 12V1 = 60
V1 = F(60, 24 - 12)
assert V1 == 5
V2 = -4 * V1
assert V2 == -20
vD, vo = V1, V2
vdep = 5 * vD
assert vdep == 25 and V1 - V2 == vdep
i10 = (15 - V1) / 10
i2 = V1 / 2
i20 = V2 / 20
i40 = V2 / 40
i33 = F(15, 33)
assert (i10, i2, i20, i40) == (1, F(5, 2), -1, F(-1, 2))
i_dep = i10 - i2                   # V1'den kaynağa (soldan sağa)
assert i_dep == F(-3, 2) and i_dep == i20 + i40
i15 = i33 + i10
assert i15 == F(16, 11)
p15 = -15 * i15
p33 = F(15 ** 2, 33)
p10 = i10 ** 2 * 10
p2 = V1 ** 2 / 2
p20 = V2 ** 2 / 20
p40 = V2 ** 2 / 40
p_dep = vdep * i_dep               # + uç solda, i_dep + uçtan giriyor
assert p15 == F(-240, 11) and p33 == F(75, 11)
assert (p10, p2, p20, p40, p_dep) == (10, F(25, 2), 20, 10, F(-75, 2))
assert abs(float(p15) + 21.82) < 0.005 and abs(float(p33) - 6.82) < 0.005
assert p15 + p33 + p10 + p2 + p20 + p40 + p_dep == 0
assert p15 + p33 == -15            # 15 V + 33 Ω birlikte: net -15 W
v, _ = mna(3, [('V', 1, 0, 15), ('R', 1, 0, 33), ('R', 1, 2, 10), ('R', 2, 0, 2),
               ('VCVS', 2, 3, 5, 2, 0), ('R', 3, 0, 20), ('R', 3, 0, 40)])
assert close(v[2], 5) and close(v[3], -20)
ok("vΔ", vD); ok("vo", vo); ok("p_dep", p_dep)

# ===========================================================================
# 5) ÇY2 s.1 · 6   (3 mA, 4 kΩ, 2 kΩ + 3vo, 1 kΩ)  — kΩ, mA, mW birimleriyle
# ===========================================================================
print("cy2-s1-d6")
# 2 kΩ'un sağ ucu: v2 - 3vo = v2 - 3v2 = -2v2 ; kol akımı (v1 + 2v2)/2  [mA, kΩ]
# v1 ×4: -12 + (v1 - v2) + 2(v1 + 2v2) = 0 -> 3v1 + 3v2 = 12 -> v1 + v2 = 4
# v2 ×4: (v2 - v1) - 2(v1 + 2v2) + 4v2 = 0 -> -3v1 + v2 = 0
assert (1 + 2, -1 + 4) == (3, 3)
assert (-1 - 2, 1 - 4 + 4) == (-3, 1)
v1, v2 = solve2(F(1), F(1), F(4), F(-3), F(1), F(0))
assert v1 == 1 and v2 == 3
vo = v2
vx = v2 - 3 * vo
assert vx == -6
i4k = (v1 - v2) / 4                 # mA, v1 -> v2
i2k = (v1 - vx) / 2                 # mA, v1 -> v2 kolundan
i1k = v2 / 1
assert (i4k, i2k, i1k) == (F(-1, 2), F(7, 2), 3)
assert i4k + i2k == 3 and i1k == i4k + i2k   # KCL
p3mA = -v1 * 3
p4k = (v1 - v2) ** 2 / 4
p2k = i2k ** 2 * 2
p_dep = -(3 * vo) * i2k             # akım - uçtan girip + uçtan çıkıyor
p1k = v2 ** 2 / 1
assert (p3mA, p4k, p2k, p_dep, p1k) == (-3, 1, F(49, 2), F(-63, 2), 9)
assert p3mA + p4k + p2k + p_dep + p1k == 0
v, _ = mna(3, [('I', 0, 1, 3e-3), ('R', 1, 2, 4e3), ('R', 1, 3, 2e3),
               ('VCVS', 2, 3, 3, 2, 0), ('R', 2, 0, 1e3)])
assert close(v[1], 1) and close(v[2], 3) and close(v[3], -6)
ok("v1", v1); ok("v2=vo", v2); ok("p_dep [mW]", p_dep)

print("\n".join(report))
print("TÜM ASSERT'LER GEÇTİ (q3a).")
