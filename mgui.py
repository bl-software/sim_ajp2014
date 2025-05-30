#!/usr/bin/env python3
# Copyright © 2015 Dale Huffman, Walter Boron
# SPDX-License-Identifier: GPL-3.0-or-later

'''GUI frontend for Cell Modelling program'''

import sys
import socket
import os
import wx
#import wx.svg
import wx.lib.scrolledpanel as scrolled
print(f'wxpython: {wx.version()}')
print('Name:',__name__)

import collections
from itertools import zip_longest
import datetime
import math
import re
import glob
import time
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=3)


from CCI import ColChangeInput

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matlab.engine

import wx.lib.fancytext as fancytext
def o_start_sub(self, attrs):
    ''' this is to override the subscript height '''
    if attrs.keys():
        raise ValueError("<sub> does not take attributes")
    font = self.getCurrentFont()
    self.offsets.append(self.offsets[-1] + self.dc.GetFullTextExtent("M", font)[1]*0.2)
    self.start_font({"size" : font.GetPointSize() * 0.9})
fancytext.Renderer.start_sub= o_start_sub



from VERSION import version
program_version= version.split(' ')[0]

import wx.lib.wxcairo
import cairo
haveCairo = True

#INSPECT=True
INSPECT=False
if INSPECT:
    import wx.lib.inspection

#import Figures
from Params import myParams
#pprint.pp(myParams)
from Params.Param_Validators import *

from Figures import Figs
#pprint.pp(Figs)

from support import *

def hex_to_float( h ):
    return float((h>>16)&0xff)/255, float((h>>8)&0xff)/255, float(h&0xff)/255

class RGB_JTB_2012:
    icfo     = hex_to_float( 0xA9CFA0 )
    icfi     = hex_to_float( 0x79AF70 )
    eufo     = hex_to_float( 0xb1dcff )
    eufi     = hex_to_float( 0xC1C1D5 )
    memsurf  = hex_to_float( 0x9F7F5D )
    memcent  = hex_to_float( 0xA4AF7F )
    rad      = hex_to_float( 0x606060 )
    radtxt   = hex_to_float( 0x000000 )
    arrowtxt = hex_to_float( 0x0000ff )
    arrow    = hex_to_float( 0x0000ff )
    bg = '#b1dcff'
class RGB_AJP_2014:
    icfo     = hex_to_float( 0x8C5D2F )
    icfi     = hex_to_float( 0x231000 )
    eufo     = hex_to_float( 0xDBDBE6 )
    eufi     = hex_to_float( 0xC1C1D5 )
    memsurf  = hex_to_float( 0x465723 )
    memcent  = hex_to_float( 0xC1C1D5 )
    rad      = hex_to_float( 0xf0f0f0 )
    radtxt   = hex_to_float( 0xffffff )
    arrowtxt = hex_to_float( 0xc0c0ff )
    arrow    = hex_to_float( 0xffffff )
    bg= '#808080'

rgbs = { 'JTB'      : RGB_JTB_2012,
         'AJP'      : RGB_AJP_2014,
}

class CellPanel(object):#(wx.Panel):
    def __init__(self,app,cpname='CPNull',xsz=600,ysz=800,makepanel=True):
        #print(f'CP:name={cpname}')
        self.app= app
        self.panelsize_x = xsz
        self.panelsize_y = ysz
        self.panelsize = (self.panelsize_x, self.panelsize_y)
        self.rendercount=0
        if makepanel:
            #self.parent=self.app.panel
            self.vs= wx.BoxSizer(wx.VERTICAL)
            self.panel= wx.Panel(self.app.panel, wx.ID_ANY, size=(self.panelsize_x,self.panelsize_y), name=cpname)
            self.vs.Add(self.panel, 0)

    def Destroy(self):
        self.panel.Destroy()
        self.vs.Remove(self.panel, 0)

    def angled_linetext(self, ctx, angle, li,lj,lk,ll, textlines, spacing=2, lineoffset=1.0, dx=0, dy=0, dr=0, dc=0, debug=[]):
        ''' centers on the radial line (I think)'''
        r=math.radians(angle)
        angle= math.degrees(math.atan2(math.sin(r),math.cos(r)))
        radians= math.radians(angle)#2*math.pi*angle/360

        line_cx= (li + lk) /2
        line_cy= (lj + ll) /2
        
        def cross(x,y,r=None,g=None,b=None,a=None):
            #print('cross:',x,y,r,g,b,a)
            if r or g or b or a:
                ctx.set_source_rgba( r, g, b, a)
            ctx.move_to( x-100, y )
            ctx.line_to( x+100, y )
            ctx.move_to( x    , y-100 )
            ctx.line_to( x    , y+100 )
            ctx.stroke()

        if 'initcross' in debug:
            cross(line_cx,line_cy, 1.0, 1.0, 0.0, 1.0) # Yellow
            cross(   20.0,   20.0, 0.0, 0.0, 0.0, 1.0) # Black

        if 'blah' in debug:
            ctx.set_source_rgba( 0.5, 0.5, 0.5, 0.5)
            ctx.move_to(100,100)
            ctx.line_to(500,500)
            ctx.stroke()

        face = wx.lib.wxcairo.FontFaceFromFont(wx.FFont(10, wx.SWISS))#, wx.FONTFLAG_BOLD))
        height= ctx.font_extents()[2]

        ctx.set_font_face(face)
        ctx.set_font_size(16)
        ctx.set_source_rgb(*self.rgb.rad)
        ctx.move_to(line_cx,line_cy)
        #print('mt:',line_cx, line_cy)

        for i,tl in enumerate(textlines):
            x_bearing, y_bearing, width, Xheight, Xxadvance, Xyadvance = ctx.text_extents(tl)
            #print('init  tes', ctx.text_extents(tl))
            ctx.save()
            if abs(angle) < 90:
                text_x, text_y = self.PolarToCartesian((i+lineoffset)*(height + spacing), angle -90 , line_cx, line_cy )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 1.0, 0.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    ctx.stroke()
                #    print('lt1a:',text_x,text_y)
                #    cross(text_x+15,text_y+15,1.0, 0.0, 0.0, 1.0)
                text_x, text_y = self.PolarToCartesian(   (width + x_bearing)/2, angle -180,  text_x,  text_y )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 0.0, 1.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    ctx.stroke()
                #    print('lt1b:',text_x,text_y)
                #    cross(text_x,text_y,0.0, 1.0, 0.0, 1.0)
                #    cross(0.0,0.0,0.0, 1.0, 1.0, 1.0)
            else:
                text_x, text_y = self.PolarToCartesian((i+lineoffset)*(height + spacing), angle +90 , line_cx, line_cy )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 1.0, 0.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    print('lt2a:',text_x,text_y)
                #    ctx.stroke()
                text_x, text_y = self.PolarToCartesian(   (width + x_bearing)/2, angle     ,  text_x,  text_y )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 0.0, 1.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    print('lt2b:',text_x,text_y)
                #    ctx.stroke()
            ctx.translate(text_x, text_y )
            if abs(angle) < 90:
                ctx.rotate(-radians) # ROTATE is positive clockwise
            else:
                ctx.rotate(math.pi-radians)#abs(radians)%math.pi/2) # ROTATE is positive clockwise
            ctx.move_to(0,0)
            #print('final tes', ctx.text_extents(tl))
            ctx.show_text(tl)
            if 'pathcross' in debug:
                cross(0.0,0.0, 1.0, 1.0, 1.0, 1.0)
            ctx.restore()

        if 'initcross' in debug:
            #print('OUTCROSS:')
            cross( 0.0, 0.0, 1.0, 0.0, 1.0, 1.0) # Magenta offset from IN

    def arrowhead(self, ctx, r, g, b, xs, ys, xe, ye, length=5, deg=math.pi * .15):
        angle = math.atan2 (ye - ys, xe - xs) + math.pi

        x1 = xe + length * math.cos(angle - deg)
        y1 = ye + length * math.sin(angle - deg)
        x2 = xe + length * math.cos(angle + deg)
        y2 = ye + length * math.sin(angle + deg)
 
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        ctx.set_source_rgba( *self.rgb.arrowtxt, 1 )
        ctx.move_to (xe, ye)
        ctx.line_to (x1, y1)
        ctx.stroke()

        ctx.set_source_rgba( *self.rgb.arrowtxt, 1 )
        ctx.move_to (xe, ye)
        ctx.line_to (x2, y2)
        ctx.stroke()

    def offset(self,x,y,l,deg):
        rads= math.radians(deg)
        return x+l*math.cos(rads), y+l*math.sin(rads)

    def PolarToCartesian(self, radius, angle, cx, cy):
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        return (cx+x, cy-y)

