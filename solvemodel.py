# docstring

"""
"""

from modelSolver.solve import solve

# Simulation settings / settings as global variable?
settings = {"solver": "powerSystemModelSolver (psms) v1.0"}

# Power system model XML filename
settings["model_filename"] = "case9_DYN_V1.xml";

# Simulation time step (only for dynamics)
settings["dT"] = 1e-3;

# Simulation time/time final
settings["tf"] = 5;

# Choose variables to plot
settings["plot"] = {
    "w": [],
    "V": [],
};

# Run model solver to perform computations
results = solve(settings);

