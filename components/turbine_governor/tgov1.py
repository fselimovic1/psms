# docstring

"""
"""

import numpy as np

def tgov1(no, settings, ppc, dict4xml, comments):

    igen = int(ppc["tg"][no, 0]);

    # VARIABLES
    countVars = 0;
    # Valve opening
    dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "xg" + str(igen)});
    countVars = countVars + 1;
    # Mechanical input power
    dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "tm" + str(igen)});
    countVars = countVars + 1;
    # vars XML comment
    comments["vars"][no + ppc["nsg"] + ppc["navr"] +  1] = comments["vars"][no + ppc["nsg"] + ppc["navr"]] + countVars;

    # PARAMETERS
    countParams = 0;
    # wREF
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Porder" + str(igen), "val": str(1)});
    countParams = countParams + 1;
    # wREF
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "wref" + str(igen), "val": str(1)});
    countParams = countParams + 1;
    # Rd
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Rd" + str(igen), "val": str(ppc["tg"][no, 2])});
    countParams = countParams + 1;
    # T1
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "T1_" + str(igen), "val": str(ppc["tg"][no, 3])});
    countParams = countParams + 1;
    # T2
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "T2_" + str(igen), "val": str(ppc["tg"][no, 6])});
    countParams = countParams + 1;
    # T3
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "T3_" + str(igen), "val": str(ppc["tg"][no, 7])});
    countParams = countParams + 1;
    # params XML comment
    comments["params"][no + ppc["nsg"] + ppc["navr"] + 1] = comments["params"][no + ppc["nsg"] + ppc["navr"]] + countParams;


    # ODEs
    countOdes = 0;
    # xg
    rxgEq = "(1/T1_" + str(igen) + ") * (Porder" + str(igen) + " + (wref" + str(igen) + " - w" \
        + str(igen) + ")/Rd" + str(igen) +" - xg" + str(igen) + ")";
    xgEq = "xg" + str(igen) + "' = " + rxgEq;
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": xgEq});
    countOdes = countOdes + 1;
    # pm 
    vrfEq = "tm" + str(igen) + "' = (1/T3_" + str(igen) + ") * (T2_" + str(igen) + " * (" + rxgEq + ") + xg"\
        + str(igen) + " - tm" + str(igen) + ")"; 
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vrfEq});
    countOdes = countOdes + 1;
    # odes XML comment
    comments["odes"][no + ppc["nsg"] + ppc["navr"]] = comments["odes"][no + ppc["nsg"] + ppc["navr"] - 1] + countOdes;
    

    ################# INITIALIZATION #######################
    # POST-PROCESSING
    countInitPproc = 0;
    # Porder
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.Porder" + str(igen) + " = Pm" + str(igen) + "_0"})
    countInitPproc = countInitPproc + 1;
    # xtg
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.xg" + str(igen) + " = Pm" + str(igen) + "_0"})
    countInitPproc = countInitPproc + 1;
    # tm
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.tm" + str(igen) + " = Pm" + str(igen) + "_0"})
    countInitPproc = countInitPproc + 1;
    comments["init"]["pproc"][ppc["nsg"] + no + ppc["navr"] + 1] = comments["init"]["pproc"][ppc["nsg"] + no + ppc["navr"]] + countInitPproc;
