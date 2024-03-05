#!/usr/bin/python
import numpy as np
import os

# abudance can be M_n1 (solar abundance), R(Twice), J(Dopita), P(SMC), Q(LMC)
# or abundance solar with diferent density (T_n0.01), (U_n0.1), (V_n10),
#                                          (L_n100)

abudic = {'M': 'M_n1_', 'R': 'R_n1_', 'J': 'J_n1_', 'P': 'P_n1_', 'Q': 'Q_n1_',
          'T': 'T_n0_01_', 'U': 'U_n0_1_', 'V': 'V_n10_', 'L': 'L_n100_',
          'S': 'S_n1000_'}

magv = ['b0', 'b0_5', 'b1', 'b2', 'be', 'b4', 'b5', 'b10']
magvt = ['b0_5', 'b1', 'b2', 'be', 'b4', 'b5', 'b10']


magdic = {'M': magv, 'R': magv, 'J': magv, 'P': magvt, 'Q': magv,
          'T': ['b0_001', 'b0_01', 'b0_05', 'b0_1', 'b0_2', 'b0_4', 'b0_5',
                'b1', 'b10'],
          'U': ['b0_0001', 'b0_001', 'b0_01', 'b0_1', 'b0_2', 'b0_32', 'b0_4',
                'b0_5', 'b0_632', 'b1_0', 'b1_26', 'b1_58', 'b2_0', 'b3_16',
                'b4_0', 'b5_0', 'b10'],
          'V': ['b0_001', 'b0_01', 'b0_1', 'b1', 'b1_58', 'b3_16', 'b5',
                'b6_32', 'b10', 'b10_2', 'b12_65', 'b15_8', 'b20', 'b30',
                'b40', 'b50', 'b100'],
          'L': ['b0_001', 'b0_01', 'b0_1', 'b1', 'be', 'b5', 'b10', 'b20',
                'b40', 'b50', 'b100'],
          'S': ['b0_01', 'b0_1', 'b1', 'b5', 'b10', 'b16', 'b32', 'b63',
                'b100', 'b160', 'b316', 'b1000']}



Bval0 = ['0.0001', '0.5', '1.0', '2.0', '3.23', '4.0', '5.0', '10.0']
Bval = { 'M': Bval0, 'R': Bval0, 'J': Bval0, 'P': Bval0, 'Q': Bval0,
         'T': ['0.001', '0.01', '0.05', '0.1', '0.2', '0.4', '0.5',
                '1.0', '10.0'],
         'U': ['0.0001', '0.001', '0.01', '0.05', '0.1', '0.2', '0.32', '0.4',
                '0.5', '0.63', '1.0', '1.26', '1.58', '2.0', '3.16',
                '4.0', '5.0', '10.0'],
         'V': ['0.001', '0.01', '0.1', '1.0', '1.58', '3.16', '5.0',
                '6.32', '10.0', '10.2', '12.6', '15.8', '20.0', '30.0',
                '40.0', '50.0', '100.0'],
         'L': ['0.001', '0.01', '0.1', '1.0', '32.3', '5.0', '10.0', '20.0',
                '40.0', '50.0', '100.0'],
         'S': ['0.01', '0.1', '1.0', '5.0', '10.0', '16.0', '32.0', '63.0',
               '100.0', '126.0', '316.0', '1000.0'] }


direc = './models_shock/'
direcbase = os.path.dirname(os.path.realpath(__file__))
direc = direcbase  + '/models_shock/'

lindic= {'hbeta': 1404, 'OIII': 1411, 'OI': 1435,  'NII2': 1443, 'halfa': 1445,
         'NII': 1446, 'SII': 1450, 'SII2': 1451}

#(1405) 1393 H I 4861.3200
#(1412) 1400 O III 5006.7700
#(1436) 1424 O I 6363.6700
#(1444) 1432 N II 6547.9600
#(1446) 1434 H I 6562.8000
#(1447) 1435 N II 6583.3400
#(1451) 1439 S II 6716.3100
#(1452) 1440 S II 6730.6800

