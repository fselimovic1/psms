# docstring

"""
"""

import re

import matplotlib.pyplot as plt

from common.message import psms_message

def firstnumberidx(string):

    for i in range(len(string)):
        if isinstance(string[i], (int, float)): 
            return i; 
    return -1;

def plot(results, settings):
    
    if not bool(settings["plot"]):
        psms_message(2, "No variables have been selected for plotting.");
        exit();

    for quantitiy in settings["plot"].keys():
        plt.figure()
        plotAll = False
        if not bool(settings["plot"][quantitiy]):
            plotAll = True;

        for var in results.keys():
            if plotAll:
                if quantitiy in var:
                    plt.plot(results["t[s]"], results[var], label = var);
            else:
                if quantitiy in var and int(var[firstnumberidx(var):]) in settings["plot"][quantitiy]:
                    plt.plot(results["t[s]"], results[var], label = var);

        plt.legend()
        plt.show()

            
        



    """
    plt.figure(1)
    for i in range(ppc["sg"].shape[0]):
        vr = settings["v2plot"] + str(int(ppc["sg"][i, 0])); 
        plt.plot(simdata["t[s]"][1:], simdata[vr][1:], label = vr)
    #plt.plot(simdata["t[s]"][1:], np.array(simdata["theta1"][1:]) - np.array(simdata["theta2"][1:]), label = "w1")
    plt.legend()
    plt.show()
    """

