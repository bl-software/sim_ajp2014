# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_2__AJP.Param_Defaults_AJP2014 import *
from Params.Params import *

#                    Human Readable  Matlab        Valid    Format Col  Group                    Type    Value                            OVCCallback   Dependents                  Dropdown Choices
fig_params= {\
'oos_tort_lambda': (('oos_tort_lambda', 'oos_tort_lambda', pos_float, '{}', 2, 'Intracellular Fluid (ICF)',  'tb', [ 1.0,  0.5, 0.25, 0.12, 0.06, 0.03], None, ( )), {} ),
   'layer_in_mem': (('Enable Vesicles',    'layer_in_mem',    mlbool, '{}', 2, 'Intracellular Fluid (ICF)',  'cb', [True, True, True, True, True, True], None, ( )), {} ),
             #'Pm_CO2_input': (('CO<sub>2</sub>' ,    'Pm_CO2_input', pos_float, '{}', 1, 'Permeability Across PM'   , 'dtb', [0.0308                            ], None, ( )), {} ),
             #    'Pm_CO2_input': (('CO<sub>2</sub>'              , 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'               , 'dtb', [0.003420 ], None, (                   )), {} ),
}
#NOTE WARNING TODO checkbox not multipled for batch

fig_param_list= build_param_list(param_list_AJP2014,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 4'],
    'fname':__file__,
}
