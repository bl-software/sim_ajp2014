import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig
from support import *
class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 2,
            ncols = 3,
            title = 'JTB 2012 Fig 5: Extra- and intracellular concentration-distance profiles',
            plot_d= { 'colors'   : (self.shades_345,)*6,
                      'remborder': ['top','right'],
                         #'tickspos' : 'both',
                    }
        )
        self.make_fig()

        axs={'CO2'  : self.axs[0,0], # NOTE - keys here must match solute names in ed.solutes
             'H2CO3': self.axs[0,1],
             'HCO3m': self.axs[0,2],
             'pH'   : self.axs[1,0],
             'HA'   : self.axs[1,1],
             'Am'   : self.axs[1,2]
            }

        xlims = [[0,0.075]] * 6
        #ylims = [[ 0.0, 0.6], [ 0.0,0.001696], [  0.0, 12.75], [ 6.8, 7.8], [0.0,20.0], [0.0,20.5]]
        ylims = [[0.0, None], [0.0, None], [0.0, None], [6.8, None], [0.0, None], [0.0, None]]
        paneltext= [ 'A', 'B', 'C', 'D', 'E', 'F' ]

        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        for i,(subsn,ax) in enumerate(axs.items()):
            fpp.axtitle   = rf'$\mathrm{{{sr.substances[subsn].matht}}}$'
            fpp.paneltate = paneltext[i]
            fpp.ylabel    = sr.substances[subsn].yunits
            fpp.xlabel    = 'Radius (cm)'
            fpp.plotkwargs= { 'linestyle':'-', 'linewidth':3.0, 'marker':'' }
            self.setup_axes( ax, fpp )

        times= [ 0, 0.0004, 0.034, 3.051, 150.98, 1200.0 ]
        legend_text = [ rf'$t_{{{i}}} = {{{v}}} sec$' for i,v in enumerate(times) ]

        top={}
        bot={}
        ri= 0 # only 1 run here

        radii,_,_,_= sr.radii_in_out()
        fpp.xvar= radii

        sr.extract( [sr.get_substance], [('CO2','H2CO3','HCO3m','pH','HA','Am')], [{}] )

        for timepoint,label in zip(times,legend_text):
            #sr.extract( [sr.get_solutes], [(t,)], [{'over':'radius'}] )
            ed= sr.eds[-1]
            for solname in axs.keys():
                fpp.plotkwargs['label']=label
                timeidx= np.nonzero(ed.np_time >= timepoint)[0][0]
                y= ed.substance[solname][timeidx,:]
                fpp.yvar= y
                top[solname]=max(max(y), top.get(solname,0.0))
                bot[solname]=min(min(y), bot.get(solname,np.inf))
                self.plot_t(axs[solname], fpp)

        for i,solname in enumerate(axs.keys()):
            height10=(top[solname]-bot[solname]) * 0.10
            ylims[i][1]=top[solname] + height10

        r_memb_cm = sr.cp['D']()[0]/20     # 0.065 #R_memb
        r_inf_cm  = sr.cp['D_inf']()[0]/20 # 0.075 #R_inf_cm
        for (axn,ax),xlim,ylim in zip(axs.items(),xlims,ylims):
            self.bluegreenpatch(ax,xlim,ylim,r_memb_cm,r_inf_cm,ie_anno=axn=='CO2')

            ax.set_xlim(xlim)
            ax.set_ylim(ylim)

        self.set_legend(axs['HCO3m'])
        self.show_fig()
