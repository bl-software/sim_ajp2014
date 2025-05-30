from Figures.Sim_2__AJP.Paper_1__AJP2014.AJP2014_Figs import AJP2014_Fig

class Fig(AJP2014_Fig):
    def __init__(self,run_time,run_data,run_params,*args,**kwargs):
        super().__init__(run_time,run_data,run_params,'5',args,kwargs)

#    def fig__AJP_fig_8(self, fignum, rp):
        print('rp=',rp)
        plot_rows=1
        plot_cols=3
        b= self.shades_ajp8o
        o= self.shades_ajp8b
        plot_d={ 'colors'   : (b,b,b,o,o,o),#fp.shades,
                 'remborder': []  ,
                 'tickspos' : 'both', }

        try:
            panel=rp['Panel'][0]
            title='AJP 2014 Fig 8 {panel}'
        except KeyError:# for Fig 13 this is like panels 'AB'
            panel='AB'
            title='AJP 2014 Fig 13'

        fig,axs = self.fig_makefig(plot_rows, plot_cols, size=None, title=title, plot_d=plot_d )
        plotax=axs[0,0]
        dphiax=axs[0,1]
        deltax=axs[0,2]
#AJP 8
        Ais=[]
        Ass=[]
        dpHi_dts=[]
        delta_pHss=[]
        n_runs= len(self.run_time)
        for ri in range(n_runs):
            t       = self.run_time              [ri]
            X       = self.run_data              [ri]
            D       = self.run_params['D']       [ri]
            D_inf   = self.run_params['D_inf']   [ri]
            n_in    = self.run_params['n_in']    [ri]
            n_out   = self.run_params['n_out']   [ri]
            n_buff  = self.run_params['n_buff']  [ri]
            tf_CO2on= self.run_params['tf_CO2on'][ri]
            Ai      = self.run_params['CAII_in']  [ri]
            As      = self.run_params['CAIV_out']  [ri]

            idx_tfCO2on = np.nonzero(t < tf_CO2on)[0][-1]
