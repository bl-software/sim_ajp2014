from Figures.SimFigure import SimFigure
import matplotlib.patches as mpatch

class JTB2012_Fig(SimFigure):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__()

    shades_345 = [\
        ( 102/255,  51/255,       0),#  brown
        (       0,  0.5000,       0),#  green
        (  1.0000,       0,       0),#  red
        (       0,  0.7500,  0.7500),#  cyan
        (  0.7500,       0,  0.7500),#  magenta
        ( 204/255, 153/255,       0)]#  gold
    shades_6 = [\
        (       0,  0.5000,       0), # green
        (       0,       0,  1.0000), # blue
        (  1.0000,       0,       0), # red
        (       0,  0.7500,  0.7500), # cyan
        (  0.7500,       0,  0.7500), # magenta
        ( 162/255, 120/255,       0), # gold
        (  0.2500,  0.2500,  0.2500)] # black
    shades_7 = [\
        (      0,        0,       1), # blue
        (      1,     0.40,       0), # orange
        (   0.40,     0.20,       0), # brown
        (      0,     0.75,    0.75), # cyan
        (   0.75,        0,    0.75), # magenta
        ( 0.7500,   0.7500,       0), # yellow
        ( 0.2500,   0.2500,  0.2500), # black
        (   1.00,        0,       0), # red
        (      0,     0.50,       0)] # green 
    shades_8 = [\
        ( 150/255,  75/255,       0), # brown     
        (       0,  0.5000,       0), # green
        (  1.0000,       0,       0), # red
        (       0,  0.7500,  0.7500), # cyan
        (  0.7500,       0,  0.7500), # magenta
        ( 204/255, 153/255,       0), # gold
        (  0.2500,  0.2500,  0.2500)] # black
    shades_9 = [\
        (       0,  0.5000,       0), # green
        ( 204/255, 153/255,       0), # gold
        (  1.0000,       0,       0), # red
        (       0,       0,  1.0000)] # blue         
    shades_10 = [\
        (    0.75,    0   ,    0.75), # magenta
        (    0   ,    0.75,    0.75), # cyan
        (    1.00,    0   ,    0   ), # red
        (    0   ,    0   ,    1   ), # blue
        (    0   ,    0.50,    0   ), # green  
        (    0   ,    0   ,    0   )] # black
    shades_11 = [\
        ( 0      ,       0,       1), # blue
        ( 0      ,    0.50,       0), # green 
        ( 1      ,    0.40,       0), # orange
        ( 0.40   ,    0.20,       0), # brown
        ( 204/255, 153/255,       0), # gold
        ( 0      , 153/255, 204/255), # cyan
        ( 0.75   ,       0,    0.75)] # magenta
    shades_12a = [\
        ( 0      ,       0,       0), # black (10um)
        ( 0.75   ,       0,    0.75), # magenta(50um) 
        ( 70/255 ,  70/255,  70/255), # (150um)
        ( 90/255 ,  90/255,  90/255), # (250um)
        ( 110/255, 110/255, 110/255), # (350um)
        ( 130/255, 130/255, 130/255), # (450um)
        ( 160/255, 160/255, 160/255), # (550um)
        ( 190/255, 190/255, 190/255)] # (150um)       
    shades_12b = [\
        (       0,       0,       0), # black (10um)
        ( 204/255, 153/255,       0), # gold  (50um)
        ( 70/255 ,  70/255,  70/255), # (150um)
        ( 90/255 ,  90/255,  90/255), # (250um)
        ( 110/255, 110/255, 110/255), # (350um)
        ( 130/255, 130/255, 130/255), # (450um)
        ( 160/255, 160/255, 160/255), # (550um)
        ( 190/255, 190/255, 190/255)] # (150um)  

    def bluegreenpatch(self, ax, xlim, ylim, r_memb_cm, r_inf_cm, ie_anno=False):
        print('XLs',xlim)
        left= xlim[0]
        bot = ylim[0]
        top = ylim[1]
        height  = top - bot
        totwidth= r_inf_cm - left
        lwidth  = r_memb_cm - left
        rwidth  = r_inf_cm - r_memb_cm

        if ie_anno:
            midicfx= (lwidth/2) / (totwidth)
            midecfx= (r_memb_cm + rwidth/2 - left) / totwidth
            self.anno_icf_euf(ax, midicfx, midecfx)

        ax.add_patch(mpatch.Rectangle((left  ,bot), lwidth, height,facecolor=self.borongreen))
        ax.add_patch(mpatch.Rectangle((r_memb_cm,bot), rwidth, height,facecolor=self.boronblue ))

        ax.vlines(r_memb_cm, bot, bot + 0.9*height,
                  linestyle='--', color='black', linewidth=1, zorder=10)

    def anno_icf_euf(self, ax, midicfx, midecfx):
        ax.annotate('ICF', xy=(midicfx,0.95), xytext=(midicfx,0.95), xycoords="axes fraction",
                    size=20, ha='center' )
        ax.annotate('ECF', xy=(midecfx,0.95), xytext=(midecfx,0.95), xycoords="axes fraction",
                    size=20, ha='center' )