class CellPanel_Oocyte(CellPanel):
    def __init__(self,app):
        super().__init__(app, 'CellPanel_Oocyte')
        self.rgb= rgbs[self.app.cur_sim_type]
        self.panel.SetBackgroundColour( self.rgb.bg )

        self.paint_panel= self.panel
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.CallLater(250,self.init_refresh)

    def Refresh(self):
        print('Refresh')
        self.panel.Refresh()
        

    def OnPaint(self,e): # CellPanel_Oocyte
        dc=wx.PaintDC(self.paint_panel)    # NOTE this is called a LOT
        self.rb,self.gb,self.bb= hex_to_float( 0xb1dcff )
        dc.Clear()
        self.Render(dc)

    def init_refresh(self): # CellPanel_Oocyte
        return

    def Render(self, dc): # CellPanel_Oocyte
        self.rendercount+=1
        if self.rendercount %100 == 0:
            print(f'CP_Oocyte:render rendercount={self.rendercount}')
        self.rgb= rgbs[self.app.cur_sim_type]
        self.panel.SetBackgroundColour( self.rgb.bg )

        cx= self.cx = int(self.panelsize_x/2)
        cy= self.cy = int(self.panelsize_x/2 + 50)
        center_pt = wx.Point(cx, cy)

        # D and D_inf are in mm 
        actual_radius_cell_mm = self.app.cur_params["D"]()[0] / 2
        actual_radius_euf_mm  = self.app.cur_params["D_inf"]()[0] / 2
        actual_thickness_euf_mm  = actual_radius_euf_mm - actual_radius_cell_mm
        #print('actual_radius_cell_mm:', actual_radius_cell_mm,
        #      'actual_radius_euf_mm:', actual_radius_euf_mm,
        #      'actual_thickness_euf_mm:', actual_thickness_euf_mm )

        graphical_space_around_cell= 50
        ratio = (self.panelsize_x - graphical_space_around_cell)/2 / actual_radius_euf_mm  # pixels / mm

        radius_cell = actual_radius_cell_mm * ratio
        radius_euf = actual_radius_euf_mm * ratio
        thickness_euf = actual_thickness_euf_mm * ratio
        one_mm_line = 1.0 * ratio

        num_shells_in= self.app.cur_params["n_in"]()[0]
        num_shells_out= self.app.cur_params["n_out"]()[0]

        shell_thick_in= actual_radius_cell_mm / num_shells_in * 1000
        shell_thick_out= actual_thickness_euf_mm / num_shells_out * 1000

        self.arrowPen= wx.Pen(wx.BLACK,width=4,style=wx.PENSTYLE_SOLID)
        self.linePen= wx.Pen(wx.BLACK,width=2,style=wx.PENSTYLE_SOLID)

        ctx = wx.lib.wxcairo.ContextFromDC(dc)

        ### 1mm Scale line
        # the line
        ctx.set_line_width(2)
        line_y=5
        ctx.move_to( 5, line_y )
        ctx.line_to( 5 + one_mm_line, line_y )
        ctx.set_source_rgba( 0,0,0, 1 )
        line_y_lower= ctx.stroke_extents()[3]
        ctx.stroke()
        # the text
        the_text= '1.00 mm'
        spacing= 2
        face = wx.lib.wxcairo.FontFaceFromFont(wx.FFont(10, wx.SWISS))#, wx.FONTFLAG_BOLD))
        ctx.set_font_face(face)
        ctx.set_font_size(16)
        x_bearing, y_bearing, width, height, xadvance, yadvance = ctx.text_extents(the_text)

        text_y= line_y_lower + height + spacing
        ctx.move_to((5 + one_mm_line ) / 2, text_y )
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text(the_text)

        ### CELL ###
        ## Cell Body
        ptn= cairo.RadialGradient( cx, cy, 0, cx, cy, radius_cell )
        ptn.add_color_stop_rgba( 0, *self.rgb.icfi, 1.0 )
        ptn.add_color_stop_rgba( 1, *self.rgb.icfo, 1.0 )
        ctx.set_source( ptn )
        ctx.arc(cx, cy, radius_cell, 0, math.pi*2)
        ctx.fill()

        # Membrane
        membrane_line_width= 3
        ctx.set_line_width(membrane_line_width)
        # Membrane - outer
        ctx.set_source_rgba( *self.rgb.memsurf, 1 )
        ctx.arc(cx, cy, radius_cell, 0, math.pi*2)
        ctx.stroke()
        # Membrane - middle
        ctx.set_source_rgba( *self.rgb.memcent, 1 )
        ctx.arc(cx, cy, radius_cell - membrane_line_width, 0, math.pi*2)
        ctx.stroke()
        # Membrane - inner
        ctx.set_source_rgba( *self.rgb.memsurf, 1 )
        ctx.arc(cx, cy, radius_cell - 2*membrane_line_width, 0, math.pi*2)
        ctx.stroke()

        #EUF
        euf_start= membrane_line_width / 2 + radius_cell
        ptn= cairo.RadialGradient( cx, cy, euf_start, cx, cy, radius_euf )
        ptn.add_color_stop_rgba( 0, *self.rgb.eufi, 1.0 )
        ptn.add_color_stop_rgba( 1, *self.rgb.eufo, 1.0 )
        ctx.set_source( ptn )
        ctx.arc(cx, cy, euf_start, 0, math.pi*2)
        ctx.arc(cx, cy, radius_euf, 0, math.pi*2)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        ctx.fill()
        # EUF : outer ring highlight
        if self.app.cur_sim_type == 'JTB_2012':
            ctx.set_source_rgba( *hex_to_float( 0xb5e0ff ), 1 )
            ctx.arc(cx, cy, radius_euf, 0, math.pi*2)
            ctx.stroke()
 
        # Cell Radius
        ctx.set_source_rgba( *self.rgb.rad, 1 )
        ctx.move_to(cx, cy)
        ctx.line_to( cx + radius_cell, cy )
        li,lj,lk,ll= ctx.stroke_extents()
        ctx.stroke()
        self.arrowhead( ctx, *self.rgb.rad, cx, cy, cx + radius_cell, cy, 7)
        self.arrowhead( ctx, *self.rgb.rad, cx + radius_cell, cy, cx, cy, 7)

        angle=0
        textlines= [ #'%s'%angle,
                     '%0.0f \u00b5m'%(actual_radius_cell_mm*1000),
                     '%d shells'%(num_shells_in),
                     '%0.2f \u00b5m/shell'%(shell_thick_in),
                   ]
        self.angled_linetext( ctx, 0, li,lj,lk,ll, textlines )

        ### EUF ###
        ## EUF Short Radius
        angle = -30
        xs,ys = self.PolarToCartesian( euf_start, angle, cx, cy)
        xe,ye = self.PolarToCartesian( radius_euf+30, angle, cx, cy)
        textlines= [ #'%s'%angle,
                     '%0.0f \u00b5m'%(actual_thickness_euf_mm*1000),
                     '   %d shells'%(num_shells_out),
                     '      %0.2f \u00b5m/shell'%(shell_thick_out),
                   ]

        ctx.set_source_rgba( *self.rgb.rad, 1 )
        ctx.move_to(xs, ys)
        ctx.line_to(xe, ye)
        li,lj,lk,ll= ctx.stroke_extents()
        ctx.stroke()

        self.arrowhead( ctx, *self.rgb.rad, xs, ys, xe, ye)
        self.arrowhead( ctx, *self.rgb.rad, xe, ye, xs, ys)

        self.angled_linetext( ctx, angle, xs,ys,xe,ye, textlines)

        eq_top = int(cy * 1.75 + 50)
        for eq in self.app.equations.values():
            if eq['visible'] == True:
                bm = eq[ 'bm' ]
                eq[ 'p' ] = dc.DrawBitmap( bm, cx - int(bm.GetWidth()/2) , eq_top)
                eq_top += bm.GetHeight()

        ## EUF Circle
        angle = 30
        ## EUF Title
        loc = self.PolarToCartesian( (radius_euf - 5), angle + 10, cx, cy)
        dc.DrawRotatedText( 'EUF', int(loc[0]), int(loc[1]),-(90-(angle + 10)))

        # SHELL MARKERS
        sm_line_width= 1
        ctx.set_line_width(sm_line_width)
        ctx.set_source_rgba( *self.rgb.arrow, 1 )
        r_per_shell_in  = radius_cell / num_shells_in
        r_per_shell_out = (radius_euf - radius_cell) / num_shells_out

        def arrow_at(rad, angle, off=5, deg=-45, length=150, **overrides):
            xe,ye = self.PolarToCartesian( rad, angle, cx, cy)
            xlinestart,ylinestart = self.offset(xe,ye,off,deg)
            if 'xlinestart' in overrides:
                xlinestart=overrides['xlinestart']
            if 'ylinestart' in overrides:
                ylinestart=overrides['ylinestart']
            ctx.move_to(xlinestart ,ylinestart)

            xtext,ytext= self.offset(xlinestart,ylinestart,length,deg)
            if 'xtext' in overrides:
                xtext=overrides['xtext']
            if 'ytext' in overrides:
                ytext=overrides['ytext']
            ctx.line_to(xtext, ytext)
            self.arrowhead( ctx, *self.rgb.arrowtxt, xtext, ytext, xlinestart, ylinestart, length=20, deg=math.pi * .15)
            ctx.stroke()
            ctx.move_to(xtext +5,ytext + height/2)
            ctx.show_text(the_text)
            return xlinestart,ylinestart,xtext,ytext
      
        # equal lenth
        ''' l = r1 * as * math.pi = r2 * 2 * math.pi '''

        divider=2
        rings = range(0,num_shells_in,divider)
        lrings = len(rings)
        scale= 5
        ''' arc angles starts at pos x axis and goes clockwise UGH!!!'''
        for ii,i in enumerate(rings):
            ctx.new_sub_path()
            r_ring = i * r_per_shell_in
            sa_arc= 9*math.pi/8
            ea_arc= 10*math.pi/8
            #print(ii,i,'r_ring=',r_ring,'r_per_shell_in=',r_per_shell_in)
            ea_arc= (11-i/num_shells_in)*math.pi/8
            #print('SAEA:', sa_arc, ea_arc)
            ctx.arc(cx, cy, r_ring, sa_arc, ea_arc)
            ctx.stroke()

        text_offset = radius_cell / 4

        #the_text= 'Shell 0'
#        x_bearing, y_bearing, width, Xheight, Xxadvance, Xyadvance = ctx.text_extents(the_text)
        ea = 2*math.pi - ea_arc
        angle = math.degrees(ea)

        the_text= 'Shell 0 = Center of Cell'
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( divider*r_per_shell_in/2, angle, length=80, deg=-40  )

        the_text= 'Shell %d = Membrane'%(num_shells_in)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_cell, angle,  length=80, deg=-20  )

        the_text= 'Shell %d = At Inner Surface'%(num_shells_in-1)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_cell - 2 * membrane_line_width - divider*r_per_shell_in/2, angle, length=80, deg=0, xtext=xtext  )

        divider=10
        rings = range(0,num_shells_out,divider)
        lrings = len(rings)
        scale= 5
        ''' arc angles starts at pos x axis and goes clockwise UGH!!!'''
        for ii,i in enumerate(rings):
            ctx.new_sub_path()
            r_ring = radius_cell + (i * r_per_shell_out)
            ctx.arc(cx, cy, r_ring, sa_arc, ea_arc)
            ctx.stroke()

        the_text= 'Shell %d = Edge of EUF'%(num_shells_in+num_shells_out)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_euf, angle, deg=-60, length=100 + 2.0*height )#, xlinestart=40 )
        the_text= 'Shell %d = At Outer Surface'%(num_shells_in+1)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_cell + 2 * membrane_line_width - divider*r_per_shell_out, angle,
                deg=-60, length=100,
                )#xtext=xtext, ytext=ytext+height*2.0 )
        
        #Vesicles
        vpink= hex_to_float( 0xFFCDE6 )
        vbrown= hex_to_float( 0x0B0706 )
        rings = range(0,num_shells_in)
        idx= int(0.9*len(rings))
        ves_rings = np.arange(idx,idx + 5)*r_per_shell_in
        vesdel = ves_rings[-1] - ves_rings[0]
        sa=150
        ea=360
        oos_tort_lambda= self.app.cur_params["oos_tort_lambda"]()[0]
        density=oos_tort_lambda/0.125# 1.0#1.0
        for ri,vr in enumerate(ves_rings):
            a=np.arange(sa,ea) + (np.random.random_sample(ea-sa)-0.5)
            degs= np.random.choice(a,int(90*density))
            for deg in degs:
                vrad=vr+np.random.random()*0.1
                ctx.new_sub_path()
                icx, icy = self.PolarToCartesian(vrad, deg, cx, cy)
                thisr= np.random.random_sample()*r_per_shell_in #+r_per_shell_in/2.0
                ctx.set_source_rgb( *vpink )
                ctx.arc(icx, icy, thisr, 0, 360)
                #ctx.set_source_rgba( *vbrown, 0.01 )
                #ctx.arc(icx, icy, thisr*1.2, 0, 360)
                ctx.stroke()
                #ctx.fill()

        if self.rendercount %100 == 0:
            print(f'CP_Oocyte:render DONE rendercount={self.rendercount}')


class InputError(Exception):
    pass

