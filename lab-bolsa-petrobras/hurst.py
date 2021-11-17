import numpy as np

def calculate_rescaled_range(ts, n):
    """
    Calculates the rescaled range of the time series vector ts
    """
    if n > len(ts):
        raise ValueError("n must be smaller than the length of the time series")
    
    if n == len(ts):
        ts_list = [ts]
    else:
        ts_list = [ts[i:i+n] for i in range(0, len(ts)-n, n)]
    
    ris = []
    for ts in ts_list:
        m = ts.mean()
        Yk = ts - m
        Zk = Yk.cumsum()
        Rk = Zk.max() - Zk.min()
        Sk = ts.std(ddof=0)
        ris.append(Rk/Sk)
    
    return np.mean(ris)

def compute_hurst_exponent(ts):
    ns = np.logspace(2, np.log2(len(ts)), num=30, base=2, dtype=int)
    ri = np.array([calculate_rescaled_range(ts, n) for n in ns])
    h = np.polyfit(np.log2(ns), np.log2(ri), 1)[0]

    return h, ns, ri