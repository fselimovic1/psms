# docstring

"""
"""

import os
import math
import numpy as np

from common.message import psms_message

# STATIC
BUS_DATA_SIZE = 13;
GEN_DATA_SIZE = 10;
BRANCH_DATA_SIZE = 13;
STATIC_PATH = "data\\static\\";

# DYNAMIC
SG_DATA_SIZE = 16;
GENCLS_DATA_SIZE = 5;
GENTRA_DATA_SIZE = 12;
AVR_DATA_SIZE = 13;
IEEET1_DATA_SIZE = 17;
TG_DATA_SIZE = 16;
DYN_PATH = "data\\dynamic\\";


def satfun_coeff(points):

    E1 = points[0];
    S1 = points[1];
    E2 = points[2];
    S2 = points[3];

    # Coefficient for exponential saturation function
    Bx = (math.log(S1/S2))/(E1 - E2);
    Ax = S1/(math.exp(Bx * E1));

    return [ Ax, Bx ];

def readmfile(sfile):

    if sfile[-2:] == ".m":
        filename = STATIC_PATH + sfile;
    else:
        filename = STATIC_PATH + sfile + ".m"

    # Check if file exist
    if not os.path.isfile(filename):
        psms_message(1, f"The file '{sfile}' does not exist or it is not in the folder '{STATIC_PATH}'.");
        exit();

    # define internal power system data format
    ppc = {
        "bus": np.empty((0, BUS_DATA_SIZE)),
        "gen": np.empty((0, GEN_DATA_SIZE)),
        "branch": np.empty((0, BRANCH_DATA_SIZE)),
        "baseMVA": 0
    }

    # read data from file
    busmat = False;
    genmat = False;
    branchmat = False;
    # Open the .m file in read mode
    with open(filename, 'r') as file:
        # Read and process each line
        for line in file:
            sline = line.strip();
            if sline[0:13] == "mpc.baseMVA =":
                ppc["baseMVA"] = float(sline[14:-1]);
            if sline[0:11] == "mpc.bus = [":
                if len(sline) > 11:
                    psms_message(1, "Incorrect data format detected. The M file must be written in accordance"
                                    + " with the software manual.");
                    exit();
                busmat = True;
                continue;
            if sline[0:11] == "mpc.gen = [":
                if len(sline) > 11:
                    psms_message(1, "Incorrect data format detected. The M file must be written in accordance"
                                    + " with the software manual.");
                    exit();
                genmat = True;
                continue;
            if sline[0:14] == "mpc.branch = [":
                if len(sline) > 14:
                    psms_message(1, "Incorrect data format detected. The M file must be written in accordance"
                                    + " with the software manual.");
                    exit();
                branchmat = True;
                continue;
            if sline[-2:] == "];":
                if len(sline) > 2:
                    psms_message(1, "Incorrect data format detected. The M file must be written in accordance"
                                    + " with the software manual.");
                    exit();
                busmat = False;
                genmat = False;
                branchmat = False;
            
            if busmat:
                array = np.fromstring(sline, sep = " ")
                # check data format
                a_len = len(array);
                n_row = ppc["bus"].shape[0] + 1;
                if a_len < BUS_DATA_SIZE:
                    psms_message(1, "The row number {n_row} of the matrix mpc.bus has {a_len} elements which is lower"
                           + f" than the required  number of {BUS_DATA_SIZE} elements.\n")
                    exit();   
                elif a_len > BUS_DATA_SIZE:
                    psms_message(2, f"The row number {n_row} of the matrix mpc.bus has {a_len} elements which is higher" 
                           + f" than the required  number of {BUS_DATA_SIZE} elements. Excess elements will be ignored.")
                    array = array[:BUS_DATA_SIZE];

                ppc["bus"] = np.vstack([ppc["bus"], array]);
            if genmat:
                array = np.fromstring(sline, sep = " ")
                # check data format
                a_len = len(array);
                n_row = ppc["gen"].shape[0] + 1;
                if a_len < GEN_DATA_SIZE:
                    psms_message(1, f"ERROR!\nThe row number {n_row} of the matrix mpc.gen has {a_len} elements which is lower"
                           + f" than the required  number of {GEN_DATA_SIZE} elements.\n")
                    exit();   
                elif a_len > GEN_DATA_SIZE:
                    psms_message(2, f"The row number {n_row} of the matrix mpc.gen has {a_len} elements which is higher" 
                           + f" than the required  number of {GEN_DATA_SIZE} elements. Excess elements will be ignored.")
                    array = array[:GEN_DATA_SIZE];
                
                ppc["gen"] = np.vstack([ppc["gen"], array[:10]]);
            if branchmat:
                array = np.fromstring(sline, sep = " ")
                # check data format
                a_len = len(array);
                n_row = ppc["branch"].shape[0] + 1;
                if a_len < BRANCH_DATA_SIZE:
                    psms_message(1, f"The row number {n_row} of the matrix mpc.branch has {a_len} elements which is lower"
                           + f" than the required  number of {BRANCH_DATA_SIZE} elements.\n")
                    exit();   
                elif a_len > BRANCH_DATA_SIZE:
                    print(2, f"The row number {n_row} of the matrix mpc.branch has {a_len} elements which is higher" 
                           + f" than the required  number of {BRANCH_DATA_SIZE} elements. Excess elements will be ignored.")
                    array = array[:BRANCH_DATA_SIZE];
                ppc["branch"] = np.vstack([ppc["branch"], array]);

    # Set nominal frequency
    ppc["fn"] = 60;
    
    # Number of buses
    ppc["nb"] = ppc["bus"].shape[0];
    # Number of generators
    ppc["ng"] = ppc["gen"].shape[0];
    # Number of branches
    ppc["nbr"] = ppc["branch"].shape[0];

    ppc["ndyn"] = 0;

    # Basic data check
    if not ppc["nb"]:
        psms_message(1, "Matrix mpc.bus is not entered or data format is incorrect. The M file must be written in accordance"
                        + " with the software manual.\n")
        exit()
    if not ppc["ng"]:
        psms_message(1, "Matrix mpc.gen is not entered or data format is incorrect. The M file must be written in accordance"
                        + " with the software manual.\n")
        exit()
    if not ppc["nbr"]:
        psms_message(1, "Matrix mpc.branch is not entered or data format is incorrect. The M file must be written in accordance"
                        + " with the software manual.\n")
        exit()
    if not int(ppc["baseMVA"]):
        psms_message(1, "baseMVA not entered or equal to zero. The M file must be written in accordance"
                        + " with the software manual.\n")
        exit()
                    
    return ppc;



