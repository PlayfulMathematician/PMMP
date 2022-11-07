__version__ = "0.1.1"
__name__ = "PMMP"

try:
    from PMMP.functions import *
    from PMMP.probability import *
    from PMMP.numbers import *


except ModuleNotFoundError:
    pass