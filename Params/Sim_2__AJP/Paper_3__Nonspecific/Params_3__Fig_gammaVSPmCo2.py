# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_2__AJP.Param_Defaults_AJP2014 import *
from Params.Params import *

#                   Human Readable              Matlab      Valid  Format Col      Group                  Type    Value                                       OVCCallback Dependents Dropdown Choices
fig_params= {\
         'vit_mem': (('Vitelline Membrane Flag'     , 'vit_mem'      ,    mlbool,   '{}', 2, 'Plasma Membrane (PM)'                 ,  'cb', [False             ],     None, (                          )), {}                                         ),
#    'layer_in_mem': (('Enable Vesicles'             , 'layer_in_mem'   ,    mlbool,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'cb', [False             ],     None, (                          )), {}                                         ),
      'tort_gamma': (('tort_gamma'     , 'tort_gamma'     , pos_float, '{}', 2, 'Intracellular Fluid (ICF)',  'tb', [0.24, 0.22, 0.20, 0.18, 0.16, 0.14, 0.12, 0.10, 0.08, 0.06], None, (  )), {} ),
    'Pm_CO2_input': (('CO<sub>2</sub>' , 'Pm_CO2_input'   , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/10000                                                ], None, (  )), {} ),
 'cust_plot_title': (('CustomPlotTitle', 'cust_plot_title',  a_string, '{}', 1,                     'Extra',  'tb', ['PmCO2 Divisor= 10000'                                    ], None, (  )), {} ),
 # ADD TITLES

#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/20000                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/22500                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/25000                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/27500                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input'  , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/30000                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input'  , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/32500                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input'  , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/35000                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/37500                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/40000                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/45000                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/50000                                                ], None, (  )), {} ),
#    'Pm_CO2_input': (('CO<sub>2</sub>', 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [34.2/100000                                                ], None, (  )), {} ),
}

fig_param_list= build_param_list(param_list_AJP2014,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 5'],
    'fname':__file__,
}
