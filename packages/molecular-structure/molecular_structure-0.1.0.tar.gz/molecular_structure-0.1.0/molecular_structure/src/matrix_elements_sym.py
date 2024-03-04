import sympy as sy
import numpy as sy
from sympy.physics.wigner import wigner_3j, wigner_6j, wigner_9j

"""
Each matrix element is a function of an isyut state vector and an output
state vector.
The matrix elements are packaged into dictionaries. Each Hund's Case in the
molecule gets a separate dictionary. Dictionaries are at the end of the file.
"""


def kronecker(a, b):  # Kronecker delta function
    return int(a == b)


def b2a_matrix(a, b, S=1 / 2):
    if (
        not kronecker(a["K"], b["K"])
        * kronecker(a["J"], b["J"])
        * kronecker(a["F"], b["F"])
        * kronecker(a["M"], b["M"])
    ):
        return 0
    else:
        if "F1" in b.keys():
            if not kronecker(a["F1"], b["F1"]):
                return 0
        return (
            (-1) ** (b["N"] - S + a["P"])
            * sy.sqrt(2 * b["N"] + 1)
            * wigner_3j(a["J"], S, b["N"], a["P"], -a["Sigma"], -a["K"])
        )


def decouple_b_even(dcpl, b, S=1 / 2, I=1 / 2):  # dcpl = decoupled
    if (
        not kronecker(dcpl["M_F"], b["M"])
        * kronecker(dcpl["K"], b["K"])
        * kronecker(dcpl["N"], b["N"])
    ):
        return 0
    else:
        M_J = dcpl["M_N"] + dcpl["M_S"]
        if I == 0:
            if not kronecker(M_J, b["M"]):
                return 0
            else:
                return (
                    (-1) ** (S - b["N"] + M_J)
                    * sy.sqrt(2 * b["J"] + 1)
                    * wigner_3j(b["N"], S, b["J"], dcpl["M_N"], dcpl["M_S"], -M_J)
                )
        else:
            return (
                (-1) ** (I - b["J"] + dcpl["M_F"] + S - b["N"] + M_J)
                * sy.sqrt((2 * b["F"] + 1) * (2 * b["J"] + 1))
                * wigner_3j(b["J"], I, b["F"], M_J, dcpl["M_I"], -dcpl["M_F"])
                * wigner_3j(b["N"], S, b["J"], dcpl["M_N"], dcpl["M_S"], -M_J)
            )


def recouple_J_even(
    dcpl_a, dcpl_b, S=1 / 2, I=1 / 2
):  # This function "recouples" M_N and M_S (ie dcpl_b) to form J, M_J (ie dcpl_a)
    if (
        not kronecker(dcpl_a["M_F"], dcpl_b["M_F"])
        * kronecker(dcpl_a["K"], dcpl_b["K"])
        * kronecker(dcpl_a["N"], dcpl_b["N"])
    ):
        return 0
    else:
        return (-1) ^ (S - dcpl_b["N"] + dcpl_b["M_F"]) * sy.sqrt(
            2 * dcpl_a["J"] + 1
        ) * wigner_3j(
            dcpl_b["N"], S, dcpl_a["J"], dcpl_b["M_N"], dcpl_b["M_S"], -dcpl_a["M_J"]
        )


def bBS_2_bBJ_matrix(bBS, bBJ, S=1 / 2, I=5 / 2):
    if "F1" in bBJ.keys():
        F = bBJ["F1"]
        if (
            not kronecker(bBS["F1"], bBJ["F1"])
            * kronecker(bBS["M"], bBJ["M"])
            * kronecker(bBS["N"], bBJ["N"])
            * kronecker(bBS["F"], bBJ["F"])
        ):
            return 0
    else:
        F = bBJ["F"]
        if (
            not kronecker(bBS["M"], bBJ["M"])
            * kronecker(bBS["N"], bBJ["N"])
            * kronecker(bBS["F"], bBJ["F"])
        ):
            return 0
    N = bBJ["N"]
    G = bBS["G"]
    J = bBJ["J"]
    return (
        (-1) ** (I + S + F + N)
        * sy.sqrt((2 * G + 1) * (2 * J + 1))
        * wigner_6j(I, S, G, N, F, J)
    )


# Case bBJ ##############


def Parity_l_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(K0, -K1)
        * kronecker(N0, N1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
    ):
        return 0
    else:
        return (-1) ** (N0 + abs(K0))


def Parity_L_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(K0, -K1)
        * kronecker(N0, N1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
    ):
        return 0
    else:
        return (-1) ** (N0)


def Rot_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(K0, K1)
        * kronecker(N0, N1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
    ):
        return 0
    else:
        return N0 * (N0 + 1) - K0**2


def SR_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(K0, K1)
        * kronecker(J0, J1)
        * kronecker(N0, N1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
    ):
        return 0
    else:
        return (
            (-1) ** (N0 + J0 + S)
            * sy.sqrt(S * (S + 1) * (2 * S + 1) * N0 * (N0 + 1) * (2 * N0 + 1))
            * wigner_6j(S, N0, J0, N0, S, 1)
        )


