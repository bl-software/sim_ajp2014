#!/usr/bin/python
'''Copyright 2012 Dale Huffman'''

import wx
import numpy as np

class ColChangeInput( wx.TextCtrl ):
    '''A TextCtrl that changes color on modify and resets on Enter'''
    def __init__(self, parent, id, cci_def_text='', cci_size=(-1,-1), on_enter_func=None, j=None, *args, **kwargs ):
        wx.TextCtrl.__init__( self, parent, id, cci_def_text, size = cci_size, style= wx.TE_PROCESS_ENTER)#, *args, **kwargs )
        ccifont= wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.FONTWEIGHT_NORMAL)
        self.SetFont(ccifont)
        if j == 'right':
            self.SetWindowStyleFlag(self.GetWindowStyle()|wx.TE_RIGHT)

        self.parent = parent
        self.param= kwargs['param']
        self.Fit()
        self.Layout()

        self.linspace=kwargs.get('linspace',False)

        if on_enter_func:
            self.on_enter_func = on_enter_func
        else:
            self.on_enter_func = self.dummy

        self.Bind( wx.EVT_TEXT, self.OnTextChange, id= self.GetId() )
        self.Bind( wx.EVT_TEXT_ENTER, self.OnTextEnter, id= self.GetId() )
        self.Bind( wx.EVT_LEFT_DCLICK, self.OnEntryDialog)#, id= self.GetId() ) 
        self.def_text_bg_color = self.GetBackgroundColour()

    def dummy(self, e=None):
        print('Dummy')
        pass 

    def OnTextChange( self, e ):
        print(f'OTChange {self.GetName()}')
        self.set_modified_bg()

    def OnEntryDialog( self, e ):
        print("OED")
        vals= self.GetValue().split(',')
        print( 'VALS\n'*5,vals )
        
        def UpdateResult(e):
            start=float(tb1.GetValue())
            end=float(tb2.GetValue())
            npoints=int(tb3.GetValue())
            print( 'TB1',tb1.GetValue() )
            print( 'TB2',tb2.GetValue() )
            print( 'TB3',tb3.GetValue() )
            spantype=cb_typespan.GetString(cb_typespan.GetSelection())
            if spantype=='LinSpace':
                rval=','.join([str(x) for x in np.linspace(start,end,npoints).tolist()])
            elif spantype=='LogSpace':
                rval=','.join([str(x) for x in np.logspace(start,end,npoints).tolist()])
            else:
                rval=str(start)
            tl_result.SetLabel(rval)
            print('rval=',rval)
            return rval


        try:
            dlg=wx.Dialog(self,title='Param Change Dialog')
            #breakpoint()
            butsz=dlg.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
            #dlg.SetMinSize(( 800, 800 )) #TODO move this to after - ceanup with setminsize
            vs=wx.BoxSizer(wx.VERTICAL)

            tc_gbs= wx.GridBagSizer(hgap=15, vgap=15) #print(' >>> made NEW group "%s"'%(group))
            tl_start= wx.StaticText(dlg, wx.ID_ANY, 'Start')
            tl_end  = wx.StaticText(dlg, wx.ID_ANY, 'End')
            tl_pts  = wx.StaticText(dlg, wx.ID_ANY, 'NPoints')
            tb1= wx.TextCtrl(dlg, wx.ID_ANY, vals[0]       , size=(300,-1))
            tb2= wx.TextCtrl(dlg, wx.ID_ANY, vals[-1]      , size=(300,-1))
            tb3= wx.TextCtrl(dlg, wx.ID_ANY, f'{len(vals)}', size=(300,-1))
            dlg.Bind( wx.EVT_TEXT, UpdateResult, id= tb1.GetId() )
            dlg.Bind( wx.EVT_TEXT, UpdateResult, id= tb2.GetId() )
            dlg.Bind( wx.EVT_TEXT, UpdateResult, id= tb3.GetId() )

            bsz=5
            tc_gbs.Add(tl_start, (0,0), (1,1), wx.ALIGN_LEFT | wx.EXPAND, border=bsz )
            tc_gbs.Add(tl_end  , (0,1), (1,1), wx.ALIGN_LEFT | wx.EXPAND, border=bsz )
            tc_gbs.Add(tl_pts  , (0,2), (1,1), wx.ALIGN_LEFT | wx.EXPAND, border=bsz )
            tc_gbs.Add(tb1     , (1,0), (1,1), wx.ALIGN_LEFT | wx.EXPAND, border=bsz )
            tc_gbs.Add(tb2     , (1,1), (1,1), wx.ALIGN_LEFT | wx.EXPAND, border=bsz )
            tc_gbs.Add(tb3     , (1,2), (1,1), wx.ALIGN_LEFT | wx.EXPAND, border=bsz )
            vs.Add(tc_gbs, 0, wx.ALL|wx.EXPAND, border=5)

            hbox_choice=wx.BoxSizer(wx.HORIZONTAL)
            tl_typespan= wx.StaticText(dlg, wx.ID_ANY, 'Span Type')
            cb_typespan=wx.Choice(dlg, wx.ID_ANY, choices=['-----','LinSpace','LogSpace'])
            cb_typespan.SetSelection(0)
            dlg.Bind( wx.EVT_CHOICE, UpdateResult, id= cb_typespan.GetId() )
            hbox_choice.Add(tl_typespan)
            hbox_choice.Add(cb_typespan)
            vs.Add(hbox_choice, 0, wx.ALL|wx.EXPAND, border=5)

            hbox_res=wx.BoxSizer(wx.HORIZONTAL)
            tl_result= wx.StaticText(dlg, wx.ID_ANY, 'blah\nblah\nblah')
            tl_result.Wrap(10)
            hbox_res.Add(tl_result)
            vs.Add(hbox_res, 0, wx.ALL|wx.EXPAND, border=5)
            vs.Add(butsz)

            dlg.SetSizer(vs)
            dlg.Fit()
#            dlg.SetAutoLayout(True)
            #if dlg.Show() == wx.ID_OK:
            if dlg.ShowModal() == wx.ID_OK:
                self.SetValue(UpdateResult(None))
        finally:
            #pass
            dlg.Destroy()

    def set_modified_bg(self):
        #print('SMBG')
        self.SetBackgroundColour('orange')
        self.Refresh()

    def OnTextEnter( self, e ):
        print(f'OTEnter {self.GetName()}')
        self.set_regular_bg()
        self.on_enter_func(e)

    def set_regular_bg(self): # needed separate for calls to SetValue
        #print('set_reg:')
        self.SetBackgroundColour(self.def_text_bg_color)
        self.Refresh()


#WARNING NOTE I broke this - by adding text change callback -completely untested
class ColChangeInput_2( wx.TextCtrl ):
    '''A TextCtrl that changes color on modify and resets on Enter
       unbound ENTER FUNC - call from user defined callback '''
    def __init__(self, parent, id, cci_def_text='', cci_size=(-1,-1), on_change_callback=None ):
        wx.TextCtrl.__init__( self, parent, id, cci_def_text, size = cci_size, style= wx.TE_PROCESS_ENTER )

        self.parent = parent
        self.parent.Bind( wx.EVT_TEXT, self.OnTextChange, id= self.GetId() )
        self.def_text_bg_color = self.GetBackgroundColour()
        self.on_change_callback= on_change_callback

    def dummy(self):
        pass 

    def OnTextChange( self, e ):
        self.SetBackgroundColour('yellow')
        if not self.on_change_callback:
            self.SetBackgroundColour('orange')
        self.Refresh()

    def OnTextEnter( self ): 
        self.SetBackgroundColour(self.def_text_bg_color)
        self.Refresh()

