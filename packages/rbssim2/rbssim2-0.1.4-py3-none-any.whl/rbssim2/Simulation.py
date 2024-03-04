import numpy as np
from dataclasses import dataclass
from copy import deepcopy
from typing import List, Tuple, Dict
from .Stopping import EnergyAfterStopping, equation, inverseIntegrate
from .Detector import Detector
from .Element import Beam, Isotope
from .Geometry import Geometry
from .Globals import MIN_YEILD_DISCRETIZATION
from .utilsRBS import kinFactor, bohr_spread
try:
    from .fortran.utilsrbs import get_spread_responce
    print('imported fast')
except ImportError:
    from .utilsRBS import get_spread_responce


@dataclass
class Layout:

    energyDiscrete: np.ndarray
    ionRanges: np.ndarray
    straggling: np.ndarray


class Simulation:
    """
    This class represents model experiment of backscattering
    """

    def __init__(self, beam: Beam, geometry: Geometry, detector: Detector):

        self.beam: Beam = beam
        self.geometry: Geometry = geometry
        self.detector: Detector = detector
        self.partialSpectra: Dict[str, np.ndarray] = {}
        self.dxerr: Tuple[np.ndarray] = None

        self.__Qsr = np.float32(1e11)
        self.__energy_step = np.float32(2.1)
        self.__energy_threshold = np.float32(200)
        self.useStraggling = True
        self.is_sigmacalc = True
        self.initGeometry()
        self.initSpectra()
        self.initCrossSection()


    @property
    def Qsr(self): return self.__Qsr


    @Qsr.setter
    def Qsr(self, Qsr): self.__Qsr = np.float32(Qsr)


    @property
    def energy_step(self): return self.__energy_step


    @energy_step.setter
    def energy_step(self, energy_step):
        if isinstance(energy_step, (int, float)):
            self.__energy_step = np.float32(energy_step)
            if energy_step < 0:
                self.__energy_step *= -1


    @property
    def energy_threshold(self): return self.__energy_threshold


    @energy_threshold.setter
    def energy_threshold(self, energy_threshold):
        if isinstance(energy_threshold, (int, float)):
            self.__energy_threshold = np.float32(energy_threshold)


    def initGeometry(self):

        tuple(map(lambda Layer: Layer.setBraggRule(self.beam),
                  self.geometry.target))

        tuple(map(lambda Layer: Layer.setBraggRule(self.beam),
                  self.geometry.foils))

        tuple(map(lambda Layer: Layer.setCrossSection(self.beam,
                                                      self.beam,
                                                      self.geometry.theta,
                                                      self.is_sigmacalc),
                                                      self.geometry.target))


    def initCrossSection(self):
        """
        This method compiles cross-sections for each isotope in target
        """
        for layer in self.geometry.target:
            for element in layer.getComponents():
                for isotope in element[0].isotopes:
                    isotope.crossSection.theta = self.geometry.theta
                    try:
                        isotope.crossSection.selectR33(None)
                    except FileNotFoundError:
                        print(f'force using Rutherford for {isotope.crossSection}')
                        isotope.crossSection.selectRutherford()


    def initSpectra(self):
        """This method reset ndarray holder for partial spectra of each isotope"""
        self.partialSpectra = {}
        for layer in self.geometry.target:
            for element in layer.getComponents():
                for isotope in element[0].isotopes:

                    self.partialSpectra[str(isotope)] = np.zeros_like(self.detector.EnergyChannels,
                                                                      dtype=np.float32)

        if 'total' in self.partialSpectra.keys():
            self.partialSpectra['total'] = np.zeros_like(self.detector.EnergyChannels,
                                                         dtype=np.float32)

    def run(self) -> Dict[str, np.ndarray]:
        """Returns dict where key is name of isotope (12C for example)
          value contains array of ADC channels counts"""
        self.initSpectra()
        EnergyAtFrontOfLayers: List[float] = []
        EnergyAtFrontOfLayers.append(self.beam.Energy)

        for layerNumber, layer in enumerate(self.geometry.target):
            layout = self.layerMapping(EnergyAtFrontOfLayers, layerNumber)
            for element in layer.getComponents():
                for isotope in element[0].isotopes:

                    self.calculatePartialSpectrum(
                        layout,
                        isotope,
                        element[1],
                        layerNumber)

        sp = np.zeros_like(self.detector.EnergyChannels)
        for i_name in self.partialSpectra.keys():
            sp = sp + self.partialSpectra[i_name]

        self.partialSpectra['total'] = sp
        return self.partialSpectra

    def calculatePartialSpectrum(
            self, layout: Layout,
            isotope: Isotope,
            elementConcentration: float,
            layerNumber: int):
        """
        This is main method where describes all physics
        """
        layout = deepcopy(layout)
        cosb = np.cos(np.deg2rad(self.geometry.beta))
        cosa = np.cos(np.deg2rad(self.geometry.alpha))

        Yield = isotope.crossSection.calculate(layout.energyDiscrete)

        k = kinFactor(self.beam.A, isotope.A, self.geometry.theta)
        kE = layout.energyDiscrete * k

        xlow = inverseIntegrate(
            np.ones_like(layout.energyDiscrete)*self.beam.Energy,
            layout.energyDiscrete + np.sqrt(layout.straggling),
            self.geometry.target[layerNumber].stoppingParams)

        xhigh = inverseIntegrate(
            np.ones_like(layout.energyDiscrete)*self.beam.Energy,
            layout.energyDiscrete - np.sqrt(layout.straggling),
            self.geometry.target[layerNumber].stoppingParams)

        dx = xhigh - xlow
        self.dxerr = (layout.ionRanges, dx)

        if self.useStraggling:
            Yield = self.applyStraggling(
                Yield,
                layout.energyDiscrete,
                layout.straggling,
                k)

        E3 = EnergyAfterStopping(
                    kE,
                    layout.ionRanges / cosb,
                    self.geometry.target[layerNumber].stoppingParams,
                    self.energy_threshold)

        E3 = self.getEnergyFromLayer(layerNumber, E3)
        mask = np.where(E3 > 0)

        E3 = E3[mask]
        Yield = Yield[mask]
        layout.ionRanges = layout.ionRanges[mask]
        layout.straggling = layout.straggling[mask]
        layout.energyDiscrete = layout.energyDiscrete[mask]

        mask = np.argsort(E3)
        E3 = E3[mask]
        Yield = Yield[mask]
        layout.ionRanges = layout.ionRanges[mask]
        layout.straggling = layout.straggling[mask]
        layout.energyDiscrete = layout.energyDiscrete[mask]
        if len(E3) == 0:
            return

        Yield = np.interp(self.detector.EnergyChannels,
                          E3,
                          Yield,
                          left=0, right=0)
        # number of isotope atoms at/cm2'
        nOfTarget = isotope.abundance * elementConcentration * 1e15
        self.E1 = np.interp(self.detector.EnergyChannels,
                            E3,
                            layout.energyDiscrete)
        self.R = np.interp(self.detector.EnergyChannels,
                           E3,
                           np.append(layout.ionRanges[:-1]-layout.ionRanges[1:], 0))
        Einter = np.interp(self.detector.EnergyChannels,
                           E3,
                           layout.energyDiscrete)
        de3dx = equation(self.detector.EnergyChannels,
                         self.geometry.target[layerNumber].stoppingParams)
        dde3ddx = (
            cosa/cosb +
            equation(
                    Einter,
                    self.geometry.target[layerNumber].stoppingParams) /
            equation(
                    k * Einter,
                    self.geometry.target[layerNumber].stoppingParams) * k
                    )
        de3dx = de3dx * dde3ddx
        mask = de3dx > 0

        YieldChannels = np.zeros_like(Yield)

        YieldChannels[mask] = (Yield[mask] *
                               nOfTarget *
                               self.Qsr *
                               self.detector.linear / de3dx[mask])
        YieldChannels[np.isnan(YieldChannels)] = 0

        if self.detector.resolution > 2:
            self.partialSpectra[str(isotope)] += np.convolve(
                    self.detector.responce,
                    YieldChannels, mode='same')
        else:
            self.partialSpectra[str(isotope)] += YieldChannels

    def layerMapping(self,
                     EnergyAtFrontOfLayers: List[float],
                     layerNumber: int) -> Layout:

        if EnergyAtFrontOfLayers[-1] <= self.energy_threshold:
            EnergyAtFrontOfLayers.append(0)
            EnergyDiscrete = np.linspace(
                EnergyAtFrontOfLayers[layerNumber],
                EnergyAtFrontOfLayers[layerNumber+1],
                MIN_YEILD_DISCRETIZATION)

            return Layout(EnergyDiscrete,
                          np.zeros_like(EnergyDiscrete),
                          np.zeros_like(EnergyDiscrete))

        cosa = np.cos(np.deg2rad(self.geometry.alpha))
        EnergyAtFrontOfLayers.append(
                EnergyAfterStopping(
                    np.array((EnergyAtFrontOfLayers[-1],)),
                    np.array((self.geometry.target[layerNumber].thickness,)) /
                    cosa,
                    self.geometry.target[layerNumber].stoppingParams,
                    self.energy_threshold)[0])

        if EnergyAtFrontOfLayers[layerNumber+1] < self.energy_threshold:
            EnergyAtFrontOfLayers[layerNumber+1] = self.energy_threshold

        energyDiscrete = np.arange(
            EnergyAtFrontOfLayers[layerNumber],
            EnergyAtFrontOfLayers[layerNumber+1],
            -self.energy_step, dtype=np.float32)

        if energyDiscrete.size < MIN_YEILD_DISCRETIZATION:

            energyDiscrete = np.linspace(
                EnergyAtFrontOfLayers[layerNumber],
                EnergyAtFrontOfLayers[layerNumber+1],
                MIN_YEILD_DISCRETIZATION)

        ionRanges = inverseIntegrate(
            np.ones_like(energyDiscrete) *
            EnergyAtFrontOfLayers[layerNumber],
            energyDiscrete,
            self.geometry.target[layerNumber].stoppingParams)

        straggling = np.zeros_like(ionRanges)

        for element in self.geometry.target[layerNumber].getComponents():
            # additive rule for straggling
            straggling += bohr_spread(ionRanges * 1e-3,
                                      self.beam.Z,
                                      element[0].Z) * element[1]
        layout = Layout(energyDiscrete, ionRanges, straggling)
        return layout

    def applyStraggling(self, Yield, energyDiscrete, straggling, k):

        matrix = get_spread_responce(np.float32(energyDiscrete), straggling,  energyDiscrete.size, k)
        Yield = np.dot(np.float32(matrix), np.float32(Yield))
        Yield[np.isnan(Yield)] = 0
        return Yield

    def getEnergyFromLayer(self,
                           layernumber: int,
                           E3: np.ndarray) -> np.ndarray:

        for j, foil in enumerate(self.geometry.target[:layernumber][::-1] +
                                 self.geometry.foils):

            cosb = np.cos(np.deg2rad(self.geometry.beta))
            E3 = EnergyAfterStopping(
                                    E3,
                                    np.ones_like(E3)*foil.thickness / cosb,
                                    foil.stoppingParams,
                                    self.energy_threshold)
        return E3

    def __repr__(self) -> str:
        return f'simlulation: \n<{self.geometry}>\n\tbeam<{self.beam}>'
