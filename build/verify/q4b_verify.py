# -*- coding: utf-8 -*-
"""
q4b doğrulama — Soru 4 (güç hesabı / güç dengesi), ÇY1 problemleri.
Her problem bağımsız olarak Fraction ile çözülür; ara ve son sonuçlar assert edilir, Σp = 0 kontrol edilir.
Çalıştır:  python build/verify/q4b_verify.py
"""
from fractions import Fraction as F


def check_sum_zero(name, powers):
    s = sum(powers.values())
    assert s == 0, f"{name}: Σp = {s} ≠ 0  ({powers})"
    absorbed = sum(v for v in powers.values() if v > 0)
    delivered = -sum(v for v in powers.values() if v < 0)
    print(f"  {name}: Σp = 0  (emilen {float(absorbed):.4g} = üretilen {float(delivered):.4g})")
    return absorbed


# ---------------------------------------------------------------------------
# Şekil 2.23 (Örnek 2.10)
#   Sol göz: 10 V (+ üstte) ile 6 Ω paralel; i_s üst telde sağa (kaynağın + ucundan çıkar).
#   Sağ göz: 3 i_s (+ üstte) → 2 Ω (i_o sağa) → 3 Ω (v_o + üstte). Gözler yalnız alt telden ortak.
# ---------------------------------------------------------------------------
def fig2_23():
    i_s = F(10, 6)
    assert i_s == F(5, 3)
    v_dep = 3 * i_s
    assert v_dep == 5
    # sağ göz KVL (saat yönü): -3i_s + 2 i_o + 3 i_o = 0
    i_o = v_dep / (2 + 3)
    assert i_o == 1
    v_o = 3 * i_o
    assert v_o == 3
    p = {
        "10V": -10 * i_s,          # akım + uçtan çıkıyor
        "6Ω": 6 * i_s ** 2,
        "3is": -v_dep * i_o,       # akım + uçtan çıkıyor
        "2Ω": 2 * i_o ** 2,
        "3Ω": 3 * i_o ** 2,
    }
    assert p["10V"] == F(-50, 3) and p["6Ω"] == F(50, 3)
    assert p["3is"] == -5 and p["2Ω"] == 2 and p["3Ω"] == 3
    tot = check_sum_zero("Şekil 2.23", p)
    assert tot == F(65, 3)          # 21.67 W
    print(f"  v_o = {v_o} V, i_s = {i_s} A, i_o = {i_o} A")


# ---------------------------------------------------------------------------
# P2.1  : i_b/4 (+ üstte) || v_g (+ üstte) || 8 A (ok aşağı). i_b üst sağ telde sola.
# ---------------------------------------------------------------------------
def p2_1():
    # 8 A kaynağı akımı üst telden çekip aşağı basar → üst sağ telde akım sağa 8 A → i_b (sola) = -8 A
    i_b = F(-8)
    v_dep = i_b / 4
    assert v_dep == -2
    v_g = v_dep                      # paralel gerilim kaynakları eşit olmalı
    assert v_g == -2
    # 8 A: akım + (üst) uçtan giriyor → p = +v i
    p8 = v_g * 8
    assert p8 == -16
    # İki gerilim kaynağının (aşağı yönlü) akımları toplamı: KCL üst düğüm: i1 + i2 + 8 = 0
    i_sum_down = F(-8)
    p_vsources = v_g * i_sum_down    # her ikisi de + üstte, akım aşağı = + uçtan giriş
    assert p_vsources == 16
    assert p8 + p_vsources == 0
    print(f"  P2.1: v_g = {v_g} V, p_8A = {p8} W, p(iki V kaynağı toplam) = {p_vsources} W, Σp = 0")


