# docstring
"""
"""

import math 
import random

import numpy as np

from common.ybus import ybus
from common.ybus import conn_matrix


def network(settings, ppc, dict4xml, comments = {}):
    
    # Compute the admittance matrix
    Y = ybus(ppc);
    cmat = conn_matrix(ppc);

    countVars = 0;
    # VARIABLES
    for i in range(ppc["nb"]):
        # magnitude
        dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "V" + str(i + 1), "val": str(1)});
        countVars = countVars + 1
        # angle
        dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "theta" + str(i + 1), "val": str(0)});
        countVars = countVars + 1
    comments["vars"][0] = countVars; 

    # PARAMETERS
    countParams = 0
    # wn & ws
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "wn", "val": str(2 * math.pi * ppc["fn"])});
    countParams = countParams + 1
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "ws", "val": str(1)});
    countParams = countParams + 1
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "pi", "val": str(math.pi)});
    countParams = countParams + 1
    # Voltage data
    for i in range(ppc["nb"]):
        # Magnitude
        idx = np.where(ppc["gen"][:, 0] == i + 1)[0];
        if not len(idx):
            dict4xml["params"] = np.append(dict4xml["params"], {"name": "V" + str(i + 1) + "_0", "val": str(ppc["bus"][i, 7]) });
        else:
            dict4xml["params"] = np.append(dict4xml["params"], {"name": "V" + str(i + 1) + "_0", "val": str(ppc["gen"][idx[0], 5])});
        countParams = countParams + 1
        # Angle
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "theta" + str(i + 1) + "_0", "val": str(ppc["bus"][i, 8])});
        countParams = countParams + 1
    # Ybus
    for i in range(ppc["nb"]):
        for j in range(ppc["nb"]):
            # G
            dict4xml["params"] = np.append(dict4xml["params"], {"name": "G" + str(i + 1) + "_" + str(j + 1), "val": str(np.real(Y[i, j])) });
            # B
            dict4xml["params"] = np.append(dict4xml["params"], {"name": "B" + str(i + 1) + "_" + str(j + 1), "val": str(np.imag(Y[i, j])) });
            countParams = countParams + 2;
    # Load powers
    for i in range(ppc["nb"]):
        # active
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "pl" + str(i + 1) + "_0", "val": str(ppc["bus"][i, 2])});
        # reactive
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "ql" + str(i + 1) + "_0", "val": str(ppc["bus"][i, 3])});
        countParams = countParams + 2;
    # Nominal generator powers
    for i in range(ppc["nb"]):
        pi = 0;
        qi = 0;
        for j in range(ppc["ng"]):
            if ppc["gen"][j, 0] == i + 1:
                pi = pi + ppc["gen"][j, 1];
                qi = qi + ppc["gen"][j, 2];
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "pg" + str(i + 1) + "_0", "val": str(pi)});
        countParams = countParams + 1;
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "qg" + str(i + 1) + "_0", "val": str(qi)});
        countParams = countParams + 1;
    comments["params"][0] = countParams;
    
    # NLEqs
    countNLEqs = 0;
    for i in range(ppc["nb"]):
        # SLACK GENERATOR NODE
        if ppc["bus"][i, 1] == 3 and settings["analysis"] == "powerflow":
            # Magnitude
            mEqStr = "V" + str(i + 1) + " - V" + str(i + 1) + "_0 = 0";
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": mEqStr});
            countNLEqs = countNLEqs  + 1;
            # Angle
            aEqStr = "theta" + str(i + 1) + " - theta" + str(i + 1) + "_0 = 0";
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": aEqStr});
            countNLEqs = countNLEqs  + 1;
        # PV GENERATOR NODE
        elif ppc["bus"][i, 1] == 2 and settings["analysis"] == "powerflow":
            # Magnitude
            mEqStr = "V" + str(i + 1) + " - V" + str(i + 1) + "_0 = 0";
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": mEqStr});
            countNLEqs = countNLEqs  + 1;
            # Active power
            pEqStr = "V" + str(i + 1) + "^2*G" + str(i + 1) + "_" + str(i + 1); 
            for j in range(ppc["nb"]):
                if j != i and cmat[i, j]:
                    pEqStr = pEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                    "*cos(theta" + str(i + 1) + "- theta" + str(j + 1) + ") + B" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + \
                    str(i + 1) + " - theta" + str(j + 1) + "))";
            pEqStr = pEqStr + " - (pg" + str(i + 1) + "_0" + "- pl" + str(i + 1) + "_0)"; 
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": pEqStr});
            countNLEqs = countNLEqs  + 1;
        elif ppc["bus"][i, 1] == 2 or ppc["bus"][i, 1] == 3:
            # Active power
            pEqStr = "V" + str(i + 1) + "^2*G" + str(i + 1) + "_" + str(i + 1); 
            for j in range(ppc["nb"]):
                if j != i and cmat[i, j]:
                    pEqStr = pEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                            "*cos(theta" + str(i + 1) + "- theta" + str(j + 1) + ") + B" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + \
                            str(i + 1) + " - theta" + str(j + 1) + "))";
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": pEqStr + " - (busPgenEq" + str(i + 1) + ") + pl" + str(i + 1) + "_0"});
            countNLEqs = countNLEqs  + 1;
            # Reactive power
            qEqStr = "-V" + str(i + 1) + "^2*B" + str(i + 1) + "_" + str(i + 1); 
            for j in range(ppc["nb"]):
                if j != i and cmat[i, j]:
                    qEqStr = qEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                        "*sin(theta" + str(i + 1) + "- theta" + str(j + 1) + ") - B" + str(i + 1) + "_" + str(j + 1) + "*cos(theta" + \
                        str(i + 1) + " - theta" + str(j + 1) + "))";
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": qEqStr + " - (busQgenEq" + str(i + 1) + ") + ql" + str(i + 1) + "_0"});                
            countNLEqs = countNLEqs + 1;
        # PQ BUS - LOAD
        else:
            # Active power
            pEqStr = "V" + str(i + 1) + "^2*G" + str(i + 1) + "_" + str(i + 1); 
            for j in range(ppc["nb"]):
                if j != i and cmat[i, j]:
                    pEqStr = pEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                    "*cos(theta" + str(i + 1) + "- theta" + str(j + 1) + ") + B" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + \
                    str(i + 1) + " - theta" + str(j + 1) + "))";
            pEqStr = pEqStr + " + pl" + str(i + 1) + "_0 - pg" + str(i+ 1) + "_0"; 
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": pEqStr});
            countNLEqs = countNLEqs + 1;
            # Reactive power
            qEqStr = "-V" + str(i + 1) + "^2*B" + str(i + 1) + "_" + str(i + 1); 
            for j in range(ppc["nb"]):
                if j != i and cmat[i, j]:
                    qEqStr = qEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                        "*sin(theta" + str(i + 1) + "- theta" + str(j + 1) + ") - B" + str(i + 1) + "_" + str(j + 1) + "*cos(theta" + \
                        str(i + 1) + " - theta" + str(j + 1) + "))";
            qEqStr = qEqStr + " + ql" + str(i + 1) + "_0 - qg" + str(i + 1) + "_0";
            dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": qEqStr});
            countNLEqs = countNLEqs + 1;
    comments["nleqs"][0] = countNLEqs;
   
    # POST-PROCCESSING
    #### EVENT SETUP ####
    if settings["analysis"] == "dynsim" and settings["event"]["etype"] == "loadOn":
        loadpower = settings["event"]["power"];
        totalload = sum(ppc["bus"][:, 2])
        load_toadd = loadpower * totalload/100
        loadbus = np.where(ppc["bus"][:, 2] != 0)[0]
        bus_toadd = loadbus[random.randint(0, len(loadbus) - 1)];
        new_load = ppc["bus"][bus_toadd, 2] + load_toadd;
        dict4xml["pproc"] = np.append(dict4xml["pproc"], {"cond": "t > " + str(settings["etime_s"]), "fx": "pl" + \
                                                          str(bus_toadd + 1) + "_0 = " + str(new_load)});
    
    ################################################## INITIALIZATION ##################################################
    if settings["analysis"] == "dynamics":
        # VARIABLES
        for i in range(ppc["nb"]):
            # magnitude
            dict4xml["init"]["vars"] = np.append(dict4xml["init"]["vars"], {"name": "V" + str(i + 1), "val": str(1)});
            # angle
            dict4xml["init"]["vars"] = np.append(dict4xml["init"]["vars"], {"name": "theta" + str(i + 1), "val": str(0)}); 
        # PARAMETERS  
        # bus injected powers
        countInitParams = 0;
        # additonal parameters/injected currents
        for i in range(ppc["nb"]):
            # real injected current
            dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "I" + str(i + 1) + "r", "val": str(0)});
            countInitParams = countInitParams + 1;
            # imag injected current
            dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "I" + str(i + 1) + "im", "val": str(0)});
            countInitParams = countInitParams + 1;
        comments["init"]["params"][0] = countInitParams;

        # NLEqs
        for i in range(ppc["nb"]):
            # equations for slack bus
            if ppc["bus"][i][1] == 3:
                # magnitude
                mEqStr = "V" + str(i + 1) + " - V" + str(i + 1) + "_0 = 0";
                dict4xml["init"]["nleqs"] = np.append(dict4xml["init"]["nleqs"], {"fx": mEqStr});
                # angle
                aEqStr = "theta" + str(i + 1) + " - theta" + str(i + 1) + "_0 = 0";
                dict4xml["init"]["nleqs"] = np.append(dict4xml["init"]["nleqs"], {"fx": aEqStr});
            # equations for pv bus
            elif ppc["bus"][i][1] == 2:
                # magnitude
                mEqStr = "V" + str(i + 1) + " - V" + str(i + 1) + "_0 = 0";
                dict4xml["init"]["nleqs"] = np.append(dict4xml["init"]["nleqs"], {"fx": mEqStr});
                # active power
                pEqStr = "V" + str(i + 1) + "^2*G" + str(i + 1) + "_" + str(i + 1); 
                for j in range(ppc["nb"]):
                    if j != i and cmat[i, j]:
                        pEqStr = pEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                        "*cos(theta" + str(i + 1) + "- theta" + str(j + 1) + ") + B" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + \
                        str(i + 1) + " - theta" + str(j + 1) + "))";
                pEqStr = pEqStr + " - (pg" + str(i + 1) + "_0" + "- pl" + str(i + 1) + "_0)"; 
                dict4xml["init"]["nleqs"] = np.append(dict4xml["init"]["nleqs"], {"fx": pEqStr});
            # equations for pq bus
            else:
                # active power
                pEqStr = "V" + str(i + 1) + "^2*G" + str(i + 1) + "_" + str(i + 1); 
                for j in range(ppc["nb"]):
                    if j != i and cmat[i, j]:
                        pEqStr = pEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                        "*cos(theta" + str(i + 1) + "- theta" + str(j + 1) + ") + B" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + \
                        str(i + 1) + " - theta" + str(j + 1) + "))";
                pEqStr = pEqStr + " + pl" + str(i + 1) + "_0 - pg" + str(j + 1) + "_0"; 
                dict4xml["init"]["nleqs"] = np.append(dict4xml["init"]["nleqs"], {"fx": pEqStr});
                # reactive power
                qEqStr = "-V" + str(i + 1) + "^2*B" + str(i + 1) + "_" + str(i + 1); 
                for j in range(ppc["nb"]):
                    if j != i and cmat[i, j]:
                        qEqStr = qEqStr + "+ V" + str(i + 1) + "*V" + str(j + 1) + "*(G" + str(i + 1) + "_" + str(j + 1) + \
                        "*sin(theta" + str(i + 1) + "- theta" + str(j + 1) + ") - B" + str(i + 1) + "_" + str(j + 1) + "*cos(theta" + \
                        str(i + 1) + " - theta" + str(j + 1) + "))";
                qEqStr = qEqStr + " + ql" + str(i + 1) + "_0 - qg" + str(j + 1) + "_0";  
                dict4xml["init"]["nleqs"] = np.append(dict4xml["init"]["nleqs"], {"fx": qEqStr});
        
        countInitPproc = 0;
        # PostProcessing
        for i in range(ppc["nb"]):
            # magnitude
            dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.V" + str(i + 1) + " = V" + str(i + 1)});
            countInitPproc = countInitPproc + 1;
            # angle
            dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.theta" + str(i + 1) + " = theta" + str(i + 1)});
            countInitPproc = countInitPproc + 1;
        # compute injected currents
        for i in range(ppc["nb"]):
            iReStr = "I" + str(i + 1) + "r = ";
            iImStr = "I" + str(i + 1) + "im = ";
            for j in range(ppc["nb"]):
                # real
                iReStr = iReStr + "+ V" + str(j + 1) + " * (" + "G" + str(i + 1) + "_" + str(j + 1) + "*cos(theta" + str(j + 1)\
                    + ") - B" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + str(j + 1) + "))";
                # imag
                iImStr = iImStr + "+ V" + str(j + 1) + " * (" + "G" + str(i + 1) + "_" + str(j + 1) + "*sin(theta" + str(j + 1)\
                    + ") + B" + str(i + 1) + "_" + str(j + 1) + "*cos(theta" + str(j + 1) + "))";
            dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": iReStr});
            countInitPproc = countInitPproc + 1;
            dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": iImStr}); 
            countInitPproc = countInitPproc + 1;
        comments["init"]["pproc"][0] = countInitPproc;
    ####################################################################################################################