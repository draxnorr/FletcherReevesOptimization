import cexprtk
import constants_file as cnst
import numpy as np
import math
import numdifftools as nd

EPS = 10**(-8)
def calculate_derivative_in_direction(st, expr, symbol_dict, x0, d0, alfa): #sprawdzone
    H = 10**-6
    for i, key in enumerate (symbol_dict.keys (), 0):
        st.variables[key] = x0[i]+d0[i]*(alfa+H)

    fval_1 = expr()
    for i, key in enumerate (symbol_dict.keys (), 0):
        st.variables[key] = x0[i]+d0[i]*(alfa-H)
    fval_2 = expr()
    derivative = (fval_1-fval_2)/(2*H)
    return derivative

def calculate_fval_in_direction(st, expr, symbol_dict, x0, d0, alfa): #sprawdzone
    for i, key in enumerate (symbol_dict.keys (), 0):
        st.variables[key] = x0[i]+d0[i]*alfa
    fval = expr()

    return fval

#na podstawie:
#Practical Optimization: Algorithms and Engineering Applications
#cubic interpolation str.99
#zmienną 'x' jest 'alfa'
#^^ nie zadziałało
# Engineering Optimization: Theory and Practice, Fourth Edition
def optimize_cubic_interpolation(st, expr, symbol_dict, criteria_dict, t0, x0,fx0,grad_curr, d0, step):
    ## STEP1
    if "epsk1" in criteria_dict:
        eps_k1 = criteria_dict["epsk1"]
    elif "eps2" in criteria_dict:
        eps_k1 = criteria_dict["eps2"]
    else:
        eps_k1 = 0.001

    # STEP1 normalizacja kierunku
    scale = max(np.absolute(d0))
    scale = max(scale, 10**(-4))
    S = d0/scale

    dfA = grad_curr@d0 # pochodna kierunkowa

    # STEP2 sprawdzenie, czy kierunek poprawy jest poprawny oraz znalezienie punktu B, gdzie poch. kierunkowa >0
    if dfA >= 0:
        print("Wyznaczony kierunek nie jest kierunkiem poprawy. Pochodna kierunkowa dodatnia (grad f * S >=0). Zwracam alfa=0.0")
        return 0.0

    A_point = 0.0

    B_point = t0 # krok początkowy
    # znajdz taki krok, w którym pochodna kierunkowa jest dodatnia
    while (calculate_derivative_in_direction(st,expr,symbol_dict, x0, S, B_point) <=0):
        B_point = 2*B_point
        if  B_point > 10**99:
            print("Nie znaleziono punktu B, w którym pochodna kierunkowa jest dodatnia. Zwracam alfa=alfa0=",t0)
            return t0/scale
    dfB = calculate_derivative_in_direction(st,expr,symbol_dict, x0, S, B_point)

    # STEP 3 parametry wielomianu 3 stopnia
    fA = fx0
    fB = calculate_fval_in_direction(st, expr, symbol_dict, x0, S, B_point)

    lambda_opt = 10**99
    i=0
    while(True):
        i=i+1
        print(i)
        Z = 3*(fA-fB)/(B_point-A_point)+dfA+dfB
        d = (2*Z+dfA+dfB)/(3*(A_point-B_point)**2)
        c = -((A_point+B_point)*Z+B_point*dfA+A_point*dfB)/((A_point-B_point)**2)
        b = (B_point**2*dfA+A_point**2*dfB+2*A_point*B_point*Z)/((A_point-B_point)**2)
        a = fA-b*A_point-c*A_point**2-d*A_point**3

        lambda_predecessor = lambda_opt

        if abs(d) < EPS: # funkcja kwadratowa
            if c>0:
                lambda_opt = -b/(2*c)
            else:
                print("W kierunku: d=0, c<=0. Niespełniony warunek wystarczający minimum")
                return 0.0
            if A_point > lambda_opt or lambda_opt > B_point:
                print("WTF1:", A_point,lambda_opt,B_point)
                print ("WTF1: dfA,dfB:", dfA, dfB)
                print ("WTF1: lambda_opt:", lambda_opt)
                return 0.0
        else:
            lambda1 = (-c + math.sqrt(c**2-3*b*d) )/(3*d)
            lambda2 = (-c - math.sqrt(c**2-3*b*d) )/(3*d)
            if 2*c+6*d*lambda1 > 0:
                lambda_opt = lambda1
            elif 2*c+6*d*lambda2 > 0:
                lambda_opt = lambda2
            else:
                print ("W kierunku: d=0, c<=0. Niespełniony warunek wystarczający minimum")
                return 0.0
            if A_point > lambda_opt or lambda_opt > B_point:
                print("WTF2:", A_point,lambda_opt,B_point)
                print ("WTF2: dfA,dfB:", dfA, dfB)
                print ("WTF2: lambda1, lambda2:", lambda1,lambda2)
                print ("WTF2: lambda_opt:", lambda_opt)
                return 0.0

        # STEP4 Kryterium stopu
        h_lamda_opt = a+b*lambda_opt+c*lambda_opt**2+d*lambda_opt**3
        f_lamda_opt = calculate_fval_in_direction(st, expr, symbol_dict, x0, S, lambda_opt)

        if abs(lambda_predecessor-lambda_opt) <= eps_k1 or abs((h_lamda_opt-f_lamda_opt)/f_lamda_opt)<= eps_k1:
            print("Koniec. Poprawna min. w kierunku. alfa=",lambda_opt)
            return lambda_opt/scale

        df_lambda_opt = calculate_derivative_in_direction(st,expr,symbol_dict, x0, S, lambda_opt)
        # print ("poch:", df_lambda_opt)
        # print ("lambdaopt:",lambda_opt)
        if df_lambda_opt < 0:
            A_point = lambda_opt
            fA = f_lamda_opt
            dfA = calculate_derivative_in_direction(st,expr,symbol_dict, x0, S, A_point)
        elif df_lambda_opt > 0:

            B_point = lambda_opt
            fB = f_lamda_opt
            dfB = calculate_derivative_in_direction(st,expr,symbol_dict, x0, S, B_point)
        else:
            print("Koniec. Niespelnione kryterium stopu m. w kierunku, ale zerowa pochodna w punkcie lambda_opt.")
            return lambda_opt/scale

            # with open ("indirection.txt", 'a') as file:  # Use file to refer to the file object
            #         text = 'krok = ' + str (step)
            #         file.write(text)



