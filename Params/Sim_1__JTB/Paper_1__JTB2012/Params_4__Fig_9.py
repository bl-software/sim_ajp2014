# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_1__JTB.Param_Defaults_JTB2012 import *
from Params.Params import *

#               Human Readable    Matlab       Valid  Format Col  Group                                    Type   Value                    OVCCallB  Dependents
fig_params={\
#         'CAII_in': (( 'CAII In'                                            , 'CAII_in'         , pos_float,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [1.0, 1.0, 20.0, 20.0, 100.0], None         , (                  )),{} ),
#        'CAIV_out': (( 'CAIV Out'                                           , 'CAIV_out'        , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [1.0, 20.0, 1.0, 20.0, 100.0], None         , (                  )),{} ),
         'CAII_in': (( 'CAII In'                                            , 'CAII_in'         , pos_float,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [1.0, 1.0, 20.0, 20.0], None         , (                  )),{} ),
        'CAIV_out': (( 'CAIV Out'                                           , 'CAIV_out'        , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [1.0, 20.0, 1.0, 20.0], None         , (                  )),{} ),
}

fig_param_list= build_param_list(param_list_JTB2012,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 3', 'Fig 4', 'Fig 5', 'Fig 9' ],
    'fname':__file__,
}
