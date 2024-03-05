import  numpy as np

def n2_curti (ratio):
    """
    Empirical Equation derived by Curti et al. (2016) for N2
    indicator based on Te-based literature data (SLOAN), They performed a
    polynomial fitting. The parameters are taken from table 2 
    
    Diag    c0     c1    c2     c3      c4    RMS   sig   Range 12 + log (O/H)  
     N2  -0.489  1.513 -2.554 -5.293 -2.867   0.16  0.10    7.6 -- 8.85
 
    """   
    x_n2 = np.linspace(7.6,8.85,20)

    x = x_n2 -8.69

    y_n2 = (-0.489 + (1.513*x) + (-2.554*(x**2)) + (-5.293*(x**3)) +  
            (-2.867*(x**4)) )

    return np.interp(ratio, y_n2, x_n2, np.nan, np.nan) 


def o3n2_curti (ratio):
    """
    Empirical Equation derived by Curti et al. (2016) for N2
    indicator based on Te-based literature data (SLOAN), They performed a
    polynomial fitting. The parameters are taken from table 2 
    
    Diag    c0     c1    c2     c3      c4    RMS   sig   Range 12 + log (O/H)  
    O3N2  0.281 -4.765 -2.268                 0.21  0.09    7.6 -- 8.85
 
    """   
    
    x_o3n2 = np.linspace(7.6,8.85,20)

    x = x_o3n2 - 8.69

    y_o3n2 = 0.281 -4.765*x -2.268*(x**2)


    return np.interp(ratio, y_o3n2[::-1], x_o3n2[::-1], np.nan, np.nan) 


def n2_perez (ratio):
    """
    Empirical Equation derived by Perez-Montero & Contini (2009) for N2
    indicator based on Te-based literature data, eq. 11 in their papers    
    12+log(O/H) = 0.79N2+9.07
    """
    return 9.07 + 0.79*ratio

def o3n2_perez (ratio):
    """
    Empirical Equation derived by Perez-Montero & Contini (2009) for O3N2
    indicator  based on Te-based literature data, eq. 16    
    12 + log(O/H) = 8.74 - 0.31xO3N2
    """

    return 8.74 - 0.31*ratio



def n2_marino (ratio):
    """
    Empirical Equation derived by Marino et al.  & Contini (2013) for N2
    indicator  based on Te-based literature data, eq. 4    
    12 + log (O/H) = 8.743(+-0.027) + 0.462(+-0.024) x N2
    """
    
    return 8.743 + 0.462*ratio


def n2_denicolo (ratio):
    """
    Empirical Equation derived by Denicolo (2002) for N2
    indicator  based on Te-based literature data
    """
    
    return 9.12 + 0.73*ratio


def n2o2_nagao (ratio):
    """
    Empirical Equation derived by Nagao (2006) for O2N2
    indicator  based on Te-based literature data
    """
    
    return 0.1784*(ratio**3)-0.2233*(ratio**2)+0.3507*ratio+9.1960




def n2_marino2 (ratio):
    """
    Empirical Equation derived by Marino et al.  & Contini (2013) for N2
    indicator  based on CALIFA-ONS H ii regions.   
    12 + log (O/H) = 8.667[±0.006] +[0.455 ± 0.011] x N2
    """
    
    return 8.667 + 0.455*ratio


def o3n2_marino (ratio):
    """
    Empirical Equation derived by Marino et al. (2013) for O3N2
    indicator  based on Te-based literature data, eq. 2    
    12 + log (O/H) = 8.533(+-0.012) - 0.214(+-0.012) x O3N2
    """

    return 8.533 - 0.214*ratio

def o3n2_marino2 (ratio):
    """
    Empirical Equation derived by Marino et al. (2013) for O3N2
    indicator  based on CALIFA-ONS H ii regions.    
    12 + log (O/H) = 8.505[±0.001]− 0.221[±0.004] × O3N2 
    """

    return 8.505 - 0.221*ratio




