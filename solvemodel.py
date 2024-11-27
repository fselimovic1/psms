# docstring

"""
"""

import os


model_filename = "case9_PF_test.xml"

tstep = 1e-3;
tf = 5;

# Run modelSolver
os.chdir("modelSolver");
msCommand = "modelSolver NR real psModel\\" + model_filename + " ..\\" + "OUT_" + model_filename[:-4] + ".txt" + " 0 " + str(tstep) + " " + str(tf);
os.system(msCommand);
os.chdir("..")