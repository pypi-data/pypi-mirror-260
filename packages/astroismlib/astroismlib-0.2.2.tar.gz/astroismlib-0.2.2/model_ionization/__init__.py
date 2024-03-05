import numpy as np
import os

#atm is either L = Lejeune et al. extended atmospheres (+ Kurucz atmospheres)
#              K = Kurucz atmospheres

parmion = ['q3.0e8', 'q1.5e8', 'q8.0e7', 'q4.0e7', 'q2.0e7', 'q1.0e7',
           'q5.0e6']
Z_sb99 = ['Z.05', 'Z0.2', 'Z0.4', 'Z1.0', 'Z2.0']

txtQ = ['q=3.0e8', 'q=1.5e8', 'q=8.0e7', 'q=4.0e7', 'q=2.0e7', 'q=1.0e7',
           'q=5.0e6']
txtZ99  = ['Z=0.05', 'Z=0.2', 'Z=0.4', 'Z=1.0', 'Z=2.0']
txtZPeg = ['Z=0.1', 'Z=0.2', 'Z=0.5', 'Z=1.0', 'Z=1.5', 'Z=2.0', 'Z=3.0']

Z_Peg  = ['Z0.1', 'Z0.2', 'Z0.5', 'Z1.0', 'Z1.5', 'Z2.0', 'Z3.0']

direcbase = os.path.dirname(os.path.realpath(__file__))
moddic = direcbase + '/models_phot/'

#(76)  4861.32      2.55042        1.000     H  I         1
#(78)  5006.77      2.47633       0.1920     O  III       2
#(55)   6300.20      1.96794       2.4742E-02 O  I         3
#(92)  6562.80      1.88920        2.941     H  I         1
#(93)  6583.34      1.88330       5.2282E-02 N  II        2
#(94)  6716.31      1.84602       9.3020E-02 S  II        2
#(95)  6730.68      1.84208       6.4529E-02 S  II        2

lindic= {'hbeta': '4861.32', 'OIII': '5006.77', 'OI':'6300.20',
         'halfa': '6562.80',
         'NII': '6583.34', 'SII': '6716.31', 'SII2': '6730.68'}

def gridphot(line, cod, sb, age, ne, atm):

    '''
    Parameters:
    -----------
    line = str,
        Flux of the line with respect H_beta flux, possible lines: hbeta,
        OIII, halfa, NII, SII, SII2
    cod = str,
        Type of the model: Starburst99 (SB99) or Pegase 2.0 (Peg)
    sb  = str,
        Type of starburst: Continuous (cont) or Instantaneus (inst)
    age = str,
        Age model, 0Mry or 8Myr for SB99, and 0Myr or 4Mur for Peg
    ne  = str,
        Electronic Density: n10 or n350
    atm = str,
        Atmosfore model, Lejeune (L) or Kurucz (K).

    Return:
    ----------
    Return a matrix rows metallicity and columns parameters inozation (q)

    '''

    if cod == 'SB99':
        met = Z_sb99
    else:
        met = Z_Peg
    gridv = np.zeros([len(met),len(parmion)])
    direc = moddic + cod + '_' + sb + '_' + ne + '/'

    for i, meti in enumerate (met):
        for j, parmioni in enumerate (parmion):

            if atm != '' and cod == 'SB99':
                nfile = (direc + 'spec_' + meti + '_' + age + '_' + parmioni +
                         '_' + cod + '_' + atm + '.ph4')
            elif atm == '' and cod != 'SB99':
                nfile = (direc + 'spec_' + meti + '_' + age + '_' + parmioni +
                         '.ph4')
            else:
                nfile = (direc + 'spec_' + meti + '_' + age + '_' + parmioni +
                         '_' + cod + '.ph4')

            ofile  = open(nfile,'r').readlines()[19:]
            lines  = np.array([e.split()[0] for e in ofile])
            flines = [e.split()[2] for e in ofile]

            ind = np.where(lines == lindic[line])[0][0]
            gridv[i,j] = flines[ind]

    return gridv


#cod = 'SB99'
#
#atm = 'K'; age = '8Myr'; sb  = 'cont'
#ne  = 'n350'
#ne  = 'n10'
#
#atm = ''; age = '0Myr'; sb  = 'inst'
#ne  = 'n350'
#ne  = 'n10'
#
#cod = 'Peg'; atm = ''
#
#age = '4Myr'; sb  = 'cont'
#ne  = 'n350'
#ne  = 'n10'
#
#age = '0Myr'; sb  = 'inst'
#ne  = 'n350'
#ne  = 'n10'
#
#ionphbeta = gridphot('hbeta', cod, sb, age, ne, atm)
#ionpOIII  = gridphot('OIII', cod, sb, age, ne, atm)
#ionpNII   = gridphot('NII', cod, sb, age, ne, atm)
#ionphalfa = gridphot('halfa', cod, sb, age, ne, atm)
#ionpSII   = gridphot('SII', cod, sb, age, ne, atm)
#ionpSII2  = gridphot('SII2', cod, sb, age, ne, atm)
#
#from matplotlib.pyplot import *
#
### Diagram [OIII]/Hb vs [NII]/Ha
#
### run in metalicities
##for i in range(len(ionpOIII[:, 0])):
##    x1 = log10(ionpNII[i, :]/(ionphalfa[i, :]))
##    y1 = log10(ionpOIII[i, :])
##    plot(x1, y1, 'r-')
##    text(x1[-1], y1[-1]-0.2, Z_sb99[i])
##
### run in q parameters
##for i in range(len(ionpOIII[0, :])):
##    x1 = log10(ionpNII[:, i]/(ionphalfa[:, i]))
##    y1 = log10(ionpOIII[:, i])
##    plot(x1, y1, 'r--')
##    text(x1[0]-0.3, y1[0], parmion[i])
##
##xlim(-2.9,1.0)
##ylim(-2.0,1.5)
##show()
#
#
## Diagram [OIII]/Hb vs [SII]/Ha
#
## run in metalicities
#For i in range(len(ionpOIII[:, 0])):
#    x1 = log10((ionpSII[i, :] + ionpSII2[i, :])/(ionphalfa[i, :]))
#    y1 = log10(ionpOIII[i, :])
#    plot(x1, y1, 'r-')
#    text(x1[-1], y1[-1]-0.2, Z_sb99[i])
#
### run in q parameters
##for i in range(len(ionpOIII[0, :])):
##    x1 = log10((ionpSII[:, i] + ionpSII2[:, i])/(ionphalfa[:, i]))
##    y1 = log10(ionpOIII[:, i])
##    plot(x1, y1, 'r--')
##    text(x1[0]-0.3, y1[0], parmion[i])
#
#xlim(-2.0,0.7)
#ylim(-1.7,1.5)
#show()
