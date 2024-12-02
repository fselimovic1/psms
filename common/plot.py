# docstring

"""
"""

from common.message import psms_message

def plot(results, plot_settings):
    
    if not bool(plot_settings):
        psms_message(2, "No variables have been selected for plotting.")
        exit();
    
    # Time array
    t = results["t[s]"];