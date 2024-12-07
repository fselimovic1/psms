# docstring

"""
"""

import numpy as np


def gentra(no, settings, ppc, dict4xml, comments, ngeqs):
    
    ibus = int(ppc["sg"][no, 0]);

    # Check if AVR is connected to SG
    avr_connected = "avr" in ppc and any(no + 1 == avrGen for avrGen in ppc["avr"][:, 0]);

    # Check if TG is connected to SG
    tg_connected = "tg" in ppc and any(no + 1 == tgGen for tgGen in ppc["tg"][:, 0]);

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

    # Vf - optional
    if not avr_connected:
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Vf" + str(ibus), "val": str(1)});
        countParams = countParams + 1;
    # Pm - optional
    if not tg_connected:
        dict4xml["params"] = np.append(dict4xml["params"], {"name": "Pm" + str(ibus), "val": str(1)});
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
    if tg_connected:
        mechPowStr = "tm" + str(ibus);
    else:
        mechPowStr = "Pm" + str(ibus); 
    wEq = "w" + str(ibus) + "' = (1/M" + str(ibus) + ") * (" + mechPowStr +  "  - (" + pmEq + ") - D" + str(ibus) + "* (w" + str(ibus) + " - ws))";
    dict4xml["odes"] = np.append(dict4xml["odes"], {"fx": wEq});
    countOdes = countOdes + 1;
    # E1q
    if avr_connected:
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
    addsign = "";
    if ngeqs["qgEqs"][isg] != "":
        addsign = " + ";
    # + Pg
    pgEq = addsign + "V" + str(ibus) + " * (iq" + str(ibus) + " * cos(theta" + str(ibus) + " - delta" + str(ibus) + ")"\
            " - id" + str(ibus) + " * sin(theta" + str(ibus) + " - delta" + str(ibus) + "))";
    ngeqs["pgEqs"][isg] += pgEq;
    # + Qg
    qgEq = addsign + "V" + str(ibus) + " * (id" + str(ibus) + " * cos(theta" + str(ibus) + " - delta" + str(ibus) + ")"\
            " + iq" + str(ibus) + " * sin(theta" + str(ibus) + " - delta" + str(ibus) + "))";
    ngeqs["qgEqs"][isg] += qgEq;

    # VARIABLES/PARAMETERS INITIALIZATION
    # Parameters
    countInitParams = 0;
    # delta_0
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "delta" + str(ibus) + "_0", "val": str(0)});
    countInitParams = countInitParams + 1;
    # id_0 & iq_0
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "id" + str(ibus) + "_0", "val": str(0)});
    countInitParams = countInitParams + 1;
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "iq" + str(ibus) + "_0", "val": str(0)});
    countInitParams = countInitParams + 1;
    # Ig_r
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "Ig" + str(ibus) + "r", "val": "0"});
    countInitParams = countInitParams + 1;
    # Ig_im
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "Ig" + str(ibus) + "im", "val": "0"});
    countInitParams = countInitParams + 1;
    # Ig
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "Ig" + str(ibus), "val": "0"});
    countInitParams = countInitParams + 1;
    # fi
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "fi" + str(ibus), "val": "0"});
    countInitParams = countInitParams + 1;
     # dR
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "dR" + str(ibus), "val": "0"});
    countInitParams = countInitParams + 1;
     # dI
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "dI" + str(ibus), "val": "0"});
    countInitParams = countInitParams + 1;
    # dI
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "e1q" + str(ibus) + "_0", "val": "0"});
    countInitParams = countInitParams + 1;
    # vd_0 & vq_0
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "vd" + str(ibus) + "_0", "val": str(0)});
    countInitParams = countInitParams + 1;
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "vq" + str(ibus) + "_0", "val": str(0)});
    countInitParams = countInitParams + 1;
    # Vf_0
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "Vf" + str(ibus) + "_0", "val": str(0)});
    countInitParams = countInitParams + 1;
    # Pm_0
    dict4xml["init"]["params"] = np.append(dict4xml["init"]["params"], {"name": "Pm" + str(ibus) + "_0", "val": str(0)});
    countInitParams = countInitParams + 1;
    #
    comments["init"]["params"][no + 1] = comments["init"]["params"][no] + countInitParams;

    # PostProcessing
    countInitPproc = 0;
    # base w
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.w" + str(ibus) + " = ws"});
    countInitPproc = countInitPproc + 1;
    # Ig_r & Ig_im
    igrStr = "Ig" + str(ibus) + "r = I" + str(ibus) + "r + (1/V" + str(ibus) + ") * (pl" + str(ibus) + "_0 * cos(theta" +\
    str(ibus) + ") + ql" + str(ibus) + "_0 * sin(theta" + str(ibus) + "))";
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": igrStr});
    countInitPproc = countInitPproc + 1;
    igimStr = "Ig" + str(ibus) + "im = I" + str(ibus) + "im + (1/V" + str(ibus) + ") * (pl" + str(ibus) + "_0 * sin(theta" +\
    str(ibus) + ") - ql" + str(ibus) + "_0 * cos(theta" + str(ibus) + "))";
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": igimStr});
    countInitPproc = countInitPproc + 1;
    # Current magnitude
    iMagStr = "Ig" + str(ibus) + " = " + "sqrt(Ig" + str(ibus) + "r^2 + Ig" + str(ibus) + "im^2)";
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": iMagStr});
    countInitPproc = countInitPproc + 1;
    # Current phase
    iAngStr = "fi" + str(ibus) + " = " + "atg2(Ig" + str(ibus) + "r, Ig" + str(ibus) + "im)"; 
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": iAngStr});
    countInitPproc = countInitPproc + 1;
    # temp vars
    dR_Str = "dR" + str(ibus) + " = -xq" + str(ibus) + " * Ig" + str(ibus) + " * cos(fi" + str(ibus) + ") - V" + str(ibus)\
            + " * sin(theta" + str(ibus) + ")";
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": dR_Str});
    countInitPproc = countInitPproc + 1;
    dI_Str = "dI" + str(ibus) + " = -V" + str(ibus) + " * cos(theta" + str(ibus) + ") + xq" + str(ibus) + " * Ig" + str(ibus)\
            + " * sin(fi" + str(ibus) + ")" ;
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": dI_Str});
    countInitPproc = countInitPproc + 1;
    # delta_0
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "delta" + str(ibus)
                                                                      + "_0 = atg(dR" + str(ibus) 
                                                                      + "/dI" + str(ibus) + ")"});
    countInitPproc = countInitPproc + 1;
    # init delta
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.delta" + str(ibus) + "= delta" + str(ibus) + "_0"});
    countInitPproc = countInitPproc + 1;
    # vd
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "vd" + str(ibus) + "_0 = V" + str(ibus)\
        + " * cos(pi/2 - delta" + str(ibus) + "_0 + theta" + str(ibus) + ")"});
    countInitPproc = countInitPproc + 1;
    # vq
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "vq" + str(ibus) + "_0 = V" + str(ibus)\
        + " * sin(pi/2 - delta" + str(ibus) + "_0 + theta" + str(ibus) + ")"});
    countInitPproc = countInitPproc + 1;
    # id
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "id" + str(ibus) + "_0 = Ig" + str(ibus)\
        + " * cos(pi/2 - delta" + str(ibus) + "_0 + fi" + str(ibus) + ")"});  
    countInitPproc = countInitPproc + 1;
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.id" + str(ibus) + " = id" + str(ibus) + "_0"});
    countInitPproc = countInitPproc + 1;
    # iq
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "iq" + str(ibus) + "_0 = Ig" + str(ibus)\
        + " * sin(pi/2 - delta" + str(ibus) + "_0 + fi" + str(ibus) + ")"});
    countInitPproc = countInitPproc + 1;
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.iq" + str(ibus) + " = iq" + str(ibus) + "_0"});
    countInitPproc = countInitPproc + 1;
    # e1q
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "e1q" + str(ibus) + "_0 = V" + str(ibus)
        + "* cos(theta" + str(ibus) + " - delta" + str(ibus) + "_0) + x1d" + str(ibus) + " * id" + str(ibus) + "_0"});
    countInitPproc = countInitPproc + 1;
    # base e1q
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.e1q" + str(ibus) + "= e1q" + str(ibus) + "_0"});
    countInitPproc = countInitPproc + 1;
    # Vf
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "Vf" + str(ibus) + "_0 = e1q" + str(ibus)
        + "_0 + (xd" + str(ibus) + " - x1d" + str(ibus) + ") * id" + str(ibus) + "_0"});
    countInitPproc = countInitPproc + 1;
    if not avr_connected:
        dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.Vf" + str(ibus) + "= Vf" + str(ibus) + "_0"});
        countInitPproc = countInitPproc + 1;

    # Pm
    dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "Pm" + str(ibus) + "_0 = e1q" + str(ibus)
                                            + "_0 * iq" + str(ibus) + "_0 + (xq" + str(ibus) + " - x1d" + str(ibus) 
                                            + ") * id" + str(ibus) + "_0 * iq" + str(ibus) + "_0"});
    countInitPproc = countInitPproc + 1;
    if not tg_connected:
        dict4xml["init"]["pproc"] = np.append(dict4xml["init"]["pproc"], {"fx": "base.Pm" + str(ibus) + "= Pm" + str(ibus) + "_0"});
        countInitPproc = countInitPproc + 1;
    # Comments
    comments["init"]["pproc"][no + 1] = comments["init"]["pproc"][no] + countInitPproc;
    
       