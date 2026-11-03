# -*- coding: utf-8 -*-
"""
q1b.py doğrulama betiği — P4.88, P5.119, P5.117, P4.79.
Her problem iki yoldan çözülür:
  (1) adımlarda yazılan elle türetilmiş denklemler (Fraction ile, satır satır),
  (2) bağımsız tam düğüm analizi (numpy, genel MNA benzeri kurulum).
Adımlarda görünen her ara sayı burada assert edilir.
Çalıştır:  python build/verify/q1b_verify.py
"""
from fractions import Fraction as F
import numpy as np

ok = []


def eq(a, b, name, tol=1e-9):
    assert abs(float(a) - float(b)) < tol, f"{name}: {a} != {b}"
    ok.append(name)


def close(a, b, name, tol=5e-3):
    """Ekranda yuvarlatılmış yazılan sayılar için."""
    assert abs(float(a) - float(b)) < tol, f"{name}: {float(a)} ~ {b}"
    ok.append(name)


def solve(A, b):
    return np.linalg.solve(np.array(A, float), np.array(b, float))


# ===========================================================================
# P4.88  — 200 V, 25 Ω, 100 Ω, 10 Ω (i_x ->), 20 Ω + 30 i_x (+ üstte), R_o
# ===========================================================================
# (1) elle türetilen denklemler
# V1: 15V1 - 10V2 = 800  ->  3V1 - 2V2 = 160      (I)
# V2: -5V1 + 6V2 = 0                              (II)
for V1, V2 in [(F(3), F(5)), (F(-7), F(11))]:  # cebirsel genişletmeler özdeş mi
    lhs = 100 * ((V1 - 200) / 25 + V1 / 100 + (V1 - V2) / 10)
    eq(lhs, 4 * (V1 - 200) + V1 + 10 * (V1 - V2), "88 x100 açılımı")
    eq(lhs, 15 * V1 - 10 * V2 - 800, "88 (I) ham")
    ix = (V1 - V2) / 10
    lhs2 = 20 * ((V2 - V1) / 10 + (V2 - 30 * ix) / 20)
    eq(lhs2, 2 * (V2 - V1) + V2 - 3 * V1 + 3 * V2, "88 x20 açılımı")
    eq(lhs2, -5 * V1 + 6 * V2, "88 (II)")
V2 = F(160) / F(16, 10)
eq(V2, 100, "88 V2=100")
V1 = F(6, 5) * V2
eq(V1, 120, "88 V1=120")
eq(3 * V1 - 2 * V2, 160, "88 (I) sağlama")
ix = (V1 - V2) / 10
eq(ix, 2, "88 ix_oc=2")
eq(30 * ix, 60, "88 30ix_oc=60")
eq((V2 - 30 * ix) / 20, 2, "88 i20_oc=2")
Vth88 = V2
# kısa devre
V1s = F(160, 3)
close(V1s, 53.33, "88 V1_sc")
ixs = V1s / 10
eq(ixs, F(16, 3), "88 ix_sc")
close(ixs, 5.333, "88 ix_sc~")
eq(30 * ixs, 160, "88 30ix_sc=160")
i20s = (0 - 30 * ixs) / 20
eq(i20s, -8, "88 i20_sc=-8")
Isc88 = ixs + 8
eq(Isc88, F(40, 3), "88 Isc=40/3")
close(Isc88, 13.33, "88 Isc~")
Rth88 = Vth88 / Isc88
eq(Rth88, F(15, 2), "88 Rth=7.5")
eq(F(300, 40), Rth88, "88 300/40")
Pmax88 = Vth88 ** 2 / (4 * Rth88)
eq(Pmax88, F(1000, 3), "88 Pmax=1000/3")
close(Pmax88, 333.33, "88 Pmax~")
# (c) R_o = 7.5 Ω ile güçler
Ro = Rth88
V2L = Vth88 / 2
eq(V2L, 50, "88 V2_load=50")
V1L = (160 + 2 * V2L) / 3
eq(V1L, F(260, 3), "88 V1_load=260/3")
close(V1L, 86.67, "88 V1_load~")
ixL = (V1L - V2L) / 10
eq(ixL, F(11, 3), "88 ix_load=11/3")
close(ixL, 3.667, "88 ix_load~")
eq(30 * ixL, 110, "88 30ix_load=110")
i20L = (V2L - 30 * ixL) / 20
eq(i20L, -3, "88 i20_load=-3")
iS = (200 - V1L) / 25
eq(iS, F(68, 15), "88 is=68/15")
close(iS, 4.533, "88 is~")
# V2 KCL with load
eq((V2L - V1L) / 10 + i20L + V2L / Ro, 0, "88 V2 KCL yüklü")
p200 = -200 * iS
eq(p200, F(-2720, 3), "88 p200")
close(p200, -906.67, "88 p200~")
pdep = 30 * ixL * i20L
eq(pdep, -330, "88 pdep=-330")
p25 = iS ** 2 * 25
p100 = V1L ** 2 / 100
p10 = ixL ** 2 * 10
p20 = i20L ** 2 * 20
pRo = V2L ** 2 / Ro
eq(p25, F(4624, 9), "88 p25");   close(p25, 513.78, "88 p25~")
eq(p100, F(676, 9), "88 p100");  close(p100, 75.11, "88 p100~")
eq(p10, F(1210, 9), "88 p10");   close(p10, 134.44, "88 p10~")
eq(p20, 180, "88 p20")
eq(pRo, Pmax88, "88 pRo=Pmax")
eq(p200 + pdep + p25 + p100 + p10 + p20 + pRo, 0, "88 sum p = 0")
Pdev = -(p200 + pdep)
eq(Pdev, F(3710, 3), "88 Pdev");  close(Pdev, 1236.67, "88 Pdev~")
close(p25 + p100 + p10 + p20 + pRo, 1236.67, "88 Pabs~")
pct = pRo / Pdev * 100
close(pct, 26.95, "88 yuzde")
eq(pct, F(100000, 3710), "88 yuzde kesir")

