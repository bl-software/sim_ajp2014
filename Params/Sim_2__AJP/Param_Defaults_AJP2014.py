# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_1__JTB.Param_Defaults_JTB2012 import *
from Params.Params import *

#                    Human Readable                  Matlab              Valid       Format Col Group                                   Type   Value              OVCCallback   Dependents                  Dropdown Choices
def_param_list_AJP2014= {\
        'tf_CO2on': (('Time I -> E (s)'             , 'tf_CO2on'       , pos_float,   '{}', 1, 'Experiment'                           ,  'tb', [1200.0           ],     None, (                          )), {}                                         ),
       'thickness': (('EUF Thickness (mm)'          , 'thickness'      , pos_float,   '{}', 1, 'Geometry'                             ,  'tb', [0.01             ],     None, (                          )), {}                                         ),
           'n_out': (('# Shells Out'                , 'n_out'          ,   pos_int, '{:d}', 1, 'Geometry'                             ,  'tb', [10               ],     None, (                          )), {}                                         ),
     'oocyte_type': (('Oocyte Type'                 , 'oocyte_type'    ,  a_string,   '{}', 1, 'Experimental Conditions'              ,  'ch', ['Tris'           ],     None, ('pH_in_init', 'pH_in_acid')), {'choices':['Tris','H2O','CAII','CAIV']  } ),
          'CO2_pc': (('% CO<sub>2</sub>'            , 'CO2_pc'         , pos_float,   '{}', 1, 'Experimental Conditions'              ,  'ch', [1.5              ],     None, ('pH_in_init', 'pH_in_acid')), {'choices':['1.5','5.0','10.0']          } ),
      'pH_in_acid': (('pH_in_acid'                  , 'pH_in_acid'     ,        pH,   '{}', 1, 'Initial Concentrations'               ,  'tb', ('f__pH_in_acid', ),     None, ('A1tot_in',               )), {}                                         ),
      'pH_in_init': (('pH_in_init'                  , 'pH_in_init'     ,        pH,   '{}', 1, 'Initial Concentrations'               ,  'tb', ('f__pH_in_init', ),     None, ('A1tot_in',               )), {}                                         ),
   'CAII_out_flag': (('Enable CAII EUF'             , 'CAII_out_flag'  , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [False    ], None, ( )), {} ),
        'CAII_out': (('CAII Out'                    , 'CAII_out'       , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [5.0      ], None, ( )), {} ),
        'CAIV_out': (('CAIV Out'                    , 'CAIV_out'       , pos_float,   '{}', 2, 'Extracellular Unconvected Fluid (EUF)',  'tb', [150.0    ], None, ( )), {} ),

         'CAII_in': (('CAII In'                     , 'CAII_in'        , pos_float, '{}', 2, 'Intracellular Fluid (ICF)','tb', [5.0   ], None, ( )),{} ),
    'layer_in_mem': (('Enable Vesicles'             , 'layer_in_mem'   ,    mlbool, '{}', 2, 'Intracellular Fluid (ICF)', 'cb', [True ], None, ()), {} ),
              'd2': (('Thickness (µm)'              , 'd2'             , pos_float, '{}', 2, 'Intracellular Fluid (ICF)', 'tb', [30   ], None, ()), {} ),
#'oos_tort_lambda': (('oos_tort_lambda'             , 'oos_tort_lambda', pos_float, '{}', 2, 'Intracellular Fluid (ICF)', 'tb', [0.1  ], None, ()), {} ),
#     'tort_gamma': (('tort_gamma'                  , 'tort_gamma'     , pos_float, '{}', 2, 'Intracellular Fluid (ICF)', 'tb', [0.03 ], None, ()), {} ),
 'oos_tort_lambda': (('Tort Lambda Vesicles (1/𝜆)'  , 'oos_tort_lambda', pos_float, '{}', 2, 'Intracellular Fluid (ICF)', 'tb', [0.1  ], None, ()), {} ),
      'tort_gamma': (('Tort Gamma VitMem (1/𝛄)'     , 'tort_gamma'     , pos_float, '{}', 2, 'Intracellular Fluid (ICF)', 'tb', [0.03 ], None, ()), {} ),

              'SA': (('Surface Amplification Factor', 'SA'           , pos_float, '{}', 2, 'Plasma Membrane (PM)'                 ,  'tb', [9.0      ], None, (                   )), {} ),
         'vit_mem': (('Vitelline Membrane Flag'     , 'vit_mem'      ,    mlbool, '{}', 2, 'Plasma Membrane (PM)'                 ,  'cb', [True     ], None, (                   )), {} ),
         'Buff_pc': (('Immobile buffer fraction'    , 'Buff_pc'      ,   percent, '{}', 3, 'Buffer Reactions'                     ,  'tb', [0        ], None, ('pH_in_init',      )), {} ),
        'pKHA1_in': (('pK<sub>3</sub>_ICF'          , 'pKHA1_in'     , reg_float, '{}', 3, 'Reaction Rates'                       ,  'tb', [7.105    ], None, ('kb_HA1_in_minus', )), {} ),
    'Pm_CO2_input': (('CO<sub>2</sub>'              , 'Pm_CO2_input' , pos_float, '{}', 1, 'Permeability Across PM'               , 'dtb', [0.003420 ], None, (                   )), {} ),

      'PlotTitle': (('PlotTitle'      , 'PlotTitle'      ,  a_string, '{}', 2, 'Extra'                    , 'tb', ['DefaultPlotTitle' ], None, ()), {}),
        'OutFile': (('OutFile'        , 'OutFile'        ,  a_string, '{}', 2, 'Extra'                    , 'tb', ['defoutfile'       ], None, ()), {}),
         'OutCol': (('OutCol'         , 'OutCol'         ,  a_string, '{}', 2, 'Extra'                    , 'tb', ['defcolumn'        ], None, ()), {}),
    'BatchParams': (('BatchParams'    , 'BatchParams'    ,  a_string, '{}', 2, 'Extra'                    , 'tb', [''                 ], None, ()), {}),
}

param_list_AJP2014= build_param_list(param_list_JTB2012, def_param_list_AJP2014)

