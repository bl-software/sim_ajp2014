# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_2__AJP.Param_Defaults_AJP2014 import *
from Params.Params import *

#                Human Readable     Matlab      Valid      Format Col  Group                                   Type    Value                  OVCCallback   Dependents           Dropdown Choices

Ai_list= [ 5.0, 20.0, 40.0, 100.0, 1000.0, 10000.0 ]
As_list= [ 150.0, 10000.0 ]
las=len(As_list)
lai=len(Ai_list)

#Ai=     5.0
#Ai=    20.0
#Ai=    40.0
#Ai=   100.0
#Ai=  1000.0
Ai= 10000.0
#As=   150.0
As= 10000.0
plottitle=f'Ai={Ai} As={As}'
outfile  =f'Ai_{Ai}__As_{As}'
outcol=''
     
fig_params= {\
    'tf_CO2on': (('Time I -> E (s)', 'tf_CO2on'      , pos_float, '{}', 1, 'Experiment'                           ,  'tb', [600.0   ], None, (                   )), {} ), 
    'CAII_out': (('CAII Out'      , 'CAII_out'       , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [0.0     ], None, (                   )), {}                                         ),
 'oocyte_type': (('Oocyte Type'    , 'oocyte_type'   ,  a_string, '{}', 1, 'Experimental Conditions'              ,  'ch', ['CAIV'  ], None, ('pH_in_init', 'pH_in_acid')), {'choices':['Tris','H2O','CAII','CAIV']} ),
     'CAII_in': (('CAII In'        , 'CAII_in'       , pos_float, '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [Ai      ], None, (                   )), {} ),
    'CAIV_out': (('CAIV Out'       , 'CAIV_out'      , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [As      ], None, (                   )), {} ),
    'pKHA1_in': (('pK<sub>3</sub>_ICF','pKHA1_in'    , reg_float, '{}', 3, 'Reaction Rates'                       ,  'tb', [7.23    ], None, ('kb_HA1_in_minus', )), {} ),
    #'Pm_CO2_input': (('CO<sub>2</sub>','Pm_CO2_input'    , pos_float, '{}', 1, 'Permeability Across PM'               , 'dtb', [0.03078 ], None, (                   )), {} ),
   'PlotTitle': (( 'PlotTitle'     , 'PlotTitle'   ,  a_string, '{}', 2, 'Extra'                                , 'tb', [plottitle ], None, ()), {}),
     'OutFile': (( 'OutFile'       , 'OutFile'     ,  a_string, '{}', 2, 'Extra'                                , 'tb', [outfile   ], None, ()), {}),
      'OutCol': (( 'OutCol'        , 'OutCol'      ,  a_string, '{}', 2, 'Extra'                                , 'tb', [outcol    ], None, ()), {}),
      #    'FigProps': (( 'FigProps'      , 'FigProps'    ,  a_string, '{}', 2, 'Extra'                                , 'tb', [figprops      ], None, ()), {}),
# 'BatchParams': (( 'BatchParams'   , 'BatchParams' ,  a_string, '{}', 2, 'Extra'                                , 'tb', batchp_list , None, ()), {}),
'Pm_CO2_input': (('CO<sub>2</sub>' , 'Pm_CO2_input', pos_float, '{}', 1, 'Permeability Across PM'               ,'dtb', [30.78/1000, 30.78/2500, 30.78/5000,30.78/10000, 30.78/27500, 30.78/32500, 30.78/35000, 30.78/37500, 30.78/50000, 30.78/100000], None, (  )), {} ),
#'Pm_CO2_input': (('CO<sub>2</sub>' , 'Pm_CO2_input', pos_float, '{}', 1, 'Permeability Across PM'               ,'dtb', [34.2/10000, 34.2/27500, 34.2/32500, 34.2/35000, 34.2/37500, 34.2/50000, 34.2/100000], None, (  )), {} ),
}

fig_param_list= build_param_list(param_list_AJP2014,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig DKPmCO2Sweep'],
    'fname':__file__,
}
