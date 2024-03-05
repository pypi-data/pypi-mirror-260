from numpy import *
from scipy import interpolate
from task import *


# Extinction curves from table 7.1 (pag. 181) of Osterbrock
f31l = array([0.058, 0.132, 0.147, 0.282, 0.404, 0.552, 0.728, 0.818, 0.866,
              0.987, 1.122, 1.164, 1.271, 1.346, 1.409, 1.509, 1.575, 1.643,
              1.851, 1.949, 2.113, 2.601, 2.953, 3.091, 2.630, 2.529, 2.522,
              2.606, 2.617, 2.780, 3.337, 3.503])

f55l = array([0.069, 0.157, 0.174, 0.334, 0.478, 0.639, 0.784, 0.858, 0.898,
              0.991, 1.076, 1.099, 1.156, 1.194, 1.226, 1.276, 1.301, 1.304,
              1.316, 1.341, 1.390, 1.571, 1.713, 1.718, 1.456, 1.388, 1.337,
              1.323, 1.323, 1.329, 1.413, 1.448])

fsmcl = array([0.064, 0.170, 0.188, 0.334, 0.446, 0.561, 0.679, 0.753, 0.799,
               0.923, 1.049, 1.085, 1.178, 1.246, 1.310, 1.446, 1.584, 1.726,
               2.020, 2.152, 2.327, 2.649, 2.816, 3.161, 3.559, 3.806, 4.299,
               4.775, 4.822, 5.376, 6.586, 6.875])

flambda = array([33333., 20000., 18751., 12500., 10000., 8333, 7143, 6563,
                 6250, 5555, 5000, 4861, 4545, 4340, 4167, 3846, 3571, 3333,
                 2941, 2796, 2631, 2381, 2273, 2083, 1907, 1818, 1667, 1548,
                 1538, 1429, 1250, 1216])

# interpolation for the extinction curves
f31  = interpolate.interp1d(1./(flambda*1e-4), f31l, 'cubic')
f55  = interpolate.interp1d(1./(flambda*1e-4), f55l, 'cubic')
fsmc = interpolate.interp1d(1./(flambda*1e-4), fsmcl, 'cubic')

# dictionary of the extinction curves
lawext={'f31':f31,'f55':f55,'fsmc':fsmc}

def funcext(labd,flabd='f31'):
    '''
    Given a wavelenght and  a extinction law is return the value of
    the extinction curve at that wavelenght.
    (Angstrom)

    Parameters:
    -------
    labd  : float,
       wavelength in Angstrom
    flabd : string,
        extinction curve that can be use: 'f31', 'f55' and 'SMC'
    Return
    -------
    fl : float,
       extinction curve value at that wavelength
    '''
    fl=lawext[flabd](1./(labd*1e-4))
    return fl


# in order to see the theory look at pag. 178 and 179 Osterbrock

# plot extinction curve
#plt.clf()
#x=linspace(1./(flambda[0]*1e-4),1./(flambda[-1]*1e-4),100)
#y=f31(x)
#plt.plot(x,y)
#plt.show()

#E(B-V) = 2.5*c*(funcext(4450)-funcext(5510))
#E(B-V) = c*0.77298522038967421
#A_lambda = 2.5*c*funcext(lambda)
#A_lambda = 2.5log(I_lambda_obv/I_lambda_teo)

# values of the extinction curve R3.1 for the lines h_delta, h_gamma, h_beta,
# h_alfa
#fd=1.4311023297108498
#fg=1.3458284375866174
#fb=1.1638977778614874
#fa=0.8180304633472103

##########
# Case A #
##########

# Ratio value of the case A (low density nivel) of the recobination Theory
# table 4.1 (pag 72) Osterbrock
# Balmer-line intensities to h_beta, to 2.500 K, 5.000 K, 10.000 K e 20.000 K

ha_b_A = array([3.42, 3.10, 2.86, 2.69])
hg_b_A = array([0.439, 0.458, 0.470, 0.485])
hd_b_A = array([0.237, 0.250, 0.262, 0.271])

hb_a_A = 1./ha_b_A
hg_a_A = hg_b_A/ha_b_A
hd_a_A = hd_b_A/ha_b_A

diclawext_A = {'ha_b':ha_b_A, 'hg_b':hg_b_A, 'hd_b':hd_b_A, 'hb_a':1./ha_b_A,
               'hg_a':hg_b_A/ha_b_A, 'hd_a':hd_b_A/ha_b_A, 'hb_b':ones(4)}

# Effective recombination coefficient, defined by
# np*ne*(alpha^eff_nn')=4*pi*j_h_nn'/hv_nn'

#(4*pi*j_h_beta)/(ne*np)
emicoeff_A    = array([2.70e-25,1.54e-25,8.30e-26,4.21e-26]) # (erg cm^3 s^-1)
#alpha^eff_h_beta
effreccoeff_A = array([6.61e-14,3.78e-14,2.04e-14,1.03e-14]) # (cm^3 s^-1)

##########
# Case B #
##########

