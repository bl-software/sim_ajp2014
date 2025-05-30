from Figures.SimFigure import SimFigure
import matplotlib.pyplot as plt
import numpy as np

class AJP2014_Fig(SimFigure):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__()

    shades_ajp4 = plt.cm.bwr(    np.linspace(0.95, 0.4, 10))

    shades_ajp5g = plt.cm.Greens(np.linspace(0.8 , 0.3, 10))
    shades_ajp5r = plt.cm.bwr(   np.linspace(0.95, 0.4, 10))

    shades_ajp6g = plt.cm.Greens(np.linspace(0.8 , 0.3, 10))
    shades_ajp6r = plt.cm.bwr(   np.linspace(0.95, 0.4, 10))

    shades_ajp8o = plt.cm.YlOrRd(np.linspace(0.9 , 0.5, 10))
    shades_ajp8b = plt.cm.BuPu(  np.linspace(0.8 , 0.4, 10))


