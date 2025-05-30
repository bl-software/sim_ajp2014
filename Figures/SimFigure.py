import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import numpy as np
import pandas as pd
from support import *

class SimFigure():
    ''' sim_results = simultation run output results and params '''
#    shades_ajp4 = plt.cm.bwr(np.linspace(0.6, 0.95, 10))
    boronblue  = (178/255, 220/255,     1.0)
    borongreen = (169/255, 207/255, 161/255)

    class FigProps():
        def __init__(self,nrows,ncols,title,plot_d):
            self.plot_rows=nrows
            self.plot_cols=ncols
            self.title= title
            self.plot_d= plot_d

    class FigPanelProps():
        def __init__(self):
            pass

    def __init__(self):#self, figid, sim_results, sim_figprops):
        pass
    #self.fp=self.FigProps() 
    #def __init__(self, figid, sim_results, sim_figprops):
    #    self.figid= figid
    #    self.sr= sim_results
    def show_fig(self):
        plt.show()

    def make_fig(self,n=1,hs=[],ws=[]):
        self.figaxpairs=[]
        for i in range(n):
            try:
                h=hs[i]
            except IndexError:
                h=8*self.fp.plot_rows
            try:
                w=ws[i]
            except IndexError:
                w=8*self.fp.plot_cols

            fig,axs =\
                self.fig_makefig(self.fp.plot_rows, self.fp.plot_cols,
                        size=(w,h), title=self.fp.title, plot_d=self.fp.plot_d )
            self.figaxpairs.append((fig,axs))
        self.fig,self.axs=self.figaxpairs[-1]

    def fig_makefig(self, nr=1, nc=1, size=None, title='', plot_d={} ): # SimFigure
        ''' size = tuple (x,y) '''
        if not size:
            size=(8*nc,5*nr)
        fig, axs=plt.subplots(nr,nc,squeeze=0,figsize=size)
        #if nr == 1:
        #    plt.subplots_adjust( left=0.1, right=0.92, top=0.92, bottom=0.08, hspace=0.3, wspace=0.4)
        #if nr == 2:
        #    plt.subplots_adjust( left=0.1, right=0.92, top=0.92, bottom=0.08, hspace=0.4, wspace=0.4)
        plt.subplots_adjust( left=0.1, right=0.92, top=0.9, bottom=0.08, hspace=0.4, wspace=0.4)

        #fig.suptitle(rf'$\mathrm{{{title}}}$', size=20, style='normal')
        title=title.replace(' ','\ ')
        titlelines=title.split('\n')
        title= "\n".join([rf'$\mathrm{{{tl}}}$' for tl in titlelines])
        fig.suptitle(title, size=20, style='normal')
        #fig.suptitle(rf'$\mathrm{{{title}}}$', size=20, style='normal')

        self.fig_setaxesdefs(fig.axes, plot_d)
        
        return fig,axs

    def fig_setaxesdefs(self,axs_1d,plot_d={},prop_d={}): # SimFigure
        ''' axs single list of axs - note fig.axes provides 1d list
            prop_d is dict of props
        '''
        fmtr= ScalarFormatter(useOffset=True,useMathText=True)# '%.4f' )
        fmtr.set_powerlimits((-4,4))

        for figpan,ax in enumerate(axs_1d):
            ax.tick_params( direction='in', width=2.0)
            ax.yaxis.set_tick_params(labelsize=20) # 2 ways to set label size
            ax.xaxis.set_tick_params(labelsize=20) # 2 ways to set label size
            try:
                ax.xaxis.set_ticks_position(plot_d['tickspos']) # 2 ways to set label size
            except KeyError: pass

            ax.yaxis.set_major_formatter(fmtr)
            ax.yaxis.offsetText.set_fontsize(20)

            try:
                ax.set_prop_cycle(color=plot_d['colors'][figpan])
            except KeyError:
                ax.set_prop_cycle(color=self.shades)

            bs = [ "bottom", "left", "top", "right" ]
            try:
                rembs= plot_d['remborder']
                for remb in rembs:
                    ax.spines[remb].set_visible(False)
                    bs.remove(remb)
                for b in bs:
                    ax.spines[b].set_linewidth(2.0)
            except KeyError:
                pass

            ## 2nd
            #if prop_d:
            #    ax.update( prop_d )

    def setup_axes(self, ax, fpp):#xl, yl, xlims, ylims, **kwargs ):
        try:
            ax.set_xlim(fpp.xlims[0],fpp.xlims[1])
        except AttributeError:
            pass
        try:
            ax.set_ylim(fpp.ylims[0],fpp.ylims[1])
        except AttributeError:
            pass

        try:
            ax.set_xscale( fpp.logx )
        except AttributeError:
            pass
        try:
            ax.set_yscale( fpp.logy )
        except AttributeError:
            pass

        try:
            ax.set_xlabel(fpp.xlabel, size=20, style='normal')
        except AttributeError:
            pass
        try:
            ax.set_ylabel(fpp.ylabel, size=20, style='normal')
        except AttributeError:
            pass

        try:
            ax.set_title(fpp.axtitle, y=1.00, size=25, fontweight=550, fontstyle='italic')
        except AttributeError:
            pass
        
        try:
            ax.annotate( fpp.paneltate, xy=(0.0, 0.0), xytext=(0.01,1.05), xycoords="axes fraction", size=20)
        except AttributeError:
            pass

    def set_legend(self, ax, extra_leg_props={}):
        leg_props = { 'loc'       : 'best',
                      'framealpha': 0.5,
                      'edgecolor' : (0,0,0),
                      'linewidth' : (2.0),
                      'fontsize'  : 15,
                    }
        # update w/ custom params
        leg_props.update( extra_leg_props )

        # Remove non keywords
        leglinewidth= leg_props.pop('linewidth')

        legend=ax.legend( **leg_props )

        #legend.set_title()
        for l in legend.get_lines():
            l.set_linewidth(leglinewidth)


    def plot_dpHidt(self, ax, fpp): # SimFigure
        fpp.ylabel=r'-(dpHi/dt)$_{max}$' # _subscript mathml
        self.plot_dpH(ax, fpp)

    def plot_delpHs(self, ax, fpp): # SimFigure
        fpp.ylabel='ΔpHs'
        self.plot_dpH(ax, fpp)

    def plot_dpH(self, ax, fpp):
        ax.plot(fpp.xvar,fpp.yvar,**fpp.plotkwargs)

    def plot_t(self, ax, fpp):
        ax.plot(fpp.xvar, fpp.yvar, **fpp.plotkwargs)

    def add_pH_IE_bar(self, ax, x1,x2, y, text):
            # TODO this probably not generic enough - maybe need func - 
            #bar_y= 7.75
            ax.annotate( '',
                        #xy=(x_I,bar_y)        , xytext=(x_E,bar_y), xycoords="data",
                        xy=(x1,y)        , xytext=(x2,y), xycoords="data",
                        arrowprops=dict( arrowstyle='<|-|>', connectionstyle='bar,fraction=0.1'))
            ax.annotate(text,# r'$1.5\% CO_2$' '\n' r'$10 mM HCO^-_3$',
                        #xy=((x_E-x_I)/2,bar_y), xytext=(0,35),#((x_E-x_I)/2,bar_y+0.25),
                        xy=((x2-x1)/2,y), xytext=(0,35), textcoords='offset pixels',
                        ha='center', size=15 )

    def add_pHi_slopes(self, ax, x, y, m, num=None ):
        def xy_slopes(x,y,m):
            b= y - m * x
            xs= np.linspace(x-100, x+100, 10)
            ys= xs * m + b
            return xs,ys
        ax.plot( *xy_slopes(x,y,m), 'k--' )

        if num:
            # dpHidt values
            ax.annotate( '%+.4f'%m, xy=(x,y), xytext=(x+100,y), xycoords="data", size=20)#, color='green')

    def add_pHs_delta_arrow(self, ax, x, ymin, ymax, num=None ):
        if num:
            ax.annotate( '%.4f'%num,
                        xy=(x,ymax)        , xytext=(-20,5)   , xycoords="data",
                        textcoords='offset pixels', size=20)
        ax.annotate( '',
                    xy=(x,ymin), xytext=(x,ymax), xycoords="data",
                    arrowprops={'arrowstyle':'<|-|>'})

    def plot_pH(self,ax,fpp,extendstart=True): # SimFigure
        ''' d= single data line to plot '''
        # Extend plot to zero point of graph
        if extendstart:
            plot_t = np.insert(fpp.xvar,0,-100) # add first point to -infinity (-100)
            plot_pH= np.insert(fpp.yvar,0,fpp.yvar[0])
        else:
            plot_t = fpp.xvar
            plot_pH= fpp.yvar
        
        ax.plot(plot_t,plot_pH, **fpp.plotkwargs )

    def make_pretty(self,ax,): # SimFigure
        x=np_time[-1]
        y=pHs[-1]
        ax_phs.annotate( r'$pH_s$', xy=(x,y), xytext=(x+50,y), xycoords="data", size=20)#, color='green')
        y=pHi[-1]
        ax_phs.annotate( r'$pH_i$', xy=(x,y), xytext=(x+50,y), xycoords="data", size=20)#, color='green')

        self.make_space_above(axs, topmargin=1)

    def make_space_above(self, axes, topmargin=1):
        """ increase figure size to make topmargin (in inches) space for 
            titles, without changing the axes sizes"""
        fig = axes.flatten()[0].figure
        s = fig.subplotpars
        #print(s.top)
        w, h = fig.get_size_inches()
        #print(w,h)
        figh = h - (1-s.top)*h  + topmargin
        print('make_space_above',figh)
        #figh=7.0
        fig.subplots_adjust(bottom=s.bottom*h/figh, top=1-topmargin/figh)
        fig.set_figheight(figh)



