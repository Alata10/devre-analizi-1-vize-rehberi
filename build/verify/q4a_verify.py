# -*- coding: utf-8 -*-
"""
q4a doğrulama: P2.10, P2.32, P2.36, P2.37, P2.9 (güç hesabı / güç dengesi).
Her problem bağımsız olarak (fractions.Fraction ile, tam sayısal) çözülür; adımlardaki
her ara sayı ve her sonuç assert edilir; her devrede sum(p) = 0 kontrol edilir.

Güç: pasif işaret kuralı — p = v * i, i elemanın + ucundan GİRİYORSA.
Çalıştır:  python build/verify/q4a_verify.py
"""
from fractions import Fraction as F


def check_balance(name, powers):
    total = sum(powers.values())
    assert total == 0, f"{name}: sum p = {total} != 0"
    gen = -sum(p for p in powers.values() if p < 0)
    absb = sum(p for p in powers.values() if p > 0)
    assert gen == absb
    print(f"{name}: " + ", ".join(f"{k}={float(v):g}" for k, v in powers.items())
          + f"  | uretilen={float(gen):g}, harcanan={float(absb):g}, toplam=0 OK")
    return gen, absb


# ---------------------------------------------------------------------------
# P2.10   i_phi = 2 A (30 Ω'da aşağı). Üst-sol düğüm A, sağ-üst düğüm B, alt tel 0 V.
#   5 A kaynak: alttan A'ya (ok yukarı).  30 Ω: A -> 0.  2 i_phi: A -> B (ok sağa).
#   10 Ω: A–B.  v_s: + ucu B'de, - ucu altta.
# ---------------------------------------------------------------------------
def p2_10():
    i_phi = F(2)
    vA = 30 * i_phi
    assert vA == 60
    i_dep = 2 * i_phi
    assert i_dep == 4
    # KCL @A (çıkan +, giren -):  -5 + i_phi + i_dep + i10 = 0   (i10: A -> B)
    i10 = 5 - i_phi - i_dep
    assert i10 == -1
    vB = vA - 10 * i10
    assert vB == 70
    vs = vB
    # KCL @B: -i10 - i_dep + i_s = 0   (i_s: B'den aşağı, v_s'nin + ucuna giriyor)
    i_s = i10 + i_dep
    assert i_s == 3
    P = {
        "5A": -(vA * 5),                 # akım + uçtan çıkıyor
        "30ohm": i_phi ** 2 * 30,
        "10ohm": i10 ** 2 * 10,
        "2iphi": (vA - vB) * i_dep,      # akım A ucundan giriyor; A'yı + kabul et
        "vs": vs * i_s,                  # akım + uçtan giriyor
    }
    assert P["5A"] == -300 and P["30ohm"] == 120 and P["10ohm"] == 10
    assert P["2iphi"] == -40 and P["vs"] == 210
    gen, absb = check_balance("P2.10", P)
    assert gen == 340 and absb == 340
    assert P["30ohm"] + P["10ohm"] == 130
    return dict(vs=vs)


# ---------------------------------------------------------------------------
# P2.32   45 A (ok yukarı) -> düğüm A. 6 Ω: A -> 0 (i_x aşağı). 2 Ω: A–B (+v_o- soldan sağa).
#   2 i_x bağımlı gerilim kaynağı: + ucu B'de (üstte).
# ---------------------------------------------------------------------------
def p2_32():
    # vA = 6 i_x ; vB = 2 i_x ; i_2Ω (A->B) = (vA - vB)/2 = 2 i_x
    # KCL @A: -45 + i_x + 2 i_x = 0
    i_x = F(45, 3)
    assert i_x == 15
    vA, vB = 6 * i_x, 2 * i_x
    assert (vA, vB) == (90, 30)
    i2 = (vA - vB) / 2
    assert i2 == 30 == 2 * i_x
    vo = vA - vB
    assert vo == 60 == 2 * i2
    P = {
        "45A": -(vA * 45),
        "6ohm": i_x ** 2 * 6,
        "2ohm": i2 ** 2 * 2,
        "dep2ix": (2 * i_x) * i2,        # 30 A, + uçtan (üstten) giriyor
    }
    assert P == {"45A": -4050, "6ohm": 1350, "2ohm": 1800, "dep2ix": 900}
    gen, absb = check_balance("P2.32", P)
    assert gen == 4050
    return dict(vo=vo, Psup=gen)


