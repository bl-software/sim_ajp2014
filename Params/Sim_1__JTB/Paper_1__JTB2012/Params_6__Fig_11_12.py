# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_1__JTB.Param_Defaults_JTB2012 import *
from Params.Params import *

#                     Human Readable                                         Matlab                  Valid  Format Col  Group                                   Type   Value                          OVCCallB           Dependents
fig_params={\
          'CO2_pc': (( '% CO<sub>2</sub>'                                   , 'CO2_pc'          ,   percent,   '{}', 1, 'Experimental Conditions'              ,  'tb', [1.5                        ], None            , ('A1tot_in','A2tot_in'        )),{}),
              'PB': (( 'PB (mmHg)'                                          , 'PB'              , pos_float,   '{}', 1, 'Environment'                          ,  'tb', [760.0                      ], None            , ('A1tot_in','A2tot_in'        )),{}),
            'PH2O': (( 'PH<sub>2</sub>O (mmHg)'                             , 'PH2O'            , pos_float,   '{}', 1, 'Environment'                          ,  'tb', [35.0                       ], None            , ('A1tot_in','A2tot_in'        )),{}),
            'sCO2': (( 'sCO<sub>2</sub>(mM/mmHg)'                           , 'sCO2'            , pos_float,   '{}', 1, 'Environment'                          ,  'tb', [0.0434                     ], None            , ('A1tot_in','A2tot_in'        )),{}),

       'A2tot_out': (( 'A2tot_out (mM)'                                     , 'A2tot_out'       , pos_float,   '{}', 1, 'Initial Concentrations'               ,  'tb', [0                          ], None            , (                             )),{}),
          'CO2_in': (( 'CO<sub>2</sub>_in (%)'                              , 'CO2_in'          ,   percent,   '{}', 1, 'Initial Concentrations'               ,  'tb', [0.0                        ], None            , ('A1tot_in','A2tot_in'        )),{}),
      'pH_in_init': (( 'pH_in_init'                                         , 'pH_in_init'      ,        pH,   '{}', 1, 'Initial Concentrations'               ,  'tb', [7.2                        ], None            , ('A1tot_in','A2tot_in'        )),{}),
     'pH_in_final': (( 'pH_in_final'                                        , 'pH_in_final'     ,        pH,   '{}', 1, 'Initial Concentrations'               ,  'tb', [7.0                        ], None            , ('A1tot_in','A2tot_in'        )),{}),
#        'A1tot_in': (( 'A1tot_in (mM)'                                      , 'A1tot_in'        , pos_float,   '{}', 1, 'Initial Concentrations'               , 'otb', [27.3125601038655           ], None            , (                             )),{}),
        'A1tot_in': (( 'A1tot_in (mM)'                                      , 'A1tot_in'        , pos_float,   '{}', 1, 'Initial Concentrations'               , 'otb', ('f__AXtot_in',1            ), None            , (                             )),{}),
        'A2tot_in': (( 'A2tot_in (mM)'                                      , 'A2tot_in'        , pos_float,   '{}', 1, 'Initial Concentrations'               , 'otb', ('f__AXtot_in',2            ), None            , (                             )),{}),

          'n_buff': (( '# Buffers'                                          , 'n_buff'          ,   reg_int, '{:d}', 3, 'Buffer Reactions'                     ,  'tb', [3                          ], 'update_buffs'  , (                             )),{}),
         'Buff_pc': (( '3rd buffer fraction'                                , 'Buff_pc'         ,   percent,   '{}', 3, 'Buffer Reactions'                     ,  'tb', [0, 50, 70, 80, 90, 95, 100 ], None            , ('A1tot_in', 'A2tot_in'       )),{}),


             'pK1': (( 'pK<sub>1</sub>'                                     , 'pK1'             ,  sci_float,   '{}', 3, 'Reaction Rates'                       , 'otb', ('f__pK1',                  ), None            , ('A1tot_in','A2tot_in'        )),{}),

             'pK2': (( 'pK<sub>2</sub>'                                     , 'pK2'             ,  sci_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [3.618357367951740          ], None            , ('kb_4','A1tot_in','A2tot_in' )),{}),

            'kb_7': (( '𝑘<sub>4</sub>_EUF (s<sup>-1</sup>)'                 , 'kb_7'            , pos_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [1e10                       ], None            , ('kb_8',                      )),{}),
            'kb_8': (( '𝑘<sub>-4</sub>_EUF (mM<sup>-1</sup>s<sup>-1</sup>)' , 'kb_8'            , pos_float,   '{}', 3, 'Reaction Rates'                       , 'otb', ('f__kb_X',7,'HA2_out'      ), None            , (                             )),{}),
       'pKHA2_out': (( 'pK<sub>4</sub>_EUF'                                 , 'pKHA2_out'       ,  sci_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [7.5                        ], None            , ('kb_8',                      )),{}),


  'kb_HA2_in_plus': (( '𝑘<sub>4</sub>_ICF (s<sup>-1</sup>)'                 , 'kb_HA2_in_plus'  , pos_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [1e10                       ], None            , ('kb_HA2_in_minus',           )),{}),
 'kb_HA2_in_minus': (( '𝑘<sub>-4</sub>_ICF (mM<sup>-1</sup>s<sup>-1</sup>)' , 'kb_HA2_in_minus' , pos_float,   '{}', 3, 'Reaction Rates'                       , 'otb', ('f__kb_HAX_in_minus',2     ), None            , (                             )),{}),
        'pKHA2_in': (( 'pK<sub>4</sub>_ICF'                                 , 'pKHA2_in'        , reg_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [7.10                       ], None            , ('kb_HA2_in_minus',           )),{}),

  'buf_mob_in_ha1': (( 'Buffer Mobility In HA<sub>1</sub>'                  , 'buf_mob_in_ha1'  , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [0.0                        ], None            , (                             )),{}),
   'buf_mob_in_a1': (( 'Buffer Mobility In A<sub>1</sub>'                   , 'buf_mob_in_a1'   , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [0.0                        ], None            , (                             )),{}),

  'buf_mob_in_ha2': (( 'Buffer Mobility In HA<sub>2</sub>'                  , 'buf_mob_in_ha2'  , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5                    ], None            , (                             )),{}),
   'buf_mob_in_a2': (( 'Buffer Mobility In A<sub>2</sub>'                   , 'buf_mob_in_a2'   , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5                    ], None            , (                             )),{}),
 'buf_mob_out_ha2': (( 'Buffer Mobility Out HA<sub>2</sub>'                 , 'buf_mob_out_ha2' , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5                    ], None            , (                             )),{}),
  'buf_mob_out_a2': (( 'Buffer Mobility Out A<sub>2</sub>'                  , 'buf_mob_out_a2'  , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5                    ], None            , (                             )),{}),
}

fig_param_list= build_param_list(param_list_JTB2012,fig_params)

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 3', 'Fig 4', 'Fig 5', 'Fig 11', 'Fig 12' ],
    'fname':__file__,
}
