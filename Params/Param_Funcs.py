###################################################
### Fuctions that return a Params calculated value
###################################################
import math

################
### Helper Funcs
def req_setup( req_params ):
    ''' req_params - list of params
        returns max len and list of var lists
        Ex. ml=3  rpvals=[ [1.2,1.4,1.6], [400] ]
    '''
    rpvals = [ p() for p in req_params ]
    lens = set([1])
    [lens.add(len(vl)) for vl in rpvals]

    ml = max(lens) 
    for i,pvals in enumerate(rpvals):
        if len(pvals) < ml:
            rpvals[i] = pvals*ml
    return ml,rpvals

#############################
### Formula Val Functions ###
#############################
def f__d_inf(params):
    ''' f__d_inf is 2 * thickness + D '''
    ml,(thickness,D)= req_setup([ params['thickness'], params['D'] ])
    r= [ ( 2 * thickness[i] ) + D[i] for i in range(ml) ]
    return  r

def f__pK1(params):
    '''- log10 ( kb_1 / kb_2 )'''
    ml,(kb_1,kb_2)= req_setup([ params['kb_1'], params['kb_2'] ])
    return [- math.log10( kb_1[i] / kb_2[i] ) for i in range(ml) ]

def f__kb_X(params,kbn,pKstr):
    '''kb_3 / ( 10 ** ( - pK2 + 3 ) )'''
    kb_X = 'kb_%d'%kbn   # Ex. kb_3 kb_5 kb_7
    pKX  = 'pK%s'%pKstr  # Ex. pk2  pkHA2_out
    ml,(kb,pK)= req_setup([ params[kb_X], params[pKX] ])
    return [ kb[i] / ( 10 ** ( - pK[i] + 3 ) ) for i in range(ml) ]

def f__kb_HAX_in_minus(params,bufnum):
    '''kb_HAX_in_plus / ( 10 ** ( - pKHAX_in + 3 ) )
       bufnum: number like 1 ni HA1 '''
    ml,(kb_HAX_in_plus,pKHAX_in)= req_setup([ params['kb_HA%d_in_plus'%bufnum],params['pKHA%d_in'%bufnum] ])
    return [ kb_HAX_in_plus[i] / ( 10 ** ( - pKHAX_in[i] + 3 ) ) for i in range(ml) ]

def f__AXtot_in(params,bufn):
    ''' Calculate total concentration inside oocyte at initial'''
    ml,(pH_in_init, pH_in_final, CO2_in, CO2_pc, PB, PH2O, sCO2, pK1, pK2, Buff_pc)= \
        req_setup([ params['pH_in_init'],
                params['pH_in_final'],
                params['CO2_in'],
                params['CO2_pc'],
                params['PB'],
                params['PH2O'],
                params['sCO2'],
                params['pK1'],
                params['pK2'],
                params['Buff_pc'],
              ])

    # partial CO2 pressure in EUF
    PCO2 = [ CO2_pc[i]*(PB[i]-PH2O[i])/100 for i in range(ml) ]
    # concentration CO2 in EUF - Henry's Law
    CO2_out = [ sCO2[i]*PCO2[i] for i in range(ml) ]
    pK_CO2 = [ pK1[i] + pK2[i] for i in range(ml) ]

    Hplus_in = [ 10**(-pH_in_init[i]+3) for i in range(ml) ]
    H2CO3_in = [ 10**(-pK1[i])*CO2_in[i] for i in range(ml) ]
    HCO3m_in = [ 10**(-pK2[i])*H2CO3_in[i]/Hplus_in[i] for i in range(ml) ]

    HCO3m_fin = [ CO2_out[i]* 10**(pH_in_final[i] - pK_CO2[i]) for i in range(ml) ]
    slope = [ (HCO3m_fin[i]-HCO3m_in[i])/(pH_in_final[i]-pH_in_init[i]) for i in range(ml) ]

    # mean intrinsic buffer (HA/Am) power
    beta_HA  = [-slope[i] for i in range(ml) ]

    pK = [(pH_in_init[i]+pH_in_final[i])/2 for i in range(ml) ]
    # as mean between initial and final (acidic) pHi

    K = [10**(-pK[i]) for i in range(ml) ]
    Q = [(1/(1+K[i]*10**pH_in_init[i]))-(1/(1+K[i]*10**pH_in_final[i])) for i in range(ml) ]
    AXtot_in = [((pH_in_final[i]-pH_in_init[i])*beta_HA[i])/Q[i] for i in range(ml) ]
#    breakpoint()

    if bufn == 1:
        AXtot_in = [(1 - Buff_pc[i]/100) *AXtot_in[i] for i in range(ml) ]
    elif bufn == 2:
        AXtot_in = [(    Buff_pc[i]/100) *AXtot_in[i] for i in range(ml) ]
    
    return AXtot_in

def f__pH_in_init(params):
    ml,(oocyte_type,CO2_pc)= req_setup([ params['oocyte_type'], params['CO2_pc'] ])
    pii = {\
         1.5 : { 'Tris' : 7.22,
                 'H2O'  : 7.28,
                 'CAII' : 7.21,
                 'CAIV' : 7.40, },
         5.0 : { 'Tris' : 7.24,
                 'H2O'  : 7.23,
                 'CAII' : 7.21,
                 'CAIV' : 7.37, },
        10.0 : { 'Tris' : 7.18,
                 'H2O'  : 7.16,
                 'CAII' : 7.21,
                 'CAIV' : 7.40, }, }
    return [ pii[CO2_pc[i]][oocyte_type[i]] for i in range(ml) ]
                
def f__pH_in_acid(params):
    ml,(oocyte_type,CO2_pc)= req_setup([ params['oocyte_type'], params['CO2_pc'] ])
    pia = {\
         1.5 : { 'Tris' : 6.99,
                 'H2O'  : 7.01,
                 'CAII' : 6.98,
                 'CAIV' : 7.06, },
         5.0 : { 'Tris' : 6.79,
                 'H2O'  : 6.84,
                 'CAII' : 6.77,
                 'CAIV' : 6.79, },
        10.0 : { 'Tris' : 6.67,
                 'H2O'  : 6.69,
                 'CAII' : 6.66,
                 'CAIV' : 6.61, }, }
    return [ pia[CO2_pc[i]][oocyte_type[i]] for i in range(ml) ]
 

p_funcs={
    'f__d_inf': f__d_inf,
    'f__pK1': f__pK1,
    'f__kb_X': f__kb_X,
    'f__kb_HAX_in_minus': f__kb_HAX_in_minus,
    'f__AXtot_in': f__AXtot_in,
    'f__pH_in_init': f__pH_in_init,
    'f__pH_in_acid': f__pH_in_acid,
}
