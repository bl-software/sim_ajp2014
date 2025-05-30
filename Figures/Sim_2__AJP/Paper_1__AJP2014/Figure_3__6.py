import numpy as np
from Figures.Sim_2__AJP.Paper_1__AJP2014.AJP2014_Figs import AJP2014_Fig

class Fig(AJP2014_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        # fp is SimFigure:FigProps
        self.fp.plot_rows=1
        self.fp.plot_cols=3
        self.fp.plot_d={ 'remborder': ['top','right']  ,
                         'tickspos' : 'bottom', }
        self.fp.title='AJP 2014 Fig 6 (New FigFactory Version)'
        self.fp.shades = self.shades_ajp6g        # WAS "shades"

        self.make_fig()
        ax_ctrl = self.axs[0,0]
        ax_caii = self.axs[0,1]
        ax_caiv = self.axs[0,2]

        titles= ['$Control$','$CA II$','$CA IV$']

        n_runs= len(sr.t)
        sr.extract( [ sr.get_pH, sr.get_dpHi_dt, sr.get_delpHs ])

        fpp=self.FigPanelProps() 
        fpp.plotkwargs={\
            'pHi':
                {'color':   'red', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'pHi' },
            'pHs':
                {'color': 'green', 'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':'pHs' }
        }
        fpp.kwargs={\
            'toplot':['pHi','pHs'],
            'annos' :['SLOPE_LINES','SLOPE_VALS', 'LABELS', 'CO2BARS', 'DELTA_ARROWS'] }

        for ri,ax in zip(range(n_runs),(ax_ctrl,ax_caii,ax_caiv)):
            fpp.xvar= np.array(sr.t[ri])[:,0] # was np_time
            ed= sr.eds[ri]
            self.plot_pHipHs(ax,ed,fpp)

            x_I= ed.max_dpHi_dt_t_I
            y_I= ed.pH_at_max_dpHi_I

            x_E= ed.max_dpHi_dt_t_E
            y_E= ed.pH_at_max_dpHi_E

            self.add_pH_IE_bar(ax, x_I, x_E, 7.75, r'$1.5\% CO_2$' '\n' r'$10 mM HCO^-_3$' )

            self.add_pHi_slopes(ax, x_I, y_I, ed.max_dpHi_dt_I, num=True )
            self.add_pHi_slopes(ax, x_E, y_E, ed.max_dpHi_dt_E, num=True )

            ymax= ed.max_pHs_I
            ymin= ed.min_pHs_I
            self.add_pHs_delta_arrow(ax, x_I, ymin, ymax, num=ed.del_pHs_I )
            ymax= ed.max_pHs_E
            ymin= ed.min_pHs_E
            self.add_pHs_delta_arrow(ax, x_E, ymin, ymax, num=ed.del_pHs_E )
        # Add labels to first panel
        ed= sr.eds[0]
        x_I= ed.max_dpHi_dt_t_I
        ax.annotate( r'$\Delta pH_s$',
            xy=(x_I,ed.pHs[0])                   , xytext=(x_I,ed.pHs[0]-0.03), xycoords="data",
            size=15, color='green')
        ax.annotate( r'$(dpH_i/dt)_{max}$',
            xy=(x_I,ed.pHi[ed.max_dpHi_dt_idx_I]), xytext=(x_I, 7.05)         , xycoords="data",
            size=15, color='red')

        self.setup_axes(ax_ctrl, 'Time (s)', r'$pH$', None, (6.8,7.8),
                **{ 'paneltate':'A', 'axtit': titles[0] })
        self.setup_axes(ax_caii, 'Time (s)',    None, None, (6.8,7.8),
                **{ 'paneltate':'B', 'axtit': titles[1] })
        self.setup_axes(ax_caiv, 'Time (s)',    None, None, (6.8,7.8),
                **{ 'paneltate':'C', 'axtit': titles[2] })

        self.fig.tight_layout()
        self.show_fig()




