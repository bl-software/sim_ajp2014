import numpy as np
from Figures.Sim_2__AJP.Paper_1__AJP2014.AJP2014_Figs import AJP2014_Fig

class Fig(AJP2014_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 2,
            ncols = 2,
            title = 'AJP 2014 Fig 4 - Effect of intracellular vesicles on pHi',
            plot_d= { 'colors'   : (self.shades_ajp4,) * 4,
                      'remborder': ['top','right'],}
                     #'tickspos' : 'both', }
        )
        self.make_fig()
        axs={'pHi'    : self.axs[0,0],
             'XXX'    : self.axs[0,1],
             'timedel': self.axs[1,0],
             'dpHidt' : self.axs[1,1],
        } 

        paneltext= [      'A',                   '',              'B', 'C'                   ]
        axtitles = [ r'1.5% CO_2 /10 mM HCO_3^-','',               '', ''                    ]
        xlabels  = ['Time(s)',                   '', '$\lambda$'     , '$\lambda$'           ]
        ylabels  = [r'$pH_i$',                   '', 'Time Delay (s)', r'$(dpH_i/dt)_{max}$' ]

        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        for i,ax in enumerate(axs.values()):
            fpp.paneltate = paneltext[i]
            fpp.ylabel    = ylabels[i]
            fpp.xlabel    = xlabels[i]
            fpp.axtitles  = axtitles[i]
            self.setup_axes( ax, fpp )

        plotkwargs={\
                'pHi'    : {'linestyle':'-', 'linewidth':3.0  , 'marker':'' },
                'pHs'    : {'linestyle':'-', 'linewidth':3.0  , 'marker':'' },
                'dpHidt' : {'linestyle':'' , 'markersize':10.0, 'marker':'o'},
                'timedel': {'linestyle':'' , 'markersize':10.0, 'marker':'o'},
            }

        oos_tort_lambdas= sr.rp['oos_tort_lambda']

        sr.extract( [ sr.get_substance, ], [('pH',),], [{},] )
        
        # 1 / λ² = tiny = oos_tort_lambda
        for ri,oostl in enumerate(oos_tort_lambdas):

            tort_lambda = np.sqrt( 1 / oostl )

            ed= sr.eds[ri]
            pHi= sr.get_pHi(ri,ed,depth_um=50)
#something wrong here - pHI is wrong - ok in JTB so isolated ot AJP
#similar to J fig6
#Related to Buff_pc - setting to 100 makes something close
#A1tot_in is wrong
#
#rxo                                     dale                        
#        A1m_in: 13.1508     <<<<                 A1m_in: 0
#      A1tot_in: 23.2423     <<<<               A1tot_in: 0
#  CAII_flag_in: 1                          CAII_in_flag: 1
# CAII_flag_out: 0                         CAII_out_flag: 0
#     CAIV_flag: 1                         CAIV_out_flag: 1
#        HA1_in: 10.0915     <<<<                 HA1_in: 0
#        Pm_CO2: 0.0308                           Pm_CO2: 0.0034
#            SA: 9                                    SA: 1
#     beta_mean: 13.3017                         rPm_CO2: 0.0031
#                                                    rSA: 9
#                                                    rhm: 5.0000e-07

            fpp.xvar= np.array(sr.t[ri])[:,0]

            fpp.plotkwargs=plotkwargs['pHi']
            fpp.plotkwargs.update({'label':
                    r'$\lambda = {:0.2f} (1/\lambda^2 = {:0.2f})$'.format(tort_lambda,oostl)})
            fpp.yvar= pHi
            self.plot_pH(axs['pHi'], fpp)

            sr.get_dpHi_dt(ri,ed,pHi)

            fpp.xvar= tort_lambda#oos_tort_lambdas

            fpp.plotkwargs=plotkwargs['dpHidt']
            fpp.plotkwargs.update({'label':''})

            td= ed.time_delay_pHi
            axs['timedel'].plot(tort_lambda,td, 'o', markersize=10, linewidth=3.0)
           
            axs['dpHidt'].plot(tort_lambda,-ed.max_dpHi_dt_I, 'o', markersize=10, linewidth=3.0)

        self.show_fig()


        #for ri,ax in zip(range(n_runs),(ax_ctrl,ax_caii,ax_caiv)):
