import numpy as np
import os

direcbase = os.path.dirname(os.path.realpath(__file__))
dicden = direcbase + '/temden/curve_SII_ratio_vs_Ne_density.dat'

def SIIden(ratio):

    den_arr = np.loadtxt(dicden)
    return np.interp(ratio, den_arr[:,0], den_arr[:,1], left=np.nan,
                     right=np.nan)
