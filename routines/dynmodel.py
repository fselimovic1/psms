# docstring

"""
"""

import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

from common.message import psms_message
from components.network import network
from components.synchronous_generator.sg import sg
from components.automatic_voltage_regulator.avr import avr
from components.turbine_governor.tg import tg


EPS = 1E-4;


def dyn_xml(settings, ppc):
    
     # XML filename
    if settings["staticdata"][-2:] == ".m":
        xml_filename = settings["staticdata"][:-2] + "_" + "DYN_" + settings["xmlsuffix"];
    else:
        xml_filename = settings["staticdata"] + "_" + "DYN_" + settings["xmlsuffix"];
    
    # Define dictioneries for nodes in XML
    dict4xml = { 
                "vars": np.empty(0, dtype=object), 
                "params": np.empty(0, dtype=object), 
                #################################### initialization ####################################
                "init": 
                { 
                    "vars": np.empty(0, dtype = object), 
                    "params": np.empty(0, dtype = object),
                    "nleqs": np.empty(0, dtype = object), 
                    "pproc": np.empty(0, dtype = object)
                },
                ########################################################################################
                "odes": np.empty(0, dtype=object), 
                "nleqs": np.empty(0, dtype=object),
                "pproc": np.empty(0, dtype=object),
                };
    
    # comments in XML
    comments = {
                "vars": np.zeros((ppc["ndyn"] + 1)), 
                "params": np.zeros((ppc["ndyn"] + 1)), 
                "odes": np.zeros((ppc["ndyn"])),
                "init": { "params": np.zeros((ppc["ndyn"] + 1)), "pproc": np.zeros((ppc["ndyn"] + 1))},
                "nleqs": np.zeros((ppc["ndyn"] + 1))
                 };

    # POWER NETWORK XML configuration
    network(settings, ppc, dict4xml, comments); 
    
    # SYNCHRONOUS GENERATOR XML configuration
    sg(settings, ppc, dict4xml, comments);

    # AUTOMATIC VOLTAGE REGULATOR XML configuration
    avr(settings, ppc, dict4xml, comments);

    # TURBINE GOVERNOR XML configuration
    tg(settings, ppc, dict4xml, comments);

    # MODEL SOLVER
    model = ET.Element("Model", attrib={"type": "DAE", "domain": "real", "method": "Trapezoidal", "eps": str(EPS), "name": xml_filename});
    
    # VARIABLES
    model.append(ET.Comment("Variables for DAE problem"));
    vars = ET.SubElement(model, "Vars", attrib= {"out": "true"})
    nvars = dict4xml["vars"].shape[0];
    for i in range(nvars):
        if i == 0:
            vars.append(ET.Comment("Power network variables"))
        elif i != 0 and i in comments["vars"]:
            no = np.where(comments["vars"] == i)[0][0] + 1;
            if ppc["nsg"] and no >= 1 and no <= ppc["nsg"]:
                vars.append(ET.Comment(f"Synchrnous generator {int(no)} (Bus {int(ppc["sg"][int(no - 1), 0])}) variables"))    
            elif ppc["navr"] and no > ppc["nsg"] and no <= ppc["nsg"] + ppc["navr"]:
                vars.append(ET.Comment(f"Automatic voltage regulator {int(no - ppc["nsg"])} (Generator {int(ppc["avr"][int(no - ppc["nsg"] - 1), 0])}) variables"))
            elif ppc["ntg"] and no > ppc["nsg"] + ppc["navr"] and no <= ppc["nsg"] + ppc["navr"] + ppc["ntg"]:
                vars.append(ET.Comment(f"Turbine governor {int(no - ppc["nsg"] - ppc["navr"])} (Generator {int(ppc["tg"][int(no - ppc["nsg"] - ppc["navr"] - 1), 0])}) variables"))
        ET.SubElement(vars, "Var", attrib= dict4xml["vars"][i]);

    # PARAMETERS
    model.append(ET.Comment("Parameters for DAE problem"));
    params = ET.SubElement(model, "Params")
    nparams = dict4xml["params"].shape[0];
    for i in range(nparams):
        if i == 0:
            params.append(ET.Comment("Power network parameters"))
        elif i != 0 and i in comments["params"]:
            no = np.where(comments["params"] == i)[0][0] + 1;
            if ppc["nsg"] and no >= 1 and no <= ppc["nsg"]:
                params.append(ET.Comment(f"Synchrnous generator {int(no)} (Bus {int(ppc["sg"][int(no - 1), 0])}) parameters")) 
            elif ppc["navr"] and no > ppc["nsg"] and no <= ppc["nsg"] + ppc["navr"]:
                params.append(ET.Comment(f"Automatic voltage regulator {int(no - ppc["nsg"])} (Generator {int(ppc["avr"][int(no - ppc["nsg"] - 1), 0])}) parameters"))
            elif ppc["ntg"] and no > ppc["nsg"] + ppc["navr"] and no <= ppc["nsg"] + ppc["ntg"] + ppc["navr"]:
                params.append(ET.Comment(f"Turbine governor {int(no - ppc["nsg"] - ppc["navr"])} (Generator {int(ppc["tg"][int(no - ppc["nsg"] - ppc["navr"] - 1), 0])}) parameters"))
        ET.SubElement(params, "Param", attrib= dict4xml["params"][i]);
    
    ################################################  INITIALIZATION ###################################################
    model.append(ET.Comment("Power flow: variables initialization"));
    init = ET.SubElement(model, "Init");
    imodel = ET.SubElement(init, "Model", attrib={"type": "NR", "domain": "real", "eps" : str(1e-6),\
                                                   "name": "PF Subproblem for DAE"});

    # I_Vars
    imodel.append(ET.Comment("Variables: bus voltage magnitudes and angles"));
    ivars = ET.SubElement(imodel, "Vars")
    nivars = dict4xml["init"]["vars"].shape[0];
    for i in range(nivars):
        ET.SubElement(ivars, "Var", attrib= dict4xml["init"]["vars"][i]); 
    
    # I_PARAMETERS
    iparams = ET.SubElement(imodel, "Params")
    niparams = dict4xml["init"]["params"].shape[0];
    for i in range(niparams):
        if i == 0:
            iparams.append(ET.Comment("Power network additional parameters"))
        elif i != 0 and i in comments["init"]["params"]:
            no = np.where(comments["init"]["params"] == i)[0][0] + 1;
            if no >= 1 and no <= ppc["nsg"]:
                iparams.append(ET.Comment(f"Synchrnous generator {int(no)} (Bus {int(ppc["sg"][int(no - 1), 0])}) additional parameters")) 
            elif no > ppc["nsg"] and no <= ppc["nsg"] + ppc["navr"]:
                iparams.append(ET.Comment(f"Turbine governor {int(no - ppc["nsg"])} (Generator {int(ppc["avr"][int(no - ppc["nsg"] - 1), 0])}) additional parameters"))
            elif no > ppc["nsg"] + ppc["navr"] and no <= ppc["nsg"] + ppc["ntg"] + ppc["navr"]:
                iparams.append(ET.Comment(f"Automatic voltage regulator {int(no - ppc["nsg"] - ppc["ntg"])} (Generator {int(ppc["tg"][int(no - ppc["nsg"] - ppc["navr"] - 1), 0])}) additional parameters"))
        ET.SubElement(iparams, "Param", attrib= dict4xml["init"]["params"][i]);
    
    # I_NLeqs
    imodel.append(ET.Comment("Power flow non-linear equations"));
    inleqs = ET.SubElement(imodel, "NLEqs")
    ninleqs = dict4xml["init"]["nleqs"].shape[0];
    for i in range(ninleqs):
        ET.SubElement(inleqs, "Eq", attrib= dict4xml["init"]["nleqs"][i]);
    
    # I_Pproc
    ipproc = ET.SubElement(imodel, "PostProc")
    nipproc = dict4xml["init"]["pproc"].shape[0];
    for i in range(nipproc):
        if i == 0:
            ipproc.append(ET.Comment("Initalization of power network variables"))
        elif i != 0 and i in comments["init"]["pproc"]:
            no = np.where(comments["init"]["pproc"] == i)[0][0] + 1;
            if ppc["nsg"] and no >= 1 and no <= ppc["nsg"]:
                ipproc.append(ET.Comment(f"Initalization of Synchrnous generator {int(no)} (Bus {int(ppc["sg"][int(no - 1), 0])}) variables")) 
            elif ppc["navr"] and no > ppc["nsg"] and no <= ppc["nsg"] + ppc["ntg"]:
                ipproc.append(ET.Comment(f"Initalization of Automatic voltage regulator {int(no - ppc["nsg"])} (Generator {int(ppc["avr"][int(no - ppc["nsg"] - 1), 0])}) variables"))
            elif ppc["ntg"] and no > ppc["nsg"] + ppc["navr"] and no <= ppc["nsg"] + ppc["ntg"] + ppc["navr"]:
                ipproc.append(ET.Comment(f"Initalization of Turbine governor {int(no - ppc["nsg"] - ppc["navr"])} (Generator {int(ppc["tg"][int(no - ppc["nsg"] - ppc["navr"] - 1), 0])}) variables"))
        ET.SubElement(ipproc, "Eq", attrib= dict4xml["init"]["pproc"][i]);
    ####################################################################################################################

    # ODEqs
    model.append(ET.Comment("Ordinary differential equations for DAE problem"));
    odes = ET.SubElement(model, "ODEqs")
    nodes = dict4xml["odes"].shape[0];
    for i in range(nodes):
        if i == 0:
            odes.append(ET.Comment(f"Synchrnous generator {int(1)} (Bus {int(ppc["sg"][0, 0])}) ordinary differential equations"))
        elif i != 0 and i in comments["odes"]:
            no = np.where(comments["odes"] == i)[0][0] + 2;
            if ppc["nsg"] and no >= 2 and no <= ppc["nsg"]:
                odes.append(ET.Comment(f"Synchrnous generator {int(no)} (Bus {int(ppc["sg"][int(no - 1), 0])}) ordinary differential equations"))
            elif ppc["navr"] and no >= ppc["nsg"] + 1 and no <= ppc["nsg"] + ppc["navr"]:
                odes.append(ET.Comment(f"Automatic voltage regulator {int(no - ppc["nsg"])} (Generator {int(ppc["avr"][int(no - ppc["nsg"] - 1), 0])}) ordinary differential equations"))
            elif ppc["ntg"] and no >= ppc["nsg"] + ppc["navr"] + 1 and no <= ppc["nsg"] + ppc["ntg"] + ppc["navr"]:
                odes.append(ET.Comment(f"Turbine governor {int(no - ppc["nsg"] - ppc["navr"])} (Generator {int(ppc["tg"][int(no - ppc["nsg"] - ppc["navr"] - 1), 0])}) ordinary differential equations"))
        ET.SubElement(odes, "Eq", attrib= dict4xml["odes"][i]);
    
    # NLEqs
    model.append(ET.Comment("Nonlinear algebraic equations for DAE problem"));
    nleqs = ET.SubElement(model, "NLEqs")
    nnleqs = dict4xml["nleqs"].shape[0];
    for i in range(nnleqs):
        if i == 0:
            nleqs.append(ET.Comment("Power network nonlinear algebraic equations"))
        elif i != 0 and i in comments["nleqs"]:
            no = np.where(comments["nleqs"] == i)[0][0] + 1;
            if ppc["nsg"] and no >= 1 and no <= ppc["nsg"]:
                nleqs.append(ET.Comment(f"Synchrnous generator {int(no)} (Bus {int(ppc["sg"][int(no - 1), 0])}) algebraic equations")) 
            elif ppc["ntg"] and no > ppc["nsg"] and no <= ppc["nsg"] + ppc["ntg"]:
                nleqs.append(ET.Comment(f"Turbine governor {int(no - ppc["nsg"])} (Generator {int(ppc["tg"][int(no - ppc["nsg"] - 1), 0])}) algebraic equations"))
        ET.SubElement(nleqs, "Eq", attrib= dict4xml["nleqs"][i]);
    
    # PProc
    model.append(ET.Comment("Postprocessing: disturbance/perturbance definition"));
    pproc = ET.SubElement(model, "PostProc")
    npproc = dict4xml["pproc"].shape[0];
    for i in range(npproc):
        eqSub = ET.SubElement(pproc, "Eq", attrib= {"cond": dict4xml["pproc"][i]["cond"]});
        ET.SubElement(eqSub, "Then", attrib= {"fx": dict4xml["pproc"][i]["fx"]});

    # Convert the ElementTree to a string
    xml_str = ET.tostring(model, encoding='utf-8', method='xml')

    # Use minidom to pretty-print the XML string
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

    with open("modelSolver/psModel/" + xml_filename + ".xml", "w", encoding='utf-8') as files:
        files.write('<?xml version="1.0" encoding="UTF-8"?>\n' + pretty_xml.split('<?xml version="1.0" ?>\n', 1)[1])


    # Success message
    psms_message(10, f"XML file '{xml_filename}' for DYNAMIC SIMULATION analysis is successfully generated.")