# -*- coding: utf-8 -*-
"""
q3b doğrulama: P4.42, P4.48, P4.52, P4.53, ÇY2 s.2 d.4.
Çalıştır: python build/verify/q3b_verify.py
"""
from fractions import Fraction as F


def p4_42():
    # Çevre akımları (saat yönünde): i1 (sol alt), i2 (sağ alt), i3 (üst)
    # Sol 30V (+ üst, - alt), Sağ 30V (- üst, + alt), Üst 53 i_Delta (+ sol, - sağ)
    # i_Delta = i1 - i2
    i1, i2, i3 = F(52), F(60), F(110)
    iD = i1 - i2
    assert iD == -8
    assert -30 + 3 * (i1 - i3) + 20 * (i1 - i2) + 7 * i1 == 0
    assert 20 * (i2 - i1) + 5 * (i2 - i3) - 30 + 2 * i2 == 0
    assert 53 * iD + 5 * (i3 - i2) + 3 * (i3 - i1) == 0
    P = {
        "30V_sol": -30 * i1,
        "30V_sag": -30 * i2,
        "53iD": (53 * iD) * i3,
        "3ohm": (i1 - i3) ** 2 * 3,
        "5ohm": (i2 - i3) ** 2 * 5,
        "20ohm": iD ** 2 * 20,
        "7ohm": i1 ** 2 * 7,
        "2ohm": i2 ** 2 * 2,
    }
    assert P["20ohm"] == 1280
    assert P["53iD"] == -46640
    assert sum(P.values()) == 0
    return P


def p4_48():
    # Çevre akımları (saat yönünde): i1 (sol), i2 (orta), i3 (sağ)
    # v_Delta = 2 * i1, i_Delta = i2
    # i3 = -1.7 * v_Delta = -3.4 * i1
    i1, i2, i3 = F(-5), F(16), F(17)
    vD = 2 * i1
    iD = i2
    assert vD == -10 and iD == 16
    assert i3 == F(-17, 10) * vD
    assert -50 + 2 * i1 + 4 * (i1 - i2) + 9 * iD == 0
    assert -9 * iD + 4 * (i2 - i1) + 5 * i2 + 20 * (i2 - i3) == 0
    # 1.7 v_Delta kaynağı sağ kolda yukarı doğru (i3 saat yönünde aşağı doğru -> kaynak akımı = -i3 = -17 A yukarı)
    # Sağ üst düğüm gerilimi V_R = 20 * (i2 - i3) = 20 * (16 - 17) = -20 V
    VR = 20 * (i2 - i3)
    assert VR == -20
    P = {
        "50V": -50 * i1,
        "9iD": (9 * iD) * (i1 - i2),
        "1.7vD": -VR * (F(17, 10) * vD),
        "2ohm": i1 ** 2 * 2,
        "4ohm": (i1 - i2) ** 2 * 4,
        "5ohm": i2 ** 2 * 5,
        "20ohm": (i2 - i3) ** 2 * 20,
    }
    assert P["9iD"] == -3024
    assert sum(P.values()) == 0
    return P


def p4_52():
    # Çevre akımları (saat yönünde): i1 (sol alt), i2 (sol üst), i3 (sağ)
    # i_a = i2, i_b = i1, i_c = i3, i_d = i1 - i2, i_e = i1 - i3
    i1, i2, i3 = F(23, 5), F(57, 10), F(97, 100)
    ia, ib, ic = i2, i1, i3
    id_, ie = i1 - i2, i1 - i3
    assert (ia, ib, ic, id_, ie) == (F(57, 10), F(23, 5), F(97, 100), F(-11, 10), F(363, 100))
    assert -200 + 25 * (i1 - i2) + 50 * (i1 - i3) + 10 * i1 == 0
    assert i3 - i2 == F(43, 10) * id_
    assert 10 * i2 + 100 * i3 + 50 * (i3 - i1) + 25 * (i2 - i1) == 0
    return dict(ia=ia, ib=ib, ic=ic, id=id_, ie=ie)


def p4_53():
    # Düğüm gerilimleri: V1 (40 ohm üstü), V2 (2*ib üstü), V3 (240V üstü = -240 V)
    V1, V2, V3 = F(-280), F(-320), F(-240)
    ia = V1 / 40
    ib = (V2 - V1) / 5
    ic = (V3 - V2) / 10
    assert (ia, ib, ic) == (-7, -8, 8)
    # V3 - V1 = 4 * id -> id = (V3 - V1)/4 = 10 A
    id_ = (V3 - V1) / 4
    assert id_ == 10
    # Düğüm V2 KCL: -ib + ic - 2*ib = 0 -> ic = 3*ib? Wait:
    # i_b oku sola (V2 -> V1): V2'den sola çıkan akım i_b = (V2 - V1)/5 = -8 A.
    # i_c oku sola (V3 -> V2): V2'ye sağdan giren akım i_c = (V3 - V2)/10 = +8 A.
    # 2*i_b kaynağı aşağıdan yukarı (V2'ye giren): 2*i_b = -16 A.
    # KCL @ V2 (çıkanlar +): i_b - i_c - 2*i_b = -i_b - i_c = -(-8) - 8 = 0! TAM TUTUYOR!
    assert ib - ic - 2 * ib == 0
    # Düğüm V1 KCL: -19 + ia - ib + ie = 0 -> ie = 19 - ia + ib = 19 - (-7) + (-8) = 18 A
    ie = 19 - ia + ib
    assert ie == 18
    # Düğüm V3 KCL: ic + id - ie = 8 + 10 - 18 = 0! TAM TUTUYOR!
    assert ic + id_ - ie == 0
    P = {
        "19A": -V1 * 19,
        "40ohm": ia ** 2 * 40,
        "5ohm": ib ** 2 * 5,
        "10ohm": ic ** 2 * 10,
        "2ib": -V2 * (2 * ib),
        "4id": (V1 - V3) * ie,
        "240V": V3 * id_,
    }
    assert sum(P.values()) == 0
    return P


def cy2_s2_d4():
    v1, v2, v3 = F(156), F(120), F(78)
    io = v2 / 40
    assert io == 3
    assert -5 * io + v1 / 20 + (v1 - v2) / 5 == 0
    assert (v2 - v1) / 5 + v2 / 40 + (v2 - v3) / 10 == 0
    assert (v3 - v2) / 10 + (v3 - F(23, 2) * io) / 5 + (v3 - 96) / 4 == 0
    return dict(v1=v1, v2=v2, v3=v3, io=io)


if __name__ == "__main__":
    p4_42()
    p4_48()
    p4_52()
    p4_53()
    cy2_s2_d4()
    print("q3b dogrulama: TUM ASSERTLER GECTI.")
