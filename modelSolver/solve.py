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
    msCommand = MS_PATH + " " + solver + " real " + model_file + " " + RESULTS_FILE +  " " + " 0 " + \
                str(settings["dT"]) + " " + str(settings["tf"]);
    os.system(msCommand);

    # Read simulation data
    results = readout(RESULTS_FILE);

    # Success message
    psms_message(10, f"The simulation was successfully completed without any issues!")

    # Plot selected data
    plot(results, settings);

