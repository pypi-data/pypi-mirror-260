from typing import Callable

import numpy as np

from .base import Component
from .fpt import FixedPointType as FPT


class PFB(Component):
    """
    A model of CASPER PFB.

    :param logsize: Size of the FFT (2**fft_size points)
    :param ntaps: Total number of taps in the PFB
    :param logninputs: Number of parallel input streams
    :param window: The window function to use. Must have signature: window(n_points).
    """

    def __init__(self, logsize: int, ntaps: int, logninputs: int, window: Callable = np.hamming,
                 coef_delay: int = 1,
                 bwin: int = 8, bwout: int = 18, bwcoef: int = 18, **kwargs):
        super().__init__(bwin, bwout, **kwargs)
        self.logsize = logsize
        self.ntaps = ntaps
        self.logninputs = logninputs
        self.tapsize = 2 ** (logsize - logninputs)
        self.window = window

        assert bwin <= 32, ("For larger input bw you'll need to modify the dtype of the internal variables, from"
                            "32 to 64")

        self.taps = FPT(bwin, bwin - 1, np.zeros((2 ** logninputs, ntaps * self.tapsize), dtype=np.int32))
        self.tc_count = (self.tapsize - coef_delay) % self.tapsize
        self.bdataout = None

        tapscoef = np.empty((2 ** logninputs, ntaps, self.tapsize))

        for i in range(2 ** logninputs):
            for j in range(ntaps):
                # Taps use inverse order of coefficients sets (the last part of the window
                # is used in a first tap and so on)
                tapscoef[i, j] = self.pfb_coef_gen_calc(i, ntaps - j - 1)

        self.tapscoef = FPT(bwcoef, bwcoef-1, tapscoef)

    def _impl(self, bdatain: np.ndarray = None):
        """
        Run the PFB.
        """
        bdatain = np.squeeze(bdatain)
        assert isinstance(bdatain[0], np.integer), "bdatain must be an integer in binary form"

        if bdatain.size != 2 ** self.logninputs:
            raise ValueError(
                f'Invalid input data_ shape. Input array must be 1D and have {2 ** self.logninputs} elements')

        # Shifting data_ in taps and adding new data
        self.taps.shift_insert(bdatain)

        # Windowing and summing taps
        tapout = self.taps[:, ::self.tapsize]
        coefout = self.tapscoef[:, :, self.tc_count]
        if tapout.shape != coefout.shape:
            raise RuntimeError(f"Shapes of taps {tapout.shape} and coefficients {coefout.shape} "
                               f"slices shapes do not match. Check the inner algorithm")

        dataout = tapout * coefout
        add_conf = dataout.conf
        # After each addition the sum gets shifted right by 1 position
        # so the fpt_dataout type remains he same. The number of additions
        # (and shifts) is ceil(log2(n_taps))
        dataout.sum(axis=1)
        # Scaled down by 2 by adjusting the point positions before rounding; data is not changing
        # But in this case reinterpret has no effect so commented out
        # dataout.reinterpret(dataout.bw, dataout.pb+1)

        # For some reason adders do not increase output bit width, supposedly truncating frm the left
        dataout = FPT.cast(*add_conf, dataout, keep_lsb=True)

        # Finally, output is converted to the specified output type by truncating + rounding
        dataout.round_from_zero(self.bwout)
        # TODO: add overflow behaviour control

        self.tc_count = (self.tc_count + 1) % self.tapsize
        assert dataout.shape == bdatain.shape, "Out data_ does not match input shape. Check the algorithm"
        self.bdataout = dataout.bdata

    def pfb_coef_gen_calc(self, input_ind: int, tap_ind: int, fwidth: int = 1) -> np.ndarray:
        """
        Reproduces PFB coefficients from the Simulink CASPER model.

        :param input_ind: Which input stream to calculate (of the n_inputs parallel)
        :param tap_ind: Index of the tap to calculate (starting from 0; passing less than 0 will return all coefficients)
        :param fwidth: The scaling of the bin width (1 is normal)
        :return: PFB coefficients for given parameters
        """
        all_taps = self.ntaps * 2 ** self.logsize

        if tap_ind < 0:
            index = np.arange(all_taps)
        else:
            cs = (tap_ind * 2 ** self.logsize) + input_ind
            ce = (tap_ind * 2 ** self.logsize) + 2 ** self.logsize
            step = 2 ** self.logninputs
            index = np.arange(cs, ce, step)

        wval = self.window(all_taps)
        total_coefs = wval * np.sinc(fwidth * (np.arange(all_taps) / 2 ** self.logsize - self.ntaps / 2))
        return total_coefs[index]
