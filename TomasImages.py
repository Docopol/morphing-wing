import numpy as np 
import matplotlib.pyplot as plt 
import sectionDivisionExpData

'''
DO NOT RUN!!!
Will flood your folder with images.
'''

'''
experimentDatas is a 3d numpy array with [timeStampNumber] [length along contour (0) or strain (1)] [Loopletter (A,B,C,D)]
note that A C and BD are together
'''

'''
experimentDatas = sectionDivisionExpData.experimentalDatas 


for i in range (79):
    title = 'Symmetry Analysis A-C '+ str (i)
    title2 = title + '.png'
    plt.title(title)
    plt.plot (experimentDatas[i][0][0], experimentDatas[i][1][0],label = 'Outside', color = 'lime', ls = '-.')
    plt.plot (experimentDatas[i][0][2], [-x for x in experimentDatas[i][1][2]], label = 'Inside', color = 'darkred', ls = '--')

    plt.ylabel('Difference in Microstrain between Inside and Outside [μm/m]')
    plt.xlabel('Length along contour [m]')
    plt.savefig(title2)
    plt.close()

    title = 'Symmetry Analysis B-D '+ str (i)
    title2 = title + '.png'

    plt.title(title2)
    plt.plot (experimentDatas[i][0][1], experimentDatas[i][1][1],label = 'Outside', color = 'lime', ls = '-.')
    plt.plot (experimentDatas[i][0][3], [-x for x in experimentDatas[i][1][3]], label = 'Inside', color = 'darkred', ls = '--')

    plt.ylabel('Difference in Microstrain between Inside and Outside [μm/m]')
    plt.xlabel('Length along contour [m]')
    plt.savefig(title2)
    plt.close()
'''