# Ratio value of the case B (high density nivel) of the recobination Theory
# table 4.2 (pag 73) Osterbrock
# Balmer-line intensities relatives to h_beta,
# to 2.500 K, 5.000 K, 10.000 K e 20.000 K

ha_b_B = array([3.30, 3.05, 2.87, 2.76])
hg_b_B = array([0.444, 0.451, 0.466, 0.474])
hd_b_B = array([0.241, 0.249, 0.256, 0.262])

hb_a_B = 1./ha_b_B
hg_a_B = hg_b_B/ha_b_B
hd_a_B = hd_b_B/ha_b_B

diclawext_B = {'ha_b':ha_b_B, 'hg_b':hg_b_B, 'hd_b':hd_b_B, 'hb_a':1./ha_b_B,
               'hg_a':hg_b_B/ha_b_B, 'hd_a':hd_b_B/ha_b_B, 'hb_b':ones(4)}


# Effective recombination coefficient, defined by
# np*ne*(alpha^eff_nn')=4*pi*j_h_nn'/hv_nn';
# where j_h_nn' is the emission coefficient

#(4*pi*j_h_beta)/(ne*np)
emicoeff_B    = array([3.72e-25,2.20e-25,1.24e-25,6.62e-26]) # (erg cm^3 s^-1)
#alpha^eff_h_beta
effreccoeff_B = array([9.07e-14,5.37e-14,3.03e-14,1.62e-14]) # (cm^3 s^-1)

###############################################################################
# Alpha_B
# the recombination coefficient to existed levels (n>=2) of hydrogem atom
# units cm^3 s^-1
# Table 2.1 (pag. 22, Osterbrock)
# temp 5000, 10000, 20000 K
###############################################################################
reccoeffB=array([4.54e-13,2.59e-13,1.43e-13])
ev = 1.60217646e-12  # erg

def rydberg(n1,n2):
    '''
    Rydberg law, calculate the energy between energy levels of the hydrogem
    atom

    Parameters:
    -----------
    n1: float,
        first level
    n2: float,
        second level
    Return:
    --------
    float,
       Energy difference between levels n1 and n2 (erg)
    '''

    return 13.6*ev*(1./square(n1)-1./square(n2))

diclevener = {'ha_b':rydberg(2,3), 'hb_b':rydberg(2,4), 'hg_b':rydberg(2,5),
              'hd_d':rydberg(2,6)}

def facnumions(nline,case,temp):
    '''
    This function compute the factor to calculate the number of ionizing
    photons. Equation taken from Osterbrock (1989)

    Q(h_alpha) = (L(h_alpha)/hv_halpha)*(alpha_(B)/alpha_(h_alpha)) (1)

    alpha_(h_alpha) is effective recombination coefficient for h_alpha

    effective recombination coefficient is defined by (effreccoeff)

    alpha_h_line = [4*pi*j_line/((np*ne) * (h*f_h_line))] (2);

    now, if it replaces (2) in (1)

    Q(h_alpha) = L(h_alpha)*[ alpha_(B)/ emicoff ];

    where emicoff = 4*pi*j_line/np*ne

    '''

    if case == 'A':
        emicoeff = (emicoeff_A[temp]*diclawext_A[nline][temp])
    else:
        emicoeff = (emicoeff_B[temp]*diclawext_B[nline][temp])

    return reccoeffB[temp-1]/emicoeff

################
# Dictionaries #
################

dicref={'d':[4102.892,'hdelta'], 'g':[4340.464,'hgamma'],
        'b':[4861.325,'hbeta'], 'a':[6562.80,'halpha']}
#diclines = { 'hdelta':4102.892, 'hgamma':4340.464, 'heII':4685.71,
#             'hbeta':4861.325, 'OIII3': 4363.210, 'OIII2':4958.911,
#             'OIII':5006.843, 'heI':5875.6, 'halpha':6562.80, 'NII3':5754.644,
#             'NII2':6548.04,'NII':6583.46, 'SII':6716.44, 'SII2':6730.81}
dictemp={0:2500, 1:5000, 2:10000, 3:20000}




