import wx
import math
from functools import wraps

##################
### Validators ###
##################
def listvalidator(vfunc):
    @wraps(vfunc)
    def list_wrapper(alist):
        return [ vfunc(li) for li in alist ]
    return list_wrapper

@listvalidator
def no_test(v):
    return v

@listvalidator
def a_string(str_val):
    return str(str_val)

@listvalidator
def sci_float(str_val):
    '''pseudo type for float parameters in sci notation'''
    return float(str_val)

@listvalidator
def mlfloat(str_val): # MATLAB float uses 5*10^-7 instead of pythons 5e-07
    '''pseudo type for matlab defined float parameters'''
    return float(str_val.replace('*10^', 'e'))

@listvalidator
def mlarrayf(str_val): # MATLAB float uses 5*10^-7 instead of pythons 5e-07
    '''pseudo type for matlab defined array of floats parameters'''
    mat_a = str_val.strip('[]').split(';')
    for i in mat_a:
        float(i.replace('*10^', 'e'))
    return mat_a

@listvalidator
def mlbool(str_val):
    '''pseudo type for matlab boolean parameters'''
    return str_val in [ 'True', 'true', 'TRUE', '1', 'yes', 'on', True ]

@listvalidator
def pos_float(v):
    pf = float(v)
    if pf >= 0:
        return pf
    raise ValueError('Positive Float Value required!')

@listvalidator
def reg_float(v):
    return float(v)

@listvalidator
def pos_int(v):
    pi = int(v)
    if pi >= 0:
        return pi
    raise ValueError('Positive Integer Value Required!')

@listvalidator
def choice(v):
    return v

@listvalidator
def reg_int(v):
    return int(v)

@listvalidator
def percent(v):
    fv= float(v)
    if 0 <= fv <= 100:
        return float(v)
    raise ValueError( 'Float Range of [0, 100] Required!')

@listvalidator
def pH(v):
    ph = float(v)
    if 0 <= ph <= 14:
        return ph
    raise ValueError( 'Float Range of [0, 14] Required!')

