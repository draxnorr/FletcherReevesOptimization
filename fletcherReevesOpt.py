import cexprtk
import constants_file as cnst
import numpy as np
import math

EPS = 10**(-8)
def calculate_custom_derivative(st, expr, symbol_dict, x0, d0, alfa):
    H = 10**-6
    for i, key in enumerate (symbol_dict.keys (), 0):
        st.variables[key] = x0[i]+d0[i]*(alfa+H)
    fval_1 = expr()
    for i, key in enumerate (symbol_dict.keys (), 0):
        st.variables[key] = x0[i]+d0[i]*(alfa-H)
    fval_2 = expr()
    derivative = (fval_1-fval_2)/(2*H)

    return derivative

def calculate_direction_byval(st, expr, symbol_dict, x0, d0, alfa):
    for i, key in enumerate (symbol_dict.keys (), 0):
        st.variables[key] = x0[i]+d0[i]*alfa
    fval = expr()

    return fval


def optimize_bicubic_interpolation(st, expr, symbol_dict, criteria_dict, alfa0, x0, d0, step):
    #d - kierunek, a,b -
    a = 0
    b = alfa0

    df_a = calculate_custom_derivative(st, expr, symbol_dict,x0,d0,a)
    if df_a>=0: # pozniej mozna usunac
        with open ("indirection.txt", 'a') as file:  # Use file to refer to the file object
            text = 'n = ' + str (step) + ", a = " + str (a) + ", b = " +\
                   str (b) + ", df_a = " + str (df_a) + ", df_a>=0"+", m = "+str(0.0)+"\n"
            file.write(text)
        print("df_a>=0; m=0.0")
        return 0.0

    while (b > 10**-6):
        df_b = calculate_custom_derivative(st, expr, symbol_dict,x0,d0,b)
        if df_b > 0 or math.isnan(df_b):
            break
        else:
            b = b/1.5
    if df_b<=0: # pozniej mozna usunac
        with open ("indirection.txt", 'a') as file:  # Use file to refer to the file object
            text = 'n = ' + str (step) + ", a = " + str (a) + ", b = " +\
                   str (b) + ", df_a = " + str (df_a) + ", df_b<=0"+", m = "+str(0.0)+"\n"
            file.write(text)
        print("df_b<=0; m=0.0")
        return 0.0

    try:
        fval_a = calculate_direction_byval(st, expr, symbol_dict,x0,d0,a)
        fval_b = calculate_direction_byval(st, expr, symbol_dict,x0,d0,b)
        e = b - a
        z = 3*(fval_a-fval_b)/e+df_a+df_b
        w = math.sqrt(z**2-df_a*df_b)
        d = e*(df_b+w-z)/(df_b-df_a+2*w)
        m = b-d
    except OverflowError:
        print('optimize_bicubic_interpolation:OverflowError')
        m = 0.0
    except ValueError:
        print('optimize_bicubic_interpolation:OverflowError')
        m = 0.0
    print ('dfa:', df_a)
    print ('dfb:', df_b)

    with open ("indirection.txt",'a') as file:  # Use file to refer to the file object
        text = 'n = '+ str(step) + ", a = "+str(a)+", b = "+str(b)+", df_a = "+str(df_a)+\
               ", df_b = "+str(df_b)+", m = "+str(m)+"\n"
        file.write(text)

    return m


