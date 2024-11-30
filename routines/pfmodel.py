# docstring

"""
"""

import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from common.ybus import ybus
from common.message import psms_message
from components.network import network

EPS = 1e-6

def pf_xml(settings,ppc):

    # XML filename
    if settings["staticdata"][-2:] == ".m":
        xml_filename = settings["staticdata"][:-2] + "_" + "PF_" + settings["xmlsuffix"];
    else:
        xml_filename = settings["staticdata"] + "_" + "PF_" + settings["xmlsuffix"];

    # Define dictioneries for nodes in XML
    dict4xml = { 
                "vars": np.empty(0, dtype=object), 
                "params": np.empty(0, dtype=object), 
                "nleqs": np.empty(0, dtype=object),
                "pproc": np.empty(0, dtype=object)
                };
    
     # comments in XML
    comments = {
                "vars": np.zeros((ppc["ndyn"] + 1)), 
                "params": np.zeros((ppc["ndyn"] + 1)), 
                "nleqs": np.zeros((ppc["ndyn"] + 1)),
                 };
    
    # Power netowrk entries
    network(settings, ppc, dict4xml, comments)

    # MODEL SOLVER
    model = ET.Element("Model", attrib={"type": "NR", "domain": "real", "eps": str(EPS), "name": xml_filename});
    
    # VARIABLES
    model.append(ET.Comment("POWER FLOW variables: bus voltage magnitude and angles."));
    vars = ET.SubElement(model, "Vars", attrib= {"out": "true"})
    nvars = dict4xml["vars"].shape[0];
    for i in range(nvars):
        ET.SubElement(vars, "Var", attrib= dict4xml["vars"][i]);
 
    # PARAMETERS
    model.append(ET.Comment("Definition of power network parameters."));
    params = ET.SubElement(model, "Params")
    nparams = dict4xml["params"].shape[0];
    # Bus injected powers
    for i in range(nparams):
        ET.SubElement(params, "Param", attrib= dict4xml["params"][i]);

    # NONLINEAR EQUATIONS
    model.append(ET.Comment("Nonlinear POWER FLOW equations."));
    nleqs = ET.SubElement(model, "NLEqs")
    nnleqs = dict4xml["nleqs"].shape[0];
    for i in range(nnleqs):
        ET.SubElement(nleqs, "Eq", attrib= dict4xml["nleqs"][i]);
    
    # Convert the ElementTree to a string
    xml_str = ET.tostring(model, encoding='utf-8', method='xml')

    # Use minidom to pretty-print the XML string
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

    # Generate XML file
    with open("modelSolver/psModel/" + xml_filename + ".xml", "w", encoding='utf-8') as files:
        files.write('<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml.split('<?xml version="1.0" ?>\n', 1)[1])

    # Success message
    psms_message(10, f"XML file '{xml_filename}' for POWER FLOW analysis is successfully generated.")