# (2) bağımsız: tam düğüm analizi, değişkenler [V1, V2, Vm] (Vm: 20Ω-kaynak arası), R_load parametreli
def p488(RL=None, short=False):
    # bilinmeyenler V1, V2 ; Vm = 30*(V1-V2)/10 = 3V1-3V2
    gL = 0 if RL is None else 1 / RL
    if short:
        V1 = 200 / 25 / (1 / 25 + 1 / 100 + 1 / 10)
        ix = V1 / 10
        return V1, 0.0, ix + (0 - 3 * V1) / -20 * 1  # ix + (Vm-0)/20
    A = [[1 / 25 + 1 / 100 + 1 / 10, -1 / 10],
         [-1 / 10 - 3 / 20, 1 / 10 + 1 / 20 + 3 / 20 + gL]]
    b = [200 / 25, 0]
    return solve(A, b)

V1n, V2n = p488()
eq(V2n, 100, "88 numpy Voc", 1e-6)
_, _, Iscn = p488(short=True)
eq(Iscn, 40 / 3, "88 numpy Isc", 1e-6)
V1n, V2n = p488(RL=7.5)
eq(V2n, 50, "88 numpy V_load", 1e-6)
# R_o taraması: 7.5 Ω gerçekten maksimum mu
best = max(np.linspace(1, 20, 1901), key=lambda R: p488(RL=R)[1] ** 2 / R)
eq(best, 7.5, "88 tarama max", 1e-6)

# ===========================================================================
# P5.119 — 100 V, üst kol (−+) 4Vx + 4Ω, orta 4Ω-4Ω, dikey 4Ω (Vx) + 20 V, R_L
# ===========================================================================
for V1, V2 in [(F(2), F(9)), (F(-5), F(13))]:
    e1 = 4 * ((V1 - 100) / 4 + (V1 - 20) / 4 + (V1 - V2) / 4)
    eq(e1, V1 - 100 + V1 - 20 + V1 - V2, "119 x4 açılım (I)")
    eq(e1, 3 * V1 - V2 - 120, "119 (I)")
    Vx = V1 - 20
    e2 = 4 * ((V2 - V1) / 4 + (V2 - (100 + 4 * Vx)) / 4)
    eq(e2, V2 - V1 + V2 - 100 - 4 * V1 + 80, "119 x4 açılım (II)")
    eq(e2, -5 * V1 + 2 * V2 - 20, "119 (II)")
V1 = F(240 + 20)
eq(V1, 260, "119 V1=260")
V2 = 3 * V1 - 120
eq(V2, 660, "119 V2=660")
eq(-5 * V1 + 2 * V2, 20, "119 (II) sağlama")
Vx = V1 - 20
eq(Vx, 240, "119 Vx=240")
eq(4 * Vx, 960, "119 4Vx=960")
eq(100 + 4 * Vx, 1060, "119 üst düğüm=1060")
eq((V1 - V2) / 4, -100, "119 i orta=-100")
eq((100 + 4 * Vx - V2) / 4, 100, "119 i üst=100")
Vth119 = V2
V1s = F(120, 3)
eq(V1s, 40, "119 V1_sc=40")
Vxs = V1s - 20
eq(Vxs, 20, "119 Vx_sc")
eq(4 * Vxs, 80, "119 4Vx_sc")
eq(100 + 4 * Vxs, 180, "119 üst_sc=180")
i_m = V1s / 4
i_u = (100 + 4 * Vxs) / 4
eq(i_m, 10, "119 i_m=10")
eq(i_u, 45, "119 i_u=45")
Isc119 = i_m + i_u
eq(Isc119, 55, "119 Isc=55")
Rth119 = Vth119 / Isc119
eq(Rth119, 12, "119 Rth=12")
Pmax119 = Vth119 ** 2 / (4 * Rth119)
eq(Vth119 ** 2, 435600, "119 660^2")
eq(Pmax119, 9075, "119 Pmax=9075")
# test-kaynağı sağlaması (bağımsızlar sıfır): 3V1 = VT, I_T = (2VT-5V1)/4 = VT/12
VT = F(1)
V1t = VT / 3
IT = (VT - V1t) / 4 + (VT - 4 * V1t) / 4
eq(VT / IT, 12, "119 test kaynağı Rth=12")

