import numpy as np

from numba import njit
np.seterr(all='ignore')


@njit(cache=True, fastmath=True)
def inverse(E: np.ndarray, lenE: int, params: np.ndarray, lenparams:int) -> np.ndarray:
    lnE = np.log(E)
    lnE2 = lnE * lnE
    lnE3 = lnE2 * lnE
    lnE4 = lnE3 * lnE
    return (params[0] +
            params[1] * lnE +
            params[2] * lnE2 +
            params[3] * lnE3 +
            params[4] * lnE4)


@njit(cache=True, fastmath=True)
def equation(E: np.ndarray, lenE: int, params: np.ndarray, lenparams:int) -> np.ndarray:
    lnE = np.log(E)
    lnE2 = lnE * lnE
    lnE3 = lnE2 * lnE
    lnE4 = lnE3 * lnE
    return 1/(params[0] +
            params[1] * lnE +
            params[2] * lnE2 +
            params[3] * lnE3 +
            params[4] * lnE4)



@njit(cache=True, fastmath=True)
def inverseintegral(E: np.ndarray, lenE: int, params: np.ndarray, lenparams:int) -> np.ndarray:

    lnE = np.log(E)
    c1 = params[1] - 2.*params[2] + 6.*params[3] - 24.*params[4]
    return E*((params[0] - c1) + params[4] * lnE * lnE * lnE * lnE +
              (params[3] - 4.*params[4]) * lnE * lnE * lnE +
              (params[2] - 3.*params[3] + 12.*params[4]) * lnE * lnE +
              c1*lnE)



def inverseintegrate(E0: np.ndarray,
                     E1: np.ndarray,
                     lenE: int,
                     params: np.ndarray,
                     lenparams: int) -> np.ndarray:
    """Inverse integral of stopping power calculates range of ion"""
    return (inverseintegral(E0, E0.size, params, params.size) - 
            inverseintegral(E1, E0.size, params, params.size))



def inversediff(E: np.ndarray, lene: int, params: np.ndarray, lenparams:int) -> np.ndarray:

    lnE = np.log(E)
    lnE2 = lnE * lnE
    lnE3 = lnE2 * lnE
    return (params[1] +
            2.*params[2]*lnE +
            3.*params[3]*lnE2 +
            4.*params[4]*lnE3)/E



def energyafterstopping(E0: np.ndarray,
                        X: np.ndarray,
                        lene: int,
                        params: np.ndarray,
                        lenparams: int,
                        E_THRESHOLD: float) -> np.ndarray:

    INT_from = inverseintegral(E0, E0.size, params, params.size)
    Eend = np.zeros_like(E0)
    isEnd = False
    _Eend = 0.0

    for i in range(0, E0.size):

        _Eend = E0[i]
        if isEnd:
            break

        for j in range(100):
            if _Eend <= E_THRESHOLD:
                Eend[i] = 0
                isEnd = True
                break

            val = INT_from[i] - inverseintegral(_Eend, 1, params, params.size) - X[i]
            if np.abs(val) <= 0.02:
                Eend[i] = _Eend
                break

            _Eend = _Eend + val/inverse(_Eend, 1, params, params.size)
    return Eend
