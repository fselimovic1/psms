# docstring

"""
"""

import os

from common.message import psms_message
from common.readout import readout
from common.plot import plot

MS_PATH = "modelSolver\\modelSolver.exe";
PSMS_MODEL_PATH = "modelSolver\\psModel\\";
RESULTS_FILE = "OUT.txt";
T_STEP = 1e-3;
TF = 10;

def solve(settings):

    model_file = PSMS_MODEL_PATH + settings["model_filename"];

    # Check if power system model exist
    if not os.path.isfile(model_file):
        psms_message(1, f"The file '{settings["model_filename"]}' do not exists or it"
                        + " is not in the folder '{PSMS_MODEL_PATH}'.");
        exit();


    # Check the type of analysis
    if "PF" in settings["model_filename"]:
        solver = "NR";
    elif "DYN" in settings["model_filename"]:
        solver = "DAE";
    else:
        psms_message(1, f"The name of the model file '{settings["model_filename"]}' is not valid." 
                     + "Please read user manual for more information");
        exit();

    # Run modelSolver
    msCommand = MS_PATH + " " + solver + " real " + model_file + " " + RESULTS_FILE +  " " + " 0 " + str(T_STEP) + " " + str(TF);
    os.system(msCommand);

    # Read simulation data
    results = readout(RESULTS_FILE);

    # Plot selected data
    plot(results, settings);

