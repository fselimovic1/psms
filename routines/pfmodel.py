# docstring

"""
"""

import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from common.ybus import ybus
from common.message import psms_message

EPS = 1e-6


# Check if two buses are connected
def busesconn(ppc, busi, busj):
    for i in range(ppc["branch"].shape[0]):
        if (ppc["branch"][i, 0] == busi and ppc["branch"][i, 1] == busj)\
            or  (ppc["branch"][i, 1] == busi and ppc["branch"][i, 0] == busj):
            return True
    return False

def pf_xml(settings,ppc):

    # XML filename
    if settings["staticdata"][-2:] == ".m":
        xml_filename = settings["staticdata"][:-2] + "_" + "PF_" + settings["xmlsuffix"];
    else:
        xml_filename = settings["staticdata"] + "_" + "PF_" + settings["xmlsuffix"];

    # Basic Power System params
    nb = ppc["bus"].shape[0]
    ng = ppc["gen"].shape[0]
    genIdx = (ppc["gen"][:, 0] - 1).astype(int)

    # Compute the admittance matrix
    Y = ybus(ppc);

    # MODEL SOLVER
    model = ET.Element("Model", attrib={"type": "NR", "domain": "real", "name": xml_filename, "eps": str(EPS)});

    # VARIABLES
    model.append(ET.Comment("POWER FLOW variables: bus voltage magnitude and angles."));
    vars = ET.SubElement(model, "Vars", attrib= {"out": "true"})
    for i in range(nb):
        # Magnitude
        if ppc["bus"][i, 1] != 1:
            ET.SubElement(vars, "Var", attrib={"name": "V" + str(i + 1), "val": str(ppc["bus"][i, 7])});
        else: 
            ET.SubElement(vars, "Var", attrib={"name": "V" + str(i + 1), "val": str(1)});
        # Angle
        ET.SubElement(vars, "Var", attrib={"name": "theta" + str(i + 1), "val": str(0)});

    # PARAMETERS
    model.append(ET.Comment("Definition of power network parameters."));
    params = ET.SubElement(model, "Params");
    # Bus injected powers
    for i in range(nb):
        # Active power
        pi = 0;
        for j in range(ng):
            if ppc["gen"][j, 0] == i + 1:
                pi = pi + ppc["gen"][j, 1];
        pi = pi - ppc["bus"][i, 2];
        ET.SubElement(params, "Param", attrib={"name": "p" + str(i + 1) + "_0", "val": str(pi)}); 
        # Reactive power
        ET.SubElement(params, "Param", attrib={"name": "q" + str(i + 1) + "_0", "val": str(-ppc["bus"][i, 3])});
    # Voltage data
    for i in range(nb):
        # Magnitude
        idx = np.where(ppc["gen"][:, 0] == i + 1)[0];
        if len(idx) == 0:
            ET.SubElement(params, "Param", attrib={"name": "V" + str(i + 1) + "_0", "val": str(ppc["bus"][i, 7])});
        else:
            ET.SubElement(params, "Param", attrib={"name": "V" + str(i + 1) + "_0", "val": str(ppc["gen"][idx[0], 5])});
        # Angle
        ET.SubElement(params, "Param", attrib={"name": "theta" + str(i + 1) + "_0", "val": str(str(ppc["bus"][i, 8]))});
    # Admittance matrix elements
    for i in range(nb):
        for j in range(nb):
            # G
            ET.SubElement(params, "Param", attrib={"name": "G_" + str(i + 1) + "_" + str(j + 1), "val": str(np.real(Y[i, j]))}); 
            # B
            ET.SubElement(params, "Param", attrib={"name": "B_" + str(i + 1) + "_" + str(j + 1), "val": str(np.imag(Y[i, j]))}); 

    # NONLINEAR EQUATIONS
    model.append(ET.Comment("Nonlinear POWER FLOW equations."));
    nleqs = ET.SubElement(model, "NLEqs")
    for i in range(nb):
        # Equations for SLACK bus
        if ppc["bus"][i][1] == 3:
            # Magnitude
            mEqStr = "V" + str(i + 1) + " - V" + str(i + 1) + "_0 = 0";
            ET.SubElement(nleqs, "Eq", attrib={"fx": mEqStr});
            # Angle
            aEqStr = "theta" + str(i + 1) + " - theta" + str(i + 1) + "_0 = 0";
            ET.SubElement(nleqs, "Eq", attrib={"fx": aEqStr});
        # Equations for PV bus
        elif ppc["bus"][i][1] == 2:
            # Magnitude
            mEqStr = "V" + str(i + 1) + " - V" + str(i + 1) + "_0 = 0";
            ET.SubElement(nleqs, "Eq", attrib={"fx": mEqStr});
            # Active power
            pEqStr = "V" + str(i + 1) + "^2*G_" + str(i + 1) + "_" + str(i + 1); 
            for j in range(nb):
                if j != i and busesconn(ppc, i + 1, j + 1):
                    pEqStr = pEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G_" + str(i + 1) + "_" + str(j + 1) + \
                    "*cos(theta" + str(i + 1) + "- theta" + str(j + 1) + ") + B_" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + \
                    str(i + 1) + " - theta" + str(j + 1) + "))";
            pEqStr = pEqStr + " - p" + str(i + 1) + "_0"; 
            ET.SubElement(nleqs, "Eq", attrib={"fx": pEqStr});
        # Equations for PQ bus
        else:
            # Active power
            pEqStr = "V" + str(i + 1) + "^2*G_" + str(i + 1) + "_" + str(i + 1); 
            for j in range(nb):
                if j != i and busesconn(ppc, i + 1, j + 1):
                    pEqStr = pEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G_" + str(i + 1) + "_" + str(j + 1) + \
                    "*cos(theta" + str(i + 1) + "- theta" + str(j + 1) + ") + B_" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + \
                    str(i + 1) + " - theta" + str(j + 1) + "))";
            pEqStr = pEqStr + " - p" + str(i + 1) + "_0"; 
            ET.SubElement(nleqs, "Eq", attrib={"fx": pEqStr}); 
           # Reactive power
            qEqStr = "-V" + str(i + 1) + "^2*B_" + str(i + 1) + "_" + str(i + 1); 
            for j in range(nb):
                if j != i and busesconn(ppc, i + 1, j + 1):
                    qEqStr = qEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G_" + str(i + 1) + "_" + str(j + 1) + \
                    "*sin(theta" + str(i + 1) + "- theta" + str(j + 1) + ") - B_" + str(i + 1) + "_" + str(j + 1) + "*cos(theta" + \
                    str(i + 1) + " - theta" + str(j + 1) + "))";
            qEqStr = qEqStr + " - q" + str(i + 1) + "_0"; 
            ET.SubElement(nleqs, "Eq", attrib={"fx": qEqStr});
    
    # Convert the ElementTree to a string
    xml_str = ET.tostring(model, encoding='utf-8', method='xml')

    # Use minidom to pretty-print the XML string
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

    # Generate XML file
    with open("modelSolver/psModel/" + xml_filename + ".xml", "w", encoding='utf-8') as files:
        files.write('<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml.split('<?xml version="1.0" ?>\n', 1)[1])

    # Success message
    psms_message(10, f"XML file '{xml_filename}' for POWER FLOW analysis is successfully generated.")