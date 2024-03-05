import h5py
import numpy as np


def load_simulink(file_name, arr_name):
    with h5py.File(file_name) as f:
        return f[arr_name][()][:, 1]


def estimate_latency(data_, data_ref):
    latency = 0
    chi2 = float("inf")
    for i in range(100):
        rdata = np.roll(data_, i)
        rdata[0:i] = 0
        chi2_new = np.sum((data_ref - rdata) ** 2)
        if chi2_new < chi2:
            chi2 = chi2_new
            latency = i
    return latency
