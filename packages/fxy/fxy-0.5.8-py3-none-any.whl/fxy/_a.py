# Actuarial

try:
    import numpy
    import numpy as np
    if True:
        print('import numpy; as np')
except:
    pass

try:
    import pandas
    import pandas as pd
    if True:
        print('import pandas; as pd')
except:
    pass

try:
    import xarray
    import xarray as xr
    if True:
        print('import xarray; as xr')
except:
    pass

try:
    from . import _scipy as sci
    import scipy.stats as st
    if True:
        print('import scipy; as sci')
        print('import scipy.stats as st')
except:
    pass

try:
    import statsmodels
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    if True:
        print('import statsmodels')
        print('import statsmodels.api as sm')
        print('import statsmodels.formula.api as smf')
except:
    pass

# And plotting
# from fxy.p import *