# ---------------------------------------------------------------------------
# P2.2  : seri göz. 15 A (sol, ok aşağı) → saatin tersi 15 A.
#          αv_x üstte ok sağa (saat yönü). 25 V sağda: − üstte, + altta; v_x + üstte → v_x = -25 V.
# ---------------------------------------------------------------------------
def p2_2():
    v_x = F(-25)
    i_cw = F(-15)                    # 15 A saatin tersi = -15 A saat yönü
    alpha = i_cw / v_x               # α v_x = i_cw
    assert alpha == F(3, 5)
    assert alpha * v_x == -15
    # 25 V: akım saatin tersi → sağ kolda aşağıdan yukarı, alt (+) uçtan girer
    p25 = 25 * 15
    assert p25 == 375
    # akım kaynaklarının toplamı: V_a (sol üst) ne olursa olsun
    for V_a in (F(0), F(7), F(-100)):
        p15 = V_a * 15                       # akım üstten (V_a) girip aşağı iner, + üstte
        p_dep = (F(-25) - V_a) * 15          # 15 A sağdan sola akar: + sağ uçta, sağ uç = -25 V
        assert p15 + p_dep == -375
        assert p15 + p_dep + p25 == 0
    print(f"  P2.2: α = {alpha} A/V, p_25V = {p25} W (emer), iki akım kaynağı toplam = -375 W, Σp = 0")


# ---------------------------------------------------------------------------
# P2.15 : hepsi paralel (V üst ray). Birimler: V, mA, kΩ → güç mW.
#   6 kΩ, 6 mA (ok yukarı), 3 I_x (ok aşağı), 3 mA (ok aşağı), 2 kΩ (I_x aşağı), 3 kΩ (I_L aşağı)
# ---------------------------------------------------------------------------
def p2_15():
    # KCL (çıkan +): V/6 - 6 + 3(V/2) + 3 + V/2 + V/3 = 0
    coef = F(1, 6) + F(3, 2) + F(1, 2) + F(1, 3)
    assert coef == F(5, 2)
    # ×6: V - 36 + 9V + 18 + 3V + 2V = 0 → 15V = 18
    assert 1 + 9 + 3 + 2 == 15 and 36 - 18 == 18
    V = F(18, 15)
    assert V == F(6, 5)
    assert V / 6 - 6 + 3 * (V / 2) + 3 + V / 2 + V / 3 == 0
    I_x = V / 2
    I_L = V / 3
    assert I_x == F(3, 5) and I_L == F(2, 5)
    dep = 3 * I_x
    assert dep == F(9, 5)
    p = {
        "6k": V ** 2 / 6,
        "6mA": -V * 6,     # ok yukarı: akım + uçtan çıkar
        "3Ix": V * dep,    # ok aşağı: akım + uçtan girer
        "3mA": V * 3,
        "2k": V ** 2 / 2,
        "3k": V ** 2 / 3,
    }
    assert p["6k"] == F(6, 25) and p["6mA"] == F(-36, 5) and p["3Ix"] == F(54, 25)
    assert p["3mA"] == F(18, 5) and p["2k"] == F(18, 25) and p["3k"] == F(12, 25)
    check_sum_zero("P2.15 (mW)", p)
    print(f"  V = {V} V, I_x = {I_x} mA, I_L = {I_L} mA")


# ---------------------------------------------------------------------------
# P2.18 : seri göz. 45 V (+ üstte), 1 Ω üstte (V_o + solda), 3V_o sağda (− üstte, + altta), 5 Ω altta.
# ---------------------------------------------------------------------------
def p2_18():
    # i saat yönü; V_o = 1·i ; KVL: -45 + V_o - 3V_o + 5 i = 0
    # → -45 + i - 3i + 5i = 0 → 3i = 45
    i = F(45, 3)
    assert i == 15
    V_o = 1 * i
    assert -45 + V_o - 3 * V_o + 5 * i == 0
    dep = 3 * V_o
    assert dep == 45
    p = {
        "45V": -45 * i,     # akım + (üst) uçtan çıkar
        "1Ω": 1 * i ** 2,
        "3Vo": -dep * i,    # akım − (üst) uçtan girip + (alt) uçtan çıkar
        "5Ω": 5 * i ** 2,
    }
    assert p["45V"] == -675 and p["1Ω"] == 225 and p["3Vo"] == -675 and p["5Ω"] == 1125
    check_sum_zero("P2.18", p)
    print(f"  i = {i} A, V_o = {V_o} V, P_5Ω = {p['5Ω']} W")


if __name__ == "__main__":
    fig2_23()
    p2_1()
    p2_2()
    p2_15()
    p2_18()
    print("q4b: TÜM KONTROLLER GEÇTİ")
