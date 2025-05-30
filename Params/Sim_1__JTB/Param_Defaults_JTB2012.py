# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
'''
 NOTE: Unicode: ? U+2082  - these print at baseline not decended
'''
'''
 key = Matlab Var Name
   Human Readable Name
   Matlab Var Name
   Validator function
   Format String
   Display Column - dynamic column creation based on what is found here
   Display Group  - dynamic group  creation based on what is found here
   Display Type   - used to create widget and set some attributes
   Value - if applicablen - default in this file - can be a callable function to return the value.
   Callback when value is set - example to show equation on the screen
   List of Dependents - other vals that need to change when this changes

'''
from Params.Param_Validators import *

#                          Human Readable                                         Matlab         Valid      Format Col Group                                    Type    Value                OnValCh Callback    Dependents
def_param_list_JTB2012= {\
            'tmax': (( 'Max Time (s)'                                       , 'tmax'            , pos_float,   '{}', 1, 'Experiment'                           ,  'tb', [1200.0             ], None          , (                  )),{} ),
     'temperature': (( 'Temp (°C)'                                          , 'temperature'     , pos_float,   '{}', 1, 'Experiment'                           ,  'tb', [22.0               ], None          , (                  )),{} ),

               'D': (( 'Cell Diameter (mm)'                                 , 'D'               , pos_float,   '{}', 1, 'Geometry'                             ,  'tb', [1.3                ], None          , ('thickness',      )),{} ),
           'D_inf': (( 'Edge of BECF (mm)'                                  , 'D_inf'           , pos_float,   '{}', 1, 'Geometry'                             , 'otb', ('f__d_inf',        ), None          , ('thickness',      )),{} ),
       'thickness': (( 'EUF Thickness (mm)'                                 , 'thickness'       , pos_float,   '{}', 1, 'Geometry'                             ,  'tb', [0.1000             ], None          , (                  )),{} ),
            'n_in': (( '# Shells In'                                        , 'n_in'            , pos_int  , '{:d}', 1, 'Geometry'                             ,  'tb', [80                 ], None          , (                  )),{} ),
           'n_out': (( '# Shells Out'                                       , 'n_out'           , pos_int  , '{:d}', 1, 'Geometry'                             ,  'tb', [100                ], None          , (                  )),{} ),

          'CO2_pc': (( '% CO<sub>2</sub>'                                   , 'CO2_pc'          , percent  ,   '{}', 1, 'Experimental Conditions'              ,  'tb', [1.5                ], None          , ('A1tot_in',       )),{} ),

              'PB': (( 'PB (mmHg)'                                          , 'PB'              , pos_float,   '{}', 1, 'Environment'                          ,  'tb', [760.0              ], None          , ('A1tot_in',       )),{} ),
            'PH2O': (( 'PH<sub>2</sub>O (mmHg)'                             , 'PH2O'            , pos_float,   '{}', 1, 'Environment'                          ,  'tb', [35.0               ], None          , ('A1tot_in',       )),{} ),
            'sCO2': (( 'sCO<sub>2</sub>(mM/mmHg)'                           , 'sCO2'            , pos_float,   '{}', 1, 'Environment'                          ,  'tb', [0.0434             ], None          , ('A1tot_in',       )),{} ),

          'pH_out': (( 'pH_out'                                             , 'pH_out'          , pH       ,   '{}', 1, 'Initial Concentrations'               ,  'tb', [7.5                ], None          , (                  )),{} ),
       'A1tot_out': (( 'A1tot_out (mM)'                                     , 'A1tot_out'       , pos_float,   '{}', 1, 'Initial Concentrations'               ,  'tb', [5                  ], None          , (                  )),{} ),
          'CO2_in': (( 'CO<sub>2</sub>_in (%)'                              , 'CO2_in'          , percent  ,   '{}', 1, 'Initial Concentrations'               ,  'tb', [0.0                ], None          , ('A1tot_in',       )),{} ),
      'pH_in_init': (( 'pH_in_init'                                         , 'pH_in_init'      , pH       ,   '{}', 1, 'Initial Concentrations'               ,  'tb', [7.2                ], None          , ('A1tot_in',       )),{} ),
     'pH_in_final': (( 'pH_in_final'                                        , 'pH_in_final'     , pH       ,   '{}', 1, 'Initial Concentrations'               ,  'tb', [7.0                ], None          , ('A1tot_in',       )),{} ),
        #'A1tot_in':m( 'A1tot_in (mM)'        , 'A1tot_in'   ,
        #            pos_float,   '{}', 1, 'Initial Concentrations'               , 'otb', lambda:f__AXtot_in(1), None              , (                  )),{} ),
        'A1tot_in': (( 'A1tot_in (mM)'                                      , 'A1tot_in'        , pos_float,   '{}', 1, 'Initial Concentrations'               , 'otb', ('f__AXtot_in',1    ), None          , (                  )),{} ),

    'CAII_in_flag': (( 'Enable CAII ICF'                                    , 'CAII_in_flag'    ,    mlbool,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'cb', [True               ], None          , (                  )),{} ),
          'A_CAII': (( 'A-factor CAII'                                      , 'A_CAII'          , pos_float,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [1.0                ], None          , (                  )),{} ),
         'CAII_in': (( 'CAII In'                                            , 'CAII_in'         , pos_float,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [20.0               ], None          , (                  )),{} ),
    'layer_in_mem': (( 'Enable Vesicles'                                    , 'layer_in_mem'    ,    mlbool,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'cb', [0                  ], None          , (                  )),{} ),
              'd1': (( 'Dist from PM (µm)'                                  , 'd1'              , pos_float,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [10                 ], None          , (                  )),{} ),
              'd2': (( 'Thickness (µm)'                                     , 'd2'              , pos_float,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [50                 ], None          , (                  )),{} ),
 'oos_tort_lambda': (( 'oos_tort_lambda'                                    , 'oos_tort_lambda' , pos_float,   '{}', 2, 'Intracellular Fluid (ICF)'            ,  'tb', [0.125              ], None          , (                  )),{} ),

              'SA': (( 'Surface Amplification Factor'                       , 'SA'              , pos_float,   '{}', 2, 'Plasma Membrane (PM)'                 ,  'tb', [1                  ], None          , (                  )),{} ),

   'CAIV_out_flag': (( 'Enable CAIV EUF'                                    , 'CAIV_out_flag'   ,    mlbool,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'cb', [True               ], None          , (                  )),{} ),
          'A_CAIV': (( 'A-factor CAIV'                                      , 'A_CAIV'          , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [1.0                ], None          , (                  )),{} ),
        'CAIV_out': (( 'CAIV Out'                                           , 'CAIV_out'        , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [20.0               ], None          , (                  )),{} ),
          'd_CAIV': (( 'd_CAIV'                                             , 'd_CAIV'          , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [0.005              ], None          , (                  )),{} ),

          'n_buff': (( '# Buffers'                                          , 'n_buff'          ,   reg_int, '{:d}', 3, 'Buffer Reactions'                     ,  'tb', [2                  ], 'update_buffs', (                  )),{} ),
         'Buff_pc': (( 'Immobile buffer fraction'                           , 'Buff_pc'         ,   percent,   '{}', 3, 'Buffer Reactions'                     ,  'tb', [0                  ], None          , (                  )),{} ),

            'kb_1': (( '𝑘<sub>1</sub> (s<sup>-1</sup>)'                     , 'kb_1'            , pos_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [0.0302             ], None          , ('pK1',            )),{} ),
            'kb_2': (( '𝑘<sub>-1</sub> (s<sup>-1</sup>)'                    , 'kb_2'            , pos_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [10.9631            ], None          , ('pK1',            )),{} ),
             'pK1': (( 'pK<sub>1</sub>'                                     , 'pK1'             , sci_float,   '{}', 3, 'Reaction Rates'                       , 'otb', ('f__pK1',          ), None          , ('A1tot_in',       )),{} ),

            'kb_3': (( '𝑘<sub>2</sub> (s<sup>-1</sup>)'                     , 'kb_3'            , pos_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [1e16               ], None          , ('kb_4',           )),{} ),
            'kb_4': (( '𝑘<sub>-2</sub> (mM<sup>-1</sup>s<sup>-1</sup>)'     , 'kb_4'            , pos_float,   '{}', 3, 'Reaction Rates'                       , 'otb', ('f__kb_X',3,'2'    ), None          , (                  )),{} ),
             'pK2': (( 'pK<sub>2</sub>'                                     , 'pK2'             , sci_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [3.618357367951740  ], None          , ('kb_4','A1tot_in',)),{} ),

            'kb_5': (( '𝑘<sub>3</sub>_EUF (s<sup>-1</sup>)'                 , 'kb_5'            , pos_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [1e10               ], None          , ('kb_6',           )),{} ),
            'kb_6': (( '𝑘<sub>-3</sub>_EUF (mM<sup>-1</sup>s<sup>-1</sup>)' , 'kb_6'            , pos_float,   '{}', 3, 'Reaction Rates'                       , 'otb', ('f__kb_X',5,'HA1_out'), None        , (                  )),{} ),
       'pKHA1_out': (( 'pK<sub>3</sub>_EUF'                                 , 'pKHA1_out'       , sci_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [7.5                ], None          , ('kb_6',           )),{} ),

  'kb_HA1_in_plus': (( '𝑘<sub>3</sub>_ICF (s<sup>-1</sup>)'                 , 'kb_HA1_in_plus'  , pos_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [1e10               ], None          , ('kb_HA1_in_minus',)),{} ),
 'kb_HA1_in_minus': (( '𝑘<sub>-3</sub>_ICF (mM<sup>-1</sup>s<sup>-1</sup>)' , 'kb_HA1_in_minus' , pos_float,   '{}', 3, 'Reaction Rates'                       , 'otb', ('f__kb_HAX_in_minus',1,), None      , (                  )),{} ),
        'pKHA1_in': (( 'pK<sub>3</sub>_ICF'                                 , 'pKHA1_in'        , reg_float,   '{}', 3, 'Reaction Rates'                       ,  'tb', [7.10               ], None          , ('kb_HA1_in_minus',)),{} ),

       'mobdialog': (( 'Edit Mobilities'                                    , 'mobdialog'       ,   no_test,   '{}', 2, 'Mobilities'                           ,   'b', ['OnMobilities'     ], None          , (                  )),{} ),
    'kappa_in_co2': (( 'Inner Mobility CO<sub>2</sub>'                      , 'kappa_in_co2'    , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.71e-5            ], None          , (                  )),{} ),
     'kappa_in_hp': (( 'Inner Mobility H<sup>+</sup>'                       , 'kappa_in_hp'     , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [8.69e-5            ], None          , (                  )),{} ),
  'kappa_in_h2co3': (( 'Inner Mobility H<sub>2</sub>CO<sub>3</sub>'         , 'kappa_in_h2co3'  , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.11e-5            ], None          , (                  )),{} ),
  'kappa_in_hco3m': (( 'Inner Mobility HCO<sub>3</sub><sup>-</sup>'         , 'kappa_in_hco3m'  , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.11e-5            ], None          , (                  )),{} ),
   'kappa_out_co2': (( 'Outer Mobility CO<sub>2</sub>'                      , 'kappa_out_co2'   , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.71e-5            ], None          , (                  )),{} ),
    'kappa_out_hp': (( 'Outer Mobility H<sup>+</sup>'                       , 'kappa_out_hp'    , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [8.69e-5            ], None          , (                  )),{} ),
 'kappa_out_h2co3': (( 'Outer Mobility H<sub>2</sub>CO<sub>3</sub>'         , 'kappa_out_h2co3' , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.11e-5            ], None          , (                  )),{} ),
 'kappa_out_hco3m': (( 'Outer Mobility HCO<sub>3</sub><sup>-</sup>'         , 'kappa_out_hco3m' , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.11e-5            ], None          , (                  )),{} ),
  'buf_mob_in_ha1': (( 'Buffer Mobility In HA<sub>1</sub>'                  , 'buf_mob_in_ha1'  , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5            ], None          , (                  )),{} ),
   'buf_mob_in_a1': (( 'Buffer Mobility In A<sub>1</sub>'                   , 'buf_mob_in_a1'   , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5            ], None          , (                  )),{} ),
 'buf_mob_out_ha1': (( 'Buffer Mobility Out HA<sub>1</sub>'                 , 'buf_mob_out_ha1' , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5            ], None          , (                  )),{} ),
  'buf_mob_out_a1': (( 'Buffer Mobility Out A<sub>1</sub>'                  , 'buf_mob_out_a1'  , pos_float,   '{}', 1, 'Mobilities'                           , 'dtb', [1.56e-5            ], None          , (                  )),{} ),

      'permdialog': (( 'Edit Permeabilities'                                , 'permdialog'      ,   no_test,   '{}', 2, 'Permeability Across PM'               ,   'b', ['OnPermeabilities' ], None          , (                  )),{} ),
    'Pm_CO2_input': (( 'CO<sub>2</sub>'                                     , 'Pm_CO2_input'    , pos_float,   '{}', 1, 'Permeability Across PM'               , 'dtb', [34.20              ], None          , (                  )),{} ),
 'cust_plot_title': (('CustomPlotTitle'                                     , 'cust_plot_title' ,  a_string,  'HMM', 1, 'Extra'                                ,  'tb', ['HWHYYY'           ], None          , (                  )),{} ),
}

param_list_JTB2012 = def_param_list_JTB2012
