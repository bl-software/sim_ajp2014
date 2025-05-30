# 𝜆 λ
# 00000000: f09d 9c86 20ce bb0a 0a23 2054 6869 7320  .... ....# This
# https://www.compart.com/en/unicode/U+1D740
# https://www.compart.com/en/unicode/search?q=lamda#characters
# U03bb  λ 0xCE 0xBB           Greek Small Letter Lamda
# U1d706 𝜆 0xF0 0x9D 0x9C 0x86 Mathematical               Italic Small Lambda    <<<
# U1d740 𝝀 0xF0 0x9D 0x9D 0x80 Mathematical          Bold/Italic Small Lambda
# U1d6cc 𝛌 0xF0 0x9D 0x9B 0x8C Mathematical          Bold        Small Lambda
# U1d77a 𝝺 0xF0 0x9D 0x9D 0xBA Mathematical SanSerif Bold        Small Lambda
# U1d7b4 𝞴 0xF0 0x9D 0x9E 0xB4 Mathematical SanSerif Bold/Italic Small Lambda

# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_2__AJP.Param_Defaults_AJP2014 import *
from Params.Params import *
import numpy as np

Ai_list= [ 5.0, 20.0, 40.0, 100.0, 1000.0, 10000.0 ]
As_list= [ 150.0, 10000.0 ]
las=len(As_list)
lai=len(Ai_list)

#Ai=[     5.0 ]
#Ai=[    20.0 ]
Ai=[    40.0 ]
#Ai=[   100.0 ]
#Ai=[  1000.0 ]
#Ai=[ 10000.0 ]
#As=[   150.0 ]
As=[ 10000.0 ]

#sweepvar=["tort_gamma"]
sweepvar=["oos_tort_lambda"]
#sweepvar=["Pm_CO2_input"]

#          0      1      2      3      4      5      6      7      8      9     10     11     12     13     14     15     16     17     18     19     20    21     22     23    24      25       26   
#lams= [0.001, 0.005, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.026, 0.030, 0.040, 0.060, 0.080, 0.100, 0.130, 0.160]
#lams= [0.001, 0.005, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.026, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090, 0.100, 0.130, 0.160, 0.200, 0.250, 0.400, 0.500, 0.600, 0.800, 1.000]
#lams= [0.010, 0.015, 0.020, 0.025, 0.030, 0.040, 0.050, 0.060, 0.070, 0.080, 0.090, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0 ]
['0.01', '0.0127', '0.0162', '0.0207', '0.0264', '0.0336', '0.0428', '0.0546', '0.0695', '0.0886', '0.113', '0.144', '0.183', '0.234', '0.298', '0.379', '0.483', '0.616', '0.785', '1.0']
lams= list(np.logspace( -2, 0, 21))
lamsel=20
#          0      1      2      3      4      5     6

#gams= [0.030, 0.075, 0.120, 0.165, 0.210, 0.255, 0.300]
#gams= [0.010, 0.015, 0.020, 0.025, 0.030, 0.075, 0.120, 0.165, 0.210, 0.255, 0.300]
gams= list(np.logspace( -2, 0, 21))
gamsel=20

#            0       1       2       3        4
pmco2s=[0.0009, 0.0017, 0.0034, 0.0068,0.0340, 0.03078]
pmcsel=3

if sweepvar[0] == 'tort_gamma':
    gams  = gams # list(np.linspace( 0.03, 0.3, 7))
    lams  = [lams[lamsel]]
    pmco2s= [pmco2s[pmcsel]]
    plottitle=f'Ai={Ai} As={As} λ{lams}(ves) γs(vitmem)'
    outfile  =f'Ai_{Ai[0]}_As_{As[0]}_λ{lams[0]:0.3f}_γs'.replace('.','_')
    outcol=f'gamma_at_lam={lams[0]}'
if sweepvar[0] == 'oos_tort_lambda':
    lams= lams #list(np.linspace( 0.01, 0.15, 9))
    gams= [gams[gamsel]]
    pmco2s= [pmco2s[pmcsel]]
    plottitle=f'Ai={Ai} As={As} λs(ves) γ{gams}(vitmem)'
    outfile  =f'Ai_{Ai[0]}_As_{As[0]}_λs_γ{gams[0]:0.3f}'.replace('.','_')
    outcol=f'lambda_at_gam={gams[0]}'
