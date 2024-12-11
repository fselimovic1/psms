# docstring

"""
"""

from common.processdata import processdata
from routines.generate import generatexml

# simulation settings / settings as global variable?
settings = {"solver": "powerSystemModelSolver (psms) v1.0"}

# analysis type: "powerflow" / "dynamics"
settings["analysis"] = "dynamics";

# input files - static data
settings["staticdata"] = "case9.m";

# input file - dynamic data, empty string if static analysis only
settings["dyndata"] = "case9d";

# suffix for XML file name, file name format: staticdatafilename_analysis_suffix
settings["xmlsuffix"] = "V1";

# EVENT settings
# 1 Load on: {"etype": "loadOn", "power": 5} 
# 2 Load off: {"etype": "loadOff", "power": 5} 
# 3 Line removal: {"etype": "lrem", "noLine": 7 } -> to be implemented
# ts - time instant when event starts
# te - time instant when event ends
settings["event"] = {
        "etype": "lrem",
        "noLine": 5,
        "ts": 1,
        }

# input data processing 
ppc = processdata(settings);

# generate power system model in XML format
generatexml(settings, ppc); 