# ---------------------------------------------------------------------------
# P2.36   Üst tel: 50 V(+üst) -> T ; 20 i_s (- sol,+ sağ) T->A ; A: 18 Ω (i_D aşağı) ;
#   5 i_s (+ sol, - sağ) A->B ; B: 40 Ω (i_s aşağı, v_o + üstte) ; 8 i_D (ok sağa) B->C ;
#   C: 20 V (+ üst).
# ---------------------------------------------------------------------------
def p2_36():
    # vA = 50 + 20 i_s ; vB = vA - 5 i_s = 50 + 15 i_s ; vB = 40 i_s
    i_s = F(50, 40 - 15)
    assert i_s == 2
    vA = 50 + 20 * i_s
    vB = vA - 5 * i_s
    assert vA == 90 and vB == 80 and vB == 40 * i_s
    vo = vB
    i_D = vA / 18
    assert i_D == 5
    i8 = 8 * i_D
    assert i8 == 40
    # KCL @B: -i_AB + i_s + i8 = 0
    i_AB = i_s + i8
    assert i_AB == 42
    # KCL @A: -i_TA + i_D + i_AB = 0
    i_TA = i_D + i_AB
    assert i_TA == 47
    vC = 20
    P = {
        "50V": -(50 * i_TA),             # + uçtan çıkıyor
        "20is": -(20 * i_s) * i_TA,      # 40 V; akım - uçtan girip + uçtan çıkıyor
        "18ohm": i_D ** 2 * 18,
        "5is": (5 * i_s) * i_AB,         # 10 V; akım + uçtan giriyor
        "40ohm": i_s ** 2 * 40,
        "8iD": (vB - vC) * i8,           # akım B (80 V) ucundan giriyor
        "20V": 20 * i8,                  # akım + uçtan giriyor
    }
    assert P == {"50V": -2350, "20is": -1880, "18ohm": 450, "5is": 420,
                 "40ohm": 160, "8iD": 2400, "20V": 800}
    gen, absb = check_balance("P2.36", P)
    assert gen == 4230
    return dict(i_D=i_D, vo=vo)


# ---------------------------------------------------------------------------
# P2.37   v_o = 5 V. Üç ayrı bölüm, yalnız alt telle bağlı.
#   Sağ: 40 i_2 (ok aşağı) || 40 Ω || 10 Ω, gerilim v_o.
#   Orta: 25 i_1 (ok aşağı) || 20 Ω || 80 Ω, gerilim v_1; i_2 = 80 Ω'a giren akım.
#   Sol: v_g -> 60 Ω (i_1 sağa) -> 260 Ω -> geri (seri).
# ---------------------------------------------------------------------------
def p2_37():
    vo = F(5)
    i40, i10 = vo / 40, vo / 10
    assert i40 == F(1, 8) and i10 == F(1, 2)
    # KCL üst sağ düğüm: 40 i_2 + v_o/40 + v_o/10 = 0
    dep2 = -(i40 + i10)
    assert dep2 == F(-5, 8)
    i2 = dep2 / 40
    assert i2 == F(-1, 64)           # -15.625 mA
    v1 = 80 * i2
    assert v1 == F(-5, 4)            # -1.25 V
    i20 = v1 / 20
    assert i20 == F(-1, 16)          # -62.5 mA
    # KCL üst orta düğüm: 25 i_1 + v1/20 + i2 = 0
    dep1 = -(i20 + i2)
    assert dep1 == F(5, 64)          # 78.125 mA
    i1 = dep1 / 25
    assert i1 == F(1, 320)           # 3.125 mA
    vg = (60 + 260) * i1
    assert vg == 1
    P_left = {"vg": -(vg * i1), "60ohm": i1 ** 2 * 60, "260ohm": i1 ** 2 * 260}
    P_mid = {"25i1": v1 * dep1, "20ohm": v1 ** 2 / 20, "80ohm": v1 ** 2 / 80}
    P_right = {"40i2": vo * dep2, "40ohm": vo ** 2 / 40, "10ohm": vo ** 2 / 10}
    # mW cinsinden
    assert P_left["vg"] * 1000 == F(-25, 8)          # -3.125 mW
    assert P_left["60ohm"] * 1000 == F(75, 128)      # 0.5859375 mW
    assert P_left["260ohm"] * 1000 == F(325, 128)    # 2.5390625 mW
    assert P_mid["25i1"] * 1000 == F(-3125, 32)      # -97.65625 mW
    assert P_mid["20ohm"] * 1000 == F(625, 8)        # 78.125 mW
    assert P_mid["80ohm"] * 1000 == F(625, 32)       # 19.53125 mW
    assert P_right == {"40i2": F(-25, 8), "40ohm": F(5, 8), "10ohm": F(5, 2)}
    for nm, P in (("P2.37 sol", P_left), ("P2.37 orta", P_mid), ("P2.37 sag", P_right)):
        check_balance(nm, P)
    allP = {**P_left, **P_mid, **P_right}
    gen, absb = check_balance("P2.37 tum", allP)
    assert gen * 1000 == F(25, 8) + F(3125, 32) + 3125   # 3225.78125 mW
    return dict(v1=v1, vg=vg)