def IS_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(K0, K1)
        * kronecker(N0, N1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
    ):
        return 0
    else:
        return (
            (-1) ** (J1 + F0 + I + J0 + N0 + S + 1)
            * sy.sqrt(
                (2 * J1 + 1)
                * (2 * J0 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
            )
            * wigner_6j(I, J1, F0, J0, I, 1)
            * wigner_6j(J0, S, N0, S, J1, 1)
        )


def T2IS_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if not kronecker(F0, F1) * kronecker(M0, M1) * kronecker(K0, K1):
        return 0
    else:
        return (
            -sy.sqrt(5 / 3)
            * (-1) ** (3 * F0 - 2 * M0 + I + J0 + N0 - K0)
            * sy.sqrt((2 * I + 1) * (I + 1) * I)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * 3 * (2 * S + 1) * (S + 1) * S)
            * wigner_6j(I, J1, F0, J0, I, 1)
            * wigner_9j(S, N1, J1, 1, 2, 1, S, N0, J0)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1))
            * wigner_3j(N0, 2, N1, -K0, 0, K1)
        )


def Iz_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if not kronecker(F0, F1) * kronecker(M0, M1):
        return 0
    else:
        return (
            (-1) ** (I + F0 + S - K0 + 1)
            * sy.sqrt(
                (2 * J1 + 1)
                * (2 * J0 + 1)
                * (2 * N0 + 1)
                * (2 * N1 + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
            )
            * wigner_6j(J1, I, F0, I, J0, 1)
            * wigner_6j(N1, J1, S, J0, N0, 1)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
        )


def Sz_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if not kronecker(F0, F1) * kronecker(M0, M1) * kronecker(J0, J1):
        return 0
    else:
        return (
            (-1) ** (N1 + N0 + S + J0 - K0)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1) * S * (S + 1) * (2 * S + 1))
            * wigner_6j(N1, S, J0, S, N0, 1)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
        )


def NzSz_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(K0, K1)
    ):
        return 0
    else:
        return (
            K0
            * (-1) ** (N1 + N0 + S + J0 - K0)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1) * S * (S + 1) * (2 * S + 1))
            * wigner_6j(N1, S, J0, S, N0, 1)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
        )


def ZeemanZ_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if not kronecker(K0, K1) * kronecker(M0, M1) * kronecker(N0, N1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0 + F1 + 2 * J0 + I + N0 + S)
            * sy.sqrt(
                (2 * F0 + 1)
                * (2 * F1 + 1)
                * (2 * J0 + 1)
                * (2 * J1 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
            )
            * wigner_6j(F0, J0, I, J1, F1, 1)
            * wigner_6j(J0, S, N0, S, J1, 1)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
        )


# def Zeemasylus_bBJ():

# def ZeemanMinus_bBJ():


def StarkZ_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if not kronecker(M0, M1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0 + J0 + I + 2 + F1 + S + J1 - K0)
            * sy.sqrt(
                (2 * F0 + 1)
                * (2 * F1 + 1)
                * (2 * J0 + 1)
                * (2 * J1 + 1)
                * (2 * N0 + 1)
                * (2 * N1 + 1)
            )
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * wigner_6j(J1, F1, I, F0, J0, 1)
            * wigner_6j(N1, J1, S, J0, N0, 1)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
        )


def p_lD_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(M0, M1)
        * kronecker(F0, F1)
        * kronecker(J0, J1)
        * (not kronecker(K0, K1))
    ):
        return 0
    else:
        return sum(
            [
                (-1) ** (-2 * M0 + 2 * I + 3 * J0 + S + N0)
                * -sy.sqrt(10 / 6)
                * wigner_6j(S, N0, J0, N1, S, 1)
                * sy.sqrt(S * (S + 1) * (2 * S + 1))
                * sy.sqrt(3)
                * (-1) ** (1 + N0 + N1)
                * wigner_6j(2, 1, 1, N1, N0, N0)
                * sy.sqrt(N0 * (N0 + 1) * (2 * N0 + 1))
                * (-1) ** (N0 - K0)
                * wigner_3j(N0, 2, N1, -K0, 2 * q, K1)
                * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1))
                * kronecker(K0, K1 + 2 * q)
                for q in [-1, 1]
            ]
        )


def q_lD_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):
    if (
        not kronecker(M0, M1)
        * kronecker(F0, F1)
        * kronecker(J0, J1)
        * (not kronecker(K0, K1))
    ):
        return 0
    else:
        return sum(
            [
                (-1) ** (-2 * M0 + 2 * I + 2 * J0)
                * sy.sqrt((2 * J1 + 1))
                * (-1) ** (S + J1 + N1)
                * wigner_6j(N1, J1, S, J0, N0, 0)
                * sy.sqrt(5)
                * (-1) ** (N0 + N1)
                * wigner_6j(2, 2, 0, N1, N0, N0)
                * (-1) ** (N0 + K0)
                * wigner_3j(N0, 2, N1, -K0, 2 * q, K1)
                * 1
                / (2 * sy.sqrt(6))
                * sy.sqrt(
                    (2 * N0 - 1)
                    * (2 * N0)
                    * (2 * N0 + 1)
                    * (2 * N0 + 2)
                    * (2 * N0 + 3)
                    * (2 * N0 + 1)
                    * (2 * N1 + 1)
                )
                * kronecker(K0, K1 + 2 * q)
                for q in [-1, 1]
            ]
        )  # there is ambiguity over the inclusion of extra sqrt(2J0+1)


