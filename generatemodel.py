# docstring

"""
"""

from common.processdata import processdata
from routines.generate import generatexml

# simulation settings / settings as global variable?
settings = {"solver": "powerSystemModelSolver (psms) v1.0"}

# analysis type
settings["analysis"] = "dynamics";

# input files - static data
settings["staticdata"] = "case9.m";

# input file - dynamic data, empty string if static analysis only
settings["dyndata"] = "case9d_gentra";

# suffix for XML file name, file name format: staticdatafilename_analysis_suffix
settings["xmlsuffix"] = "test";

# input data processing 
ppc = processdata(settings);

# generate power system model in XML format
generatexml(settings, ppc); 