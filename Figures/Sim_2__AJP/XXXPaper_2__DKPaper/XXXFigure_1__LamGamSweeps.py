import numpy as np
from Figures.Sim_2__AJP.Paper_1__AJP2014.AJP2014_Figs import AJP2014_Fig

class Fig(AJP2014_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)
        sr=sim_results
        
        sweepvarname= self.sr.get_run_var(-1, 'SweepVar')[0] # 'tort_gamma'
        sweepvars= self.sr.rp[sweepvarname]
        xlabel= self.sr.cp[sweepvarname].human_name
        titlerunpart = self.sr.get_run_var(0, 'PlotTitle')

        # fp is SimFigure:FigProps
        self.fp.plot_rows=2
        self.fp.plot_cols=3
        self.fp.plot_d={ 'remborder': ['top','right']  ,
                         'tickspos' : 'bottom', }
        self.fp.title='AJP Sweep'
        self.fp.shades = self.shades_ajp6g        # WAS "shades"

        self.make_fig()

        ax_ph     = self.axs[0,0]
        ax_dphidt = self.axs[0,1]
        ax_delphs = self.axs[0,2]
        ax_tdelayphi = self.axs[1,1]
        ax_ttpeakphs = self.axs[1,2]
        
        n_runs= len(sr.t)
        sr.extract( [ sr.get_pH, sr.get_dpHi_dt, sr.get_delpHs ])

        fpp=self.FigPanelProps() 
        fpp.plotkwargs={\
            'pHi':
                {'color':   'red', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'pHi' },
            'pHs':
                {'color': 'green', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'pHs' },
            'dpHi':
                {'color': 'blue', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'dpHidtmax' },
            'dpHs':
                {'color': 'orange', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'ΔpHs' },
        }
        fpp.kwargs={ 'toplot':['pHi','pHs', 'dpHi', 'dpHs'], }


        dphis=[]
        dphss=[]
        pmco2s=[]
        for ri in range(fp.n_runs):
            fpp.xvar= np.array(sr.t[ri])[:,0] # was np_time
            ed= sr.eds[ri]
            self.plot_pHipHs(ax,ed,fpp)
            #ph_ylims=(6.8,7.8)
            #ax_ph.set_ylim(ph_ylims)#0.0,0.007)


            #OLDprint(f'\nri={ri}\n')
            #np_time    = np.array(fp.run_time    [ri])[:,0]
            #np_data    = np.array(fp.run_data    [ri])
            #n_buff     =          fp.n_buffs     [ri]
            #n_in       =          fp.n_ins       [ri]
            #n_out      =          fp.n_outs      [ri]
            #N          =          fp.Ns          [ri]
            #R_cm       =          fp.Rs_cm       [ri]
            #R_inf_cm   =          fp.R_infs_cm   [ri]
            #pH_in_init =          fp.pH_in_inits [ri]
            #tf_CO2on   =          fp.tf_CO2ons   [ri]
            #Ai         =          fp.A_CAIIs     [ri]
            #As         =          fp.A_CAIVs     [ri]
            #Pm_CO2     =          fp.Pm_CO2s     [ri]

            pmco2s.append(Pm_CO2)
            breakpoint()

            # pH near the membrane
#            n1 = (1+n_buff)*N + n_in -1 # one shell below membrane; n1+1 = @membrane

            idx_tfCO2on = np.nonzero(np_time < tf_CO2on)[0][-1]
#            print(idx_tfCO2on)

#            pHs = self.pH_from_Hplus(np_data[:,n1+2])