def lD_bBJ(K0, N0, J0, F0, M0, K1, N1, J1, F1, M1, S=1 / 2, I=1 / 2):  # effective term
    if (
        not kronecker(N0, N1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(F0, F1)
        * (not kronecker(K0, K1))
    ):
        return 0
    else:
        delta_L = K0 - K1
        return (
            N0
            * (N0 + 1)
            * (
                kronecker(delta_L, -2) * (-1) ** (-abs(K0))
                + kronecker(delta_L, 2) * (-1) ** (abs(K0))
            )
        )


# Case bBS ##############


def Rot_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
        * kronecker(G0, G1)
        * kronecker(N0, N1)
    ):
        return 0
    else:
        return (-1) ** (-2 * M0 + 2 * iH + 2 * 2 * G0) * N0 * (N0 + 1) - K0**2


def SR_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
        * kronecker(N0, N1)
    ):
        return 0
    else:
        return (
            (-1) ** (-2 * M0 + 2 * iH + 3 * F10 + N1 + G0 + G1 + I + S + 1)
            * sy.sqrt(
                (2 * G0 + 1)
                * (2 * G1 + 1)
                * N0
                * (N0 + 1)
                * (2 * N0 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
            )
            * wigner_6j(N1, G1, F10, G0, N0, 1)
            * wigner_6j(S, G1, I, G0, S, 1)
        )


def NzSz_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
        * kronecker(N0, N1)
    ):
        return 0
    else:
        return (
            K0
            * (-1)
            ** (-2 * M0 + 2 * iH + 2 * F10 + N1 + G0 + F10 + N0 - K0 + G1 + S + I + 1)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1) * (2 * G0 + 1) * (2 * G1 + 1))
            * wigner_6j(N1, G1, F10, G0, N0, 1)
            * wigner_6j(S, G1, I, G0, S, 1)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
            * sy.sqrt(S * (S + 1) * (2 * S + 1))
        )


def ISM_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
        * kronecker(N0, N1)
        * kronecker(G0, G1)
    ):
        return 0
    else:
        return (
            (-1) ** (-2 * M0 + 2 * iH + 2 * N0 + 2 * G0 + I + S + G0)
            * sy.sqrt(S * (S + 1) * (2 * S + 1) * I * (I + 1) * (2 * I + 1))
            * wigner_6j(I, S, G0, S, I, 1)
        )


def T2ISM_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
        * kronecker(K0, K1)
    ):
        return 0
    else:
        return (
            (-1) ** (-2 * M0 + 2 * iH + 3 * F10 + N0 + G1 + N0 - K0)
            * wigner_9j(G0, G1, 2, I, I, 1, S, S, 1)
            * sy.sqrt(
                (2 * N0 + 1)
                * (2 * N1 + 1)
                * 5
                * (2 * G0 + 1)
                * (2 * G1 + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
            )
            * wigner_6j(N1, G1, F10, G0, N0, 2)
            * wigner_3j(N0, 2, N1, -K0, 0, K1)
        )


def T2QM_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if abs(I) < 1:
        return 0
    if (
        not kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
        * kronecker(K0, K1)
    ):
        return 0
    else:
        return (
            (-1) ** (-2 * M0 + 2 * iH + 3 * F10 + N0 + G1 + N0 - K0 + G1 + I + S + 2)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1) * (2 * G0 + 1) * (2 * G1 + 1))
            * I
            * (2 * I - 1)
            / sy.sqrt(6)
            / wigner_3j(I, 2, I, -I, 0, I)
            * wigner_3j(N0, 2, N1, -K0, 0, K1)
            * wigner_6j(N1, G1, F10, G0, N0, 2)
            * wigner_6j(I, G1, S, G0, I, 2)
        )


