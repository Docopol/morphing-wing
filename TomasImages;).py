import numpy as np 
import matplotlib.pyplot as plt 
#import sectionDivisionExpData


'''
experimentDatas is a 3d numpy array with [timeStampNumber] [length along contour (0) or strain (1)] [Loopletter (A,B,C,D)]
note that A C and BD are together
'''
experimentDatas = sectionDivisionExpData.experimentalDatas 


for i in range (79):
    title = 'Symmetry Analysis A-C '+ str (i)
    title2 = title1 + '.png'
    plt.set_title(title)
    plt.plot (experimentDatas[timeStamps[i]][0][0], experimentDatas[timeStamps[i]][1][0],label = 'Outside', color = 'lime', ls = '-.')
    plt.plot (experimentDatas[timeStamps[i]][0][2], [-x for x in experimentDatas[timeStamps[i]][1][2]], label = 'Inside', color = 'darkred', ls = '--')

    plt.set_ylabel('Difference in Microstrain between Inside and Outside [μm/m]')
    plt.set_xlabel('Length along contour [m]')
    plt.savefig(title2.png)

    title = 'Symmetry Analysis B-D '+ str (i)
    title2 = title1 + '.png'

    plt.set_title(title)
    plt.plot (experimentDatas[timeStamps[i]][0][1], experimentDatas[timeStamps[i]][1][1],label = 'Outside', color = 'lime', ls = '-.')
    plt.plot (experimentDatas[timeStamps[i]][0][3], [-x for x in experimentDatas[timeStamps[i]][1][3]], label = 'Inside', color = 'darkred', ls = '--')

    plt.set_ylabel('Difference in Microstrain between Inside and Outside [μm/m]')
    plt.set_xlabel('Length along contour [m]')
    plt.savefig(title2)


