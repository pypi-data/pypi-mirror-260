import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from numba import njit
try:
    from .fortran import utilsrbs
    is_fortran = True
except ImportError:
    is_fortran = False


def correlation(array: np.ndarray,
                resp: np.ndarray) -> np.ndarray:
    # nomalized correlation for find signal position
    corr = np.correlate(array, resp, mode='same')
    norm = np.correlate(array, np.ones_like(resp), mode='same')
    return corr/norm

@njit(parallel=True, cache=True)
def vector_shift(vector: np.ndarray, step: int) -> np.ndarray:
    """shift vector values to right by step"""
    new_vector = np.empty_like(vector)
    step = step % len(vector)
    if step == 0:
        return vector
    if step < 0:
        step = step % len(vector)
        step = len(vector) - step
    new_vector[step:] = vector[:-step]
    new_vector[:step] = vector[-step:]
    return new_vector

@njit(fastmath=True)
def bohr_spread(X: float,
                z1: float,
                z2: float) -> float:
    """Bohr`s straggling theory\nclear gaussian\nsigma^2 ~ z1^2*z2*X"""
    return 0.26 * z1 ** 2 * z2 * X * 1e-3

@njit(parallel=True, cache=True, fastmath=True)
def get_spread_responce(E: np.ndarray,
                        spreading: np.ndarray,
                        size: int,
                        k: float) -> np.ndarray:

    matrix = np.zeros((E.size, E.size), dtype=np.float32)
    matrix[0, 0] = 1
    spreading += spreading * k * k
    spreading = np.sqrt(spreading)

    for i in range(1, E.size, 1):
        matrix[i, :] = gauss(E, 1, E[i], spreading[i], 0)
        matrix[i, :] /= np.sum(matrix[i, :])

    return matrix

@njit(parallel=True, cache=True, fastmath=True)
def get_responce(size: int, resolution: float, linear: float) -> np.ndarray:
    """Get responce matrix for SSD detector"""
    matrix = np.empty((size, size))
    E = np.arange(0, size)
    tmp = gauss(E,
                1,
                size // 2,
                resolution / linear / 2 / np.sqrt(2 * np.log(2)), 0)
    tmp[np.where(tmp < 0.001)] = 0
    tmp /= np.sum(tmp)
    for i in range(size):
        matrix[i, :] = vector_shift(tmp, i + size // 2)
    matrix[size-10: size, 0: 20] = 0
    matrix[0: 20, size - 10: size] = 0
    return matrix

@njit(parallel=True, cache=True, fastmath=True)
def gauss(x: np.ndarray,
          a: np.float32,
          b: np.float32,
          c: np.float32,
          d: np.float32) -> np.ndarray:
    """"y(x) = a*e^(-(x-b)^2/2c^2) + d"""
    return a * np.exp(-0.5 * (x - b) * (x - b) / c / c) + d


def smooth(array, window=5):
    filt = np.ones(window) / window
    return np.convolve(array, filt, mode='same')

@njit(parallel=True, cache=True, fastmath=True)
def kinFactor(m: float, M: float, theta: float) -> float:
    """
    m - mass of projectile in aem
    M - mass of targer in aem
    theta - scattering angle in degrees
    """
    return 1/(1+M/m)**2*(np.cos(np.deg2rad(theta)) +
                         np.sqrt((M/m)**2 - np.sin(np.deg2rad(theta))**2))**2


def root(func, a, b, eps=2e-2) -> float:
    """
    find root of equation by bisection
    """
    if func(a)*func(b) < 0:
        err = np.abs(a - b)
        x = (a + b)/2
        while err > eps:
            if func(a)*func(x) < 0:
                b = x
            elif func(b) * func(x) < 0:
                a = x
            x = (a + b)/2
            err = np.abs(a - b)
        return x
    else:
        return -1


def find_extream(array: np.ndarray, mode: str) -> float:

    modes = {'min': np.argmin, 'max': np.argmax}

    mask = np.where(array > 500)[0][10:-10]
    point = modes[mode](array[mask]) + mask[0]

    coef = np.polyfit(x=np.arange(-15, 15, dtype=int) + point,
                      y=array[np.arange(-15, 15, dtype=int) + point],
                      deg=3)
    roots = np.roots(coef[:-1]*np.arange(3, 0, -1))

    return roots[np.argmin(np.abs(roots-point))]


def find_right_edge(spectrum: np.ndarray,
                    width: int = 30,
                    thres: float = 200.) -> float:
    """returns position in channel"""

    diff_spectrum = np.diff(savgol_filter(spectrum, 7, 2), append=0)
    edge0 = np.where(spectrum > thres)[0][-1]
    window = (edge0 - width, edge0 + width)

    p, _ = curve_fit(gauss, 
                     np.arange(*window), 
                     diff_spectrum[np.arange(*window)], 
                     p0=np.array((-40, edge0, 10, 0)))

    return p[1]


def Rutherford(E: np.ndarray,
               z1: int,
               z2: int,
               m1: float,
               m2: float,
               theta: float) -> np.ndarray:
        """
        E: keV return cross-section in mb/sr
        """
        if is_fortran:
            return utilsrbs.rutherford(E, E.size, z1, z2, m1, m2, theta)

        cost = np.cos(np.deg2rad(theta))
        sint = np.sin(np.deg2rad(theta))
        c = 5.1837436e6
        D = (z1 * z2 / E) ** 2
        A = (m2 ** 2 - m1 ** 2 * sint ** 2) ** 0.5 + m2 * cost
        B = m2 * sint ** 4 * (m2 ** 2 - m1 ** 2 * sint ** 2) ** 0.5
        return c * D * A ** 2 / B


def applyEnergyCalibration(E0: float,
                           GVM_linear: float,
                           GVM_offset: float,
                           extraction_voltage: float,
                           ionCharge: float) -> float:

    return ((E0 - extraction_voltage)/(ionCharge+1) *
            GVM_linear + GVM_offset) * (ionCharge+1) + extraction_voltage


def minimize_(func, x0, step, niter, args):

    x = x0
    bestfun = func(x, *args)
    bestx = x

    cs = bestx
    for i in range(niter):

        eps = np.random.uniform(1 - step, 1 + step, size=len(x))
        cs = bestx * eps
        value = func(cs, *args)

        if (bestfun > value):

            bestfun = value
            bestx = cs

        if i % 20 == 0:
            print(f'iter {i} of {niter}, func={bestfun: .4f}', end='\r', flush=True)
    return {'x': bestx, 'fun': bestfun}