def calc2c2EVB(lawext, temp, case, fext, flux_l, flux_ref):
    '''
    From the fluxes of the two Balmer lines is calculate the extinction factor
    of a given extinction law, recombination case (A or B) and electronic
    temperature.

    Parameters:
    -----------
    lawext : string,
        ratio between line using reference line, e.g., 'ha_b' (H_alfa/H_beta)
    temp   : int,
        temperature of the nebula, 0=2500, 1=5000, 2=10000, 3=20000 K
    case   : str,
        case of the recombination theory 'A' or 'B'
    fext   : string,
        extinction curve that can be use: 'f31', 'f55' and 'SMC'
    flux_l : float,
        flux of the line
    flux_ref : float,
        flux of the reference line

    Return
    ------
    C: float,
       factor of the extinction
    E_B_V: float,
        extinction factor
    '''

    flambda     = funcext(dicref[lawext[1]][0],fext)
    flambda_ref = funcext(dicref[lawext[3]][0],fext)
    #print (flambda, flambda_ref, lawext[1], dicref[lawext[1]])
    print (("\nThe extinction curve (A_lambda/Av) used {0}:" +
            "\n{0}(A_lambda = {1} {2})={3:.2f}" +
            "\n{0}(A_lambda = {4} {5})={6:.2f}").format(fext,
            dicref[lawext[1]][0], dicref[lawext[1]][1], flambda,
            dicref[lawext[3]][0], dicref[lawext[3]][1], flambda_ref))
    if case == 'A' : ratio_lines = diclawext_A[lawext][temp]
    else           : ratio_lines = diclawext_B[lawext][temp]
    print (("For the case {} the theoretical ratio between these lines at a" +
           " T= {:.0f} K is {:.3f}").format(case, dictemp[temp], ratio_lines))

    c=( -1./(flambda-flambda_ref)  )*log10( (flux_l/flux_ref)/ratio_lines )

    E_B_V=2.5*c*(funcext(4450)-funcext(5510))

    return c, E_B_V


def correcbyc(fline,nline,c,flabd='f31'):
    '''
    This function given a extinction factor (c) and extinction law does the
    correction flux

    Parameters:
    -----------
    fline : float,
        observed flux of the line
    nline : float or str,
        name of the line that will be corrected by the extinction factor or
        wavelength array.
    c     : float,
        factor of the extinction
    flabd : string,
        curve extinction that  can be use: 'f31', 'f55' and 'SMC'

    Return
    ------
    fline_cor, flux of the line corrected  by the extinction factor
    mag_ext, extinction magnitude

    '''

    if type(nline)==str:
        A_lambda  = 2.5*c*funcext(diclines[nline], flabd)
    else:
        A_lambda  = 2.5*c*funcext(nline, flabd)
    fline_cor = fline*( 10**(0.4*A_lambda) )

    return fline_cor, A_lambda


def correcbyEBV(fline,nline,EBV,flabd='f31'):
    '''
    This function given a extinction factor (EBV) and extinction law does the
    correction flux

    Parameters:
    -----------
    fline: float,
        observed flux of the line
    nline: float or str,
        name of the line that will be corrected by the extinction factor or
        wavelength array.
    EBV: float,
        the color excess E(B-V)=A_B-A_V
    flabd: string,
        curve extinction that  can be use: 'f31', 'f55' and 'SMC'

    Return
    ------
    fline_cor, flux of the line corrected  by the extinction factor
    mag_ext, extinction magnitude
    '''

    c = EBV/(2.5*(funcext(4450) - funcext(5510)))
    if type(nline)==str :
        A_lambda  = 2.5*c*funcext(diclines[nline], flabd)
    else                :
        A_lambda  = 2.5*c*funcext(nline, flabd)
    fline_cor = fline*( 10**(0.4*A_lambda) )

    return fline_cor, A_lambda


####################################################


#f1n='mapflux_halfa.fits'
#f2n='mapflux_hgamma.fits'


#dx=1.0
#dy=1.0
#f1 = pf.getdata(f1n)
#f2 = pf.getdata(f2n)

##hdr  = pf.getheader(espectro)

#y=f1.shape[0]
#x=f1.shape[1]

#axiscoord=[-x*dx*0.5,x*dx*0.5,-y*dy*0.5,y*dy*0.5]

#mapc=cext('hg_a',2,'f31',10**(f2),10**(f1))
#mapa(mapc,'mapfactor_c_halfa_hgamma.png',axiscoord,'x (pix)','y (pix)','c')
#pf.writeto('mapfactor_c_halfa_hgamma.fits',mapc,clobber=True)

#putmask(mapc,mapc<0.0,nan)
#mapa(mapc,'mapfactor_c_halfa_hgamma_positive.png',axiscoord,'x (pix)','y (pix)','c')
#pf.writeto('mapfactor_c_halfa_hgamma_positive.fits',mapc,clobber=True)


###############################################################


#f1n='mapflux_hbeta.fits'
#f2n='mapflux_halfa.fits'



#dx=1.0
#dy=1.0
#f1 = pf.getdata(f1n)
#f2 = pf.getdata(f2n)

##hdr  = pf.getheader(espectro)

#y=f1.shape[0]
#x=f1.shape[1]

#axiscoord=[-x*dx*0.5,x*dx*0.5,-y*dy*0.5,y*dy*0.5]

#mapc=cext('ha_b',2,'f31',10**(f2),10**(f1))
#mapa(mapc,'mapfactor_c_halfa_hbeta.png',axiscoord,'x (pix)','y (pix)','c')
#pf.writeto('mapfactor_c_halfa_hbeta.fits',mapc,clobber=True)

#putmask(mapc,mapc<0.0,nan)
#mapa(mapc,'mapfactor_c_halfa_hbeta_positive.png',axiscoord,'x (pix)','y (pix)','c')
#pf.writeto('mapfactor_c_halfa_hbeta_positive.fits',mapc,clobber=True)