def gridshock(line, abu, modelo, verbose='-',
              list_vel=[(np.arange(125,1025,50)), np.arange(150,1050,100)]):
    '''
    Creating a grid for a given shock model with a given metalicity and
    electronic density.

    Parameters
    ----------
    line = str,
        Emission Line which will be calculate the grid (e.g., hbeta, NII)
    abu  = str,
        Nick to indicate the metalicity and electronic density of the model
        (e.g., M_n1, R_n1)
    model = str,
        What model grid can be, model shock (_s_lines.txt),
        precusor (_p_lines.txt), shock+precusor (_sp_lines.txt)
    Returns
    ---------
    A grid (rows = magnetic field, coluns = shock velocities)
    '''
    # finding the intercept set between velocities entries of each magnetic
    # field
    for i in range(len(magdic[abu])-1):
        if i==0:
            file1  = direc + abudic[abu] + magdic[abu][i] + modelo
            ofile1 = open(file1, 'r').readlines()[10].split()[5:]
            vel1   = np.array([ float(s) for s in ofile1 ])
            if verbose != '-':
                print ('velocity fields for B=',  magdic[abu][i],vel1)

            file2  = direc + abudic[abu] + magdic[abu][i+1] + modelo
            ofile2 = open(file2, 'r').readlines()[10].split()[5:]
            vel2   = np.array([ float(s) for s in ofile2 ])
            if verbose != '-':
                print ('velocity fields for B=',  magdic[abu][i+1],vel2)


            vel_I  = set(vel1) & set (vel2)
        else:
            file3  = direc + abudic[abu] + magdic[abu][i + 1] + modelo
            ofile3 = open(file3,'r').readlines()[10].split()[5:]
            vel3   = np.array([ float(s) for s in ofile3 ])
            if verbose != '-':
                print ('velocity fields for B=',  magdic[abu][i+1],vel3)

            vel_I  = vel_I & set (vel3)


    if verbose != '-':
          print ('velocity fields in commun for all B fields',
                       sort(list(vel_I)))

    for e in list_vel:
        vel_I = vel_I - set(e)

    vel_I = np.sort(list(vel_I))


    if verbose != '-':
         print ('velocity fields in commun for all B fields',
                       sort(list(vel_I)))

    if verbose != '-':
         print('''
         # Creating grid for shock model {} (rows = magnetic field,
         #                                   columns = shock velocities (km/s))
         rows= {}

         columns = {}'''.format(abu, magdic[abu], vel_I) )

    for i, field in enumerate(magdic[abu]):
        file4  = direc + abudic[abu] + field + modelo
        ofile4 = open(file4,'r').readlines()[10].split()[5:]
        vel4   = np.array([ float(s) for s in ofile4 ])

        vel_indexes = np.in1d(vel4,vel_I)

        ofile5 = open(file4,'r').readlines()[lindic[line]].split()[4:]

        if i==0:
            grid = np.array([ float(s) for s in ofile5 ])[vel_indexes]
        else:
            gridtmp = np.array([ float(s) for s in ofile5 ])[vel_indexes]
            grid    = np.row_stack((grid,gridtmp))

    gvel = vel4[vel_indexes]
    gB = Bval[abu]

    return grid, gB, gvel

#vechbeta=gridshock(direc,'hbeta','M','_s_lines.txt')
#vecOIII=gridshock(direc,'OIII','M','_s_lines.txt')
#vecNII=gridshock(direc,'NII','M','_s_lines.txt')
#vechalfa=gridshock(direc,'halfa','M','_s_lines.txt')


#import matplotlib.pyplot as plt


#for i in range(len(vecOIII[:,0])):

# x=log10(vecNII[i,:]/(vechalfa[i,:]))
# y=log10(vecOIII[i,:])
# plt.plot(x,y)

#for i in range(len(vecOIII[0,:])):

# x=log10(vecNII[:,i]/(vechalfa[:,i]))
# y=log10(vecOIII[:,i])
# plt.plot(x,y)

#plt.xlim(-0.7,0.3)
#plt.ylim(-0.8,1.3)
#plt.show()




#print a