#D        for  ri    in     range(n_runs):#,(ax_ctrl,ax_caii,ax_caiv)):
#D            ricolor= shades_ajp4[ri]
#D            ed=sr.eds[ri]
#D            fpp1.xvar= np.array(sr.t[ri])[:,0] # was np_time
#D            oos_tort_lambda= sr.rp['oos_tort_lambda'][ri]
        #NEW for ri,oos_tort_lambda in enumerate(fp.oos_tort_lambdas):
        #NEW     np_time    = np.array(fp.run_time   [ri])[:,0]
        #NEW     np_data    = np.array(fp.run_data   [ri])
        #NEW     n_buff     =          fp.n_buffs    [ri]
        #NEW     n_in       =          fp.n_ins      [ri]
        #NEW     n_out      =          fp.n_outs     [ri]
        #NEW     N          =          fp.Ns         [ri]
        #NEW     R_cm       =          fp.Rs_cm      [ri]
        #NEW     R_inf_cm   =          fp.R_infs_cm  [ri]
            #NEWpH_in_init =    sr.rp['pH_in_inits'][ri]
        
#TESTS            test_var= f'{oos_tort_lambda:.04f}'
#TESTS            test_res[test_var]={}

            #NEW plot_t = np.insert(np_time,0,-100) # add first point to -infinity (-100)

            #NEW pHi,pHs= self.get_pH(np_data,n_buff,N,n_in,n_out,R_cm,depth_um=50)
            #NEW plot_pHi= np.insert(pHi,0,pHi[0])
            #NEW plot_pHs= np.insert(pHs,0,pHs[0])

            #NEW dpHi_dt, max_dpHi_dt_idx, max_dpHi_dt= self.get_ddata_dt(pHi,np_time)

            #NEW xmax = ed.max_dpHi_dt_t_I #np_time[max_dpHi_dt_idx] # time  at max dpHi_dt
            #NEW mmax = ed.max_dpHi_dt_I  #dpHi_dt[max_dpHi_dt_idx] # slope at max dpHi_dt - also = max_dpHi_dt - but for consistency
            #NEW ymax =ed.pH_at_max_dpHi_E# pHi[max_dpHi_dt_idx]     # yval  at max dpHi_dt
            #NEW b = ymax - mmax * xmax

            #NEW xcross = (pH_in_init - b ) / mmax  # TODO which ???
            #NEW xcross = (pHi[0]     - b ) / mmax

#test            test_res[test_var]['max_dpHi_dt'  ]= max_dpHi_dt   ,None
#test            test_res[test_var]['index_dpHi_dt']= max_dpHi_dt_idx,None
#test            test_res[test_var]['time_delay'   ]= xcross         ,None

#D            ''' 1 / λ² = tiny = oos_tort_lambda   '''
#D#D            tort_lambda = np.sqrt( 1 / oos_tort_lambda )
#D#D            fpp1.plotkwargs['pHi'].update({\
        #D                    'label':r'$\lambda = {:0.2f} (1/\lambda^2 = {:0.2f})$'.format(tort_lambda,oos_tort_lambda),
#D                    'color':ricolor})
#D            self.plot_pHipHs(ax_pHi,ed,fpp1)
            #NEW ax_pHi.plot(plot_t,plot_pHi, '-', linewidth=2.0,
            #NEW     label=r'$\lambda = {:0.2f} (1/\lambda^2 = {:0.2f})$'.format(tort_lambda,oos_tort_lambda))#'LineWidth',2)
#D            self.plot_pHipHs(ax_pHiz1,ed,fpp1)
            #NEW ax_pHiz1.plot(np_time,pHi, '-')
            #NEW ax_pHiz1.plot(np_time,mmax*np_time + b,'k-')
            #NEW ax_pHiz1.axvline(xcross,0.1,0.9)
            #NEW ax_pHiz1.axhline(pH_in_init,0.1,0.99)

            #NEW ax_pHiz2.plot(np_time,pHi, '-')
            #NEW ax_pHiz2.plot(np_time,mmax*np_time + b,'k-')
            #NEW ax_pHiz2.axvline(xcross,0.1,0.9)
            #NEW ax_pHiz2.axhline(pH_in_init,0.1,0.99)
#D            xcross= ed.time_delay_pHi
#D            ax_tdl.plot(tort_lambda,xcross, 'o', markersize=10, linewidth=3.0)
            
#D            ax_dphl.plot(tort_lambda,-ed.max_dpHi_dt_I, 'o', markersize=10, linewidth=3.0)

#TEST        if self.TESTING:
#TEST            self.test_mfiles()
#TEST            self.test_results(exp_results,test_res)
#NEW        plt.show()

#D        self.show_fig()