from operator import add
class ModelApp(object):
    '''The app'''
    #pylint: disable=too-many-instance-attributes, too-many-statements
    def sims(self,nvi='v',li='i'):
        ''' 'n','v','i'= names, values, items
            'l','i'= list, iterator
        '''
        rv= { 'n' : myParams.keys,
              'v' : myParams.values,
              'i' : myParams.items
            }[nvi]()
        return { 'i' : rv,
                 'l' : list(rv)}[li]

    def papers(self,nvi='v',li='i',sim_name=None):
        ''' 'n','v','i'= names, values, items
            'l','i'= list, iterator
        '''
        if not sim_name:
            sim_name= self.cur_sim_type
        rv= { 'n' : myParams[sim_name].keys,
              'v' : myParams[sim_name].values,
              'i' : myParams[sim_name].items
            }[nvi]()
        return { 'i' : rv,
                 'l' : list(rv)}[li]

    def figures(self,nvi='v',li='i',sim_name=None,paper_name=None):
        ''' 'n','v','i'= names, values, items
            'l','i'= list, iterator
        '''
        if not sim_name:
            sim_name= self.cur_sim_type
        if not paper_name:
            paper_name= self.cur_paper
        rv= { 'n' : myParams[sim_name][paper_name].keys,
              'v' : myParams[sim_name][paper_name].values,
              'i' : myParams[sim_name][paper_name].items
            }[nvi]()
        return { 'i' : rv,
                 'l' : list(rv)}[li]

    def __init__(self, myargs):
        self.myargs=myargs
        if myargs.testing:
            self.TESTING = True
        else:
            self.TESTING = False

        self.on_val_funcs= {\
            'update_buffs'   :self.update_buffs,

        }

        self.matlab_eng = None

        self.cur_sim_type= self.sims('n','l')[0]
        print(f'\ncur_sim_type={self.cur_sim_type}')

        self.cur_paper= self.papers('n','l')[0]
        print(f'\ncur_paper={self.cur_paper}\n')

        self.cur_fig= self.figures('n','l')[0]

        self.wxapp = wx.App()
        hn= socket.gethostname()
        #print(f'HN: {hn}')
        ww=2500
        wh=1600
        mypos= (1600,32)

        self.frame = wx.Frame(None, wx.ID_ANY, f'Modelling Front End ({program_version})', pos=mypos, size=(ww,wh))
        self.frame.SetBackgroundColour((249,249,248,255))#wx.NullColour)
        self.panel = scrolled.ScrolledPanel(self.frame, wx.ID_ANY, name='main_panel')
        self.panel.SetBackgroundColour((249,249,248,255))#wx.NullColour)

        spacer_size= 20
        v_spacer_size= 10

        self.t_sim_type = wx.StaticText(self.panel, wx.ID_ANY, 'Simulation Type: ')
        self.c_sim_type = wx.Choice(    self.panel, wx.ID_ANY, choices=self.sims('n','l'), name='SimTypes')
        self.t_sim_type.SetForegroundColour( wx.BLACK )
        self.c_sim_type.Bind(wx.EVT_CHOICE, self.OnSelectSimType)
        self.c_sim_type.SetSelection(0)

        self.t_load_def       = wx.StaticText(self.panel, wx.ID_ANY, 'Load Default Parameters for: ')
        self.t_load_def_paper = wx.StaticText(self.panel, wx.ID_ANY, 'Paper:')
        self.c_load_def_paper = wx.Choice(    self.panel, wx.ID_ANY, choices=self.papers('n','l'), name='Paper')
        self.t_load_def_fig   = wx.StaticText(self.panel, wx.ID_ANY, 'Figure:')
        self.c_load_def_fig   = wx.Choice(    self.panel, wx.ID_ANY, choices=['',], name='Fig')
        self.t_load_def.SetForegroundColour( wx.BLACK )
        self.t_load_def_paper.SetForegroundColour( wx.BLACK )
        self.t_load_def_fig.SetForegroundColour( wx.BLACK )
        self.c_load_def_paper.Bind(wx.EVT_CHOICE, self.OnSelectPaper)
        self.c_load_def_fig.Bind(wx.EVT_CHOICE, self.OnSelectFigure)
        self.c_load_def_paper.SetSelection(0)
        self.c_load_def_fig.SetSelection(0)
        
        self.t_load_cust = wx.StaticText(self.panel, wx.ID_ANY, 'Load Custom Parameters File: ')
        self.b_load_cust = wx.Button(self.panel, wx.ID_ANY, label='Load')
        self.t_load_cust.SetForegroundColour( wx.BLACK )
        self.b_load_cust.Bind(wx.EVT_BUTTON, self.OnLoadParamFile)

        self.t_load_sim = wx.StaticText(self.panel, wx.ID_ANY, 'Load Sim Data Files: ')
        self.b_load_sim = wx.Button(self.panel, wx.ID_ANY, label='Load')
        self.t_load_sim.SetForegroundColour( wx.BLACK )
        self.b_load_sim.Bind(wx.EVT_BUTTON, self.OnLoadSimData)

        br_acv_al = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT
        bl_acv_ar = wx.LEFT  | wx.ALIGN_CENTER_VERTICAL# | wx.ALIGN_RIGHT

        self.hsiz_simt = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_simt.Add( self.t_sim_type          , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_simt.Add( self.c_sim_type          , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace

        self.hsiz_load_def = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_load_def.Add( self.t_load_def      , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.AddSpacer(spacer_size)
        self.hsiz_load_def.Add( self.t_load_def_paper, 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.Add( self.c_load_def_paper, 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.AddSpacer(spacer_size)
        self.hsiz_load_def.Add( self.t_load_def_fig  , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.Add( self.c_load_def_fig  , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace

        self.hsiz_load_cust = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_load_cust.Add( self.t_load_cust    , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_cust.Add( self.b_load_cust    , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_sim = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_load_sim.Add( self.t_load_sim     , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_sim.Add( self.b_load_sim     , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace

        self.vsiz_load = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_load.Add(self.hsiz_load_def        , 0, wx.ALL , border=5)
        self.vsiz_load.Add(self.hsiz_load_cust       , 0, wx.ALL , border=5)
        self.vsiz_load.Add(self.hsiz_load_sim        , 0, wx.ALL , border=5)

        self.hsiz_sim_load = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_sim_load.Add( self.hsiz_simt       , 0, wx.ALIGN_CENTER_VERTICAL )
        self.hsiz_sim_load.AddSpacer(spacer_size)
        self.hsiz_sim_load.Add( self.vsiz_load       , 0, wx.ALIGN_CENTER_VERTICAL )

        ### Save/Run Current Simulation ###
        self.t_save_cur_params = wx.StaticText(self.panel, wx.ID_ANY, 'Save Parameters Only without Running Simulation')
        self.b_save_cur_params = wx.Button(    self.panel, wx.ID_ANY,  label='Save Only')
        self.t_run_cur_sim     = wx.StaticText(self.panel, wx.ID_ANY, 'Set Ouput Folder, Save Parameters and Run Simulation')
        self.b_run_cur_sim     = wx.Button(    self.panel, wx.ID_ANY,  label='Run Simulation')
        self.t_save_cur_params.SetForegroundColour( wx.BLACK )
        self.t_run_cur_sim.SetForegroundColour( wx.BLACK )
        self.b_save_cur_params.Bind(wx.EVT_BUTTON, self.OnSaveCurParams)
        self.b_run_cur_sim    .Bind(wx.EVT_BUTTON, self.OnRunSim)
        self.b_run_cur_sim.SetBackgroundColour((244,100,100,255))
        self.b_run_cur_sim.SetMinSize(self.b_run_cur_sim.GetSize()*1.1)
        self.b_save_cur_params.SetMinSize(self.b_run_cur_sim.GetSize())

        self.hsiz_save_cur_params = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_save_cur_params.AddSpacer(v_spacer_size)
        self.hsiz_save_cur_params.Add( self.b_save_cur_params, 0, wx.EXPAND )# | wx.ALIGN_CENTER_VERTICAL)
        self.hsiz_save_cur_params.AddSpacer(spacer_size)
        self.hsiz_save_cur_params.Add( self.t_save_cur_params, 0, wx.EXPAND )# | wx.ALIGN_CENTER_VERTICAL)

        self.hsiz_run_cur_sim = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_run_cur_sim.AddSpacer(v_spacer_size)
        self.hsiz_run_cur_sim.Add( self.b_run_cur_sim, 0, wx.EXPAND )#| wx.ALIGN_CENTER_VERTICAL)
        self.hsiz_run_cur_sim.AddSpacer(spacer_size)
        self.hsiz_run_cur_sim.Add( self.t_run_cur_sim, 0, wx.EXPAND )#| wx.ALIGN_CENTER_VERTICAL)

        # Fig Buttons
        self.hsiz_cur_button= wx.BoxSizer(wx.HORIZONTAL)
        self.t_jspecific_figs  = wx.StaticText(self.panel, wx.ID_ANY, label=f'Valid SimType-Paper Figures:')
        self.t_jspecific_figs.SetForegroundColour( wx.BLACK )
        self.hsiz_cur_button.Add( self.t_jspecific_figs, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, border=5 ) 

        self.fig_buttons= {}
        for sim_n,sim in self.sims('i','i'):
            for paper_n,paper in self.papers('i','i',sim_n):
                for fig_n,fig in paper.items():
                    for i,vf in enumerate(fig['valid_figs']):
                        #dprint(DBG_PF,'\n    vf=',vf)
                        but_name = '%s %s'%(paper_n,vf)
                        #dprint(DBG_PF,'    but_name=',but_name)
                        try:
                            self.fig_buttons[but_name]
                        except KeyError:
                            b= wx.Button(self.panel, wx.ID_ANY, label=vf)
                            b.SetBackgroundColour((0xaa,0x0,0xff,255))
                            b.Bind(wx.EVT_BUTTON, lambda e, figname=vf : self.OnCreateFigure(e,figname))
                            self.hsiz_cur_button.Add( b, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, border=5 )
                            self.fig_buttons[but_name]=b
        #dprint(DBG_PF,'  fig_buts[keys]=',list(self.fig_buttons.keys()) )

        self.vsiz_save_run = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_save_run.Add( self.hsiz_save_cur_params, 1, wx.EXPAND)
        self.vsiz_save_run.AddSpacer(5)
        self.vsiz_save_run.Add( self.hsiz_run_cur_sim , 1, wx.EXPAND) #pylint: disable=bad-whitespace
        self.vsiz_save_run.AddSpacer(5)
        self.vsiz_save_run.Add( self.hsiz_cur_button , 0 )#, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT )

        ### Current Sim and Output ###
        self.l_sim_outputf = wx.StaticText(self.panel, wx.ID_ANY, 'Output Folder: ')
        self.t_sim_outputf = wx.TextCtrl(  self.panel, wx.ID_ANY, '<NOT SET>' )
        self.l_sim_current = wx.StaticText(self.panel, wx.ID_ANY, 'Current Param File: ' )
        self.t_sim_current = wx.TextCtrl(  self.panel, wx.ID_ANY, '')

        self.l_sim_outputf.SetForegroundColour( wx.BLACK )
#       self.l_sim_outputf.SetBackgroundColour((255,25,255,255))
        self.l_sim_outputf.SetMinSize((150,-1))
        self.t_sim_outputf.SetForegroundColour( wx.BLACK )
        self.t_sim_outputf.SetBackgroundColour((255,255,255,255))
        self.t_sim_outputf.SetEditable(False)

        self.l_sim_current.SetForegroundColour( wx.BLACK )
        self.l_sim_current.SetMinSize((150,-1))
        self.t_sim_current.SetForegroundColour( wx.BLACK )
        self.t_sim_current.SetBackgroundColour((255,255,255,255))
        self.t_sim_current.SetEditable(False)

        self.hsiz_outfold = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_outfold.Add( self.l_sim_outputf, 1, wx.ALIGN_LEFT ) #pylint: disable=bad-whitespace
        self.hsiz_outfold.AddSpacer(spacer_size)
        self.hsiz_outfold.Add( self.t_sim_outputf, 4, wx.ALIGN_LEFT | wx.EXPAND  ) #pylint: disable=bad-whitespace

        self.hsiz_curpfile = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_curpfile.Add( self.l_sim_current, 1, wx.ALIGN_LEFT ) #pylint: disable=bad-whitespace
        self.hsiz_curpfile.AddSpacer(spacer_size)
        self.hsiz_curpfile.Add( self.t_sim_current, 4, wx.ALIGN_LEFT | wx.EXPAND  ) #pylint: disable=bad-whitespace

        self.vsiz_outcur = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_outcur.Add( self.hsiz_outfold, 0, wx.EXPAND)
        self.vsiz_outcur.AddSpacer(v_spacer_size)
        self.vsiz_outcur.Add( self.hsiz_curpfile, 0, wx.EXPAND)

        # Custom Figures x vs time
        headfont= wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.BOLD)
        self.t_cust_note = wx.StaticText(  self.panel, wx.ID_ANY, label='Notation:\nsingle values and start:stop:step ranges\n4 9:2:17 50 => 4,9,11,13,15,50\nnegative counts from end => -1 = last value in series')
        self.t_cust_note.SetForegroundColour( wx.BLACK )

        self.c_matlab= [  'CO_2',      'H_2CO_3',          'HA_1',      'H^{+}',    'HCO_3^{-}',        'A_1^{-}'       ]
        self.c_ptype = [  'linear',    'linear',           'linear',    'pH',       'linear',           'linear'        ]
        self.c_python= [ u'CO\u2082', u'H\u2082CO\u2083', u'HA\u2081', u'H\u207A', u'HCO\u2083\u207B', u'A\u2081\u207B' ]
        self.c_ascii = [  'CO2',       'H2CO3',            'HA',        'H',        'HCO3',             'A'             ]
        self.c_fig_solute  = wx.Choice(self.panel, wx.ID_ANY, choices=self.c_python, name='Solute')
        self.c_fig_solute.SetSelection(0)

        self.l_fig_shells = wx.StaticText( self.panel, wx.ID_ANY, label='Shells:')
        self.t_fig_shells = wx.TextCtrl(   self.panel, wx.ID_ANY, '0 20 40 60 78:80:1' )
        
        self.l_fig_times  = wx.StaticText( self.panel, wx.ID_ANY, label='Times:')
        self.t_fig_times  = wx.TextCtrl(   self.panel, wx.ID_ANY, '0:-1')

        self.b_fig_cust_vt= wx.Button(     self.panel,  wx.ID_ANY, label='Fig vs. Time')
        self.b_fig_cust_vs= wx.Button(     self.panel,  wx.ID_ANY, label='Fig vs. Shell')

        self.l_runs       = wx.StaticText( self.panel, wx.ID_ANY, label='Run# (If applicable):')
        self.t_fig_runs   = wx.TextCtrl(   self.panel, wx.ID_ANY, '0:-1')

        self.l_fig_shells.SetForegroundColour( wx.BLACK )
        self.t_fig_shells.SetMinSize((350,-1))
        self.t_fig_shells.SetMaxSize((350,-1))
        self.l_fig_times.SetForegroundColour( wx.BLACK )
        self.t_fig_times.SetMinSize((350,-1))
        self.t_fig_times.SetMaxSize((350,-1))
        self.b_fig_cust_vt.Bind(wx.EVT_BUTTON, lambda e, figname='custom' : self.OnCreateFigure(e,figname,'vt'))
        self.b_fig_cust_vs.Bind(wx.EVT_BUTTON, lambda e, figname='custom' : self.OnCreateFigure(e,figname,'vs'))
        self.l_runs.SetForegroundColour( wx.BLACK )

        spacer_size= 10
        x_br_acv_al = wx.EXPAND | wx.RIGHT# | wx.ALIGN_LEFT
        x_bl_acv_ar = wx.EXPAND | wx.LEFT # | wx.ALIGN_RIGHT
        x_bl_acv_al = wx.EXPAND | wx.LEFT # | wx.ALIGN_LEFT

        self.hsiz_cust_fig_shells = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_cust_fig_shells.Add( self.l_fig_shells , 1, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_shells.Add( self.t_fig_shells , 3, x_bl_acv_ar, border=10 ) #pylint: disable=bad-whitespace

        self.hsiz_cust_fig_times  = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_cust_fig_times.Add( self.l_fig_times   , 1, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_times.Add( self.t_fig_times   , 3, x_bl_acv_ar, border=10 ) #pylint: disable=bad-whitespace

        self.hsiz_cust_fig_run    = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_cust_fig_run.Add( self.l_runs          , 3, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_run.Add( self.t_fig_runs      , 1, x_bl_acv_al, border=10 ) #pylint: disable=bad-whitespace

        self.hsiz_fig_cust    = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_fig_cust.Add( self.b_fig_cust_vt       , 0, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_fig_cust.Add( self.b_fig_cust_vs       , 0, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        
        bcfig = wx.StaticBox(self.panel, wx.ID_ANY, 'Custom Figures ')
        bcfig.SetForegroundColour(wx.BLACK)
        bcfig.SetFont( headfont )
        self.vsiz_cust_fig = wx.StaticBoxSizer(bcfig,wx.VERTICAL)
        x_lr_al = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.ALIGN_LEFT
        self.vsiz_cust_fig.Add( self.t_cust_note         , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(v_spacer_size)
        self.vsiz_cust_fig.Add( self.c_fig_solute        , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(v_spacer_size)
        self.vsiz_cust_fig.Add( self.hsiz_cust_fig_shells, 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(5)
        self.vsiz_cust_fig.Add( self.hsiz_cust_fig_times , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(5)
        self.vsiz_cust_fig.Add( self.hsiz_cust_fig_run   , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(v_spacer_size)
        self.vsiz_cust_fig.Add( self.hsiz_fig_cust       , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace

        bpm= wx.StaticBox(self.panel, wx.ID_ANY, 'Parameters')
        bpm.SetForegroundColour(wx.BLACK)
        bpm.SetFont( headfont )
        self.hsiz_param_main = wx.StaticBoxSizer(bpm,wx.HORIZONTAL)
        self.hsiz_param_main.name='hsiz_param_main'

        ### Main Sizer Layout ###
        bsim = wx.StaticBox(self.panel, wx.ID_ANY, 'Simulation ')
        bsim.SetForegroundColour(wx.BLACK)
        bsim.SetFont( headfont )
        self.vsiz_sim = wx.StaticBoxSizer(bsim,wx.VERTICAL)
        self.vsiz_sim.Add(self.hsiz_sim_load          , 0, wx.ALL, border=5 )
        self.vsiz_sim.Add(self.vsiz_save_run          , 0, wx.ALL, border=5 )
        self.vsiz_sim.Add(self.vsiz_outcur            , 0, wx.ALL | wx.EXPAND, border=5 )

        self.hsiz_sim_cust_fig = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_sim_cust_fig.Add( self.vsiz_sim     , 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )
        self.hsiz_sim_cust_fig.Add( self.vsiz_cust_fig, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )

        self.equations= collections.OrderedDict()
        self.equations['show_co2_k1'] = \
            { 'bm':wx.Bitmap('latex_stuff/co2_k1_fromweb_150.png'   , wx.BITMAP_TYPE_PNG), 'visible':False, 'storage':None }
        self.equations['show_h2co3_pk2'] = \
            { 'bm':wx.Bitmap('latex_stuff/h2co3_pk2_fromweb_150.png', wx.BITMAP_TYPE_PNG), 'visible':False, 'storage':None }
        self.equations['show_ha1_pk3'] = \
            { 'bm':wx.Bitmap('latex_stuff/ha1_pk3_fromweb_150.png'  , wx.BITMAP_TYPE_PNG), 'visible':False, 'storage':None }

        self.hsiz_param_cell = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_param_cell.Add( self.hsiz_param_main, 0, wx.ALL | wx.EXPAND, border=5 )

        self.vsiz_main = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_main.Add( self.hsiz_sim_cust_fig    , 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )
        self.vsiz_main.Add( self.hsiz_param_cell      , 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )


        # DEFAULT TO LOAD
        self.OnSelectSimType(None,simtype=myargs.simtype,paper=myargs.paper,fig=myargs.figure)

        self.panel.SetSizer(self.vsiz_main)
        self.panel.SetupScrolling()
        self.panel.SetAutoLayout(True)

        self.reset_run_data()

        self.frame.Show(True)

        if myargs.dosim:
            self.OnRunSim(None)
        elif myargs.sdp:
            self.loadSimData(myargs.sdp)

        if self.myargs.dofig:
            self.OnCreateFigure(None,self.myargs.dofig)

        if INSPECT:
            wx.lib.inspection.InspectionTool().Show()

        self.wxapp.MainLoop()

    def reset_run_data(self):
        self.run_data=[]
        self.run_time=[]
        self.run_params={}

    def sel_idx(self, seltype, arg, guichoice):
        hprint('sel_idx:',arg,guichoice)
        if arg != None:
            try: # an integer
                idx= int(arg)
                print(f'  sel_idx: from int={idx}')
            except ValueError: # a string
                idx= guichoice.FindString(arg)
                print(f'  sel_idx: found from choice list={idx}')
        else: # get it from gui
            try:
                idx= guichoice.GetSelection()
                print(f'  sel_idx: from selection= {idx}')
            except:
                idx= 0
                print(f'  sel_idx: defaulting to {idx}')

        nchoices=guichoice.GetCount()
        print(f'  sel_idx: gui nchoices= {nchoices}')
        if idx < nchoices:
            print('  selidx')
            print(f'   idx={idx}')
            print(f'   guich={guichoice}')
            guichoice.SetSelection(idx) 
            return guichoice.GetString(guichoice.GetCurrentSelection())
        else:
            print(f'Incorrect {seltype} selection index, choices are:')
            for i,idx in enumerate(range(nchoices)):
                print(f'  {i:2}: {guichoice.GetString(idx)}')


    def OnSelectSimType(self,e,simtype=None,paper=None,fig=None):
        ''' simtype is name from dropdown or index number '''
        #pprint.pp(Figs)
        print(f'\nOnSelectSimType e={e}, st={simtype}, p={paper}, f={fig}')
        print('avail sime=', self.sims('n','l'))

        self.cur_sim_type= new_sim_type= self.sel_idx('Sim',simtype,self.c_sim_type)
        print(f'         : cur_sim_type set to {self.cur_sim_type}')
        
        self.c_load_def_paper.Clear()
        self.c_load_def_paper.AppendItems( self.papers('n','l',new_sim_type) )
        self.c_load_def_paper.SetSelection(0)


        try:
            self.hsiz_param_cel.Remove( self.p_cell.vs )
        except AttributeError: # On initial run
            pass

        self.OnSelectPaper(e, paper, fig, newPanel=True)
        self.setup_cell_panel()
        self.hsiz_param_cell.Add( self.p_cell.vs, 0, wx.ALL , border=5 )


    def OnSelectPaper(self,e, paper=None, fig=None, newPanel=False):
        print(f'\nOnSelectPaper: paper={paper}')
        print('cur papers=', self.papers('n','l') )

        print('OnPaperTypeCalling')
        self.cur_paper= new_paper= self.sel_idx('Paper',paper,self.c_load_def_paper)
        print(f'         : cur_paper = {self.cur_paper}')

        self.c_load_def_fig.Clear()
        self.c_load_def_fig.AppendItems(self.figures('n','l',None,new_paper))
        self.c_load_def_fig.SetSelection(0)

        self.OnSelectFigure(e,fig,newPanel)


    def OnSelectFigure(self,e,fig=None,newPanel=False):
        print(f'\nOnSelectFigure: fig={fig}')
        print('cur figs=', self.figures('n','l',None) )

        print('OnFigureTypeCalling')
        self.cur_fig= new_fig= self.sel_idx('Figure',fig,self.c_load_def_fig)
        print(f'         : cur_fig = {self.cur_fig}')

        for b in self.fig_buttons.values():
            self.hsiz_cur_button.Hide(b)

        cur_pg              = myParams[self.cur_sim_type][self.cur_paper][self.cur_fig]
        self.cur_params     = cur_pg['params']
        self.cur_params_f   = cur_pg['fname']
        self.cur_valid_figs = cur_pg['valid_figs']

        self.cur_params_tb_outs= [ p for p in self.cur_params.values() if (p.is_textbox and     p.is_output) ]
        self.cur_params_tb_ins=  [ p for p in self.cur_params.values() if (p.is_textbox and not p.is_output) ]

        self.make_param_groups()

        self.t_sim_current.SetValue( '%s'%self.cur_params_f)

        for fn in self.cur_valid_figs:
            self.hsiz_cur_button.Show(self.fig_buttons['%s %s'%(self.cur_paper,fn)])

        try:
            self.hsiz_param_main.Layout()
            self.vsiz_main.Layout()

            s=self.panel.GetSizer()
            w,h = s.GetMinSize()
            self.panel.SetVirtualSize((w,h))
            #self.frame.Layout()
            #self.frame.Refresh()
            #self.frame.Update()

            if not newPanel:
                self.p_cell.Refresh()

        except AttributeError:
            pass

    def make_param_groups(self):
        self.dialogs = {}
        self.vc_sizers_d = {}
        self.group_gbs_od = collections.OrderedDict()
        rows={}
        for param in self.cur_params.values():
            print('\nmake_param_groups:PARAM:',param.human_name,param.mlvar_name)
            if param.is_in_dialog:
                self.make_set_dialog( param )
                vcs= param.dialog.dlg_vcs
                parent= param.dialog
            else:
                vcs= self.make_vcs( param ) # vertical BoxSizer
                parent= self.panel

            if self.make_set_param_group_gbs( parent, param, vcs ): # Created New GBS
                rows[param.disp_grp] = 1

            try:
                param.row = rows[param.disp_grp]
            except KeyError:
                param.row= 0 # Hidden

            if param.is_button:
                param.wx_button= wx.Button(parent, wx.ID_ANY, label=param.human_name)
                param.wx_button.Bind(wx.EVT_BUTTON, getattr(self, param()[0]))
                param.gbs.Add(param.wx_button, (param.row, 0), (1, 1))#, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
            else:
                if param.is_output:
                    self.make_output( parent, param )
                elif param.is_textbox:
                    self.make_tb( parent, param )
                elif param.is_checkbox:
                    self.make_cb( parent, param )
                elif param.is_choice:
                    self.make_ch( parent, param )
                if not param.is_hidden:
                    param.gbs.Add(param.wx_label,  (param.row, 0), (1, 1), wx.ALIGN_LEFT)#|            wx.ALIGN_CENTER_VERTICAL)
                    param.gbs.Add(param.wx_item,   (param.row, 1), (1, 1), wx.LEFT|wx.RIGHT|wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=5)
                    param.gbs.Layout()

                    rows[param.disp_grp] = param.row + 1

            if param.onval:
                self.on_val_funcs[ param.onval ](new_wx_item=True)

        for d in self.dialogs.values():
            d.Fit()
            d.Layout()

        self.hsiz_param_main.Clear(delete_windows=True)

        for i,(k,vcs) in enumerate(self.vc_sizers_d.items()):
            ''' SP VCS SP VCS CELL OUT '''
            vcs.Layout()
            self.hsiz_param_main.InsertSpacer(i*2,20)
            self.hsiz_param_main.Insert(i*2+1,vcs)
            #self.hsiz_param_main.Insert(i*2,vcs, wx.LEFT | wx.ALIGN_RIGHT, border=30)
            self.hsiz_param_main.Show(vcs)

    def make_vcs(self, param):
        # Vertical Column Sizer for Param Columns
        try:
            return self.vc_sizers_d[param.disp_col]
        except KeyError:
            self.vc_sizers_d[param.disp_col] = wx.BoxSizer(wx.VERTICAL)
            return self.vc_sizers_d[param.disp_col]

    def make_set_dialog(self, param):
        try:
            dlg = self.dialogs[ param.disp_grp ]
        except KeyError:
            dlg = wx.Dialog(None, wx.ID_ANY, 'the '+param.disp_grp[2:])#, style=wx.RESIZE_BORDER)
            dlg.dlg_vcs= wx.BoxSizer(wx.VERTICAL)
            dlg.SetSizer(dlg.dlg_vcs)
            dlg.SetAutoLayout(True)
            dlg.SetMinSize(( 400, 400 )) #TODO move this to after - ceanup with setminsize

            ok_button = wx.Button(dlg, wx.ID_ANY, label='Close')
            ok_button.Bind(wx.EVT_BUTTON, lambda e,dlg=dlg:self.OnDoneEditing(e,dlg))

            self.dialogs[ param.disp_grp ] = dlg

        param.dialog= dlg

    def OnDoneEditing(self,e,dlg):
        dlg.Show(False)

    def make_set_param_group_gbs(self, parent, param, vcs):
        col,group = param.disp_col, param.disp_grp
        if col==None or group==None:
            return False

        try:
            self.group_gbs_od[col]
        except KeyError:
            self.group_gbs_od[col] = collections.OrderedDict()

        try:
            param.gbs = self.group_gbs_od[col][group]
        except (KeyError, NameError):
            param.gbs= self.group_gbs_od[col][group] = wx.GridBagSizer(hgap=15, vgap=2)
            if not param.is_in_dialog:
                param.gbs.Add(fancytext.StaticFancyText( parent, wx.ID_ANY,
                    u'<font weight="bold" color="black" size="12">%s</font>'%param.disp_grp, name=f'SFT:{param.disp_grp}'),
                        (0, 0), (1, 2), wx.ALIGN_LEFT | wx.ALIGN_TOP )

            vcs.Add(param.gbs, 0, wx.TOP | wx.EXPAND | wx.GROW, border=5)
            vcs.AddSpacer(5)
            return True # New GBS Created
        return False

    def make_fancy_label(self, parent, param):
        param.wx_label = fancytext.StaticFancyText(parent, wx.ID_ANY, ('%s'%param.human_name),
             background=wx.Brush((249,249,248,255),wx.SOLID), name=f'SFT:{param.mlvar_name}')

    def update_buffs(self,new_wx_item=False):
        n_buffs= self.cur_params['n_buff']()[0]
        self.show_eq('show_co2_k1'   , True )
        self.show_eq('show_h2co3_pk2', True )
        self.show_eq('show_ha1_pk3'  , n_buffs >= 3)

    def show_eq(self, eq, s):
        eq= self.equations[eq]
        eq['visible'] = s

    def make_cb(self, parent, param ):
        self.make_fancy_label(parent, param)
        param.wx_item= wx.CheckBox( parent, wx.ID_ANY, '' )
        param.wx_item.SetValue(param()[0])
        param.wx_item.Bind(wx.EVT_CHECKBOX, lambda e, param=param: self.OnValChange(e, param))

    def make_ch(self, parent, param ):
        self.make_fancy_label(parent, param)#, db=True)
        param.wx_item= wx.Choice( parent, wx.ID_ANY, choices=param.choices, name='HI' )
        param.wx_item.SetSelection(param.choices.index(str(param()[0])))
        param.wx_item.Bind(wx.EVT_CHOICE, lambda e, param=param: self.OnValChange(e, param))
        def GV():
            return param.wx_item.GetString(param.wx_item.GetSelection())
        param.wx_item.GetValue= GV


    def format_param_list(self, param):
        if param.formatter == '{}' and param.validator in [pos_float, sci_float, reg_float]:
            l = [ np.format_float_positional(v) for v in param() ]
            l = [ np.format_float_positional(v,fractional=False,trim='0') for v in param() ]
        else:
            l = [ param.formatter.format(v)     for v in param() ]
        rv= ', '.join( l )
        return rv

    def make_tb(self, parent, param ):
        self.make_fancy_label(parent, param)
        sz=param.wx_label.GetSize()
        param.wx_item = ColChangeInput(
            parent,
            wx.ID_ANY,
            cci_def_text= self.format_param_list(param),
            cci_size=(300,sz[1]),
            on_enter_func=lambda e, param=param: self.OnValChange(e, param),
            name=f'TC:{param.mlvar_name}',
            linspace=True,
            param=param,
        )

    def set_modified_bg(self,param):
        param.wx_item.SetBackgroundColour('orange')

    def set_regular_bg(self,param):
        param.wx_item.SetBackgroundColour(param.wx_item.def_text_bg_color)

    def make_output(self, parent, param ):
        self.make_fancy_label(parent,param)
        if param.is_textbox:
            sz=param.wx_label.GetSize()
            param.wx_item = wx.TextCtrl( parent, wx.ID_ANY, self.format_param_list(param), size=(200,sz[1]))
        elif param.is_checkbox:
            param.wx_item= wx.CheckBox( parent, wx.ID_ANY, self.format_param_list(param))
        param.wx_item.SetEditable(False)
        param.wx_item.def_text_bg_color = (232,232,232)
        param.wx_item.SetBackgroundColour(param.wx_item.def_text_bg_color)
        param.wx_item.SetForegroundColour((0,0,0))
        param.wx_item.set_modified_bg= lambda param=param: self.set_modified_bg(param)
        param.wx_item.set_regular_bg = lambda param=param: self.set_regular_bg(param)

    def OnMobilities(self,e):
        if self.dialogs['d_Mobilities'].Show():
            pass
        
    def OnBufferReactions(self,e):
        if self.dialogs['d_Buffer Reactions'].Show(): # Get these from the name in the file
            pass

    def OnPermeabilities(self,e):
        if self.dialogs['d_Permeability Across PM'].Show():
            pass

    def mark_modified(self,param):
        try:
            param.wx_item.set_modified_bg()
        except AttributeError:
            pass # not all have this method

    def mark_bad_lengths(self, ps=None):
        ''' list lengths for batch runs '''
        if ps == None:
            ps= self.cur_params_tb_ins
        pvals= [ p() for p in ps ]
        lens = set([1])
        [lens.add(len(vl)) for vl in pvals]

        if len(lens) not in [1,2]: # should only be 2 lengths 1 and some higher batch_len
            for i,p in enumerate(ps):
                if len(p.valstore) != 1:
                    self.mark_modified(p)
            raise InputError('!!!! Wrong number of params!!!!!!!')
        else:
            for i,p in enumerate(ps):
                try: p.wx_item.set_regular_bg()
                except AttributeError: pass
        return lens

    def update_deps_and_outs(self, param):
        for p in set( param.dependents  + self.cur_params_tb_outs ):
            dprint(DDEPS,( 'DEPS: doin: %s'%p.mlvar_name, ))
            if p.set_valstore(p()):
                p.wx_item.SetEditable(True)
                p.wx_item.SetValue(self.format_param_list(p))
                p.wx_item.SetEditable(False)
                p.wx_item.set_regular_bg()
            else:
                self.mark_modified(p)
                self.mark_modified(param)

    def OnValChange(self, e, param):
        ''' event handler for user hitting enter on a field '''
        in_vals = param.wx_item.GetValue()
        dprint(DDEPS,( f'\nOVC: {param.mlvar_name} in_vals={in_vals} {type(in_vals)}', ))
        if param.is_textbox:
            in_val_l= [ v.strip() for v in in_vals.split(',') ]
        elif param.is_checkbox:
            in_val_l= [ in_vals ] #for v in in_vals ] #bool # Only singles now
        elif param.is_choice:
            in_val_l= [ in_vals ]

        bad = True if not param.set_valstore( in_val_l ) else False

        self.mark_bad_lengths()

        if bad:
            self.mark_modified(p)
        else:
            if param.onval:
                self.on_val_funcs[ param.onval ](new_wx_item=False)

            self.update_deps_and_outs(param)

        self.p_cell.Refresh()

    def setup_cell_panel(self):
        try:
            self.p_cell.Destroy()
        except Exception as e:
            pass
        self.p_cell = CellPanel_Oocyte(self)

    def add_shape(self,shape,x,y,pen=None,brush=None,text=None):
        shape.SetX( x )
        shape.SetY( y )
        if pen: shape.SetPen( pen )
        if brush: shape.SetBrush( brush )
        if text:
            for line in text.split('\n'):
                shape.AddText(line)
        self.sc.AddShape(shape)

    def add_lineshape(self,lineshape,ends,pen=None,brush=None,arrow=None):
        lineshape.MakeLineControlPoints(2)
        lineshape.SetEnds( ends[0], ends[1], ends[2], ends[3] )
        if pen: lineshape.SetPen( pen )
        if brush: lineshape.SetBrush( brush )
        if arrow: lineshape.AddArrow( arrow )
        self.sc.AddShape(lineshape)

    def OnSaveCurParams(self, e):
        ''' event-handler - create a parameter file to be stored in the sim directory '''
        self.create_param_files()

    def set_sim_dirs(self,fullpath):
        print('set_sim_dirs: fullpath=', fullpath)
        ''' fullpath default is def_sim_dir, but status is used to ask user '''
        newdir=False

        if not fullpath:
            dlg = wx.DirDialog(self.panel,
                    message="Create/Select Simulation Output Directory",
                    defaultPath='.',
                    style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                fullpath=dlg.GetPath()
            else:
                fullpaht='def_sim_dir'

        if not os.path.isdir(fullpath):
            os.mkdir(fullpath)
            newdir=True

        self.sim_dir_path= fullpath
        if fullpath.endswith(os.sep):
            bn=fullpath[:-1]
        else:
            bn=fullpath
        self.sim_base_name= os.path.basename( bn )
        dprint(DBG_DIRS,'  sim_dir_path :', self.sim_dir_path)
        dprint(DBG_DIRS,'  sim_base_name:', self.sim_base_name)
        self.t_sim_outputf.SetValue( os.path.relpath(self.sim_dir_path) )
        self.t_sim_current.SetValue( self.sim_base_name )
        return newdir

    def create_param_files(self):
        ''' create a parameter file to be stored in the sim directory '''
        batch_len = max(self.mark_bad_lengths())
        dprint(DBG_DIRS,('batch_len=',batch_len))

        #for run_idx in range(self.mark_bad_lengths):
        self.fnl=[]
        for ri in range(batch_len): # ri = run_idx
            name_parts=[]
            vals=[]
            for p in self.cur_params.values():
                print(f'  ri:{ri}: p:{p.mlvar_name}   {p()}')
                pvals = p()

                try:
                    v=pvals[ri]
                except IndexError:
                    print('  IndexError: using 0th')
                    v=pvals[0]

                if not p.is_button:
                    if p.is_choice:
                        if p.is_string:
                            vals.append( '%s = \'%s\''%(p.mlvar_name,v) )
                        else:
                            vals.append( '%s = %s'%(p.mlvar_name,v) )
                    elif p.is_checkbox:
                        vals.append( '%s = %s'%(p.mlvar_name,{ True : 'true', False: 'false' }[v]) )
                    else:
                        if p.formatter == '{}' and p.validator in [pos_float, sci_float, reg_float]:
                            s = np.format_float_positional(v,fractional=False,trim='0')
                        else:
                            s = p.formatter.format(v)
                        if p.is_string:
                            vals.append( '%s = \'%s\''%(p.mlvar_name,s) )
                        else:
                            vals.append( '%s = %s'%(p.mlvar_name,s) )
                    if len(pvals) > 1 and not p.is_output:
                        name_parts.append( '__%s_%s'%(p.mlvar_name,s.replace('.','_')) )

            name_parts = ''.join(name_parts)
            dprint(DBG_DIRS,('nameparts=',name_parts))

            fn=f'{self.sim_base_name}{name_parts}' # Matlab Funcs want the base name only - no path or '.m'

            # Matlab limit 63 char for variable name, which file becomes
            name_end='paramsIn'
            if len(fn)+len(name_end)+1 > 60:
                with open( f'LOG_long_{name_end}.txt', 'a') as logfn:
                    shortfn=fn[:30] +datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                    logfn.write(f'SHORTFILE:{shortfn},FILE:{fn}\n')
                    fn=shortfn

            fp= os.path.join( self.sim_dir_path, f'{fn}_{name_end}.m' )

            if os.path.exists(fp):
                dlg = wx.MessageDialog(None,
                                       "Simulation %s exists do you want to overwrite it?"%fp,
                                       'Overwrite!',
                                       wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_NO:
                    return False

            f = open(fp, 'w')
            flen = len(fp)+7
            f.write('''fprintf(' -> %s\\n')\n'''%('*'*flen))
            f.write('''fprintf('    * In %s *\\n')\n'''%fp)
            f.write('''fprintf('    %s\\n')\n'''%('*'*flen))
            text= ';\n'.join( vals ) + ';\n'
            print( text )
            f.write( text )
            f.close()

            self.fnl.append( fn )

        self.panel.Update()

        return True

    def OnRunSim(self, e):
        ''' run the sim event handler '''
        self.set_sim_dirs( self.myargs.sdp )
        if self.create_param_files():
            self.run_sims()

    def get_run_param(self,ri,pname):
        pvals = self.cur_params[pname]()
        print(f'pvals for {pname} = {pvals}')

        if pname not in self.run_params:
            self.run_params[pname]=[]

        try:
            self.run_params[pname].append( pvals[ri] )
        except IndexError: # occurs when only 1 value for this but many for another prarm
            self.run_params[pname].append( pvals[0] )

    SAVETESTFILES= False
    SAVETESTFILES= True 
    def run_sims(self):
        ''' run the sim '''

        if not self.matlab_eng:
            self.matlab_eng = matlab.engine.start_matlab("-desktop")

        self.reset_run_data()
        time.sleep(1)
        totruns= len(self.fnl)
        for ri,fn in enumerate(self.fnl):
            self.t_sim_current.SetValue( '%s ( %s )'%(self.sim_base_name,fn) )
            self.panel.Update()

            progress_title= 'Simulation Time: (Run %d/%d)'%(ri+1,totruns)
            
            ret_time,ret_data= self.matlab_eng.Simulate(self.cur_sim_type,progress_title, self.sim_dir_path, fn, nargout=2)

            self.run_time.append(np.asarray(ret_time))
            self.run_data.append(np.asarray(ret_data))
            desired_run_params = [\
                'n_in', 'n_out',
                'D', 'D_inf',
                'n_buff', 'pH_out', 'pH_in_init', 'Pm_CO2_input', 'cust_plot_title',
                'CAII_in_flag' , 'CAII_in' , 'A_CAII',
                'CAIV_out_flag', 'CAIV_out', 'A_CAIV',
                'A1tot_in', 'A2tot_in',
                'Buff_pc', 'oos_tort_lambda', 'tort_gamma',
                'tf_CO2on','PlotTitle','OutFile','OutCol','FigProps','Panel', 'SweepVar'
            ]

            didntgetlist=[]
            for rp in desired_run_params:
                try:
                    self.get_run_param(ri,rp)
                except KeyError: # only in 11 12
                    didntgetlist.append(rp)
            print(progress_title)
           
            dl= len(self.run_time[ri])
            f=open(os.path.join( self.sim_dir_path, f'{fn}.csv'),'w')
            [ f.write('%f,%s\n'%(self.run_time[ri][i][0],
                             ','.join(['%f'%v for v in self.run_data[ri][i]]))) for i in range(dl) ]
            f.close()
            
            pickle.dump(self.run_time  , open(self.build_fn('run_time_'  ), 'wb'))
            pickle.dump(self.run_data  , open(self.build_fn('run_data_'  ), 'wb'))
            pickle.dump(self.run_params, open(self.build_fn('run_params_'), 'wb'))

        self.t_fig_runs.Clear()
        numruns = ri+1
        self.t_fig_runs.SetValue('[' + ' '.join([ '%d'%v for v in range(numruns) ]) + ']')

        print('Simulation Completed.')

        if self.myargs.dofig:
            self.OnCreateFigure(None,self.myargs.dofig)

    def build_fn(self, prefix, includepath=True):
        ''' prefix = 'run_time_', 'run_data_', 'run_params_'
        '''
        fn  = f'{prefix}{self.cur_sim_type}_{self.cur_fig}.p'.replace(' ','_').replace(',','_')
        if includepath:
            rfn= os.path.join( self.sim_dir_path, fn )
            print(f'build_fn: {rfn}') 
            return rfn
        else:
            print(f'build_fn: {fn}') 
            return fn

    def extract_fn(self, fn, prefix, includesPath=False):
        ''' prefix = 'run_time_', 'run_data_', 'run_params_'
        '''
        print(f'extract_fn: fn={fn}')
        pgkey=fn.replace(prefix,'').split('.')[0]
        print('  pgkey  :',pgkey)
        simtype = pgkey.split('_Fig')[0]
        print('  simtype:',simtype)
        fig=pgkey.replace(f'{simtype}_','')
        print('  figure :',fig)
        return pgkey, simtype, fig

    def load_sim_data(self):
        self.run_time  = pickle.load( open(self.build_fn('run_time_'  ), 'rb') )
        self.run_data  = pickle.load( open(self.build_fn('run_data_'  ), 'rb') )
        self.run_params= pickle.load( open(self.build_fn('run_params_'), 'rb') )

    def OnLoadSimData(self,e):
        dlg=wx.FileDialog(None, 'Choose Sim Data (run_data) File', wildcard='Sim .p files (*.p)|*.p',
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        pathname = dlg.GetPath()
        print('OLSD: pathname=',pathname)
        self.loadSimData(pathname)

    def loadSimData(self,pathname):
        dirn,fn= os.path.split(pathname)
        if not fn:
            fns= glob.glob(f'{dirn}/run_data_*')
            l= len(fns)
            if l != 1:
                if l == 0:
                    msg=f'Did not find run_data_ file in {dirn}'
                elif l > 1:
                    msg=f'Found multiple run_data_ files in {dirn}'
                dlg = wx.MessageDialog(None, msg, "Sim Data Load Error!", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                return

            fn=fns[0] 
       
        self.set_sim_dirs(dirn)
        print('loadSimData:\n  sdp=',self.sim_dir_path)

        self.load_sim_data()

    def OnLoadParamFile(self, e):
        ''' event_handler - load a parameter file to run NOT IMPLEMENTED '''
        dlg=wx.FileDialog(None, 'Open Custom Parameter File', wildcard='Matlab .m files (*.m)|*.m',
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        pathname = dlg.GetPath()
        with open(pathname,'r') as pfile:
            pflines= pfile.readlines()
            for l in pflines:
                try:
                    mlvar,val = [ v.strip().strip(';') for v in l.split('=') ]
                except ValueError: 
                    continue
                try:
                    p=self.cur_params[mlvar]
                except KeyError: continue

                if (p.is_textbox or p.is_checkbox) and not p.is_output:
                    bad = True if not p.set_valstore( [val] ) else False
                    if bad:
                        self.mark_modified(p)
                    else:
                        self.update_deps_and_outs(p)
                    try:
                        val= { 'true':True, 'false':False }[val]
                    except KeyError: pass

                    if p.is_checkbox:
                        p.wx_item.SetValue( val )
                    elif p.is_textbox:
                        p.wx_item.SetValue(self.format_param_list(p))

        self.mark_bad_lengths()
        self.t_sim_current.SetValue( '%s'%(os.path.relpath(pathname)))

    def fig__custom(self, fp):
        solute_idx      = fp.solute_idx
        shell_str       = fp.shell_str
        time_str        = fp.time_str
        run_str         = fp.run_str
        print('solute_idx:%d  shell_str:%s  time_str:%s  run_str:%s'%(solute_idx, shell_str, time_str, run_str))
        mat_solute_name = self.c_matlab[solute_idx]
        chart_data_type = self.c_ptype[solute_idx]
        sol_vs_X        = fp.versusX

        plot_rows=1
        plot_cols=1
        plot_d={ 'colors'   : (fp.shades,)*plot_rows * plot_cols,
                 'remborder': []  ,} #'tickspos' : 'both', }

        title= '%s vs. %s'%(mat_solute_name,sol_vs_X)
        fig,axs = self.fig_makefig(plot_rows, plot_cols, size=None, title=title, plot_d=plot_d )

        def slice_from_s( str_in, last_idx ):
            print('last_idx=',last_idx)
            ss=re.split(r'[,\s]', str_in)
            ss= [ v for v in ss if v != '' ]
            l=[]
            for vv in ss:
                vs= [int(u) for u in vv.split(':')]
                c=len(vs)
                if c == 3:
                    start,stop,step=vs#[int(u) for u in v.split(':')]
                    print('    ',start,stop,step)
                    l.append(np.arange(start,stop+1,step)) # NOTE: Users??? +1 to make inclusive
                elif c == 2:
                    start,stop=vs#[int(u) for u in v.split(':')]
                    print('    ',start,stop)
                    if start < 0:
                        start=last_idx + start
                    if stop < 0:
                        stop=last_idx + stop
                    print('    ',start,stop)
                    l.append(np.arange(start,stop+1,1)) # NOTE:: Users??? +1 to make inclusive
                elif c == 1:
                    start,=vs
                    print('    ',start)
                    l.append(np.arange(start,start+1))
            print('    l=',l)
            return np.concatenate(l)

        for ri in [0]:#runs:
            print('ri=',ri)
            np_time  = np.array(fp.run_time[ri])[:,0] 
            np_data  = np.array(fp.run_data[ri])
            N        = fp.Ns[ri]
            n_in     = fp.n_ins[ri]
            n_out    = fp.n_outs[ri]
            n_buff   = fp.n_buffs[ri]
            R_cm     = fp.Rs_cm[ri]
            R_inf_cm = fp.R_infs_cm[ri]
            n_runs   = fp.n_runs
            #print(np_time.shape)
            #print(np_data.shape)

            radii_in,radii_out= self.radii_in_out(R_cm,R_inf_cm,n_in,n_out)
            r_plot  = np.concatenate((radii_in,radii_out))
            x_radii=r_plot/10
            # 0:180:1
            # 0:3000:610
            print('shells=')
            shells=slice_from_s(shell_str,None)
            print('    ',shells)
            print('times=')
            times =slice_from_s(time_str, len(np_time))
            print('    ',times)
            print('runs=')
            runs  =slice_from_s(run_str, n_runs)
            print('    ',runs)


            sol_start = N * solute_idx
            sol_memb  = sol_start + n_in
            sol_end   = sol_memb + n_out

            electrode_idx = self.electrode_index_from_um( 50, R_cm, n_in )

            print('np_time=',np_time)
            plot_t = np_time[ times ]
            print('plot_t=',plot_t)
            plot_t = np.insert(np_time,0,-100) # add first point to -infinity (-100)
            #dt     = np.ediff1d( np_time ) #The differences between consecutive elements of an array.

            shells= [ v + sol_start for v in shells ]
            print(shells)

            ax = axs[0,0]
            ax.set_ylabel(mat_solute_name)
            if sol_vs_X=='vt': # vs Time
                print('VTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVT')
                ax.set_xlabel('Time(s)')
                for shell in shells:
                    print('shell=',shell)
                    sol_plot= np_data[times,shell]
                    sol_plot= np.insert(sol_plot,0,sol_plot[0])
                    if chart_data_type == 'pH':
                        sol_plot= self.pH_from_Hplus( sol_plot )

                    ax.plot(plot_t,sol_plot,label='run:%d shell:%d'%(ri,shell))
            if sol_vs_X == 'vs': # vs Shell
                print('VSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVS')
                ax.set_xlabel('Distance(shell)')
                for t in times:
                    print('time=',t)
                    sol_plot= np_data[t,shells]
                    if chart_data_type == 'pH':
                        sol_plot= self.pH_from_Hplus( sol_plot )
                    ax.plot(x_radii,sol_plot,label='run:%d time:%d'%(ri,t))

            ax.legend()
        plt.show()


    def OnCreateFigure(self,e,fig_name,*args):
        print('OnCreateFigure, fig_name=', fig_name, 'args=', args)

        if self.TESTING:
            self.run_time  = pickle.load( open(self.build_fn('run_time_'  ), 'rb') )
            self.run_data  = pickle.load( open(self.build_fn('run_data_'  ), 'rb') )
            self.run_params= pickle.load( open(self.build_fn('run_params_'), 'rb') )

        sim_results= SimResults(self.run_time,self.run_data,self.run_params,self.cur_params)

        exitafter= self.myargs.doexit

        CHART_DEBUGGING=True
        CHART_DEBUGGING=False
        pprint.pp(Figs)
        print('fig_name=',fig_name)
        if fig_name=='custom':
            #self.matlab_eng.create_fig_t_v_x(args[0],args[1],args[2],nargout=0)
            #self.matlab_eng.create_fig_t_v_x(*args,nargout=0)
            FP.versusX=args[0]

            FP.shades= self.shades

            FP.solute_idx = self.c_fig_solute.GetSelection()
            FP.shell_str  = self.t_fig_shells.GetValue()
            FP.time_str   = self.t_fig_times.GetValue()
            FP.run_str    = self.t_fig_runs.GetValue()

            self.fig__custom(FP)

        else:
            if fig_name.startswith('Fig '):
                fig_name=fig_name.removeprefix('Fig ')
            print(f'{self.cur_sim_type}, *** {self.cur_paper}, ### {fig_name}')
            Figs[self.cur_sim_type][self.cur_paper][fig_name](sim_results, CHART_DEBUGGING)

        print('OUT OnCreateFigure, fig_name=', fig_name, 'args=', args)
        if exitafter:
            sys.exit()

class Substance():
    def __init__(self,t):
        self.order       = t[0]  # order in X
        self.matht       = t[1]  # math text string
        self.yunits      = t[2]  # units for y axis
        self.fconv       = t[3]  # conversion function
        self.fig345panel = t[4]  # figure 3 and 4 panel

class ExtractedData:
    ''' single simulation run extracted data storage class '''
    pass

class SimResults():
    def __init__(self,sim_time,sim_data,sim_runparams,curparams):
        self.t = sim_time # from matlab time
        self.d = sim_data # from matlab X
        self.n_runs = len(self.t)
        self.rp= sim_runparams
        self.cp= curparams
        self.edclass=ExtractedData

        self.substances={\
            'CO2'   : Substance((0, 'CO_2'    , 'Concentration (mM)' , lambda x:x        , 0  )),
            'H2CO3' : Substance((1, 'H_2CO_3' , 'Concentration (mM)' , lambda x:x        , 1  )),
            'HA'    : Substance((2, 'HA_1'    , 'Concentration (mM)' , lambda x:x        , 4  )),
            'pH'    : Substance((3, 'pH'      , 'pH'                 , self.pH_from_Hplus, 3  )),
            'HCO3m' : Substance((4, 'HCO_3^-' , 'Concentration (mM)' , lambda x:x        , 2  )),
            'Am'    : Substance((5, 'A^-_1'   , 'Concentration (mM)' , lambda x:x        , 5  )),
        }


        self.eds=[]

    def make_output(self,outfile,indexvarname,indexvar,datadict): # SimResults
        # Output batch data to file
        thisdf= pd.DataFrame( datadict, 
                #{'dpHi'  :dphis,
                # 'delpHs':dphss,
                #},
            index=indexvar,
        )
        print('thisdf=',thisdf)
        thisdf.to_csv(outfile, index=True,index_label=indexvarname)


    def extract(self,extractors,alist=[],klist=[]):# SimResults
        ''' extract time x shell data matrix for a single species from raw sim data
            and store it in an ExtractedData (ed) class for each run

            call with list of extractors and
                      list of lists of args to pass to each extractor and
                      list of dicts of kwargs 
            example:
            sr.extract( [sr.get_solutes], [[shell_depth,3.15]], [{'over':'time'}] )
        '''
        for ri in range(self.n_runs):
            print('ri=',ri)
            self.eds.append( ExtractedData() )
            ed=self.eds[-1]
            ed.np_time = np.array(self.t[ri])[:,0]
            ed.np_data = np.array(self.d[ri])

            for ex,args,kwargs in zip_longest(extractors,alist,klist):
                print(f'->ex {ex}\n  a:{args}\n  k:{kwargs}')
                ex(ri,self.eds[-1],args,kwargs)

    # Data Extractor methods
    def pH_from_Hplus(self, v): # SimResults
        pH      = 3-np.log10(v)
        return pH

    def index_from_R_um(self, ri, R_um):
        ''' R_um is desired radius to return index into X '''

        R_cm = R_um * 1e-4
        radii,radii_in,radii_m,radii_out= self.radii_in_out(ri)
        rad_idx = int(np.nonzero(radii >= R_cm)[0][0]) # nonzero returns tuple of arrays for each dimension of input
        print('rad_idx=',rad_idx, '  rad[elec_idx]=',radii[rad_idx])
        print('RI:\n',radii_in)
        print('RO:\n',radii_out)
        return rad_idx

    def radii_in_out(self,ri=0): # SimResults
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        N        = n_in + n_out +1
        D        = self.rp['D'         ][ri]
        D_inf    = self.rp['D_inf'     ][ri]
        R_m_cm   = (D/10) / 2
        R_inf_cm = (D_inf/10) / 2

        radii_in = (R_m_cm/n_in)            *np.array(range(0,n_in))
        radii_m  =  R_m_cm                  *np.array([1])
        radii_out= ((R_inf_cm-R_m_cm)/n_out)*np.array(range(1,n_out+1)) + R_m_cm
        radii     = np.concatenate((radii_in,radii_m,radii_out))
        return radii,radii_in,radii_m,radii_out

    def get_subst_idxs(self,sol_order,n_buff,N,n_in,n_out): # SimResults
        sol_start = sol_order * N
        sol_memb  = sol_start + n_in
        sol_end   = sol_memb + n_out
        #print('ss:',sol_start,'sm:',sol_memb,'se:',sol_end)
        return sol_start, sol_memb, sol_end


    def get_run_var(self,ri,vname): # SimResults
        if ri == -1:
            return self.rp[vname]
        else:
            return self.rp[vname][ri]

    def get_substance(self,ri,ed,substance,*args,**kwargs): # SimResults
        n_buff   = self.rp['n_buff'    ][ri]
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        N        = n_in + n_out +1

        try:
            tf_CO2on = self.rp['tf_CO2on'  ][ri]
            ed.idx_tfCO2on= np.nonzero(ed.np_time >= tf_CO2on)[0][0]
        except KeyError:
            pass
        ed.substance={}

        for sp in substance:
            solv= self.substances[sp]
            sol_order = solv.order + (n_buff - 2)
            ss,sm,se = self.get_subst_idxs(sol_order,n_buff,N,n_in,n_out)

            ed.substance[sp]= solv.fconv( ed.np_data[:, ss : se+1 ] )
    
    def get_pHi(self,ri,ed,depth_um=50,timelo=None,timehi=None):
        D        = self.rp['D'         ][ri]
        R_cm     = (D/10) / 2
        n_in     = self.rp['n_in'      ][ri]

        ed.pHi= ed.substance['pH'][:,0:n_in]

        R_um= (R_cm*10000) - depth_um
        shellidx = self.index_from_R_um( ri, R_um )
        hprint('pHi:',ri,shellidx)
        return ed.pHi[:,shellidx]

    def get_pHs(self,ri,ed,depth_um=0):
        D        = self.rp['D'         ][ri]
        R_cm     = (D/10) / 2
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        N        = n_in + n_out +1

        ed.pHs= ed.substance['pH'][:,n_in+1:N]

        R_um= (R_cm*10000) - depth_um
        shellidx = self.index_from_R_um( ri, R_um )
        shellidxpHs= shellidx - n_in
        hprint('pHs:',ri,shellidxpHs)
        return ed.pHs[:,shellidxpHs]

    def get_dpHi_dt(self,ri,ed,pHi,*args,**kwargs): # SimResults
        ''' extractor for dpHi/dt related data
            data is broken into 2 parts
            pHi_I = CO2 Influx ( see ModelParams )
            pHi_E = CO2 Efflux ( see ModelParams )
        '''
        print(f'get_dpHi_dt ri={ri} args={args}  kwargs={kwargs}')
        try:
            idx= ed.idx_tfCO2on                   # 1873
        except AttributeError:
            idx=-1

        t_I   = ed.np_time[   0 : idx ]  # 0 - 1872 ( t= 0 - 1195.148
        t_E   = ed.np_time[ idx :  -1 ]  # 1873

        pHi_I = pHi[   0 : idx ]           #
        pHi_E = pHi[ idx :  -1 ]           #

        if pHi_I.size: # not empty
            dpHi_dt_I, max_dpHi_dt_idx_I, max_dpHi_dt_I= self.get_ddata_dt(pHi_I, t_I)
            ed.max_dpHi_dt_I     =       max_dpHi_dt_I
            ed.max_dpHi_dt_idx_I =       max_dpHi_dt_idx_I
            ed.max_dpHi_dt_t_I   =   t_I[max_dpHi_dt_idx_I]
            ed.pH_at_max_dpHi_I  = pHi_I[max_dpHi_dt_idx_I]

            y1= pHi_I[0]
            y2= ed.pH_at_max_dpHi_I
            t2= ed.max_dpHi_dt_t_I
            m = ed.max_dpHi_dt_I
            #(y2 - y1) = m * (t2 - t1)
            t1 = ((y2 - y1) /  m) - t2
            ed.time_delay_pHi= t1

        if pHi_E.size: # not empty
            dpHi_dt_E, max_dpHi_dt_idx_E, max_dpHi_dt_E= self.get_ddata_dt(pHi_E, t_E)
            ed.max_dpHi_dt_E     =       max_dpHi_dt_E
            ed.max_dpHi_dt_idx_E =       max_dpHi_dt_idx_E
            ed.max_dpHi_dt_t_E   =   t_E[max_dpHi_dt_idx_E]
            ed.pH_at_max_dpHi_E  = pHi_E[max_dpHi_dt_idx_E]

    def get_delpHs(self,ri,ed,pHs,*args,**kwargs): # SimResults
        ''' extractor for delta pHs related data
            data is broken into 2 parts, Influx and Efflux
        '''
        try:
            idx= ed.idx_tfCO2on
        except AttributeError:
            idx= -1
        t_I   = ed.np_time   [   0 : idx ]
        t_E   = ed.np_time   [ idx :  -1 ]
        pHs_I = pHs[   0 : idx ]
        pHs_E = pHs[ idx :  -1 ]

        if pHs_I.size:
            ed.max_pHs_I= max(pHs_I)
            ed.min_pHs_I= pHs_I[0]
            ed.del_pHs_I= ed.max_pHs_I - ed.min_pHs_I
            #print(f'max  {ed.max_pHs_I}  min {ed.min_pHs_I}  del: {ed.del_pHs_I}')

            ed.max_pHs_idx_I = np.argmax(pHs_I)
            startingpoint= 0.0
            ed.time_to_peak_pHs= ed.np_time[ed.max_pHs_idx_I] - startingpoint

        if pHs_E.size:
            ed.max_pHs_E= pHs_E[0]
            ed.min_pHs_E= min(pHs_E)
            ed.del_pHs_E= ed.max_pHs_E - ed.min_pHs_E

    def get_ddata_dt(self,data,t): # SimResults
        dt    = np.ediff1d( t )
        dd    = np.ediff1d( data )
        dd_dt = dd/dt
        max_dd_idx  = np.argmax(np.absolute(dd_dt))
        max_dd      = dd_dt[max_dd_idx]
        print('max_dd=',max_dd)
        return dd_dt, max_dd_idx, max_dd

    
import argparse
def doit():
    parser=argparse.ArgumentParser(
        prog='mgui.py',
        description='Modelling GUI',
        epilog='''Run Simulations, Generate Data, Create standard graphs from papers
Example:
python mgui.py --simtype=JTB --paper=0 --figure=Fig_11_12 --sdp=testJ12 --dofig=12 --dosim
''')
    cwd=os.getcwd()
    parser.add_argument('--testing', action='store_true', default=False, help='Are we TESTING. (generally no)')
    parser.add_argument('--simtype', type=str, help='SimType 0:JTB 1:AJP(future) name:"AJP"')
    parser.add_argument('--paper'  , type=str, help='Paper 0:JTB_2012 1:AJP_2014(future) or name "JTB_2012"')
    parser.add_argument('--figure' , type=str, help='Figure Number (order in dropdown) or dropdown name "Fig_6"')
    parser.add_argument('--sdp'    , type=str, help='Path to set, either new or Previous Simulation Data (run_data file) to load')
    parser.add_argument('--dosim'  , action='store_true', default=False, help='Auto Run Sim (requires --simtype --sdp and --figure)')
    parser.add_argument('--dofig'  , type=str, help='Create figure, number or Button Name (requires --sdp with data in that folder, and --figure)')
    parser.add_argument('--doexit' , action='store_true', default=False, help='Exit after Figure generation. (rarely used, only in batch runs)')
    appargs=parser.parse_args()
    print('testing=',appargs.testing)
    print('simtype=',appargs.simtype)
    print('paper=',appargs.paper)
    print('figure=',appargs.figure)
    if appargs.sdp:
        if appargs.sdp[-1] != os.sep:
            appargs.sdp=appargs.sdp+os.sep
    print('simdatapath=',appargs.sdp)

    ModelApp( appargs )

if __name__ == '__main__':
    doit()

''' Matlab 2024a
    linux:
        make venv and activate
        in /usr/local/MATLAB/R2024a/extern/engines/python
        sudo chown -R <username> dist
        sudo mkdir build
        sudo chown -R <username> build/
        pip install .

older notes: python3 setup.py build --build-base="~/matbuild" install

From Matlab site http://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
Verify Python and MATLAB Installations

First, verify that your system has the correct versions of Python and MATLAB. Then, find the path to the MATLAB folder. You need the path to the MATLAB folder to install the MATLAB Engine for Python.

    Check that Python is installed on your system and that you can run Python at the operating system prompt.

    Find the path to the MATLAB folder. Start MATLAB and type matlabroot in the command window. Copy the path returned by matlabroot.
'''
