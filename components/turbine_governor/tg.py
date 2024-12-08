# docstring

"""
"""


from components.turbine_governor.tgov1 import tgov1

def tg(settings, ppc, dict4xml, comments):

    for i in range(ppc["ntg"]):
        if ppc["tg"][i, 1] == 1:
            tgov1(i, settings, ppc, dict4xml, comments);