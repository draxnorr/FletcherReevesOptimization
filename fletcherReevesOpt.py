import cexprtk
import constants_file as cnst

def optimize_fletcher_reeves(text_expression, symbol_dict, criteria_dict):
    st = cexprtk.Symbol_Table (symbol_dict, cnst.m_constants, add_constants=True)
    expr = cexprtk.Expression (text_expression, st)

    k = 1
    v_m1 =