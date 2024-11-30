# docstring

"""
"""

import numpy as np

from components.synchronous_generator.gencls import gencls
from components.synchronous_generator.gentra import gentra

def sg(settings, ppc, dict4xml, comments):
    
    sgbus = np.unique(ppc["sg"][:, 0]);
    nsg_bus = len(sgbus);
    ngeqs = { "pgEqs": [""] * nsg_bus,  "qgEqs" : [""] * nsg_bus, "sgbus": sgbus};

    for i in range(ppc["nsg"]):
        if ppc["sg"][i, 1] == 1:
            gencls(i, settings, ppc, dict4xml, comments, ngeqs);
        elif ppc["sg"][i, 1] == 2:
            gentra(i, settings, ppc, dict4xml, comments, ngeqs);

    # Network NLEqs: generator part
    for i in range(len(dict4xml["nleqs"])):

        eq = dict4xml["nleqs"][i]["fx"];

        if "busPgenEq" in eq:
            idx = eq.find("busPgenEq");
            nidx = idx + len("busPgenEq");
            bus = 0;
            mult = 1;
            while eq[nidx] != ")":
                bus = bus * mult + int(eq[nidx]);
                mult *= 10;
                nidx += 1;
            dict4xml["nleqs"][i]["fx"] = dict4xml["nleqs"][i]["fx"].replace("busPgenEq" + str(bus), ngeqs["pgEqs"][np.where(sgbus == bus)[0][0]]);

        elif "busQgenEq" in eq:
            idx = eq.find("busQgenEq");
            nidx = idx + len("busQgenEq");
            bus = 0;
            mult = 1;
            while eq[nidx] != ")":
                bus = bus * mult + int(eq[nidx]);
                mult *= 10;
                nidx += 1;
            dict4xml["nleqs"][i]["fx"] = dict4xml["nleqs"][i]["fx"].replace("busQgenEq" + str(bus), ngeqs["qgEqs"][np.where(sgbus == bus)[0][0]]);






