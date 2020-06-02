import cexprtk
import constants_file as cnst
import numpy as np
import math

EPS = 10**(-8)

def optimize_bicubic_interpolation():
    pass
#TODO


def optimize_fletcher_reeves(text_expression, symbol_dict, criteria_dict, alfa0):
    st = cexprtk.Symbol_Table (symbol_dict, cnst.m_constants, add_constants=True)
    expr = cexprtk.Expression (text_expression, st)
    n = len(symbol_dict)

    step = 1
    x_predecessor = np.array(list(symbol_dict.values()),dtype=float)
    fx_predecessor = expr()
    v_predecessor = np.zeros((n,),dtype=float)
    grad_predecessor = np.zeros((n,),dtype=float)
    x_current = np.array (list(symbol_dict.values ()), dtype=float)

    while(True):
        grad_current = calculate_gradient(symbol_dict,st,expr)
        fx_current = expr()

        crit1 = grad_current.dot(grad_current)
        crit2 = np.linalg.norm(np.subtract(x_current,x_predecessor))
        crit3 = abs(fx_current-fx_predecessor)
        crit4 = step

        if 'eps1' in criteria_dict:
            if crit1 > criteria_dict['eps1']:
                break # przerwij algorytm
        if 'eps2' in criteria_dict:
            if crit2 > criteria_dict['eps2']:
                break # przerwij algorytm
        if 'eps3' in criteria_dict:
            if crit3 > criteria_dict['eps3']:
                break # przerwij algorytm
        if 'eps4' in criteria_dict:
            if crit4 > criteria_dict['eps4']:
                break # przerwij algorytm

        if step % n == 0:
            ak = 0
        else:
            ak = (np.transpose(grad_current)@grad_current)/(np.transpose(grad_predecessor)@grad_predecessor)

        v_current = -grad_current+ak*v_predecessor
        beta = optimize_bicubic_interpolation(alfa0)

        x_predecessor = x_current
        fx_predecessor = fx_current
        grad_predecessor = grad_current
        v_predecessor = v_current

        x_current = x_current + beta*v_current
        for i, key in enumerate(symbol_dict.keys(),0):
            st.variables[key] = x_current[i]


    return grad_current


def calculate_gradient(symbol_dict, st, expr):
    grad = []
    for symbol in symbol_dict.keys():
        default_val = st.variables[symbol]

        if abs(default_val) < 0.001:
            st.variables[symbol] = default_val + EPS
            f_ph = expr()
            st.variables[symbol] = default_val - EPS
            f_mh = expr()
            grad.append((f_ph-f_mh)/(2*EPS))
        else:
            st.variables[symbol] = default_val*(1+math.sqrt(EPS))
            f_ph = expr()
            st.variables[symbol] = default_val*(1-math.sqrt(EPS))
            f_mh = expr()
            grad.append((f_ph - f_mh) / (2*default_val*math.sqrt(EPS)))
        st.variables[symbol] = default_val

    grad = np.array(grad,dtype=float)
    return grad


#test1
text_expression = "x1^2+5"
symbol_dict = {'x1':2.0}
criteria_dict={}
ans = optimize_fletcher_reeves(text_expression, symbol_dict, criteria_dict)
### 2*2.0 = 4.0

#test2
text_expression = "x1^2+x2^3+50*x1"
symbol_dict = {'x1':5.0,'x2':10.0}
criteria_dict={}
ans = optimize_fletcher_reeves(text_expression, symbol_dict, criteria_dict)
print(ans.shape)
ans = ans.dot(ans)
print(ans)
### 60.0 300.0          # 2*5.0+50 = 60.0, 3*10.0**2 = 300.0
#print(np.linalg.norm(ans))