def ISH_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(F0, F1)
        * kronecker(N0, N1)
        * kronecker(M0, M1)
        * kronecker(K0, K1)
    ):
        return 0
    else:
        return (
            (-1)
            ** (2 * F0 - 2 * M0 + iH + F0 + F10 + F11 + N0 + G0 + 1 + G1 + I + S + 1)
            * sy.sqrt(
                iH
                * (iH + 1)
                * (2 * iH + 1)
                * (2 * F10 + 1)
                * (2 * F11 + 1)
                * (2 * G0 + 1)
                * (2 * G1 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
            )
            * wigner_6j(iH, F11, F0, F10, iH, 1)
            * wigner_6j(G1, F11, N0, F10, G0, 1)
            * wigner_6j(S, G1, I, G0, S, 1)
        )


def T2ISH_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if not kronecker(F0, F1) * kronecker(M0, M1) * kronecker(K0, K1):
        return 0
    else:
        return (
            (-1) ** (3 * F0 - 2 * M0 + iH + F10 + N0 - K0 + G1 + S + I + 1)
            * sy.sqrt(
                iH
                * (iH + 1)
                * (2 * iH + 1)
                * (2 * F10 + 1)
                * (2 * F11 + 1)
                * 3
                * (2 * G0 + 1)
                * (2 * G1 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
            )
            * wigner_6j(iH, F11, F0, F10, iH, 1)
            * wigner_9j(F10, F11, 1, N0, N1, 2, G0, G1, 1)
            * wigner_3j(N0, 2, N1, -K0, 0, K1)
            * wigner_6j(S, G1, I, G0, S, 1)
        )


def StarkZ_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if not kronecker(G0, G1) * kronecker(M0, M1) * kronecker(K0, K1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0 + F1 + F10 + iH + F11 + 2 * N0 + G0 + 2 - K0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * sy.sqrt(
                (2 * F0 + 1)
                * (2 * F1 + 1)
                * (2 * F10 + 1)
                * (2 * F11 + 1)
                * (2 * N0 + 1)
                * (2 * N1 + 1)
            )
            * wigner_6j(F11, F1, iH, F0, F10, 1)
            * wigner_6j(N1, F11, G0, F10, N0, 1)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
        )


def ZeemanZ_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if not kronecker(N0, N1) * kronecker(M0, M1) * kronecker(K0, K1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0 + F1 + F10 + iH + 1 + F11 + N0 + G0 + 1 + G0 + I + S + 1)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * sy.sqrt(
                (2 * F0 + 1)
                * (2 * F1 + 1)
                * (2 * F10 + 1)
                * (2 * F11 + 1)
                * (2 * G0 + 1)
                * (2 * G1 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
            )
            * wigner_6j(F11, F1, iH, F0, F10, 1)
            * wigner_6j(G1, F11, N0, F10, G0, 1)
            * wigner_6j(S, G1, I, G0, S, 1)
        )


def lD_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(N0, N1)
        * kronecker(M0, M1)
        * kronecker(G0, G1)
        * kronecker(F10, F11)
        * kronecker(F0, F1)
        * (not kronecker(K0, K1))
    ):
        return 0
    else:
        delta_L = K0 - K1
        return (
            N0
            * (N0 + 1)
            * (
                kronecker(delta_L, -2) * (-1) ** (-abs(K0))
                + kronecker(delta_L, 2) * (-1) ** (abs(K0))
            )
        )


def Parity_l_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(N0, N1)
        * kronecker(M0, M1)
        * kronecker(G0, G1)
        * kronecker(F10, F11)
        * kronecker(F0, F1)
        * kronecker(K0, -K1)
    ):
        return 0
    else:
        return (-1) ** (N0 + abs(K0))


def Parity_L_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(N0, N1)
        * kronecker(M0, M1)
        * kronecker(G0, G1)
        * kronecker(F10, F11)
        * kronecker(F0, F1)
        * kronecker(K0, -K1)
    ):
        return 0
    else:
        return (-1) ** (N0)


# Using combined tensor form


def MQM_bBS_old(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
    ):
        return 0
    else:
        return (
            (-1) ** (-2 * M0 + 2 * iH + 2 * F10 + N0 - K0)
            * sy.sqrt((2 * G0 + 1) * (2 * G1 + 1) * (3) * (2 * F11 + 1))
            * wigner_9j(F10, F11, 0, G0, G1, 1, N0, N1, 1)
            * wigner_9j(G0, G1, 1, I, I, 2, S, S, 1)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1) * S * (S + 1) * (2 * S + 1))
            * I
            * (2 * I - 1)
            / (sy.sqrt(6) * wigner_3j(I, 2, I, -I, 0, I))
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
        )


def MQM_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
    ):
        return 0
    else:
        return (
            (-1) ** (-2 * M0 + 2 * iH + 2 * F10 + N1 + G0 + F10)
            * wigner_6j(N1, G1, F10, G0, N0, 1)
            * (-1) ** (N0 - K0)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1))
            * sy.sqrt((2 * G0 + 1) * (2 * G1 + 1) * 3)
            * wigner_9j(G0, G1, 1, I, I, 2, S, S, 1)
            * sy.sqrt((2 * S + 1) * (S + 1) * S)
            * I
            * (2 * I - 1)
            / sy.sqrt(6)
            / wigner_3j(I, 2, I, -I, 0, I)
        )


# Using Sz(3Iz-I2) format


def EDM_bBS(
    K0, N0, G0, F10, F0, M0, K1, N1, G1, F11, F1, M1, S=1 / 2, I=5 / 2, iH=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
    ):
        return 0
    else:
        return (
            (-1)
            ** (-2 * M0 + 2 * iH + 2 * F10 + N1 + G0 + F10 + N0 - K0 + G1 + S + I + 1)
            * sy.sqrt((2 * N0 + 1) * (2 * N1 + 1) * (2 * G0 + 1) * (2 * G1 + 1))
            * wigner_6j(N1, G1, F10, G0, N0, 1)
            * wigner_6j(S, G1, I, G0, S, 1)
            * wigner_3j(N0, 1, N1, -K0, 0, K1)
            * sy.sqrt(S * (S + 1) * (2 * S + 1))
        )


