# docstring

"""
"""

import numpy as np

def ybus(ppc):

    bus = ppc["bus"]
    branch = ppc["branch"]
    Y = np.zeros((bus.shape[0], bus.shape[0]), dtype=complex) 

    admittance = np.ones((branch.shape[0]))/(branch[:, 2] + 1j*branch[:, 3]);
    transratio = np.zeros((branch.shape[0]), dtype=complex);
    idxline = np.nonzero(branch[:,8] == 0);
    idxtrans = np.nonzero(branch[:,8]);
    transratio[idxline] =  np.exp(1j * branch[idxline, 9]);
    transratio[idxtrans] = branch[idxtrans, 8] * np.exp(1j * branch[idxtrans, 9]);

    transratio_conj = np.conj(transratio)

    toto = admittance + 1j/2 * branch[:, 4];
    fromfrom = toto / (transratio * transratio_conj);
    fromto = -admittance / transratio_conj;
    tofrom = -admittance/transratio;

    # Branch parameters
    for i in range(branch.shape[0]):
        Y[branch[i, 0].astype(int) - 1, branch[i, 0].astype(int) - 1] += fromfrom[i]
        Y[branch[i, 1].astype(int) - 1, branch[i, 1].astype(int) - 1] += toto[i]
        Y[branch[i, 0].astype(int) - 1, branch[i, 1].astype(int) - 1] += fromto[i]
        Y[branch[i, 1].astype(int) - 1, branch[i, 0].astype(int) - 1] += tofrom[i]

    # Shunt admittances and susceptances
    Y[bus[:,0].astype(int) - 1, bus[:,0].astype(int) - 1] += (bus[:,4] + 1j * bus[:,5])

    return Y


def conn_matrix(ppc):

    cmat = np.empty((ppc["nb"], ppc["nb"]), dtype=bool);
    cmat.fill(False);
    for i in range(ppc["nbr"]):
        cmat[int(ppc["branch"][i, 0] - 1),  int(ppc["branch"][i, 1] - 1)] = True;
        cmat[int(ppc["branch"][i, 1] - 1),  int(ppc["branch"][i, 0] - 1)] = True;

    return cmat;