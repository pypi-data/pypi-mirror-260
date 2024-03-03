from .data_function import *
from .optimize import *
from .indicator import *
##########

class back_test:

    @classmethod
    def buy_conditions(cls, conds = None) -> pd.DataFrame:
        conds = conds.replace('and', '*')
        conds = conds.replace('or', '+')
        df_raw = eval(conds).astype(int)
        cls.buy_matrix = df_raw

    @classmethod
    def sell_conditions(cls, conds = None) -> pd.DataFrame:
        conds = conds.replace('and', '*')
        conds = conds.replace('or', '+')
        df_raw = eval(conds).astype(int)
        cls.sell_matrix = df_raw
        cls.order_matrix = cls.buy_matrix.mask(cls.sell_matrix == 1, -1).apply(order_matrix_optimize, axis=0,result_type='expand')

        
    sub_matrix = 1
    @classmethod
    def sub_conditions(cls,els = [['totalVolume',False,5]]) -> pd.DataFrame:
        result = 1
        for el in els:
            df = element(el[0])
            result *= df.apply(sub_conditions_optimize,axis = 1,result_type='expand')
            cls.sub_matrix = result





    