# 174YbOH Case aBJ ##############


def Parity_l_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(K0, -K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, -Sigma1)
        * kronecker(P0, -P1)
    ):
        return 0
    else:
        return (-1) ** (J0 - S + abs(K0))


def Parity_L_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(K0, -K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, -Sigma1)
        * kronecker(P0, -P1)
    ):
        return 0
    else:
        return (-1) ** (J0 - S)


def Rot_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
    ):
        return 0
    else:
        return kronecker(Sigma0, Sigma1) * kronecker(P0, P1) * (
            J0 * (J0 + 1) + S * (S + 1) - 2 * P0 * Sigma0
        ) - 2 * (-1) ** (J0 - (P0) + S - Sigma0) * sy.sqrt(
            (2 * J0 + 1) * J0 * (J0 + 1) * (2 * S + 1) * S * (S + 1)
        ) * sum(
            [
                wigner_3j(J0, 1, J1, -P0, q, P1)
                * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                for q in [-1, 1]
            ]
        )

        # Note: in N^2 formulation, you get -2*Omega*Sigma. Brown uses R^2 form which results in
        # a term -Omega^2 - Sigma^2. You can show for us that Omega^2 + Sigma^2 = Lambda^2 + 2 Omega*Sigma


def SO_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, Sigma1)
        * kronecker(P0, P1)
    ):
        return 0
    else:
        return K0 * Sigma0


def IL_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(K0, K1) * kronecker(F0, F1) * kronecker(M0, M1):
        return 0
    else:
        return (
            K0
            * (-1) ** (2 * F0 - 2 * M0 - J1 + I + F0 + J0 - P0)
            * wigner_6j(J1, I, F0, I, J0, 1)
            * wigner_3j(J0, 1, J1, -P0, 0, P1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * (2 * I + 1) * (I + 1) * I)
        )


