# docstring

"""
"""

import os

import numpy as np

from common.message import psms_message


BUS_DATA_SIZE = 13;
GEN_DATA_SIZE = 10;
BRANCH_DATA_SIZE = 13;

def readmfile(data):

    path = "data\\static\\";
    if data[-2:] == ".m":
        filename = path + data;
    else:
        filename = path + data + ".m"

    # check if file exist
    if not os.path.isfile(filename):
        psms_message(1, f"The file'{data}' do not exists or it is not in a folder '{path}'.");
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

        # basic data check
        if not ppc["bus"].shape[0]:
            psms_message(1, "Matrix mpc.bus is not entered or data format is incorrect. The M file must be written in accordance"
                          + " with the software manual.\n")
            exit()
        if not ppc["gen"].shape[0]:
            psms_message(1, "Matrix mpc.gen is not entered or data format is incorrect. The M file must be written in accordance"
                          + " with the software manual.\n")
            exit()
        if not ppc["branch"].shape[0]:
            psms_message(1, "Matrix mpc.branch is not entered or data format is incorrect. The M file must be written in accordance"
                          + " with the software manual.\n")
            exit()
        if not int(ppc["baseMVA"]):
            psms_message(1, "baseMVA not entered or equal to zero. The M file must be written in accordance"
                          + " with the software manual.\n")
            exit()

                    
    return ppc;



def readdyrfile(settings, ppc):
    pass
