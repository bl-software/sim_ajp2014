import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig

class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 1,
            ncols = 2,
            title = 'JTB 2012 Fig 9: CA Activity',
            plot_d= { 'colors'   : (self.shades_9,self.shades_9),
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
        for ax,pt,xlabel,ylabel in zip(axs.values(),paneltext,xlabels,ylabels):
            fpp.paneltate = pt
            fpp.ylabel    = ylabel
            fpp.xlabel    = xlabel
            fpp.logx= 'linear'
            self.setup_axes( ax, fpp )

        plotkwargs={
            'pHi': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
            'pHs': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
        }

        Ais = sr.cp['CAII_in']()
        Aos = sr.cp['CAIV_out']()

        depth=50
        sr.extract( [ sr.get_substance, ], [('pH',),], [{},]  )

        for ri,(Ai,Ao) in enumerate(zip(Ais,Aos)):
            ed= sr.eds[ri]
            pHi= sr.get_pHi(ri,ed,depth_um=50)
            pHs= sr.get_pHs(ri,ed,depth_um=0 )

            try:
                label_extra = {\
                    (1,1)  : '\ \ (No CA)',
                    (20,20): '\ \ (Std Exp)',
                }[ (Ai, Ao) ]
            except KeyError:
                label_extra = ''
            label = r'$A_i=%s\ \ A_o=%s %s$'%(f'{Ai:10}',f'{Ao:10}',label_extra)

            fpp.xvar= np.array(sr.t[ri])[:,0]

            fpp.yvar= pHs
            fpp.plotkwargs=plotkwargs['pHs']
            fpp.plotkwargs.update({'label':label})
            self.plot_pH(axs['pHs'], fpp)

            fpp.yvar= pHi
            self.plot_pH(axs['pHi'], fpp)

        self.set_legend(axs['pHs'])
        self.fig.tight_layout()
        self.show_fig()
