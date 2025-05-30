from Figures.Sim_2__AJP.Paper_1__AJP2014.AJP2014_Figs import AJP2014_Fig

class Fig(AJP2014_Fig):
    def __init__(self,run_time,run_data,run_params,*args,**kwargs):
        super().__init__(run_time,run_data,run_params,'5',args,kwargs)

#def fig__AJP_fig_5(self, fignum, fp):
        if fignum in [5.1,]:
            self.TESTING = False
        plot_rows=2
        plot_cols=2
        reds   = self.shades_ajp5r
        greens = self.shades_ajp5g
        plot_d={ 'colors'   : (greens, greens, reds, reds),
                 'remborder': []  ,
                 'tickspos' : 'both', }
        title='AJP 2014 Fig 5'
        if fignum == 5.1:
            cust_plot_title= fp.cust_plot_titles[0]
            title=f'AJP 2014 Fig 5(Custom) {cust_plot_title}'
        fig,axs = self.fig_makefig(plot_rows, plot_cols, size=None, title=title, plot_d=plot_d )

        xlims,ylims = ([[ None, 1200], [  1,    6], [None, 1200], [     1,     6]],
                       [[7.499, 7.54], [0.0, 0.04], [6.98, 7.23], [1.2e-3,2.2e-3]])

        exp_results,exp_testkeys = self.ajp2014_fig5_expected()
        test_res= {}

        #fig.suptitle(rf'$Effect\ of\ the\ Vitelline\ Membrane$', size=20, style='normal')
        for ri,oos_tort_gamma in enumerate(fp.tort_gammas):
            np_time    = np.array(fp.run_time   [ri])[:,0]
            np_data    = np.array(fp.run_data   [ri])
            n_buff     =          fp.n_buffs    [ri]
            n_in       =          fp.n_ins      [ri]
            n_out      =          fp.n_outs     [ri]
            N          =          fp.Ns         [ri]
            R_cm       =          fp.Rs_cm      [ri]
            R_inf_cm   =          fp.R_infs_cm  [ri]
            pH_in_init =          fp.pH_in_inits[ri]
            pH_out     =          fp.pH_outs    [ri]

            test_var= f'{oos_tort_gamma:.04f}'
            test_res[test_var]={}

            plot_t = np.insert(np_time,0,-100) # add first point to -infinity (-100)

            pHi,pHs= self.get_pH(np_data,n_buff,N,n_in,n_out,R_cm,depth_um=50)
            plot_pHi= np.insert(pHi,0,pHi[0])
            plot_pHs= np.insert(pHs,0,pHs[0])

            delta_pHs= max(pHs) - pH_out#pHs[0]

            dpHi_dt, max_dpHi_dt_idx, max_dpHi_dt= self.get_ddata_dt(pHi,np_time)
            dpHs_dt, max_dpHs_dt_idx, max_dpHs_dt= self.get_ddata_dt(pHs,np_time)

            gam = np.sqrt( 1 / oos_tort_gamma )

            max_pHs_idx = np.argmax(pHs)
            time_to_peak= np_time[max_pHs_idx]

            time_delay= np_time[max_dpHi_dt_idx]

            test_res[test_var]['delta_pHs'     ]=delta_pHs   , None
            test_res[test_var]['index_peak_pHs']=max_pHs_idx , None
            test_res[test_var]['max_dpHi_dt'   ]=max_dpHi_dt, None
            test_res[test_var]['time_delay'    ]=time_delay  , None

            lab= r'$\gamma = {:0.2f} (1/\gamma^2 = {:0.2f})$'.format(gam,oos_tort_gamma)
            ax = axs[0,0]
            ax.plot(plot_t ,plot_pHs, '-', linewidth=2.0, label=lab)
            self.update_xylims( ylims[0], pHs )

            ax = axs[0,1]
            ax.plot(gam, delta_pHs, 'o', markersize=10, linewidth=3.0,clip_on=False)
            self.update_xylims( ylims[1], (delta_pHs,) )

            ax = axs[1,0]
            ax.plot(plot_t, plot_pHi, '-', linewidth=2.0, label=lab)
            self.update_xylims( ylims[2], pHi )

            ax = axs[1,1]
            ax.plot(gam, -max_dpHi_dt, 'o', markersize=10, linewidth=3.0,clip_on=False)
            self.update_xylims( ylims[3], (-max_dpHi_dt,) )


        self.setup_axes(axs[0,0], 'Time (s)', r'$pH_s$', xlims[0], ylims[0],
                **{ 'paneltate':'A', 'axtit': r'1.5% CO_2 /10 mM HCO_3^-',
                    'leg':True, 'legalpha':0.15,
                    'leg_props':{'loc':(0.4,0.25), 'fontsize':15} })
        self.setup_axes(axs[0,1], '$\gamma$''Time (s)', r'$\Delta pH_s$', xlims[1], ylims[1],
                **{ 'paneltate':'B' })
        self.setup_axes(axs[1,0], 'Time (s)', r'$pH_i$', xlims[2], ylims[2],
                **{ 'paneltate':'C', 'axtit': r'1.5% CO_2 /10 mM HCO_3^-',
                    'leg':True, 'legalpha':0.15,
                    'leg_props':{'loc':(0.4,0.25), 'fontsize':15} })
        self.setup_axes(axs[1,1], '$\gamma$', r'$(dpH_i/dt)_{max}$', xlims[3], ylims[3],
                **{ 'paneltate':'D' })

        if self.TESTING:
            self.test_mfiles()
            self.test_results(exp_results,test_res)

        plt.show()