# (2) bağımsız numpy
def p5119(RL=None, short=False):
    gL = 0 if RL is None else 1 / RL
    # V1: (V1-100)/4 + (V1-20)/4 + (V1-V2)/4 = 0
    # V2: (V2-V1)/4 + (V2-100-4(V1-20))/4 + gL V2 = 0
    if short:
        V1 = 120 / 3
        return V1, 0.0, V1 / 4 + (100 + 4 * (V1 - 20)) / 4
    A = [[3 / 4, -1 / 4], [-1 / 4 - 1, 2 / 4 + gL]]
    b = [120 / 4, (100 - 80) / 4]
    return solve(A, b)

eq(p5119()[1], 660, "119 numpy Voc", 1e-6)
eq(p5119(short=True)[2], 55, "119 numpy Isc", 1e-6)
best = max(np.linspace(1, 40, 3901), key=lambda R: p5119(RL=R)[1] ** 2 / R)
eq(best, 12, "119 tarama max", 1e-6)

# ===========================================================================
# P5.117 — 12 V, 4k, 4k, R_L (iç yük, V1-V2 arası), 6k (I_x ↓), 2 mA ↑, 2I_x ↑
# birimler: kΩ, mA, V
# ===========================================================================
V2 = F(2) * 6
eq(V2, 12, "117 V2_oc=12")
Ix = V2 / 6
eq(Ix, 2, "117 Ix_oc=2")
eq(2 * Ix, 4, "117 2Ix_oc=4")
V1 = 12 + 4 * 2 * Ix
eq(V1 - 12, 16, "117 V1-12=16")
eq(V1, 28, "117 V1_oc=28")
Vth117 = V1 - V2
eq(Vth117, 16, "117 Vth=16")
for V in [F(7), F(-3)]:
    e = 12 * ((V - 12) / 4 - 2 * (V / 6) + V / 6 - 2)
    eq(e, 3 * (V - 12) - 2 * V - 24, "117 x12 açılım")
    eq(e, V - 60, "117 sadeleşme")
V = F(60)
Ixs = V / 6
eq(Ixs, 10, "117 Ix_sc=10")
Isc117 = Ixs - 2
eq(Isc117, 8, "117 Isc=8")
eq((V - 12) / 4, 12, "117 sol 4k akımı=12")
eq(2 * Ixs, 20, "117 2Ix_sc=20")
eq(2 * Ixs - (V - 12) / 4, Isc117, "117 a tarafı sağlaması")
Rth117 = Vth117 / Isc117
eq(Rth117, 2, "117 Rth=2k")
Pmax117 = Vth117 ** 2 / (4 * Rth117)  # V^2/kΩ = mW
eq(Vth117 ** 2, 256, "117 256")
eq(Pmax117, 32, "117 Pmax=32 mW")
# test kaynağı sağlaması
It = F(1)
V2t = -6 * It
Ixt = V2t / 6
V1t = 4 * (It + 2 * Ixt)
eq(V1t, -4, "117 test V1")
eq((V1t - V2t) / It, 2, "117 test Rth=2k")

# (2) bağımsız numpy: bilinmeyenler V1, V2 ; R_L parametreli
def p5117(RL=None, short=False):
    if short:
        # süperdüğüm: (V-12)/4 - 2V/6 + V/6 - 2 = 0
        Vv = (3 + 2) / (1 / 4 - 1 / 6)  # (12/4 + 2) / (1/4 - 2/6 + 1/6)
        Vv = (12 / 4 + 2) / (1 / 4 - 2 / 6 + 1 / 6)
        return Vv, Vv, Vv / 6 - 2
    g = 0 if RL is None else 1 / RL
    # V1: (V1-12)/4 - 2*(V2/6) + g(V1-V2) = 0
    # V2: V2/6 - 2 + g(V2-V1) = 0
    A = [[1 / 4 + g, -2 / 6 - g], [-g, 1 / 6 + g]]
    b = [12 / 4, 2]
    return solve(A, b)

