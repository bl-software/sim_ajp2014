import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig
from support import *

class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 1,
            ncols = 2,
            title = 'JTB 2012 Fig 8: CO_2 profile',
            plot_d= { 'colors'   : (self.shades_8,self.shades_8),
                      'remborder': ['top','right'],
                      #'tickspos' : 'both',
                    }
        )
        self.make_fig()

        axs={'A': self.axs[0,0],
             'B': self.axs[0,1], }

        xlims = [[0.055,0.075]] * 2#self.fp.nr * self.fp.nc
        ylims = [[0.0  , None]] * 2#self.fp.nr * self.fp.nc
        paneltext= [ 'A', 'B' ]
        titles=[ r'$CO_2\ @\ P_{M,CO_{2}} = 34.20 cm/s$',
                 r'$CO_2\ @\ P_{M,CO_{2}} = 0.00342 cm/s$' ]

        times= [ 0, 0.01, 0.25, 5.0, 35.0, 200.0, 1200.0 ]
        legend_text = [ rf'$t_{{{i}}} = {{{v}}} sec$' for i,v in enumerate(times) ]

        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        for i,ax in enumerate(axs.values()):
            fpp.axtitle   = titles[i]
            fpp.paneltate = paneltext[i]
            fpp.ylabel    = 'Concentration (mM)'
            fpp.xlabel    = 'Radius (cm)'
            fpp.plotkwargs= { 'linestyle':'-', 'linewidth':3.0, 'marker':'' }
            self.setup_axes( ax, fpp )


        top={}
        bot={}

        radii,_,_,_= sr.radii_in_out()
        fpp.xvar= radii
        # simpler to plot it all and set veiw bounds

        sr.extract( [ sr.get_substance, ], [('CO2',),], [{},] )
        for ri,ax in zip([0,4],axs.values()): # 0:pmco2=34.2  4:pmco2=/10^4
            #breakpoint()
            ed= sr.eds[ri]#ti*sr.n_runs+ri]

            for timepoint,label in zip(times,legend_text):
                timeidx= np.nonzero(ed.np_time >= timepoint)[0][0]
                co2= ed.substance['CO2'][timeidx]

                fpp.plotkwargs['label']=label
                y= co2
                top[ax]=max(max(y),top.get(ax,0.0))
                bot[ax]=min(min(y),bot.get(ax,np.inf))
                fpp.yvar= y
                self.plot_t(ax, fpp)

        for i,ax in enumerate(axs.values()):
            height10=(top[ax]-bot[ax]) * 0.10
            ylims[i][1]=top[ax] + height10

        r_memb_cm = sr.cp['D']()[0]/20     # 0.065 #R_memb
        r_inf_cm  = sr.cp['D_inf']()[0]/20 # 0.075 #R_inf_cm
        for (axn,ax),xlim,ylim in zip(axs.items(),xlims,ylims):
            self.bluegreenpatch(ax,xlim,ylim,r_memb_cm,r_inf_cm,ie_anno=True)

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

        self.set_legend(axs['B'])
        self.show_fig()