# ---------------------------------------------------------------------------
# P2.9 (ÇY1 s.7 — bölüm içi değerlendirme problemi 2.9)
#   5 V (+ üst) -> 54 kΩ (i_1 sağa) -> 1 V (- sol, + sağ) -> düğüm A ; A: 6 kΩ -> 0 ;
#   A <- 30 i_1 (ok sola, A'ya doğru; + v - : + sol) <- 1.8 kΩ <- 8 V (+ üst).
# ---------------------------------------------------------------------------
def p2_9():
    k = 1000
    # vA = 5 - 54k i1 + 1 ;  KCL @A: -i1 - 30 i1 + vA/6k = 0 -> vA = 186k i1
    i1 = F(6, 240 * k)
    assert i1 == F(25, 10 ** 6)                     # 25 µA
    vA = 186 * k * i1
    assert vA == F(465, 100)                         # 4.65 V
    assert vA == 5 - 54 * k * i1 + 1
    i6 = vA / (6 * k)
    assert i6 == 31 * i1 == F(775, 10 ** 6)
    idep = 30 * i1
    assert idep == F(750, 10 ** 6)                   # 0.75 mA (sağdan sola)
    vR = 8 - F(18, 10) * k * idep
    assert vR == F(665, 100)                         # 6.65 V
    v = vA - vR
    assert v == -2
    u = 10 ** 6  # µW
    P = {
        "5V": -(5 * i1),
        "54k": i1 ** 2 * 54 * k,
        "1V": -(1 * i1),                 # akım - uçtan girip + uçtan çıkıyor
        "6k": i6 ** 2 * 6 * k,
        "dep30i1": -(v * idep),          # akım + (sol) uçtan ÇIKIYOR
        "1.8k": idep ** 2 * F(18, 10) * k,
        "8V": -(8 * idep),
    }
    expect_uW = {"5V": -125, "54k": F(3375, 100), "1V": -25, "6k": F(360375, 100),
                 "dep30i1": 1500, "1.8k": F(10125, 10), "8V": -6000}
    for key, val in expect_uW.items():
        assert P[key] * u == val, (key, P[key] * u)
    gen, absb = check_balance("P2.9", P)
    assert gen * u == 6150 and absb * u == 6150
    return dict(i1=i1, v=v)


if __name__ == "__main__":
    r = {}
    r["p2-10"] = p2_10()
    r["p2-32"] = p2_32()
    r["p2-36"] = p2_36()
    r["p2-37"] = p2_37()
    r["p2-9"] = p2_9()
    print("\nSonuclar:", {k: {kk: str(vv) for kk, vv in v.items()} for k, v in r.items()})
    print("TUM ASSERTLER GECTI.")
