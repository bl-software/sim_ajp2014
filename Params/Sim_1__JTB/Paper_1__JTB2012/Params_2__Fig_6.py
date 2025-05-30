# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_1__JTB.Param_Defaults_JTB2012 import *
from Params.Params import *

#                  Human Readable        Matlab           Valid  Format Col  Group       Type   Value                                                   OVCCallB   Dependents
fig_params={\
    'thickness': (( 'EUF Thickness (mm)', 'thickness', pos_float,   '{}', 1, 'Geometry',  'tb', [0.1500, 0.1000, 0.0500, 0.0250, 0.0100, 0.0050, 0.0010],    None,         ( )),{}),
        'n_out': (( '# Shells Out'      , 'n_out'    ,   pos_int, '{:d}', 1, 'Geometry',  'tb', [   150,    100,     50,     25,     10,      5,      5],    None,         ( )),{}),
}

fig_param_list= build_param_list(param_list_JTB2012,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 3', 'Fig 4', 'Fig 5', 'Fig 6' ],
    'fname':__file__,
}