def readdyrfile(settings, ppc):
    
    # Dynamic models currently supported
    models = [ "GENCLS", "GENTRA", "IEEET1", "TGOV1" ];

    dynfile = settings["dyndata"];

    if dynfile[-4:] == ".dyr":
        filename = DYN_PATH + dynfile;
    else:
        filename = DYN_PATH + dynfile + ".dyr";

    # check if file exist
    if not os.path.isfile(filename):
        psms_message(1, f"The file '{dynfile}' does not exist or it is not in the folder '{DYN_PATH}'.");
        exit();

    # define internal power system data format
    ppc["sg"] = np.empty((0, SG_DATA_SIZE));
    ppc["avr"] = np.empty((0, AVR_DATA_SIZE));
    ppc["tg"] = np.empty((0, TG_DATA_SIZE));

    # Open the .dyr file in read mode
    with open(filename, 'r') as file:
        # Read and process each line
        data = "";
        emptydata = False;
        for line in file:
            sline = line.strip();

            # Ignore comments and blank lines
            if sline == "" or sline[:2] == "//" :
                if bool(data):
                    psms_message(1, "Incorrect data format detected. The M file must be written in accordance"
                                    + " with the software manual.");
                    exit();
                continue;
            if sline[-1:] != "/":
                data = data +  sline + " ";
                continue

            data = data + sline[:-1];

            data = data.split();   # Columns have to be separated with ', '
            modelname = data[1].replace("'", "");
            if modelname not in models:
                psms_message(1, f"Model termed {modelname} is not supported. Please read user manual to check" 
                             +" which dynamic models are supported.");
                exit();

            # SYMCHRONOUS GENERATORS
            # GENCLS
            if modelname == "GENCLS":
                if len(data) != GENCLS_DATA_SIZE:
                    psms_message(1, f"Model {modelname} requires {GENCLS_DATA_SIZE} parameters but {len(data)}"
                                 + " have been provided.");
                    exit();
            
                row_gencls = np.zeros((SG_DATA_SIZE));

                # Exclude model name
                data = data[:1] + data[2:]
                data = np.array([float(x) for x in data]);
                
                # Model type
                row_gencls[1] = 1;
                # Bus ID
                row_gencls[0] = data[0];
                # D
                row_gencls[2] = data[3];
                # M = 2 * H/ws
                row_gencls[3] = 2 * data[2];

                ppc["sg"] = np.vstack([ppc["sg"], row_gencls]);
            
            elif modelname == "GENTRA":
                if len(data) != GENTRA_DATA_SIZE:
                    psms_message(1, f"Model {modelname} requires {GENTRA_DATA_SIZE} parameters but {len(data)}"
                                 + " have been provided.");
                    exit();
                
                row_gentra = np.zeros((SG_DATA_SIZE));
                # Exclude model name
                data = data[:1] + data[2:]
                data = np.array([float(x) for x in data]);

                # Model type
                row_gentra[1] = 2;
                # Bus ID
                row_gentra[0] = data[0];
                # T1d0
                row_gentra[12] = data[2];
                # D
                row_gentra[2] = data[4];
                # M = 2 * H/ws
                row_gentra[3] = 2 * data[3];
                # xd
                row_gentra[6] = data[5];
                # xq
                row_gentra[7] = data[6];
                # xd'
                row_gentra[8] = data[7];

                ppc["sg"] = np.vstack([ppc["sg"], row_gentra]);
            elif modelname == "IEEET1":
                if len(data) != IEEET1_DATA_SIZE:
                    psms_message(1, f"Model {modelname} requires {IEEET1_DATA_SIZE} parameters but {len(data)}"
                                 + " have been provided.");
                    exit();

                row_ieeet1 = np.zeros((AVR_DATA_SIZE));

                # Exclude model name
                data = data[:1] + data[2:]
                data = np.array([float(x) for x in data]);

                # Model type
                row_ieeet1[1] = 1;
                # GEN ID
                row_ieeet1[0] = data[0];
                # vr_max
                row_ieeet1[2] = data[5];
                # vr_min
                row_ieeet1[3] = data[6];
                # Ka
                row_ieeet1[4] = data[3];
                # Ke
                row_ieeet1[5] = data[7];
                # Kf
                row_ieeet1[6] = data[9];
                # Ta
                row_ieeet1[7] = data[4];
                # Tf
                row_ieeet1[8] = data[10];
                # Te
                row_ieeet1[9] = data[8];
                # Tr
                row_ieeet1[10] = data[2];
                
                # Ae & Be
                [ row_ieeet1[11], row_ieeet1[12]] = satfun_coeff(data[12:])

                # Add to AVR data
                ppc["avr"] = np.vstack([ppc["avr"], row_ieeet1]);
            # Empty data variable
            data = ""


    # Number of SG devices
    ppc["nsg"] = ppc["sg"].shape[0];
    # Number of AVR devices
    ppc["navr"] = ppc["avr"].shape[0];
    # Number of TG devices
    ppc["ntg"] = ppc["tg"].shape[0];
    # Total number of dynamic devices
    ppc["ndyn"] = ppc["nsg"] + ppc["navr"] + ppc["ntg"]; 

    return ppc;







