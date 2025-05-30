# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_1__JTB.Param_Defaults_JTB2012 import *
from Params.Params import *

#                 Human Readable   Matlab      Valid      Format Col  Group                    Type   Value                                                                                                          OVCCallB   Dependents
fig_params={}

fig_param_list= build_param_list(param_list_JTB2012,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['BaseSim' ],
    'fname':__file__,
}
