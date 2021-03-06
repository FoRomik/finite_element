from basis_func import *
import numpy as np
from get_param import *

def gradu_gradv(topo,x,y):
    """
    A assembly code
    Input :

    topo : Information about the topology of the triangles. \n
    x    : An (n,3) array of n evaluation points with columns x1, x2, x3. \n
    y    : An (n,3) array of n evaluation points with columns y1, y2, y3. \n


    Output :
    the matrix which will be used in the LHS of the final linear system
    """
    global_matrix = np.zeros((x.shape[0],x.shape[0]))
    # square matrix, as many rows and cols as there are nodes
    for element in topo:

        # let K denote the current element (a triangle, here)
        # x_local, y_local store the coords of the vertices of K
        x_K = x[element]
        y_K = y[element]

        # dx_phi, dy_phi are x,y derivatives of the phi_i of K,
        # phi stores the value of each phi_i evaluated at (quadrature) points in K
        # surf_local is the area of K
        (dx_phi, dy_phi, phi, surf_K) = tri_p1(x_K, y_K, np.zeros((1,2)) )

        # every K contributes to global_matrix with a 3x3 matrix called K_matrix
        K_matrix = np.zeros((3,3))
        for i in range(0,3):
            for j in range(0,3):
                K_matrix[i,j] = surf_K *\
                (dx_phi[i]*dx_phi[j] + dy_phi[i]*dy_phi[j])

        # add K_matrix to global_matrix
        for i in range(0,3):
            for j in range(0,3):
                global_matrix[element[i], element[j]] += K_matrix[i,j]

    return global_matrix


def force(x,y):
    force = str(get_force())
    if force == "sinsin" :
        f = 2*(np.pi)**2 * np.sin(np.pi * x) * np.sin(np.pi * y)
    elif force == "one" :
        f = np.ones(len(x))
    else:
        print("Invalid force name")
        f = 0
    return f

def f_v(topo,x,y):
    """ F assembly code
    Input :

    topo : Information about the topology of the triangles. \n
    x    : An (n,3) array of n evaluation points with columns x1, x2, x3. \n
    y    : An (n,3) array of n evaluation points with columns y1, y2, y3. \n

    Output :

    F    : The RHS of poisson's equation

    Notice :
    """
    F=np.zeros((x.shape[0]))

    for element in topo:
        x_l = x[element]
        y_l = y[element]
		  
        surf_e = 1./2. *\
        abs(x_l[0]*y_l[2]-x_l[0]*y_l[1]+x_l[1]*y_l[0]-\
        x_l[1]*y_l[2]+x_l[2]*y_l[1]-x_l[2]*y_l[0] )
        l_F = surf_e/3. * force(x_l,y_l)
        for i in range (0,3):
            F[element[i]] += l_F[i]

    return F
