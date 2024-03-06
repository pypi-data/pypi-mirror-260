# Machine Learning

try:
    from . import _sklearn as sklearn
    print('import sklearn')
except:
    pass

try:
    import xgboost as xgb; import xgboost
    print('import xgboost; as xgb')
except:
    pass

# And plotting
# from fxy._p import *
