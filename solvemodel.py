# docstring

"""
"""

import os

from modelSolver.solve import solve


# simulation settings / settings as global variable?
settings = {"solver": "powerSystemModelSolver (psms) v1.0"}

# analysis type: "powerflow" / "dynamics"
settings["model_filename"] = "case9_DYN_test.xml";

# Choose variables to plot
settings["plot"] = {
    "V": [],
    "w": [], 
};

solve(settings);