def optimize_fletcher_reeves(text_expression, symbol_dict, criteria_dict, alfa0):
    EPS_DIVISION = 10**-6
    st = cexprtk.Symbol_Table(symbol_dict, cnst.m_constants, add_constants=True)
    expr = cexprtk.Expression(text_expression, st)
    n = len(symbol_dict)

    step = 0
    beta = 0.0
    x_predecessor = np.array(list(symbol_dict.values()),dtype=np.float64)
    x_current = np.array (list(symbol_dict.values ()), dtype=np.float64)
    fx_predecessor = expr()
    v_current = np.zeros((n,),dtype=np.float64)
    v_predecessor = np.zeros((n,),dtype=np.float64)
    grad_predecessor = np.zeros((n,),dtype=np.float64)

    while(True):
        grad_current = calculate_gradient(symbol_dict,st,expr)

        fx_current = expr()

        print('step: ', step)
        print ('x_current: ', x_current)
        print ('grad: ', grad_current)

        crit1 = grad_current.dot(grad_current)
        crit2 = np.linalg.norm(np.subtract(x_current,x_predecessor))
        crit3 = abs(fx_current-fx_predecessor)
        crit4 = step

        with open ("optimization.txt", 'a') as file:  # Use file to refer to the file object
            text = 'n = ' + str(step) + ", x_n = " + str (x_current) + ", f_n = " + str (fx_current) + \
                   ", grad_fx = " + str (grad_current) + ", beta = " + str (beta) + ", e1 = " + str(crit1) +\
                   ", e2 = " + str(crit2) + ", e3 = " + str(crit3) + ", e4 = " + str(crit4) +"\n"
            ''.join(text)
            file.write (text)

        if 'eps1' in criteria_dict:
            if crit1 <= criteria_dict['eps1']:
                print('crit1')
                break # przerwij algorytm
        if 'eps2' in criteria_dict:
            if crit2 <= criteria_dict['eps2']:
                if step >0:
                    print('crit2')
                    break # przerwij algorytm
        if 'eps3' in criteria_dict:
            if crit3 <= criteria_dict['eps3']:
                if step > 0:
                    print('crit3')
                    break # przerwij algorytm
        if 'eps4' in criteria_dict:
            if crit4 >= criteria_dict['eps4']:
                print('crit4')
                break # przerwij algorytm

        if np.prod(np.isnan(grad_current)):
            print ('error')
            arr = np.empty((n,))
            arr[:] = np.nan
            return (float('nan'),arr.tolist())

        if step % n == 0:
            ak = 0
        else:
            denominator = np.transpose(grad_predecessor)@grad_predecessor
            if abs(denominator) < EPS_DIVISION:
                if denominator >= 0:
                    denominator = EPS_DIVISION
                else:
                    denominator = -EPS_DIVISION
            print ('denominator: ', denominator)
            ak = (np.transpose(grad_current)@grad_current)/denominator
            print('ak:',ak)

        v_current = -grad_current+ak*v_predecessor
        beta = optimize_bicubic_interpolation(st, expr, symbol_dict, criteria_dict, alfa0, x_current, v_current,step)

        print('v_current:', v_current,'beta: ', beta)

        print ('----')


        x_predecessor = x_current
        fx_predecessor = fx_current
        grad_predecessor = grad_current
        v_predecessor = v_current
        step = step + 1
        x_current = x_current + beta*v_current
        for i, key in enumerate(symbol_dict.keys(),0):
            st.variables[key] = x_current[i]


    print('finished')
    return (fx_current, x_current.tolist(), (crit1, crit2, crit3, crit4))


def calculate_gradient(symbol_dict, st, expr):
    EPS_CALC = 10**(-6)
    grad = []
    for symbol in symbol_dict.keys():
        default_val = st.variables[symbol]

        if abs(default_val) < 0.001:
            st.variables[symbol] = default_val + EPS_CALC
            f_ph = expr()
            st.variables[symbol] = default_val - EPS_CALC
            f_mh = expr()
            grad.append((f_ph-f_mh)/(2*EPS_CALC))
        else:
            st.variables[symbol] = default_val*(1+math.sqrt(EPS_CALC))
            f_ph = expr()
            st.variables[symbol] = default_val*(1-math.sqrt(EPS_CALC))
            f_mh = expr()
            grad.append((f_ph - f_mh) / (2*default_val*math.sqrt(EPS_CALC)))
        st.variables[symbol] = default_val
    grad = np.array(grad,dtype=np.float64)
    return grad
