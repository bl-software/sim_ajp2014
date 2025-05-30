import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig

class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 2,
            ncols = 3,
            title = 'JTB 2012 Fig 4: Intracellular concentration-time profiles',
            plot_d={ 'colors'   : (self.shades_345,)*6,
                         'remborder': ['top','right'],
                         #'tickspos' : 'both',
                       }
        )
        self.make_fig()

        axs={'CO2'  : self.axs[0,0],
             'H2CO3': self.axs[0,1],
             'HCO3m': self.axs[0,2],
             'pH'   : self.axs[1,0],
             'HA'   : self.axs[1,1],
             'Am'   : self.axs[1,2]
            }

        shell_depths_um= [8, 160, 320, 480, 640, 650]
        legend_text= [ rf'$r \approx {{{v}}}\ \mu m$' for v in shell_depths_um] # ex: r'$r = 670\ \mu m$',
#                     ]
        xlims = [[None,1200], [None,  1200], [ None,1200], [None,1200], [None,1200], [None,1200]]
        ylims = [[ 0.0, 0.5], [ 0.0,0.0015], [  0.0, 3.5], [ 7.0, 7.2], [12.0,15.5], [12.0,15.5]]
        paneltext= [ 'A', 'B', 'C', 'D', 'E', 'F' ]

        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        for i,(subsn,ax) in enumerate(axs.items()):
            fpp.axtitle   = rf'$\mathrm{{{sr.substances[subsn].matht}}}$'
            fpp.paneltate = paneltext[i]
            fpp.ylabel    = sr.substances[subsn].yunits
            fpp.xlabel    = 'Time (s)'
            fpp.plotkwargs= { 'linestyle':'-', 'linewidth':3.0, 'marker':'' }
            self.setup_axes( ax, fpp )

        #plotkwargs={\  # all same so...
        #    'CO2'  : { 'linestyle':'-', 'linewidth':3.0, 'marker':'' },
        #    'H2CO3': { 'linestyle':'-', 'linewidth':3.0, 'marker':'' },
        #    'HCO3m': { 'linestyle':'-', 'linewidth':3.0, 'marker':'' },
        #    'pH'   : { 'linestyle':'-', 'linewidth':3.0, 'marker':'' },
        #    'HA'   : { 'linestyle':'-', 'linewidth':3.0, 'marker':'' },
        #    'Am'   : { 'linestyle':'-', 'linewidth':3.0, 'marker':'' },
        #}

        sr.extract( [sr.get_substance], [('CO2','H2CO3','HCO3m','pH','HA','Am')], [{}] )
        ri=0 # only 1 in this figure
        x= np.array(sr.t[ri])[:,0]
        fpp.xvar= np.insert(x, 0, -100) # add origin extension
        for shell_depth_um,label in zip(shell_depths_um,legend_text):
            ed= sr.eds[-1]
            shell_depth_idx= sr.index_from_R_um(ri,shell_depth_um)
            for substn in ed.substance.keys():
                y= ed.substance[substn][:,shell_depth_idx]
                fpp.plotkwargs['label']=label
                fpp.yvar= np.insert(y, 0, y[0]) # add origin extension
                self.plot_t(axs[substn], fpp)

        for (soln,ax),xl,yl in zip(axs.items(),xlims,ylims):
            ax.set_xlim(xl)
            ax.set_ylim(yl)

        self.set_legend(axs['CO2'])
        self.show_fig()

