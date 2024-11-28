# docstring

"""
"""

from common.readinput import readmfile
from common.readinput import readdyrfile
from common.base import base


def processdata(settings):

    # read static data
    ppc = readmfile(settings["staticdata"]);
    
    # convert static data to base values
    ppc = base(ppc)

    # read dynamic data
    if settings["dyndata"] != "":
        ppc = readdyrfile(settings, ppc);

    return ppc;