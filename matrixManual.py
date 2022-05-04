import numpy as np

def matrixManual(theta, eps_1, eps_2, eps_4):
    '''
    Does a matrix multiplication without any packages, assuming our theta angle and strains are correct.
    Specifically for the matrix transformation required for projecting the xx strain.

     - Takes in the theta angle as theta.
     - Takes in each strain and numbers them from 1 to 6 depending on coordinate: (xx, yy, zz, xy, yz, zx)
    '''

    '''
    First step of the multiplication:  Q * Epsilon
    '''

    # defines cosines and sines of the matrix
    c_1 = np.cos(theta)
    s_1 = np.sin(theta)

    # First row
    Qe_11 = c_1*eps_1+s_1*eps_4
    Qe_12 = c_1*eps_4+s_1*eps_2

    # Since we only need epsilon xx, which is the first element of the final matrix, here it is:
    eps_along_camber = float(c_1*Qe_11+c_1*Qe_12)

    return eps_along_camber