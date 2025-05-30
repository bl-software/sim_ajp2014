import numpy as np
import matplotlib as mpl
from Figures.Sim_2__AJP.Paper_1__AJP2014.AJP2014_Figs import AJP2014_Fig

class Fig(AJP2014_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results
        
        sweepvarname= sr.get_run_var(-1, 'SweepVar')[0] # 'tort_gamma', 'Pm_O2'
        sweepvars= sr.rp[sweepvarname]                  # List of values swept over [ 0.01, 0.012, .... ]
        xlabel= sr.cp[sweepvarname].human_name          # 'Tort Lambda Vesicles (1/𝜆)'
        titlerunpart = sr.get_run_var(0, 'PlotTitle')   # 'Ai=[40.0] As=[10000.0] λs(ves) γ[np.float64(1.0)](vitmem)'

        # fp is SimFigure:FigProps
        self.fp.plot_rows=2
        self.fp.plot_cols=3
        self.fp.plot_d={ 'remborder': ['top','right']  ,
                         'tickspos' : 'bottom', }
        self.fp.title=f'AJP Gen Sweep {xlabel}'
        self.fp.shades = self.shades_ajp6g        # WAS "shades"

        self.make_fig()
        if sweepvarname == 'Pm_CO2_input':
            logx=True
        elif sweepvarname in ['oos_tort_lambda', 'tort_gamma']:
            logx=False
            ax_ph     = self.axs[0,0]
            ax_dphidt = self.axs[0,1]
            ax_delphs = self.axs[1,1]
            ax_tdelayphi = self.axs[0,2]
            ax_ttpeakphs = self.axs[1,2]

        n_runs= len(sr.t)
        sr.extract( [ sr.get_pH, sr.get_dpHi_dt, sr.get_delpHs ])

        for ri in range(n_runs):
            if sweepvarname == 'Pm_CO2_input':
                pass

            elif sweepvarname in ['oos_tort_lambda', 'tort_gamma']:
                fpp=self.FigPanelProps() 
                fpp.plotkwargs={\
                    'pHi':
                        {'color':   'red', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'pHi' },
                    'pHs':
                        {'color': 'green', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'pHs' },
                    'dpHi':
                        {'color': 'red', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':f'-dphi/dt\n{titlerunpart}' },
                    'dpHs':
                        {'color': 'green', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'ΔpHs' },
                }
                fpp.kwargs={ 'toplot':['pHi','pHs', 'dpHi', 'dpHs'], }


                fpp.xvar= np.array(sr.t[ri])[:,0] # was np_time
                ed= sr.eds[ri]
                self.plot_pHipHs(ax_ph,ed,fpp)
                #ph_ylims=(6.8,7.8)
                #ax_ph.set_ylim(ph_ylims)#0.0,0.007)

                x_I= ed.max_dpHi_dt_t_I
                y_I= ed.pH_at_max_dpHi_I

                x_E= ed.max_dpHi_dt_t_E
                y_E= ed.pH_at_max_dpHi_E
                self.add_pH_IE_bar(ax_ph, x_I, x_E, 7.75, r'$1.5\% CO_2$' '\n' r'$10 mM HCO^-_3$' )
                self.add_pHi_slopes(ax_ph, x_I, y_I, ed.max_dpHi_dt_I, num=True )
                self.add_pHi_slopes(ax_ph, x_E, y_E, ed.max_dpHi_dt_E, num=True )


        fpp1=self.FigPanelProps() 
        fpp1.title=f'-dphi/dt\n{titlerunpart}'
        fpp1.xvar= sweepvars
        fpp1.logx= logx
        # negate for plot
        fpp1.yvar= dphidts= [ -ed.max_dpHi_dt_I for ed in sr.eds ]
        fpp1.xlabel=xlabel
        fpp1.plotkwargs={ 'color': 'red', 'linestyle':'-', 'marker':'o',
                'label':'-(dphi/dt)max' }
        self.plot_dpHidt(ax_dphidt,fpp1)

        fpp2=self.FigPanelProps() 
        fpp2.title=f'ΔpHs\n{titlerunpart}'
        fpp2.xvar= sweepvars
        fpp2.logx= logx
        fpp2.yvar= delphss= [ ed.del_pHs_I for ed in sr.eds ]
        fpp2.xlabel=xlabel
        fpp2.plotkwargs={ 'color': 'green', 'linestyle':'-', 'marker':'o',
                'label':'ΔpHs' }
        self.plot_delpHs(ax_delphs, fpp2)

        fpp4=self.FigPanelProps() 
        fpp4.title=f'TimeDelay pHi (I)\n{titlerunpart}'
        fpp4.xvar= sweepvars
        fpp4.logx= logx
        # negate for plot
        fpp4.yvar= delays= [ -ed.time_delay_pHi for ed in sr.eds ]
        fpp4.xlabel=xlabel
        fpp4.ylabel='delay (s)'
        fpp4.plotkwargs={ 'color': 'blue', 'linestyle':'-', 'marker':'o',
                'label':'TimeDelay (s)' }
        self.plot_t(ax_tdelayphi,fpp4)
        ax_tdelayphi.legend()

        tds= { 'CTRL and CAII':( 9.0, 0.0, 'grey'  ),
             #  'caii':( 9.0, 0.0, 'purple'),
             #  'caiv':( 9.0, 0.0, 'green' ),
        }
        for k, (y,yd,color) in tds.items():
            ax_tdelayphi.fill_between( fpp4.xvar, y-yd, y+yd, color=color,alpha=0.2)
            ax_tdelayphi.annotate(f'Paper {k} td= {y}±{yd}', color=color,
                    xy=(fpp4.xvar[-1],y), xycoords="data", size=14,
                    xytext=(-220,0), textcoords='offset pixels')

        fpp5=self.FigPanelProps() 
        fpp5.title=f'TimeToPeak pHs (I)\n{titlerunpart}'
        fpp5.xvar= sweepvars
        fpp5.logx= logx
        # negate for plot
        fpp5.yvar= delays= [ ed.time_to_peak_pHs for ed in sr.eds ]
        fpp5.xlabel=xlabel
        fpp5.ylabel='time to peak (s)'
        fpp5.plotkwargs={ 'color': 'orange', 'linestyle':'-', 'marker':'o',
                'label':'TimeToPeak (s)' }
        self.plot_t(ax_ttpeakphs,fpp5)
        ax_ttpeakphs.legend()
       
        ttps= { 'CTRL':(11.2, 3.7, 'grey'  ),
                'CAII':( 7.6, 2.7, 'purple'),
                'CAIV':( 6.5, 0.8, 'green' ),
        }
        for k, (y,yd,color) in ttps.items():
            ax_ttpeakphs.fill_between( fpp5.xvar, y-yd, y+yd, color=color,alpha=0.2)
            ax_ttpeakphs.annotate(f'Paper {k} tp= {y}±{yd}', color=color,
                    xy=(fpp5.xvar[-1],y), xycoords="data", size=14,
                    xytext=(-220,0), textcoords='offset pixels')


        dphidt_ylims=(0.0,0.007)
        ax_dphidt.set_ylim(dphidt_ylims)#0.0,0.007)

        delphs_ylims=(0.0,0.5)
        ax_delphs.set_ylim(delphs_ylims)

#sim was stuck on 0.03
#fix figs first


        for v,n,c in ((0.0012,'Raif','blue'),
                      (0.0009,'DK','green')):
            x=fpp2.xvar[-1]
            ax_dphidt.axhline(v,color=c, alpha=0.5)
            ax_dphidt.annotate(f'{n}= {v}', color=c,
                    xy=(x,v), xycoords="data", size=14,
                    xytext=(20,0), textcoords='offset pixels')

        if sweepvarname == 'Pm_CO2_input':
            pmco2h2o=0.00342

            ax_dphidt.axvline(pmco2h2o)
            y=(dphidt_ylims[1]-dphidt_ylims[0])*0.25
            x=pmco2h2o
            ax_dphidt.annotate(f'PmCO2H2O= {pmco2h2o}',
                    xy=(x,y), rotation=90, xycoords="data", size=14,
                    xytext=(20,0), textcoords='offset pixels')

            ax_delphs.axvline(pmco2h2o)
            y=(delphs_ylims[1]-delphs_ylims[0])*0.25
            x=pmco2h2o
            ax_delphs.annotate(f'PmCO2H2O= {pmco2h2o}',
                    xy=(x,y), rotation=90, xycoords="data", size=14,
                    xytext=(20,0), textcoords='offset pixels')


        self.fig.tight_layout()

        outfilebase= f'{sr.rp["OutFile"][0]}'.replace('/','_').replace(' ','_')
        outcol= f'{sr.rp["OutCol"][0]}'.replace('/','_').replace(' ','_')

        sr.make_output(f'{outfilebase}.csv',outcol,sweepvars,
                         {'dphidt':fpp1.yvar,
                          'delphs':fpp2.yvar,
                          'tdphi' :fpp4.yvar,
                          'ttpphs':fpp5.yvar})

        self.fig.savefig(f'{outfilebase}.png')

        self.show_fig()


