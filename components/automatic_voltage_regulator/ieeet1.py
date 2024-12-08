# docstring

"""
"""

import numpy as np


def ieeet1(no, settings, ppc, dict4xml, comments):

    igen = int(ppc["avr"][no, 0]);

    # VARIABLES
    countVars = 0;
    # Measurement vm / state
    dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vrm" + str(igen)});
    countVars = countVars + 1;
    # Stabilized feedback field voltage / state
    dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vrf" + str(igen)});
    countVars = countVars + 1;
    # Regulated input voltage / state
    dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vrr" + str(igen)});
    countVars = countVars + 1;
    # Field voltage / state
    dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vf" + str(igen)});
    countVars = countVars + 1;
    # vars XML comment
    comments["vars"][no + ppc["nsg"] + 1] = comments["vars"][no + ppc["nsg"]] + countVars;

    # PARAMETERS
    countParams = 0;
    # Vref
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Vref" + str(igen), "val": str(1)});
    countParams = countParams + 1;
    # Aef
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Aef" + str(igen), "val": str(ppc["avr"][no, 11])});
    countParams = countParams + 1;
    # Bef
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Bef" + str(igen), "val": str(ppc["avr"][no, 12])});
    countParams = countParams + 1;
    # Ka
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Ka" + str(igen), "val": str(ppc["avr"][no, 4])});
    countParams = countParams + 1;
    # Kef
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Kef" + str(igen), "val": str(ppc["avr"][no, 5])});
    countParams = countParams + 1;
    # Kf
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Kf" + str(igen), "val": str(ppc["avr"][no, 6])});
    countParams = countParams + 1;
    # Ta
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Ta" + str(igen), "val": str(ppc["avr"][no, 7])});
    countParams = countParams + 1;
    # Tef
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Tef" + str(igen), "val": str(ppc["avr"][no, 9])});
    countParams = countParams + 1;
    # Tf
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Tf" + str(igen), "val": str(ppc["avr"][no, 8])});
    countParams = countParams + 1;
    # Tr
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "Tr" + str(igen), "val": str(ppc["avr"][no, 10])});
    countParams = countParams + 1;
    # vrmax
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "vrmax" + str(igen), "val": str(ppc["avr"][no, 2])});
    countParams = countParams + 1;
    # vrmin
    dict4xml["params"] = np.append(dict4xml["params"], {"name": "vrmin" + str(igen), "val": str(ppc["avr"][no, 3])});
    countParams = countParams + 1;
    # params XML comment
    comments["params"][no + ppc["nsg"] + 1] = comments["params"][no + ppc["nsg"]] + countParams;

    # ODEs
    countOdes = 0;
    # vrm
    vrmEq = "vrm" + str(igen) + "' = (1/Tr" + str(igen) + ") * (V" + str(igen) + " - vrm" + str(igen) +")";
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vrmEq});
    countOdes = countOdes + 1;
    # vrf 
    vrfEq = "vrf" + str(igen) + "' = (-1/Tf" + str(igen) + ") * ((Kf" + str(igen) + "/Tf" + str(igen) + ") * vf" + str(igen)\
        +  " + vrf" + str(igen) + ")";
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vrfEq});
    countOdes = countOdes + 1;
    # vrr 
    vrrEq = "vrr" + str(igen) + "' = (1/Ta" + str(igen) + ") * (Ka" + str(igen) + " * (Vref" + str(igen) + " - vrm" + str(igen)\
        + " - vrf" + str(igen) + " - (Kf" + str(igen) + "/Tf" + str(igen) + ") * vf" + str(igen) + ") - vrr" + str(igen) + ")";
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vrrEq});
    countOdes = countOdes + 1;
    # vf 
    vfEq = "vf" + str(igen) + "' = (-1/Tef" + str(igen) + ") * (vf" + str(igen) + " * (Kef" + str(igen) + " + Aef" + str(igen)\
        + " * exp(Bef" + str(igen) + " * vf" + str(igen) + ")) - vrr" + str(igen) + ")";
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vfEq});
    countOdes = countOdes + 1;
    # odes XML comment
    comments["odes"][no + ppc["nsg"]] = comments["odes"][no + ppc["nsg"] - 1] + countOdes;

    ################# INITIALIZATION #######################
    # POST-PROCESSING
    countInitPproc = 0;
    # vf
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vf" + str(igen) + " = Vf" + str(igen) + "_0"});
    countInitPproc = countInitPproc + 1;
    # vem
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vrm" + str(igen) + " = V" + str(igen)});
    countInitPproc = countInitPproc + 1;
    # vrf
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vrf" + str(igen) + " =  -Kf" + str(igen) +\
                                                            " * Vf" + str(igen) + "_0 /Tf" + str(igen) });
    countInitPproc = countInitPproc + 1;
    # vrr
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vrr" + str(igen) + " = Kef" \
                                + str(igen) + " * Vf" + str(igen) + "_0 + Aef" + str(igen) + " * exp(Bef" + str(igen)\
                                      + " * Vf" + str(igen) + "_0) * Vf" + str(igen) + "_0"});
    countInitPproc = countInitPproc + 1;
    # Vref
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.Vref" + str(igen) + " = V" + str(igen) +\
        " + (1/Ka" + str(igen) + ")" + " * (Kef" + str(igen) + " * Vf" + str(igen) + "_0 + Aef" + str(igen) + " * exp(Bef" +\
    str(igen) + " * Vf" + str(igen) + "_0) * " + "Vf" + str(igen) + "_0)"});
    countInitPproc = countInitPproc + 1;
    comments["init"]["pproc"][ppc["nsg"]+ no + 1] = comments["init"]["pproc"][ppc["nsg"] + no] + countInitPproc;