v = p5117()
eq(v[0] - v[1], 16, "117 numpy Voc", 1e-6)
eq(p5117(short=True)[2], 8, "117 numpy Isc", 1e-6)
best = max(np.linspace(0.1, 10, 991), key=lambda R: (lambda s: (s[0] - s[1]) ** 2 / R)(p5117(RL=R)))
eq(best, 2, "117 tarama max", 1e-6)

# ===========================================================================
# P4.79 — bağımsız kaynak yok: 100Ω, 200Ω, 150Ω (iΔ ->), 50Ω, 250iΔ (+ üstte)
# test kaynağı V_T (a +, b −)
# ===========================================================================
for V1, VT in [(F(3), F(7)), (F(-2), F(5))]:
    V2 = F(5, 3) * (V1 - VT)
    eq(V2, 250 * (V1 - VT) / 150, "79 V2=250iΔ")
    e = 600 * (V1 / 100 + (V1 - V2) / 200 + (V1 - VT) / 150)
    eq(e, 6 * V1 + 3 * (V1 - V2) + 4 * (V1 - VT), "79 x600 açılım")
    eq(e, 13 * V1 - 3 * V2 - 4 * VT, "79 toplama")
    eq(e, 8 * V1 + VT, "79 yerine koyma")
VT = F(1)
V1 = -VT / 8
iD = (V1 - VT) / 150
eq(iD, F(-3, 400), "79 iΔ=-3VT/400")
V2 = 250 * iD
eq(V2, F(-15, 8), "79 V2=-15VT/8")
eq(VT - V1, F(9, 8), "79 VT-V1")
eq(VT - V2, F(23, 8), "79 VT-V2")
IT = (VT - V1) / 150 + (VT - V2) / 50
eq((VT - V1) / 150, F(3, 400), "79 i150")
eq((VT - V2) / 50, F(23, 400), "79 i50")
eq(IT, F(26, 400), "79 26/400")
eq(IT, F(13, 200), "79 IT=13VT/200")
Rth79 = VT / IT
eq(Rth79, F(200, 13), "79 Rth=200/13")
close(Rth79, 15.38, "79 Rth~")
# V_T = 1 V sayısal sağlama değerleri
eq(V1, F(-1, 8), "79 V1=-0.125");  eq(iD * 1000, F(-15, 2), "79 iΔ=-7.5mA")
eq(V2, F(-15, 8), "79 V2=-1.875")
eq((VT - V1) / 150 * 1000, F(15, 2), "79 7.5mA");  eq((VT - V2) / 50 * 1000, F(115, 2), "79 57.5mA")
eq(IT * 1000, 65, "79 65mA")
# KCL V1 sağlaması (sayısal satır)
eq(V1 / 100 + (V1 - V2) / 200 + (V1 - VT) / 150, 0, "79 V1 KCL")
eq(V1 / 100 * 1000, F(-5, 4), "79 -1.25mA")
eq((V1 - V2) / 200 * 1000, F(35, 4), "79 8.75mA")

# (2) bağımsız numpy: test akımı I_T = 1 A enjekte et, Va ölç ; bilinmeyenler [V1, Va]
# V2 = 250*(V1-Va)/150
A = [[1 / 100 + 1 / 200 + 1 / 150 - (250 / 150) / 200, -1 / 150 + (250 / 150) / 200],
     [-1 / 150 - (250 / 150) / 50, 1 / 150 + 1 / 50 + (250 / 150) / 50]]
V1n, Van = solve(A, [0, 1])
eq(Van, 200 / 13, "79 numpy Rth", 1e-9)
# bağımsız kaynak yokken çözüm sıfır (determinant != 0) -> V_Th = I_sc = 0
assert abs(np.linalg.det(np.array(A))) > 1e-12
ok.append("79 det != 0 -> Voc = Isc = 0")

print(f"q1b doğrulama: {len(ok)} kontrol GEÇTİ")
print(f"  P4.88 : Vth={Vth88} V, Isc={Isc88} A, Rth={Rth88} Ω, Pmax={float(Pmax88):.2f} W, yüzde={float(pct):.2f}%")
print(f"  P5.119: Vth={Vth119} V, Isc={Isc119} A, Rth={Rth119} Ω, Pmax={Pmax119} W")
print(f"  P5.117: Vth={Vth117} V, Isc={Isc117} mA, Rth={Rth117} kΩ, Pmax={Pmax117} mW")
print(f"  P4.79 : Vth=0, Rth={Rth79} = {float(Rth79):.3f} Ω")
