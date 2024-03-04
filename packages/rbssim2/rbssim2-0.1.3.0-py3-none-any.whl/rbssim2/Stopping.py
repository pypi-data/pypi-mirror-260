import numpy as np
try:
    from .fortran import Stopping
except ImportError:
    from . import _Stopping as Stopping

def inverse(E: np.ndarray, params: np.ndarray) -> np.ndarray:
    
    return Stopping.inverse(E, E.size, params, params.size)


def equation(E: np.ndarray, params: np.ndarray) -> np.ndarray:

    return Stopping.equation(E, E.size, params, params.size)


def inverseIntegral(E: np.ndarray, params: np.ndarray) -> np.ndarray:

    return Stopping.inverseintegral(E, E.size, params, params.size)


def inverseIntegrate(E0: np.ndarray,
                     E1: np.ndarray,
                     params: np.ndarray) -> np.ndarray:
    """Inverse integral of stopping power calculates range of ion"""
    assert (E0.size == E1.size)

    return Stopping.inverseintegrate(E0, E1, E0.size, params, params.size)


def inverseDiff(E: np.ndarray, params: np.ndarray) -> np.ndarray:

    return Stopping.inversediff(E, E.size, params, params.size)


def EnergyAfterStopping(E0: np.ndarray,
                        X: np.ndarray,
                        params: np.ndarray,
                        E_THRESHOLD: float) -> np.ndarray:
    assert (E0.size == X.size)

    return Stopping.energyafterstopping(E0, X, E0.size, params, params.size, E_THRESHOLD)