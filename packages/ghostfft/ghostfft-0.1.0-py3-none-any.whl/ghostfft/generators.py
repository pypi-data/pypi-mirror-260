import itertools as it

import numpy as np

from .base import Component
from .fpt import FixedPointType as FPT


class SinGenerator(Component):
    def __init__(self, ampl: int, period: int, lognout: int, bwout: int = 8, dtype: np.dtype = np.int8):
        super().__init__(bwin=0, bwout=bwout)
        self.ampl = ampl
        self.period = period
        self.nout = 2 ** lognout
        self.bwout = bwout
        signal = (np.sin(np.arange(period) * 2 * np.pi / period) * ampl).astype(dtype)
        signal = FPT(bwout, 0, signal).bdata
        self.gen = it.cycle(signal.reshape((-1, self.nout)))

    def _impl(self, datain: np.ndarray = None):
        self.bdataout = next(self.gen)

