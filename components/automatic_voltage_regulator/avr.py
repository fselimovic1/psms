# docstring

"""
"""


from components.automatic_voltage_regulator.ieeet1 import ieeet1

def avr(settings, ppc, dict4xml, comments):

    for i in range(ppc["navr"]):
        if ppc["sg"][i, 1] == 1:
            ieeet1(i, settings, ppc, dict4xml, comments);