#            print(idx_tfCO2on)
            N= n_in + n_out + 1
            R_cm= (D/10) / 2
            R_inf_cm= (D_inf/10) / 2

            pHi,pHs= self.get_pH(X,n_buff,N,n_in,n_out,R_cm,depth_um=50)
            t_I   = t[ 0 : idx_tfCO2on]    # INFLUX ???
            t_E   = t[idx_tfCO2on : -1]    # EFFLUX ???
            pHi_I = pHi[0 : idx_tfCO2on ]
            pHi_E = pHi[idx_tfCO2on : -1]
            pHs_I = pHs[0 : idx_tfCO2on ]
            pHs_E = pHs[idx_tfCO2on : -1]

            dpHi_dt_I, max_dpHi_dt_idx_I, max_dpHi_dt_I= self.get_ddata_dt(pHi_I, t_I)
            dpHi_dt_E, max_dpHi_dt_idx_E, max_dpHi_dt_E= self.get_ddata_dt(pHi_E, t_E)

            Ass.append(As)
            Ais.append(Ai)
            dpHi_dts.append(max_dpHi_dt_I)
            #dpHi_dts.append(max_dpHi_dt_E)

            plot_t = np.insert(t,0,-100) # add first point to -infinity (-100)
            plot_pHi= np.insert(pHi,0,pHi[0])
            plot_pHs= np.insert(pHs,0,pHs[0])
            
            plotax.plot(plot_t,plot_pHs, 'g-', linewidth=3.0)
            plotax.plot(plot_t,plot_pHi, 'r-', linewidth=3.0)

            # Tangent lines at max dphi 
            xI= t_I  [max_dpHi_dt_idx_I]
            yI= pHi_I[max_dpHi_dt_idx_I]
            xE= t_E  [max_dpHi_dt_idx_E]
            yE= pHi_E[max_dpHi_dt_idx_E]

            #print('xI', xI, 'yI', yI, 'xE', xE, 'yE', yE)

            xIr= np.linspace(xI - 100, xI + 100, 100)
            xIr= np.linspace(xI - 100, xI + 100, 10)
            bI= yI - max_dpHi_dt_I * xI
            yIr= xIr * max_dpHi_dt_I + bI
            #print('xIr=',xIr)
            #print('yIr=',yIr)

            xEr= np.linspace(xE - 100, xE + 100, 100)
            xEr= np.linspace(xE - 100, xE + 100, 10)
            bE= yE - max_dpHi_dt_E * xE
            yEr= xEr * max_dpHi_dt_E + bE 
            #print('xEr=',xEr)
            #print('yEr=',yEr)

            plotax.plot( xIr, yIr, 'k--')
            plotax.plot( xEr, yEr, 'k--')
            
            # Delta pHs
            max_pHs_I= max(pHs_I)
            min_pHs_I= pHs_I[0]
            del_pHs_I= max_pHs_I - min_pHs_I

            max_pHs_E= pHs_E[0]
            min_pHs_E= min(pHs_E)
            del_pHs_E= max_pHs_E - min_pHs_E

            delta_pHss.append(del_pHs_I)
            #delta_pHss.append(del_pHs_E)
            print('del_pHs_I=',del_pHs_I, 'max=', max_pHs_I, 'min=', min_pHs_I)
            print('del_pHs_E=',del_pHs_E, 'max=', max_pHs_E, 'min=', min_pHs_E)


        print('delts:',delta_pHss)
        print('dhpis:',dpHi_dts)
        print('Ais:',Ais)
        print('Ass:',Ass)
        plot_dpHi_dts= [-v for v in dpHi_dts]
        print(panel)
        if panel == 'AB':
            figprops={\
                  150.0: ("D", 'black'     ), # Diamond
                 1000.0: ("D", 'darkblue'  ), # Diamond
                 5000.0: ("o", 'blue'      ), # circle
                10000.0: ("s", 'grey'      ), # square
                25000.0: ("^", 'lightblue' ), # triangle up
                50000.0: ("x", 'black'     ), # X
            }
            xset= set(Ais)
            lxs = len(xset)
            nplots= len(set(Ass))
            print('npls=',nplots)
            for i in range(nplots):
                s=i*lxs
                e=s+lxs
                print(s,e)
                startas= Ass[s]
                fp=figprops[startas]
                pkwargs={   'label':f'As={startas}',
                            'marker':fp[0],  'markersize':10,
                            'color':fp[1], 'linestyle':'',
                        }
                dphiax.plot( Ais[s:e], plot_dpHi_dts[s:e], **pkwargs )
                deltax.plot( Ais[s:e], delta_pHss[s:e]   , **pkwargs )

        elif panel == 'CD':
            figprops={\
                    5.0: ("D", 'saddlebrown' ), # Diamond
                   20.0: ("D", 'darkred'   ), # Diamond
                   40.0: ("o", 'red'       ), # circle
                  100.0: ("s", 'darkorange'    ), # square
                 1000.0: ("^", 'gold'    ), # triangle up
                10000.0: ("x", 'black'     ), # X
            }
            xset= set(Ass)
            lxs = len(xset)
            nplots= len(set(Ais))
            print('npls=',nplots)
            for i in range(nplots):
                s=i*lxs
                e=s+lxs
                print(s,e)
                startai= Ais[s]
                fp=figprops[startai]
                pkwargs={   'label':f'Ai={startai}',
                            'marker':fp[0],  'markersize':10,
                            'color':fp[1], 'linestyle':'',
                        }
                dphiax.plot( Ass[s:e], plot_dpHi_dts[s:e], **pkwargs )
                deltax.plot( Ass[s:e], delta_pHss[s:e]   , **pkwargs )

        dphiax.set_title(f'dpHi/dt')
        deltax.set_title(f'delta pHi')
        dphiax.legend()
        deltax.legend()

        dphiax.set_ylim(0.0,0.007)
        deltax.set_ylim(0.0,0.35)
        dphiax.set_xscale('log')
        deltax.set_xscale('log')

        plotax.annotate( panel, xy=(0.0, 0.0), xytext=(-0.05,1.05), xycoords="axes fraction", size=20)

        plt.show()


