# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_1__JTB.Param_Defaults_JTB2012 import *
from Params.Params import *

#                     Human Readable    Matlab              Valid  Format  Col  Group                     Type   Value                                                                         OVCCallB   Dependents
pmco2list=[34.20, 3.42, 34.2e-2, 34.2e-3, 34.2e-4, 13.68e-4, 6.84e-4, 4.56e-4, 34.2e-5]
fig_params={\
    'Pm_CO2_input': (( 'CO<sub>2</sub>', 'Pm_CO2_input', pos_float,   '{}', 1, 'Permeability Across PM', 'dtb', pmco2list, None, ( )),{}),
            'n_in': (( '# Shells In'   , 'n_in'        ,   pos_int, '{:d}', 1, 'Geometry'              ,  'tb', [325    ], None, ( )),{}),
}

fig_param_list= build_param_list(param_list_JTB2012,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 3', 'Fig 4', 'Fig 5', 'Fig 7', 'Fig 8' ],
    'fname':__file__,
}
