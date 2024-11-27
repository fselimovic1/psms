# docstring

"""
"""

from routines.pfmodel import pf_xml
from routines.dynmodel import dyn_xml

def generatexml(settings, ppc):
    
    # anyalysis type
    if settings["analysis"] == "powerflow":
        pf_xml(settings, ppc);
    elif settings["analysis"] == "dynamics":
        dyn_xml(settings, ppc);