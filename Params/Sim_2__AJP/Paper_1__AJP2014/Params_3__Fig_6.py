# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_2__AJP.Param_Defaults_AJP2014 import *
from Params.Params import *

#                Human Readable       Matlab      Valid      Format Col  Group                                   Type  Value                  OVCCallback  Dependents           Dropdown Choices
fig_params= {\
    'tf_CO2on': (('Time I -> E (s)', 'tf_CO2on'      , pos_float, '{}', 1, 'Experiment'                           ,  'tb', [600.0                      ], None, (                   )), {} ), 
    'CAII_out': (('CAII Out'      , 'CAII_out'       , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [0.0                        ], None, (                   )), {}                                         ),
 'oocyte_type': (('Oocyte Type'    , 'oocyte_type'   ,  a_string, '{}', 1, 'Experimental Conditions'              ,  'ch', [  'Tris',   'CAII',  'CAIV'], None, ('pH_in_init', 'pH_in_acid')), {'choices':['Tris','H2O','CAII','CAIV']} ),
     'CAII_in': (('CAII In'        , 'CAII_in'       , pos_float, '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [     5.0,   1000.0,    40.0], None, (                   )), {} ),
    'CAIV_out': (('CAIV Out'       , 'CAIV_out'      , pos_float, '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [   150.0,    150.0, 10000.0], None, (                   )), {} ),
    'pKHA1_in': (('pK<sub>3</sub>_ICF','pKHA1_in'    , reg_float, '{}', 3, 'Reaction Rates'                       ,  'tb', [   7.105,    7.095,    7.23], None, ('kb_HA1_in_minus', )), {} ),
    'Pm_CO2_input': (('CO<sub>2</sub>','Pm_CO2_input', pos_float, '{}', 1, 'Permeability Across PM'               , 'dtb', [0.03078, 0.03078, 0.03078  ], None, (                   )), {} ),
    #'Pm_CO2_input': (('CO<sub>2</sub>','Pm_CO2_input', pos_float, '{}', 1, 'Permeability Across PM'               , 'dtb', [0.03078,], None, (                   )), {} ),
    #      'PlotTitle': (('PlotTitle'      , 'PlotTitle'      ,  a_string, '{}', 2, 'Extra'                    , 'tb', ['DefaultPlotTitle' ], None, ()), {}),
    #    'OutFile': (('OutFile'        , 'OutFile'        ,  a_string, '{}', 2, 'Extra'                    , 'tb', ['defoutfile'       ], None, ()), {}),
    #     'OutCol': (('OutCol'         , 'OutCol'         ,  a_string, '{}', 2, 'Extra'                    , 'tb', ['defcolumn'        ], None, ()), {}),
    #'BatchParams': (('BatchParams'    , 'BatchParams'    ,  a_string, '{}', 2, 'Extra'                    , 'tb', [                   ], None, ()), {}),
}

fig_param_list= build_param_list(param_list_AJP2014,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 6'],
    'fname':__file__,
}
