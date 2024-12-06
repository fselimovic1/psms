# docstring

"""
"""

import numpy as np


def ieeet1(settings, ppc, dict4xml, comments):


    for i in range(ppc["navr"]):

        igen = int(ppc["avr"][i, 0]);

        # VARIABLES
        countVars = 0;
        # Measurement vm / state
        dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vrm" + str(igen)});
        countVars = countVars + 1;
        # Stabilized feedback field voltage / state
        dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vrf" + str(igen)});
        countVars = countVars + 1;
        # Regulated input voltage / state
        dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vri" + str(igen)});
        countVars = countVars + 1;
        # Field voltage / state
        dict4xml["vars"] = np.append(dict4xml["vars"], {"name": "vf" + str(igen)});
        countVars = countVars + 1;
        # vars XML comment
        comments["vars"][i + ppc["nsg"] + ppc["ntg"] + 1] = comments["vars"][i + ppc["nsg"] + ppc["ntg"]] + countVars;

        # PARAMETERS
        countParams = 0;
        # Vref
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Vref" + str(igen), "val": str(1), "out": "true"});
        countParams = countParams + 1;
        # Aef
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Aef" + str(igen), "val": str(ppc["avr"][i, 2])});
        countParams = countParams + 1;
        # Bef
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Bef" + str(igen), "val": str(ppc["avr"][i, 3])});
        countParams = countParams + 1;
        # Ka
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Ka" + str(igen), "val": str(ppc["avr"][i, 4])});
        countParams = countParams + 1;
        # Kef
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Kef" + str(igen), "val": str(ppc["avr"][i, 5])});
        countParams = countParams + 1;
        # Kf
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Kf" + str(igen), "val": str(ppc["avr"][i, 6])});
        countParams = countParams + 1;
        # Tra
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Tra" + str(igen), "val": str(ppc["avr"][i, 7])});
        countParams = countParams + 1;
        # Trb
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Trb" + str(igen), "val": str(ppc["avr"][i, 8])});
        countParams = countParams + 1;
        # Trc
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Trc" + str(igen), "val": str(ppc["avr"][i, 9])});
        countParams = countParams + 1;
        # Tef
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Tef" + str(igen), "val": str(ppc["avr"][i, 10])});
        countParams = countParams + 1;
        # Trf
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Trf" + str(igen), "val": str(ppc["avr"][i, 11])});
        countParams = countParams + 1;
        # TrR
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "TrR" + str(igen), "val": str(ppc["avr"][i, 12])});
        countParams = countParams + 1;
        # vrmax
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "vrmax" + str(igen), "val": str(ppc["avr"][i, 13])});
        countParams = countParams + 1;
        # vrmin
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "vrmin" + str(igen), "val": str(ppc["avr"][i, 14])});
        countParams = countParams + 1;
        # params XML comment
        comments["params"][i + ppc["nsg"] + ppc["ntg"] + 1] = comments["params"][i + ppc["nsg"] + ppc["ntg"]] + countParams;

        # ODEs
        countOdes = 0;
        # vrm
        vrmEq = "vrm" + str(igen) + "' = (1/TrR" + str(igen) + ") * (V" + str(igen) + " - vrm" + str(igen) +")";
        dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vrmEq});
        countOdes = countOdes + 1;
        # vrf 
        vrfEq = "vrf" + str(igen) + "' = (-1/Trf" + str(igen) + ") * ((Kf" + str(igen) + "/Trf" + str(igen) + ") * vf" + str(igen)\
            +  " + vrf" + str(igen) + ")";
        dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vrfEq});
        countOdes = countOdes + 1;
        # vri 
        vriEq = "vri" + str(igen) + "' = (1/Tra" + str(igen) + ") * (Ka" + str(igen) + " * (Vref" + str(igen) + " - vrm" + str(igen)\
            + " - vrf" + str(igen) + " - (Kf" + str(igen) + "/Trf" + str(igen) + ") * vf" + str(igen) + ") - vri" + str(igen) + ")";
        dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vriEq});
        countOdes = countOdes + 1;
        # vf 
        vfEq = "vf" + str(igen) + "' = (-1/Tef" + str(igen) + ") * (vf" + str(igen) + " * (Kef" + str(igen) + " + Aef" + str(igen)\
            + " * exp(Bef" + str(igen) + " * vf" + str(igen) + ")) - vri" + str(igen) + ")";
        dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": vfEq});
        countOdes = countOdes + 1;
        # odes XML comment
        comments["odes"][i + ppc["nsg"] + ppc["ntg"]] = comments["odes"][i + ppc["nsg"] + ppc["ntg"] - 1] + countOdes;

        ################# INITIALIZATION #######################
        # POST-PROCESSING
        countInitPproc = 0;
        # vf
        dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vf" + str(igen) + " = vf" + str(igen) + "_0"});
        countInitPproc = countInitPproc + 1;
        # vem
        dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vrm" + str(igen) + " = V" + str(igen)});
        countInitPproc = countInitPproc + 1;
        # vrf
        dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vrf" + str(igen) + " =  -Kf" + str(igen) +\
                                                                " * vf" + str(igen) + "_0 /Trf" + str(igen) });
        countInitPproc = countInitPproc + 1;
        # vri
        dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.vri" + str(igen) + " = Kef" + str(igen) +\
                                    " * vf" + str(igen) + "_0 + Aef" + str(igen) + " * exp(Bef" + str(igen) + " * vf" + str(igen) + "_0) * vf" + str(igen) + "_0"});
        countInitPproc = countInitPproc + 1;
        # Vref
        dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.Vref" + str(igen) + " = V" + str(igen) +\
         " + (1/Ka" + str(igen) + ")" + " * (Kef" + str(igen) + " * vf" + str(igen) + "_0 + Aef" + str(igen) + " * exp(Bef" +\
        str(igen) + " * vf" + str(igen) + "_0) * " + "vf" + str(igen) + "_0)"});
        countInitPproc = countInitPproc + 1;
        comments["init"]["pproc"][ppc["nsg"] + ppc["ntg"] + i + 1] = comments["init"]["pproc"][ppc["nsg"] + ppc["ntg"] + i] + countInitPproc;
