# docstring

"""
"""

import numpy as np

from common.message import psms_message

def readout(outfile):

    solution_data_found = False;
    count = 0;
    first_row = True;
    is_data_line = False;

    # Read file
    with open(outfile, 'r') as file:
        islast = False;
        for line in file:
            if islast and line.strip() != "All OK!":
                psms_message(1, "Model solver: " + line.strip());
                exit()
            if solution_data_found and count  == 1 and line.strip() != "---------------------------":
                vars = line.split()
            if solution_data_found and count == 2:
                is_data_line = True
            else:
                is_data_line = False
            if is_data_line and line.strip() != "------------------------":
                if first_row:
                    data = np.array(line.split(), dtype=float);
                    first_row = False;
                else:
                    data = np.vstack((data, np.array(line.split(), dtype=float)));
            if line.strip() == 'SOLUTION DATA':
                solution_data_found = True;
            if solution_data_found and (line.strip() == "---------------------------" or line.strip() == "------------------------"):
                count += 1;
            if is_data_line and (line.strip() == "---------------------------" or line.strip() == "------------------------"):
                islast = True; 

    results = dict();
    for i in range(0,len(vars)):
        results[vars[i]] = (data[:, i]).tolist()
    return results