def IS_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(K0, K1) * kronecker(F0, F1) * kronecker(M0, M1):
        return 0
    else:
        return (
            (-1) ** (2 * F0 - 2 * M0 + J1 + I + F0 + S - Sigma0 + J0 - P0)
            * wigner_6j(J1, I, F0, I, J0, 1)
            * sy.sqrt(
                (2 * S + 1)
                * (S + 1)
                * S
                * (2 * J0 + 1)
                * (2 * J1 + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
            )
            * sum(
                [
                    wigner_3j(J0, 1, J1, -P0, q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    for q in [-1, 0, 1]
                ]
            )
        )


def IzSz_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(Sigma0, Sigma1)
    ):
        return 0
    else:
        return (
            Sigma0
            * (-1) ** (2 * F0 - 2 * M0 + J1 + I + F0 + J0 - P0)
            * wigner_6j(J1, I, F0, I, J0, 1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * I * (I + 1) * (2 * I + 1))
            * wigner_3j(J0, 1, J1, -P0, 0, P1)
        )


def T2IS_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(K0, K1) * kronecker(F0, F1) * kronecker(M0, M1):
        return 0
    else:
        return (
            (-1) ** (2 * F0 - 2 * M0 + J1 + I + F0 + J0 - P0 + S - Sigma0)
            * wigner_6j(J1, I, F0, I, J0, 1)
            * sy.sqrt(
                5
                * (2 * J0 + 1)
                * (2 * J1 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
            )
            * sum(
                [
                    (-1) ** (q)
                    * wigner_3j(1, 1, 2, q, -q, 0)
                    * wigner_3j(S, 1, S, -Sigma0, -q, Sigma1)
                    * wigner_3j(J0, 1, J1, -P0, -q, P1)
                    for q in [-1, 0, 1]
                ]
            )
        )


def ZeemanLZ_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(K0, K1)
        * kronecker(Sigma0, Sigma1)
        * kronecker(M0, M1)
        * kronecker(P0, P1)
    ):
        return 0
    else:
        return (
            K0
            * (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + J0 + I + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(J1, F1, I, F0, J0, 1)
            * (-1) ** (J0 - P0)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
            * wigner_3j(J0, 1, J1, -P0, 0, P1)
        )


def ZeemanSZ_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(K0, K1) * kronecker(M0, M1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + J0 + I + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(J1, F1, I, F0, J0, 1)
            * (-1) ** (J0 - P0 + S - Sigma0)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * S * (S + 1) * (2 * S + 1))
            * sum(
                [
                    wigner_3j(J0, 1, J1, -P0, q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    for q in [-1, 0, 1]
                ]
            )
        )


def ZeemasyarityZ_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if kronecker(K0, K1) * (not kronecker(M0, M1)):
        return 0
    else:
        return (
            (-1)
            * (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + J0 + I + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(J1, F1, I, F0, J0, 1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * S * (S + 1) * (2 * S + 1))
            * sum(
                [
                    kronecker(K1, K0 - 2 * q)
                    * (-1) ** (J0 - P0 + S - Sigma0)
                    * wigner_3j(J0, 1, J1, -P0, q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, -q, Sigma1)
                    for q in [-1, 1]
                ]
            )
        )


def StarkZ_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(K0, K1) * kronecker(Sigma0, Sigma1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + J0 + I + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(J1, F1, I, F0, J0, 1)
            * (-1) ** (J0 - P0)
            * wigner_3j(J0, 1, J1, -P0, 0, P1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
        )


def LambdaDoubling_p2q_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * (not kronecker(K0, K1))
    ):
        return 0
    else:
        return (
            (-1) ** (J0 - P0 + S - Sigma0)
            * sy.sqrt((2 * J0 + 1) * (J0 + 1) * J0 * (2 * S + 1) * (S + 1) * S)
            * sum(
                [
                    kronecker(K1, K0 + 2 * q)
                    * wigner_3j(J0, 1, J1, -P0, -q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    for q in [-1, 1]
                ]
            )
        )


def LambdaDoubling_q_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if (
        not kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, Sigma1)
        * (not kronecker(K0, K1))
    ):
        return 0
    else:
        return (
            (-1) ** (2 * J0 - 2 * P0)
            * sy.sqrt(
                (2 * J0 - 1)
                * 2
                * J0
                * (2 * J0 + 1)
                * (2 * J0 + 2)
                * (2 * J0 + 3)
                / (6 * 4)
            )
            * sum(
                [
                    kronecker(K1, K0 + 2 * q) * wigner_3j(J0, 2, J1, -P0, 2 * q, P1)
                    for q in [-1, 1]
                ]
            )
        )


def TDM_p_even_aBJ(
    p, q, K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(Sigma0, Sigma1):
        return 0
    else:
        TDM_p = sum(
            [
                (-1) ** (F0 - M0)
                * wigner_3j(F0, 1, F1, -M0, p, M1)
                * (-1) ** (F1 + J0 + I + 1)
                * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
                * wigner_6j(J1, F1, I, F0, J0, 1)
                * (-1) ** (J0 - P0)
                * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
                * wigner_3j(J0, 1, J1, -P0, _q, P1)
                for _q in q
            ]
        )
        return TDM_p


def TransitionDipole_even_aBJ(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(Sigma0, Sigma1):
        return 0
    else:
        TDM_total = sum(
            [
                (-1) ** (p)
                * TDM_p_even_aBJ(
                    p,
                    [-1, 0, 1],
                    K0,
                    Sigma0,
                    P0,
                    J0,
                    F0,
                    M0,
                    K1,
                    Sigma1,
                    P1,
                    J1,
                    F1,
                    M1,
                    S=S,
                    I=I,
                )
                for p in range(-1, 2)
            ]
        )
        # Since L is changing, can only get q=+-1 transitions
        # TDM_plus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_zero = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,0,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_minus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,-1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_total = TDM_plus + TDM_zero + TDM_minus
        return TDM_total


def TransitionDipole_even_aBJ_noM(
    K0, Sigma0, P0, J0, F0, M0, K1, Sigma1, P1, J1, F1, M1, S=1 / 2, I=1 / 2
):
    if not kronecker(Sigma0, Sigma1):
        return 0
    elif not (kronecker(F0, F1) or kronecker(F0 + 1, F1) or kronecker(F0 - 1, F1)):
        return 0
    else:
        TDM_total = (
            1
            / sy.sqrt((2 * F1 + 1))
            * sum(
                [
                    (-1) ** (F1 + J0 + I + 1)
                    * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
                    * wigner_6j(J1, F1, I, F0, J0, 1)
                    * (-1) ** (J0 - P0)
                    * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
                    * wigner_3j(J0, 1, J1, -P0, q, P1)
                    for q in range(-1, 2)
                ]
            )
        )  # If L is changing, can only get q=+-1 transitions
        # TDM_plus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_zero = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,0,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_minus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,-1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_total = TDM_plus + TDM_zero + TDM_minus
        return TDM_total


# 173YbOH Case aBJ ##############


def Parity_odd_l_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if (
        not kronecker(K0, -K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, -Sigma1)
        * kronecker(P0, -P1) ** kronecker(F10, F11)
    ):
        return 0
    else:
        return (-1) ** (J0 - S + abs(K0))


def Parity_odd_L_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if (
        not kronecker(K0, -K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, -Sigma1)
        * kronecker(P0, -P1) ** kronecker(F10, F11)
    ):
        return 0
    else:
        return (-1) ** (J0 - S)


def SO_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, Sigma1)
        * kronecker(P0, P1)
        * kronecker(F10, F11)
    ):
        return 0
    else:
        return K0 * Sigma0


def Rot_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(F10, F11)
        * kronecker(M0, M1)
        * kronecker(J0, J1)
        * kronecker(Sigma0, Sigma1)
        * kronecker(P0, P1)
    ):
        return 0
    else:
        return (J0 * (J0 + 1) + S * (S + 1) - P0**2 - Sigma0**2) - 2 * (-1) ** (
            J0 - (P0) + S - Sigma0
        ) * sy.sqrt((2 * J0 + 1) * J0 * (J0 + 1) * (2 * S + 1) * S * (S + 1)) * sum(
            [
                wigner_3j(J0, 1, J1, -P0, q, P1)
                * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                for q in [-1, 1]
            ]
        )


def ILM_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if (
        not kronecker(K0, K1)
        * kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(F10, F11)
        * kronecker(Sigma0, Sigma1)
        * kronecker(P0, P1)
    ):
        return 0
    else:
        return (
            K0
            * (-1) ** (J1 + I + F10)
            * wigner_6j(J1, I, F10, I, J0, 1)
            * (-1) ** (J0 - P0)
            * wigner_3j(J0, 1, J1, -P0, 0, P1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * (2 * I + 1) * (I + 1) * I)
        )


# Check derivation
def T2q2_ISM_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(F0, F1) * kronecker(M0, M1) * kronecker(F10, F11):
        return 0
    else:
        return (
            (-1) ** (J1 + I + F10 + J0 - P0 + S - Sigma0)
            * wigner_6j(J1, I, F10, I, J0, 1)
            * sy.sqrt(
                (2 * J0 + 1)
                * (2 * J1 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
            )
            * sum(
                [
                    (-1) ** (q)
                    * kronecker(K0, -K1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    * wigner_3j(J0, 1, J1, -P0, -q, P1)
                    for q in [-1, 1]
                ]
            )
        )


# Check derivation
def T2q0_IM_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if abs(I) < 1:
        return 0
    if (
        not kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(F10, F11)
        * kronecker(K0, K1)
        * kronecker(P0, P1)
        * kronecker(K0, K1)
        * kronecker(Sigma0, Sigma1)
    ):
        return 0
    else:
        return (
            1
            / 4
            * (-1) ** (J1 + I + F10 + J0 - P0)
            * wigner_6j(J1, I, F10, I, J0, 2)
            * wigner_3j(J0, 2, J1, -P0, 0, P1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
            / wigner_3j(I, 2, I, -I, 0, I)
        )


# Check derivation
def iHS_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(K0, K1) * kronecker(F0, F1) * kronecker(M0, M1):
        return 0
    else:
        return (
            (-1)
            ** (2 * F0 - 2 * M0 + F11 + iH + F0 + J11 + I + F10 + S - Sigma0 + J0 - P0)
            * wigner_6j(J1, I, F0, I, J0, 1)
            * wigner_6j(J1, I, F0, I, J0, 1)
            * sy.sqrt(
                (2 * S + 1)
                * (S + 1)
                * S
                * (2 * J0 + 1)
                * (2 * J1 + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
            )
            * sum(
                [
                    wigner_3j(J0, 1, J1, -P0, q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    for q in [-1, 0, 1]
                ]
            )
        )


def T2iHS_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(K0, K1) * kronecker(F0, F1) * kronecker(M0, M1):
        return 0
    else:
        return (
            (-1) ** (2 * F0 - 2 * M0 + J1 + I + F0 + J0 - P0 + S - Sigma0)
            * wigner_6j(J1, I, F0, I, J0, 1)
            * sy.sqrt(
                5
                * (2 * J0 + 1)
                * (2 * J1 + 1)
                * S
                * (S + 1)
                * (2 * S + 1)
                * I
                * (I + 1)
                * (2 * I + 1)
            )
            * sum(
                [
                    (-1) ** (q)
                    * wigner_3j(1, 1, 2, q, -q, 0)
                    * wigner_3j(S, 1, S, -Sigma0, -q, Sigma1)
                    * wigner_3j(J0, 1, J1, -P0, -q, P1)
                    for q in [-1, 0, 1]
                ]
            )
        )


# Check derivation
def LambdaDoubling_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if (
        not kronecker(F0, F1)
        * kronecker(M0, M1)
        * kronecker(F10, F11)
        * kronecker(J0, J1)
        * (not kronecker(K0, K1))
    ):
        return 0
    else:
        return (
            (-1) ** (J0 - P0 + S - Sigma0)
            * sy.sqrt((2 * J0 + 1) * (J0 + 1) * J0 * (2 * S + 1) * (S + 1) * S)
            * sum(
                [
                    kronecker(K0, K1 - 2 * q)
                    * wigner_3j(J0, 1, J1, -P0, -q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    for q in [-1, 1]
                ]
            )
        )


def ZeemanLZ_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(K0, K1) * kronecker(Sigma0, Sigma1):
        return 0
    else:
        return (
            K0
            * (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + F10 + iH + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(F11, F1, iH, F0, F10, 1)
            * (-1) ** (F11 + J0 + I + 1)
            * sy.sqrt((2 * F10 + 1) * (2 * F11 + 1))
            * wigner_6j(J1, F11, I, F10, J0, 1)
            * (-1) ** (J0 - P0)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
            * wigner_3j(J0, 1, J1, -P0, 0, P1)
        )


def ZeemanSZ_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(K0, K1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + F10 + iH + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(F11, F1, iH, F0, F10, 1)
            * (-1) ** (F11 + J0 + I + 1)
            * sy.sqrt((2 * F10 + 1) * (2 * F11 + 1))
            * wigner_6j(J1, F11, I, F10, J0, 1)
            * (-1) ** (J0 - P0 + S - Sigma0)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * S * (S + 1) * (2 * S + 1))
            * sum(
                [
                    wigner_3j(J0, 1, J1, -P0, q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    for q in [-1, 0, 1]
                ]
            )
        )


def ZeemasyarityZ_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if kronecker(K0, K1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + F10 + iH + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(F11, F1, iH, F0, F10, 1)
            * (-1) ** (F11 + J0 + I + 1)
            * sy.sqrt((2 * F10 + 1) * (2 * F11 + 1))
            * wigner_6j(J1, F11, I, F10, J0, 1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1) * S * (S + 1) * (2 * S + 1))
            * sum(
                [
                    kronecker(K0, K1 - 2 * q)
                    * (-1) ** (J0 - P0 + S - Sigma0)
                    * wigner_3j(J0, 1, J1, -P0, -q, P1)
                    * wigner_3j(S, 1, S, -Sigma0, q, Sigma1)
                    for q in [-1, 1]
                ]
            )
        )


def StarkZ_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(K0, K1) * kronecker(Sigma0, Sigma1):
        return 0
    else:
        return (
            (-1) ** (F0 - M0)
            * wigner_3j(F0, 1, F1, -M0, 0, M1)
            * (-1) ** (F1 + F10 + iH + 1)
            * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
            * wigner_6j(F11, F1, iH, F0, F10, 1)
            * (-1) ** (F11 + J0 + I + 1)
            * sy.sqrt((2 * F10 + 1) * (2 * F11 + 1))
            * wigner_6j(J1, F11, I, F10, J0, 1)
            * (-1) ** (J0 - P0)
            * wigner_3j(J0, 1, J1, -P0, 0, P1)
            * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
        )


def TDM_p_odd_aBJ(
    p,
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(Sigma0, Sigma1):
        return 0
    else:
        TDM_p = sum(
            [
                (-1) ** (F0 - M0)
                * wigner_3j(F0, 1, F1, -M0, p, M1)
                * (-1) ** (F1 + F10 + iH + 1)
                * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
                * wigner_6j(F11, F1, iH, F0, F10, 1)
                * (-1) ** (F11 + J0 + I + 1)
                * sy.sqrt((2 * F10 + 1) * (2 * F11 + 1))
                * wigner_6j(J1, F11, I, F10, J0, 1)
                * (-1) ** (J0 - P0)
                * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
                * wigner_3j(J0, 1, J1, -P0, q, P1)
                for q in range(-1, 2)
            ]
        )  # If L is changing, can only get q=+-1 transitions


def TransitionDipole_odd_aBJ(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(Sigma0, Sigma1):
        return 0
    else:
        TDM_total = sum(
            [
                (-1) ** (p)
                * TDM_p_odd_aBJ(
                    p,
                    K0,
                    Sigma0,
                    P0,
                    J0,
                    F10,
                    F0,
                    M0,
                    K1,
                    Sigma1,
                    P1,
                    J1,
                    F11,
                    F1,
                    M1,
                    S=S,
                    I=I,
                    iH=iH,
                )
                for p in range(-1, 2)
            ]
        )
        # TDM_plus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_zero = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,0,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_minus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,-1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_total = TDM_plus + TDM_zero + TDM_minus
        return TDM_total


def TransitionDipole_odd_aBJ_noM(
    K0,
    Sigma0,
    P0,
    J0,
    F10,
    F0,
    M0,
    K1,
    Sigma1,
    P1,
    J1,
    F11,
    F1,
    M1,
    S=1 / 2,
    I=5 / 2,
    iH=1 / 2,
):
    if not kronecker(Sigma0, Sigma1) * (not kronecker(K0, K1)):
        return 0
    elif not (kronecker(F0, F1) or kronecker(F0 + 1, F1) or kronecker(F0 - 1, F1)):
        return 0
    else:
        TDM_total = (
            1
            / sy.sqrt(2 * F1 + 1)
            * sum(
                [
                    (-1) ** (F1 + F10 + iH + 1)
                    * sy.sqrt((2 * F0 + 1) * (2 * F1 + 1))
                    * wigner_6j(F11, F1, iH, F0, F10, 1)
                    * (-1) ** (F11 + J0 + I + 1)
                    * sy.sqrt((2 * F10 + 1) * (2 * F11 + 1))
                    * wigner_6j(J1, F11, I, F10, J0, 1)
                    * (-1) ** (J0 - P0)
                    * sy.sqrt((2 * J0 + 1) * (2 * J1 + 1))
                    * wigner_3j(J0, 1, J1, -P0, q, P1)
                    for q in range(-1, 2)
                ]
            )
        )  # Since L is changing, can only get q=+-1 transitions
        # TDM_plus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_zero = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,0,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_minus = sum([(-1)**(F0-M0)*wigner_3j(F0,1,F1,-M0,-1,M1)*(-1)**(F1+J+I+1)*sy.sqrt((2*F0+1)*(2*F1+1))*\
        #     wigner_6j(J1,F1,I,F0,J0,1)*(-1)**(J0-P0)*sy.sqrt((2*J0+1)*(2*J1+1))*wigner_3j(J0,1,J1,-P0,q,P1) for q in range(-1,2)])
        # TDM_total = TDM_plus + TDM_zero + TDM_minus
        return TDM_total
