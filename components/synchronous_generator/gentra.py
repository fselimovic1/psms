# docstring

"""
"""

import numpy as np
import math

def gentra(no, settings, ppc, dict4xml, comments, ngeqs):
    
    ibus = int(ppc["sg"][no, 0]);

    # VARIABLES
    countVars = 0;
    varname = [ "delta", "w", "e1q", "id", "iq" ]
    for i in range(len(varname)):
        dict4xml["vars"] = np.append(dict4xml["vars"], {"name": varname[i] + str(ibus), "val": str(1)});
        countVars = countVars + 1
    
    comments["vars"][no + 1] = comments["vars"][no] + countVars;

    # PARAMETERS
    countParams = 0
    # T1d
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "T1d" + str(ibus), "val": str(ppc["sg"][no, 12])});
    countParams = countParams + 1;
    # D
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "D" + str(ibus), "val": str(ppc["sg"][no, 2])});
    countParams = countParams + 1;
    # M
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "M" + str(ibus), "val": str(ppc["sg"][no, 3])});
    countParams = countParams + 1;
    # xd
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "xd" + str(ibus), "val": str(ppc["sg"][no, 6])});
    countParams = countParams + 1;
    # xq
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "xq" + str(ibus), "val": str(ppc["sg"][no, 7])});
    countParams = countParams + 1;
    # x1d
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "x1d" + str(ibus), "val": str(ppc["sg"][no, 8])});
    countParams = countParams + 1;
    #
    comments["params"][no + 1] = comments["params"][no] + countParams;

    pmEq = "e1q" + str(ibus) + " * iq"  + str(ibus) + " + (xq" + str(ibus) + \
               " - x1d" + str(ibus) + ") * id" + str(ibus) + " * iq" + str(ibus);
    # ODEqs
    countOdes = 0;
    # delta
    dEq = "delta" + str(ibus) + "' = wn * (" + "w" + str(ibus) + " - ws)";
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": dEq});
    countOdes = countOdes + 1;
    # w
    if "tg" in ppc and any(no + 1 == tgGen for tgGen in ppc["tg"][:, 0]):
        mechPowStr = "tm" + str(ibus);
    else:
        mechPowStr = "Pm" + str(ibus); 
    wEq = "w" + str(ibus) + "' = (1/M" + str(ibus) + ") * (" + mechPowStr +  "  - (" + pmEq + ") - D" + str(ibus) + "* (w" + str(ibus) + " - ws))";
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": wEq});
    countOdes = countOdes + 1;
    # E1q
    if "avr" in ppc and any(no + 1 == avrGen for avrGen in ppc["avr"][:, 0]):
        excDCStr = "vf" + str(ibus);
    else:
        excDCStr = "Vf" + str(ibus); 
    e1qEq = "e1q" + str(ibus) + "' = (1/T1d" + str(ibus) + ") * (-e1q" + str(ibus) + " - (xd" + str(ibus) + " - x1d" \
             + str(ibus) + ") * id" + str(ibus) + " + " +  excDCStr + ")"; 
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": e1qEq});
    countOdes = countOdes + 1;
    if no == 0:
        comments["odes"][no] =  countOdes; 
    else: 
        comments["odes"][no] = comments["odes"][no - 1] + countOdes; 


    # NLEqs
    countNLEqs = 0;
    reKVLEq = "xq" + str(ibus) + " * iq" + str(ibus) + " + V" + str(ibus) + " * sin(theta" + str(ibus) + " -  delta" + \
    str(ibus) + ") = 0";
    dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": reKVLEq});
    countNLEqs = countNLEqs + 1;
    imKVLEq = "e1q" + str(ibus) + " - V" + str(ibus) +  " * cos(theta" + str(ibus) + " -  delta" + \
    str(ibus) + ") - x1d" + str(ibus) + " * id" + str(ibus) +  " = 0"
    dict4xml["nleqs"] = np.append(dict4xml["nleqs"], {"fx": imKVLEq});
    countNLEqs = countNLEqs + 1;
    # comments
    comments["nleqs"][no + 1] = comments["nleqs"][no] + countNLEqs; 

    # Correction on network NLEqs
    isg = np.where(ngeqs["sgbus"] == ppc["sg"][no, 0])[0][0];
    # + Pg
    pgEq = " + V" + str(ibus) + " * (iq" + str(ibus) + " * cos(theta" + str(ibus) + " - delta" + str(ibus) + ")"\
            " - id" + str(ibus) + " * sin(theta" + str(ibus) + " - delta" + str(ibus) + "))";
    ngeqs["pgEqs"][isg] += pgEq;
    # + Qg
    qgEq = " + V" + str(ibus) + " * (id" + str(ibus) + " * cos(theta" + str(ibus) + " - delta" + str(ibus) + ")"\
            " + iq" + str(ibus) + " * sin(theta" + str(ibus) + " - delta" + str(ibus) + "))";
    ngeqs["qgEqs"][isg] += qgEq;
    
       