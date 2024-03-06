# Machine Learning

try:
    from . import __sklearn__ as sklearn
    print('import sklearn')
except:
    pass

try:
    import xgboost as xgb; import xgboost
    print('import xgboost; as xgb')
except:
    pass

# And plotting
# from fxy.p import *
