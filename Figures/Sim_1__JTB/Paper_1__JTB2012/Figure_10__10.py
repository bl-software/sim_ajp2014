import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig
from mpl_toolkits.axes_grid1 import make_axes_locatable

class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows= 1,
            ncols= 2,
            title= 'JTB 2012 Fig 10: Intracellular buffering power effect',
            plot_d={ 'colors'   : (self.shades_10, self.shades_10),
                     #'remborder': ['top','right'],
                     'tickspos' : 'both', }
        )

        self.make_fig()
        axs={'pHs'   : self.axs[0,0],
             'pHi'   : self.axs[0,1],
        } 

        #Split axis for this figure
        bot_ax= axs['pHi']
        divider = make_axes_locatable(bot_ax)
        top_ax = divider.new_vertical(size="250%", pad=0.2)
        self.fig.add_axes(top_ax)
        self.fig_setaxesdefs([top_ax], self.fp.plot_d)

        paneltext= [      'A',       'B']
        xlabels  = ['Time(s)', 'Time(s)']
        ylabels  = [r'$pH_s$', r'$pH_i$' ]

        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        fpp.paneltate = paneltext[0]
        fpp.ylabel    = ylabels[0]
        fpp.xlabel    = xlabels[0]
        fpp.logx= 'linear'
        self.setup_axes( axs['pHs'], fpp )

        fpp.ylims=(6.85,7.25)
        fpp.paneltate = paneltext[1]
        fpp.ylabel    = ylabels[1]
        fpp.xlabel    = None
        self.setup_axes( top_ax, fpp )

        fpp.ylims=(4.7,5.2)
        fpp.paneltate = ' '# None
        fpp.ylabel    = ' '#None
        fpp.xlabel    = xlabels[1]
        self.setup_axes( bot_ax, fpp )

        bot_ax.spines['top'].set_visible(False)
        top_ax.spines['bottom'].set_visible(False)
        top_ax.tick_params(bottom=False,labelbottom=False)
        bot_ax.tick_params(top=False)

        d = .5  # proportion of vertical to horizontal extent of the slanted line
        kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
        top_ax.plot([0, 1], [0, 0], transform=top_ax.transAxes, **kwargs)
        bot_ax.plot([0, 1], [1, 1], transform=bot_ax.transAxes, **kwargs)

        plotkwargs={\
            'pHi': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
            'pHs': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
        }

        A1tot_ins= sr.cp['A1tot_in']()
        betaMults= [ av/27.312560103865501 for av in A1tot_ins]

        sr.extract( [ sr.get_substance, ], [('pH',),], [{},]  )

        for ri,(betaMult,) in enumerate(zip(betaMults,)):
            ed= sr.eds[ri]
            pHi= sr.get_pHi(ri,ed,depth_um=50)
            pHs= sr.get_pHs(ri,ed,depth_um=0 )

            label = f'{betaMult}' r'$ \cdot\beta_{std}$'

            fpp.xvar= np.array(sr.t[ri])[:,0]

            fpp.yvar= pHi
            fpp.plotkwargs=plotkwargs['pHi']
            self.plot_pH(bot_ax, fpp)
            self.plot_pH(top_ax, fpp)

            fpp.yvar= pHs
            fpp.plotkwargs=plotkwargs['pHs']
            fpp.plotkwargs.update({'label':label})
            self.plot_pH(axs['pHs'], fpp)

        self.set_legend(axs['pHs'])
        self.fig.tight_layout()
        self.show_fig()