#            depth= 50
#            electrode_idx = self.electrode_index_from_um( depth, R_cm, n_in )
#            pHi = self.pH_from_Hplus(np_data[:,n1-(n_in-electrode_idx)]) # pHi at chosen depth
            plot_t = np.insert(np_time,0,-100) # add first point to -infinity (-100)

            pHi,pHs= self.get_pH(np_data,n_buff,N,n_in,n_out,R_cm,depth_um=50)
            plot_pHi= np.insert(pHi,0,pHi[0])
            plot_pHs= np.insert(pHs,0,pHs[0])

            t_I   = np_time[ 0 : idx_tfCO2on]
            t_E   = np_time[idx_tfCO2on : -1]
            pHi_I = pHi[0 : idx_tfCO2on ]
            pHi_E = pHi[idx_tfCO2on : -1]
            pHs_I = pHs[0 : idx_tfCO2on ]
            pHs_E = pHs[idx_tfCO2on : -1]

            dpHi_dt_I, max_dpHi_dt_idx_I, max_dpHi_dt_I= self.get_ddata_dt(pHi_I, t_I)
            dpHi_dt_E, max_dpHi_dt_idx_E, max_dpHi_dt_E= self.get_ddata_dt(pHi_E, t_E)
 
            dphis.append(max_dpHi_dt_I)

            ax_phs.plot(plot_t,plot_pHs, 'g-', linewidth=3.0)
            ax_phs.plot(plot_t,plot_pHi, 'r-', linewidth=3.0)

            xI= t_I  [max_dpHi_dt_idx_I]
            yI= pHi_I[max_dpHi_dt_idx_I]
            xE= t_E  [max_dpHi_dt_idx_E]
            yE= pHi_E[max_dpHi_dt_idx_E]

            print('xI', xI, 'yI', yI, 'xE', xE, 'yE', yE)

            xIr= np.linspace(xI - 100, xI + 100, 100)
            xIr= np.linspace(xI - 100, xI + 100, 10)
            bI= yI - max_dpHi_dt_I * xI
            yIr= xIr * max_dpHi_dt_I + bI
            print('xIr=',xIr)
            print('yIr=',yIr)

            xEr= np.linspace(xE - 100, xE + 100, 100)
            xEr= np.linspace(xE - 100, xE + 100, 10)
            bE= yE - max_dpHi_dt_E * xE
            yEr= xEr * max_dpHi_dt_E + bE 
            print('xEr=',xEr)
            print('yEr=',yEr)

            ax_phs.plot( xIr, yIr, 'k--')
            ax_phs.plot( xEr, yEr, 'k--')

            max_pHs_I= max(pHs_I)
            min_pHs_I= pHs_I[0]
            del_pHs_I= max_pHs_I - min_pHs_I

            max_pHs_E= pHs_E[0]
            min_pHs_E= min(pHs_E)
            del_pHs_E= max_pHs_E - min_pHs_E
            dphss.append(del_pHs_I)

            print('del_pHs_I=',del_pHs_I, 'max=', max_pHs_I, 'min=', min_pHs_I)
            print('del_pHs_E=',del_pHs_E, 'max=', max_pHs_E, 'min=', min_pHs_E)

            ax_phs.annotate( '', xy=(xI,7.7), xytext=(xE,7.7), xycoords="data",\
                         arrowprops=dict( arrowstyle='<|-|>', connectionstyle='bar,fraction=0.1',)
                        )
            ax_phs.annotate( r'$1.5\% CO_2$' '\n' r'$10 mM HCO^-_3$', xy=((xE-xI)/2,7.7), xytext=((xE-xI)/2,7.75),ha='center', size=15 )
            xI = xI - 50 # move it over
            xE = xE - 50 # move it over

            ax_phs.annotate( r'$\Delta pH_s$     ', xy=(xI,pHs[0]                ), xytext=(xI,pHs[0]-0.03), xycoords="data", size=15, color='green')
            ax_phs.annotate( r'$(dpH_i/dt)_{max}$', xy=(xI,pHi[max_dpHi_dt_idx_I]), xytext=(xI,       7.05), xycoords="data", size=15, color='red')

            max_pHs_I = max_pHs_I + 0.01
            max_pHs_E = max_pHs_E + 0.01
            ax_phs.annotate( '%.4f'%del_pHs_I, xy=(xI,max_pHs_I), xytext=(xI,max_pHs_I), xycoords="data", size=20)
            ax_phs.annotate( '', xy=(xI,min_pHs_I), xytext=(xI,max_pHs_I), xycoords="data",
                    arrowprops={'arrowstyle':'<|-|>'})#, 'headwidth':2})#, size=20)#, color='green')

            ax_phs.annotate( '%.4f'%del_pHs_E, xy=(xE,max_pHs_E), xytext=(xE,max_pHs_E), xycoords="data", size=20)
            ax_phs.annotate( '', xy=(xE,min_pHs_E), xytext=(xE,max_pHs_E), xycoords="data",
                    arrowprops={'arrowstyle':'<|-|>'})#, 'headwidth':2})#, size=20)#, color='green')


            ax_phs.annotate( '%+.4f'%max_dpHi_dt_I, xy=(xI,yI), xytext=(xI+100,yI), xycoords="data", size=20)#, color='green')
            ax_phs.annotate( '%+.4f'%max_dpHi_dt_E, xy=(xE,yE), xytext=(xE+100,yE), xycoords="data", size=20)#, color='green')

        x=np_time[-1]
        y=pHs[-1]
        ax_phs.annotate( r'$pH_s$', xy=(x,y), xytext=(x+50,y), xycoords="data", size=20)#, color='green')
        y=pHi[-1]
        ax_phs.annotate( r'$pH_i$', xy=(x,y), xytext=(x+50,y), xycoords="data", size=20)#, color='green')

        print('\npmco2s',pmco2s)
        print('dphis',type(dphis),dphis)
        print('dphss',dphss)
        dphis= [ -v for v in dphis ]
        ax_dphi.set_xscale('log')
        ax_dphi.set_xlabel('PmCO2', size=14, style='normal')
        default_pmco2=0.03078
        ax_dphi.axvline(default_pmco2)
        #breakpoint()
        y=np.mean(dphis)
        x=default_pmco2
        print('xy=',x,y)
        ax_dphi.annotate(f'{default_pmco2}',xy=(x,y), rotation=90, xycoords="data", size=20,
            xytext=(20,0), textcoords='offset pixels')
        ax_dphi.set_ylabel('(dpHi/dt)$_{max}$', size=14, style='normal')
        ax_dphi.plot(pmco2s,dphis,linestyle='',marker='x',label='-(dphi/dt)max')
        ax_dphi.set_ylim(0.0,0.007)

        ax_dphs.set_xscale('log')
        ax_dphs.set_xlabel('PmCO2', size=14, style='normal')
        ax_dphs.axvline(default_pmco2)
        y=np.mean(dphss)
        x=default_pmco2
        print('xy=',x,y)
        ax_dphs.annotate(f'{default_pmco2}',xy=(x,y), rotation=90, xycoords="data", size=20,
            xytext=(20,0), textcoords='offset pixels')

        ax_dphs.set_ylabel('ΔpHs', size=14, style='normal')
        ax_dphs.plot(pmco2s,dphss,linestyle='',marker='x',label='dphss')
        ax_dphs.set_ylim(0.0,0.35)
        titlepart = self.run_params['PlotTitle'][0]

        ax_dphi.set_title('-(dpHi/dt)$_{max}$ %s'%titlepart, size=20)
        ax_dphs.set_title(f'ΔpHs {titlepart}', size=20)

        self.make_space_above(axs, topmargin=1)

# plot negative y
# -(dphi/dt) max
# pmco2 log scale x axis
# recreate fig 8
# larger PmCO2s

        outfile= f'{self.run_params["OutFile"][0]}.csv'.replace('/','_').replace(' ','_')
        thisdf= pd.DataFrame(
            {'dpHi'  :dphis,
             'delpHs':dphss,
            },
            index=pmco2s,
        )
        print('thisdf=',thisdf)
        thisdf.to_csv(outfile, index=True,index_label='PmO2')
        fig.savefig('ajp_dk_%s.png'%(titlepart.replace('=','_').replace(' ','_').replace('.0','')))
        plt.show()


