# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_1__JTB.Param_Defaults_JTB2012 import *
from Params.Params import *

#                 Human Readable   Matlab      Valid      Format Col  Group                    Type   Value                                                                                                          OVCCallB   Dependents
atotlist= [\
     2.731256010386550e+04, # 𝛽 = 1000 𝛽std
     1.365628005193275e+02, # 𝛽 =    5 𝛽std
    54.625120207731001,     # 𝛽 =    2 𝛽std
    27.312560103865501,     # 𝛽 =    1 𝛽std
    13.656280051932750,     # 𝛽 =      𝛽std /2
     0                      # 𝛽 =    0
]

fig_params={\
    'A1tot_in': (( 'A1tot_in (mM)'                                      , 'A1tot_in'        , pos_float,   '{}', 1, 'Initial Concentrations'               ,  'tb',              atotlist, None,           ( )),{}), }

fig_param_list= build_param_list(param_list_JTB2012,fig_params)
fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 3', 'Fig 4', 'Fig 5', 'Fig 10' ],
    'fname':__file__,
}