if sweepvar[0] == 'Pm_CO2_input':
    lams= [lams[lamsel]]
    gams= [gams[gamsel]]
    pmco2s= pmco2s
    #pmco2s= list(np.logspace( -5, -2, 9)*34.2)
    plottitle=f'Ai={Ai} As={As} λ{lams}(ves) γ{gams}(vitmem) pmco2s'
    outfile  =f'Ai_{Ai[0]}_As_{As[0]}_λ{lams[0]:0.3f}_γ{gams[0]:0.3f}_pmco2s'.replace('.','_')
    outcol=f'PmCO2_lam{lams[0]}_gam{gams[0]}'
batchp_list= ['']#'Pm_CO2_input']

#prettylist= [ float(f'{v:0.4f}') for v in gams ]
#print(prettylist)
#lamda=1d706 - math italic
#gamma=1D6C4 - math italic
#See NOTES_DK_Meeting.txt
fig_params= {\
    'tf_CO2on': (('Time I -> E (s)', 'tf_CO2on'      , pos_float, '{}', 1, 'Experiment'                           ,  'tb', [600.0   ], None, (                   )), {} ), 
    'CAII_out': (('CAII Out'      , 'CAII_out'       , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [0.0     ], None, (                   )), {}                                         ),
 'oocyte_type': (('Oocyte Type'    , 'oocyte_type'   ,  a_string, '{}', 1, 'Experimental Conditions'              ,  'ch', ['CAIV'  ], None, ('pH_in_init', 'pH_in_acid')), {'choices':['Tris','H2O','CAII','CAIV']} ),
     'CAII_in': (('CAII In'        , 'CAII_in'       , pos_float, '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', Ai        , None, (                   )), {} ),
    'CAIV_out': (('CAIV Out'       , 'CAIV_out'      , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', As        , None, (                   )), {} ),
    'pKHA1_in': (('pK<sub>3</sub>_ICF','pKHA1_in'    , reg_float, '{}', 3, 'Reaction Rates'                       ,  'tb', [7.23    ], None, ('kb_HA1_in_minus', )), {} ),
    #'Pm_CO2_input': (('CO<sub>2</sub>','Pm_CO2_input'    , pos_float, '{}', 1, 'Permeability Across PM'               , 'dtb', [0.03078 ], None, (                   )), {} ),

      'PlotTitle': (('PlotTitle'                 , 'PlotTitle'      ,  a_string, '{}', 2, 'Extra'                    , 'tb', [plottitle ], None, ()), {}),
        'OutFile': (('OutFile'                   , 'OutFile'        ,  a_string, '{}', 2, 'Extra'                    , 'tb', [outfile   ], None, ()), {}),
         'OutCol': (('OutCol'                    , 'OutCol'         ,  a_string, '{}', 2, 'Extra'                    , 'tb', [outcol    ], None, ()), {}),
    'BatchParams': (('BatchParams'               , 'BatchParams'    ,  a_string, '{}', 2, 'Extra'                    , 'tb', batchp_list , None, ()), {}),
       'SweepVar': (('SweepVar'                  , 'SweepVar'       ,  a_string, '{}', 2, 'Extra'                    , 'tb', sweepvar    , None, ()), {}),

   'Pm_CO2_input': (('CO<sub>2</sub>'            , 'Pm_CO2_input'   , pos_float, '{}', 1, 'Permeability Across PM'   ,'dtb', pmco2s      , None, ()), {}),
'oos_tort_lambda': (('Tort Lambda Vesicles (1/λ)', 'oos_tort_lambda', pos_float, '{}', 2, 'Intracellular Fluid (ICF)', 'tb', lams         , None, ()), {}),
     'tort_gamma': (('Tort Gamma VitMem (1/γ)'   , 'tort_gamma'     , pos_float, '{}', 2, 'Intracellular Fluid (ICF)', 'tb', gams         , None, ()), {}),
}
fig_param_list= build_param_list(param_list_AJP2014,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig LamGamSweeps','Fig GenSweeps', ],
    'fname':__file__,
}
