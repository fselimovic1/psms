# docstring

"""
"""

from common.readinput import readmfile
from common.base import base


def processdata(settings):

    # read static data
    ppc = readmfile(settings["staticdata"]);
    
    # convert static data to base values
    ppc = base(ppc)

    return ppc;