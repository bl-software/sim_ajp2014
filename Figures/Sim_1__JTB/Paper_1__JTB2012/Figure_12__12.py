import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig

class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 1,
            ncols = 2,
            title = 'JTB 2012 Fig 12',
            plot_d= { 'colors'   : (self.shades_12a,self.shades_12b),
                      #'remborder': ['top','right'],
                      'tickspos' : 'both', }
        )
        self.make_fig()
        axs={'pHi1'   : self.axs[0,0],
             'pHi2'   : self.axs[0,1],
        } 

        paneltext= [      'A',       'B']
        xlabels  = ['Time(s)', 'Time(s)']
        ylabels  = [r'$pH_s$', r'$pH_i$' ]
        titles   = [r'100% immobile buffer', r'90% immobile buffer']

        depths_um = [10,50,150,250,350,450,550,650]

        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        for i,ax in enumerate(axs.values()):
            fpp.paneltate = paneltext[i]
            fpp.ylabel    = ylabels[i]
            fpp.xlabel    = xlabels[i]
            fpp.axtitle   = titles[i]
            self.setup_axes( ax, fpp )

        plotkwargs={ 
            'pHi': {'linestyle':'-', 'linewidth':3.0, 'marker':'', 'label':''},
        }
        fpp.plotkwargs= plotkwargs['pHi']

        sr.extract( [ sr.get_substance, ], [('pH',),], [{},]  )

        idx90=4
        idx100=6
        for ax,ri in zip(axs.values(),[idx100,idx90]):
            ed= sr.eds[ri]
            for depth_um in depths_um:
                pHi= sr.get_pHi(ri,ed,depth_um=depth_um)

                fpp.xvar= np.array(sr.t[ri])[:,0]
                fpp.yvar= pHi
                self.plot_pH(ax, fpp)

        axs['pHi1'].annotate("", xy=( 800,7.15), xytext=(0,6.9), arrowprops=dict(arrowstyle="->"))
        axs['pHi2'].annotate("", xy=( 350,7.11), xytext=(-50,7.01), arrowprops=dict(arrowstyle="->"))
        axs['pHi2'].axvline( 400 )

        self.fig.tight_layout()
        self.show_fig()

