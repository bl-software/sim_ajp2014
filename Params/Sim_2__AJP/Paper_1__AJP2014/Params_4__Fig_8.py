# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_2__AJP.Param_Defaults_AJP2014 import *
from Params.Params import *

panel=('AB','CD')[1]
Ai_list= [ 5.0, 20.0, 40.0, 100.0, 1000.0, 10000.0 ]
As_list= [ 150.0, 1000.0, 5000.0, 10000.0, 25000.0, 50000.0 ]

las=len(As_list)
lai=len(Ai_list)

if panel == 'AB':
    #Ai=Ai_list
    #As=[As_list[0],]
    As= []
    [As.extend([v]*lai) for v in As_list]
    Ai= Ai_list * las
elif panel =='CD':
    #Ai=[Ai_list[0],]
    #As=As_list
    #Ai [   5    5    5     5     5     5   20   20   20    20    20    20 ...
    #As [ 150 1000 5000 10000 25000 50000  150 1000 5000 10000 25000 50000
    Ai= []
    [Ai.extend([v]*las) for v in Ai_list]
    As= As_list * lai
#print('Ai=',Ai)
#print('As=',As)
#import sys
#sys.exit()


#                Human Readable     Matlab      Valid      Format Col  Group                                   Type    Value                  OVCCallback   Dependents           Dropdown Choices
fig_params= {\
    'tf_CO2on': (('Time I -> E (s)', 'tf_CO2on' , pos_float, '{}', 1, 'Experiment'                           ,  'tb', [600.0         ], None, (), ),{}),
 'oocyte_type': (('Oocyte Type'    , 'oocyte_type',a_string, '{}', 1, 'Experimental Conditions'              ,  'ch', ['CAIV'        ], None, ('pH_in_init', 'pH_in_acid')), {'choices':['Tris','H2O','CAII','CAIV']} ),
    'CAII_out': (('CAII Out'       , 'CAII_out' , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [0.0           ], None, (), ),{}),
    #     'CAII_in': (('A-factor CAII'  , 'CAII_in'  , pos_float, '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', Ai              , None, (), ),{}),
    #'CAIV_out': (('A-factor CAIV'  , 'CAIV_out' , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', As              , None, (), ),{}),
     'CAII_in': (('A-factor CAII'  , 'CAII_in'  , pos_float, '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', Ai              , None, (), ),{}),
    'CAIV_out': (('A-factor CAIV'  , 'CAIV_out' , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', As              , None, (), ),{}),
    'pKHA1_in': (('pK<sub>3</sub>_ICF','pKHA1_in',reg_float, '{}', 3, 'Reaction Rates'                       ,  'tb', [7.23          ], None, ('kb_HA1_in_minus', )), {} ),
'Pm_CO2_input': (('CO<sub>2</sub>','Pm_CO2_input',pos_float, '{}', 1, 'Permeability Across PM'               , 'dtb', [0.03078       ], None, (                   )), {} ),
       'Panel': (('Panel'          , 'Panel'    ,  a_string, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [panel         ], None, (), ),{}),
}

fig_param_list= build_param_list(param_list_AJP2014,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 8'],
    'fname':__file__,
}
