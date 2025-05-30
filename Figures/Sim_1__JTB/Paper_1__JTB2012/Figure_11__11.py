import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig

class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 1,
            ncols = 2,
            title = 'JTB 2012 Fig 11: Fraction of total buffer that is immobile ([TA_2]_i)',
            plot_d= { 'colors'   : (self.shades_11,self.shades_11),
                      #'remborder': ['top','right'],
                      'tickspos' : 'both', }
        )
        self.make_fig()
        axs={'pHs'   : self.axs[0,0],
             'pHi'   : self.axs[0,1],
        } 

        paneltext= [      'A',       'B']
        xlabels  = ['Time(s)', 'Time(s)']
        ylabels  = [r'$pH_s$', r'$pH_i$' ]

        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        for i,ax in enumerate(axs.values()):
            fpp.paneltate = paneltext[i]
            fpp.ylabel    = ylabels[i]
            fpp.xlabel    = xlabels[i]
            #fpp.logx= 'linear'
            self.setup_axes( ax, fpp )

        plotkwargs={ 
            'pHi': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
            'pHs': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
        }

        Buff_pcs= sr.cp['Buff_pc']()

        sr.extract( [ sr.get_substance, ], [('pH',),], [{},]  )

        for ri,(Buff_pc,) in enumerate(zip(Buff_pcs,)):
            ed= sr.eds[ri]
            pHi= sr.get_pHi(ri,ed,depth_um=50)
            pHs= sr.get_pHs(ri,ed,depth_um=0 )

            label = f'{Buff_pc}%'

            fpp.xvar= np.array(sr.t[ri])[:,0]

            fpp.plotkwargs=plotkwargs['pHi']
            fpp.yvar= pHi
            self.plot_pH(axs['pHi'], fpp)

            fpp.plotkwargs=plotkwargs['pHs']
            fpp.plotkwargs.update({'label':label})
            fpp.yvar= pHs
            self.plot_pH(axs['pHs'], fpp)

        axs['pHs'].annotate("", xy=( 25,7.5025), xytext=(200,7.5035), arrowprops=dict(arrowstyle="->"))
        axs['pHs'].annotate("", xy=(600,7.5010), xytext=(420,7.49985), arrowprops=dict(arrowstyle="->"))
        axs['pHi'].annotate("", xy=(0,7.05), xytext=(200,7.075), arrowprops=dict(arrowstyle="->"))

        self.set_legend(axs['pHs'])
        self.fig.tight_layout()
        self.show_fig()

