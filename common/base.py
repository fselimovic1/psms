# docstring

"""
"""

import math


def base(ppc):
    
    # Convert bus data to base values
    ppc["bus"][:, 2:6] = ppc["bus"][:, 2:6]/ppc["baseMVA"];  # Powers
    ppc["bus"][:, 8] = ppc["bus"][:, 8] * 2 * math.pi/360;   # Angle

    # Convert generator data to base values
    ppc["gen"][:, [1, 2, 3, 4, 8, 9]] = ppc["gen"][:, [1, 2, 3, 4, 8, 9]]/ppc["baseMVA"];  # Powers


    # Convert branch data to base values
    ppc["branch"][:, 9] = ppc["branch"][:, 9] * 2 * math.pi/360;  # Angle

    return ppc;