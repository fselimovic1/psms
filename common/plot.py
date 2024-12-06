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
            
            plotVar = False;
            if plotAll:
                if quantitiy in var:
                    plotVar = True;
            else:
                if quantitiy in var and int(var[firstnumberidx(var):]) in settings["plot"][quantitiy]:
                    plotVar = True;
            
            # Plot variable
            if plotVar:
                plt.plot(results["t[s]"][1:], results[var][1:], label = var);
        plt.legend()
        plt.show()