class HessianCalc:
    def __init__(self,expr,st,symbol_dir):
        self.expr = expr
        self.st = st
        self.symbol_dir = symbol_dir
    def calc_fun(self,x):
        for i, key in enumerate (self.symbol_dir.keys(), 0):
            self.st.variables[key] = x[i]
        return self.expr()
    def calc_hessian(self,x):
        return nd.Hessian(self.calc_fun)(x)
    def decision(self,x):
        H = self.calc_hessian(x)
        li, U = np.linalg.eig(H)
        if np.all(li>0):
            return "Punkt stacjonarny jest minimum. Macierz Hessego dodatnio określona"
        elif np.all(li>=0):
            return "Potrzeba więcej informacji. Macierz Hessego nieujemnie określona"
        elif np.all(li<0):
            return "Coś poszło nie tak. Punkt stacjonarny jest maksimum. Macierz Hessego ujemnie określona."
        else:
            return "Punkt stacjonarny jest punktem siodłowym. Macierz Hessego nieokreślona (ujemne i dodatnie wart. własne)"


def optimize_fletcher_reeves(text_expression, symbol_dict, criteria_dict, alfa0):
    EPS_DIVISION = 10**-6
    st = cexprtk.Symbol_Table(symbol_dict, cnst.m_constants, add_constants=True)
    expr = cexprtk.Expression(text_expression, st)
    n = len(symbol_dict)

    step = 0
    alfa = 0.0
    x_predecessor = np.array(list(symbol_dict.values()),dtype=np.float64)
    x_current = np.array (list(symbol_dict.values ()), dtype=np.float64)
    fx_predecessor = expr()
    v_current = np.zeros((n,),dtype=np.float64)
    v_predecessor = np.zeros((n,),dtype=np.float64)
    grad_predecessor = np.zeros((n,),dtype=np.float64)

    while(True):
        grad_current = calculate_gradient(symbol_dict,st,expr,x_current)

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
                   ", grad_fx = " + str (grad_current) + ", v_curr = " + str (v_current) + ", alfa = " + str (alfa) + ", e1 = " + str(crit1) +\
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
            with open ("optimization.txt", 'a') as file:
                file.write ("Zakończono niepowodzeniem. Pojawienie się wartości NaN")
            return (float('nan'),arr.tolist(),(crit1, crit2, crit3, crit4))

        if step % n == 0:
            ak = 0
        else:
            denominator = np.transpose(grad_predecessor)@grad_predecessor
            if abs(denominator) < EPS_DIVISION:
                if denominator >= 0:
                    denominator = EPS_DIVISION
                else:
                    denominator = -EPS_DIVISION
            ak = (np.transpose(grad_current)@grad_current)/denominator
            print('ak:',ak)

        v_current = -grad_current+ak*v_predecessor
        alfa = optimize_cubic_interpolation(st, expr, symbol_dict, criteria_dict, alfa0, x_current,fx_current,grad_current, v_current,step)
        print ("v_current = ", v_current)

        x_predecessor = x_current
        fx_predecessor = fx_current
        grad_predecessor = grad_current
        v_predecessor = v_current
        step = step + 1
        x_current = x_current + alfa*v_current
        for i, key in enumerate(symbol_dict.keys(),0):
            st.variables[key] = x_current[i]

    hessian_calc_obj = HessianCalc(expr,st,symbol_dict)
    decision = hessian_calc_obj.decision(x_current)
    with open ("optimization.txt", 'a') as file:
        file.write ("Zakończono." + decision)

    return (fx_current, x_current, (crit1, crit2, crit3, crit4))


def calculate_gradient(symbol_dict, st, expr, x_current):
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
