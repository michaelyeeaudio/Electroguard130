import tkinter as tk
import cmath
import sys
import logging
import math
import time
from decimal import Decimal

#exec(open('images.py').read())

class ini(tk.Frame):
    def __init__(self, parent, size=100, **options):
        tk.Frame.__init__(self, parent, padx=0, pady=0, borderwidth=0,highlightthickness=0,
                          **options)
        self.size = size
    def to_absolute(self, x, y):
        return x + self.size/2, y + self.size/2
		
def draw_dial(canv,x0,y0,degree, t,r):
    this_color = "#00A2E8"
    xr=x0
    yr=y0
    angle = math.radians(degree)
    cos_val = math.cos(angle)
    sin_val = math.sin(angle)
    dy=r*sin_val
    dx=r*cos_val
    dx2=t*sin_val
    dy2=t*cos_val
    mlx=xr+dx
    mly=yr-dy
    mrx=xr-dx
    mry=yr+dy
    px=xr+dx2
    py=yr+dy2
    xy = x0-r,y0-r,x0+1*r,y0+1*r
    xyz = mlx,mly,px,py,mrx,mry
    canv.delete('dial')
    canv.create_arc(xy,start=degree,extent=180,fill=this_color,tags=('dial', 'one', 'two', 'three', 'four'))
    canv.create_polygon(xyz, fill=this_color,tags=('dial', 'two'))
    canv.create_oval(xr-5,yr-5,xr+5,yr+5,fil=this_color,tags=('dial', 'three'))
    canv.create_line(xr,yr,px,py,fill="light gray",tags=('dial', 'four'))
    
class DrawGauge2(ini):
    def __init__(self, parent,
                 max_value: (float, int)=100.0,
                 min_value: (float, int)= 0.0,
                 size: (float, int)=100,
                 img_data: str=None,
                 bg_col:str='blue',unit: str=None,bg_sel=1,
                 **options):
        super().__init__(parent, size=size, **options)
#        print("DrawGauge2")
        self.max_value = float(max_value)
        self.min_value = float(min_value)
        self.size = size
        self.bg_col = bg_col
        self.bg_sel=bg_sel
        self.unit = '' if not unit else unit
        self.canvas = tk.Canvas(self, width=self.size, height=self.size-self.size/12,bg=bg_col,highlightthickness=0)
        self.canvas.grid(row=0)
        if self.bg_sel == 1:
            self.draw_background1()
        else:
            self.draw_background2()
        self.draw_tick()
        initial_value = 0.0
        self.set_value(initial_value)
        
    def draw_background1(self, divisions=100):
#        print("draw background1")
        self.canvas.create_arc(self.size/50, self.size/50, self.size-self.size/50, self.size-self.size/50,
                       style="arc",width=4,start=-61, extent=300,
                       outline = "gray")#style=tk.PIESLICE
        self.canvas.create_arc(self.size/20, self.size/20, self.size-self.size/20, self.size-self.size/20,
                       style="arc",width=self.size/20,start=-61, extent=300,
                       outline = "light gray")#style=tk.PIESLICE

        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               style="arc",width=self.size/9,start=-61, extent=91,
                               outline = "red2")#style=tk.PIESLICE
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               width=self.size/9,style="arc",start=150, extent=90,
                               outline = "orange")
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5, font=("Arial",int(self.size/18),'bold'),fill="white", text='')

        
    def draw_background2(self, divisions=100):
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6, self.size-self.size/6,
                               style="arc",width=self.size/10,start=30, extent=36,
#                               style="arc",width=self.size/10,start=-61, extent=61,
                               outline = "red")#style=tk.PIESLICE
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6, self.size-self.size/6,
#                                style="arc",width=self.size/10,start=65, extent=61,
                               style="arc",width=self.size/10,start=65, extent=55,
#                               width=self.size/10,style="arc", start=0, extent=60,
                               outline = "green")
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6, self.size-self.size/6,
                               width=self.size/10,style="arc",start=120, extent=20,
#                               width=self.size/10,style="arc",start=60, extent=60,
                               outline = "yellow")
#         self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6, self.size-self.size/6,
#                                width=self.size/10,style="arc",start=120, extent=60,
#                                outline = "light green")
        self.canvas.create_arc(self.size/6, self.size/6, self.size-self.size/6, self.size-self.size/6,
                               width=self.size/10,style="arc",start=137, extent=13,
#                               width=self.size/10,style="arc",start=180, extent=60,
                               outline = "red")
        self.readout = self.canvas.create_text(self.size/5,.9*self.size/4, font=("Arial",int(self.size/30),'bold'),fill="white", text='over',angle=50)
        self.readout = self.canvas.create_text(.79*self.size,0.85*self.size/4, font=("Arial",int(self.size/30),'bold'),fill="white", text='under',angle=-50)
        self.readout = self.canvas.create_text(.5*self.size,.09*self.size, font=("Arial",int(self.size/30),'bold'),fill="white", text='safe',angle=0)
        
    def draw_tick(self,divisions=50):
#    def draw_tick(self,divisions=100):
        inner_tick_radius = int((self.size-self.size/9) * 0.35)
        outer_tick_radius = int((self.size-self.size/9) * 0.45)
        label = self.unit
        self.canvas.create_text(self.size/2,1.8*self.size/3, font=("Arial",int(self.size/24)),fill="white", text=label,angle=0)
        label = 'Protection Level'
        self.canvas.create_text(self.size/2,self.size/30, font=("Arial",int(self.size/24),'bold'),fill="light blue", text=label,angle=0)
#        self.canvas.create_text(self.size/2,3*self.size/5, font=("Arial",int(self.size/18),'bold'),fill="light blue", text=label,angle=0)
        self.readout = self.canvas.create_text(self.size/2,3*self.size/5, font=("Arial",int(self.size/18),'bold'),fill="white", text='')
        inner_tick_radius2 = int((self.size-self.size/9) * 0.48)
        outer_tick_radius2 = int((self.size-self.size/9) * 0.50)
        inner_tick_radius3 = int((self.size-self.size/9) * 0.3)
        outer_tick_radius3 = int((self.size-self.size/9) * 0.35)
        for tick in range(divisions+1):
            angle_in_radians = (14 * cmath.pi / 12.0)+ (2 * tick/divisions * (cmath.pi / 3.0))
#            print("angle = ", angle_in_radians)
            inner_point = cmath.rect(inner_tick_radius, angle_in_radians)
            outer_point = cmath.rect(outer_tick_radius, angle_in_radians)
            if (tick%10) == 0:
                self.canvas.create_line(
                    *self.to_absolute(inner_point.real, inner_point.imag),
                    *self.to_absolute(outer_point.real, outer_point.imag),
                    width=2,fill='blue')
            else:
#                print("tick%10 else")
                inner_point3 = cmath.rect(inner_tick_radius3, angle_in_radians)
                outer_point3 = cmath.rect(outer_tick_radius3, angle_in_radians)
                self.canvas.create_line(
                    *self.to_absolute(inner_point3.real, inner_point3.imag),
                    *self.to_absolute(outer_point3.real, outer_point3.imag),
                    width=1,fill='black')
#             if (tick%100) == 0:
#                 inner_point2 = cmath.rect(inner_tick_radius2, angle_in_radians)
#                 outer_point2 = cmath.rect(outer_tick_radius2, angle_in_radians)
#                 x= outer_point2.real + self.size/2
#                 y= outer_point2.imag + self.size/2
#            #     label = str(int(self.min_value + tick * (self.max_value-self.min_value)/100))
#                 label = str(float(self.min_value + tick * (self.max_value-self.min_value)/100))
#                 self.canvas.create_text(x,y, font=("Arial",int(self.size/25)),fill="white", text=label)   #these are the numbers around the edge
#                 
    def set_value(self, number: (float, int)):
#        print("set_value")
        org_number = number
        number = number if number <= self.max_value else self.max_value
        number = number if number > self.min_value else self.min_value
#        degree = 30.0 + (number- self.min_value) / (self.max_value - self.min_value) * 300.0
        degree = 120 + ((number- self.min_value) / (self.max_value - self.min_value) * 120.0)
#        degree = 180 is up 0 is down
        draw_dial(self.canvas,self.size/2,self.size/2,-1*degree,self.size/3,8)
#        print("number = \n", number)
        label = str('%.3f' % (org_number/1000))
        self.canvas.delete(self.readout)
        self.readout = self.canvas.create_text(self.size/2,3.3*self.size/6, font=("Arial",int(self.size/24)),fill="white", text=label,angle=0)

class DrawGauge3(ini):
    def __init__(self, parent,
                 max_value: (float, int)=100.0,
                 min_value: (float, int)= 0.0,
                 size: (float, int)=100,
                 img_data: str=None,
                 bg_col:str='blue',unit: str=None,bg_sel=1,
                 **options):
        super().__init__(parent, size=size, **options)
        print("DrawGauge3")
        self.max_value = float(max_value)
        self.min_value = float(min_value)
        self.size = size
        self.bg_col = bg_col
        self.unit = '' if not unit else unit
        self.canvas = tk.Canvas(self, width=self.size, height=3*self.size/5,bg=bg_col,highlightthickness=0)
        self.canvas.grid(row=0)
        self.bg_sel = bg_sel
        if self.bg_sel ==1:
            self.draw_background1()
        else:
            self.draw_background2()
        self.draw_tick()
        initial_value = 0.0
        self.set_value(initial_value)
    
    def draw_background1(self, divisions=100):
#        print("background1")
        self.canvas.create_arc(self.size/50, self.size/50, self.size-self.size/50, self.size-self.size/50,
                       style="arc",width=4,start=0, extent=180,
                       outline = "gray")#style=tk.PIESLICE
        self.canvas.create_arc(self.size/20, self.size/20, self.size-self.size/20, self.size-self.size/20,
                       style="arc",width=self.size/20,start=0, extent=180,
                       outline = "light gray")#style=tk.PIESLICE
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               style="arc",width=self.size/9,start=0, extent=60,
                               outline = "orange")#style=tk.PIESLICE
        good_color = "#00A2E8"
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               width=self.size/9,style="arc",start=60, extent=60,
                               outline = good_color)
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               width=self.size/9,style="arc",start=120, extent=60,
                               outline = "light green")
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5, font=("Arial",int(self.size/18),'bold'),fill="white", text='')
    
    def draw_background2(self, divisions=100):
#        print("background2")
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               style="arc",width=self.size/9,start=0, extent=60,
                               outline = "orange")#style=tk.PIESLICE
        good_color = "#00A2E8"
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               width=self.size/9,style="arc",start=60, extent=60,
                               outline = good_color)
        self.canvas.create_arc(self.size/7, self.size/7, self.size-self.size/7, self.size-self.size/7,
                               width=self.size/9,style="arc",start=120, extent=60,
                               outline = "light green")
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5, font=("Arial",int(self.size/18),'bold'),fill="white", text='')

    def draw_tick(self, divisions=100):
#        print("Draw_Tick")
        inner_tick_radius = int((self.size-self.size/9) * 0.35)
        outer_tick_radius = int((self.size-self.size/9) * 0.45)
        label = self.unit
        self.canvas.create_text(self.size/2,3*self.size/10, font=("Arial",int(self.size/28)),fill="red", text=label,angle=0)
#        label = 'Ardiotech'
#        self.canvas.create_text(self.size/2,4*self.size/10, font=("Arial",int(self.size/18),'bold'),fill="light blue", text=label,angle=0)
        self.readout = self.canvas.create_text(self.size/2,4*self.size/5, font=("Arial",int(self.size/18),'bold'),fill="dark blue", text='')
        inner_tick_radius2 = int((self.size-self.size/9) * 0.48)
        outer_tick_radius2 = int((self.size-self.size/9) * 0.50)
        inner_tick_radius3 = int((self.size-self.size/9) * 0.35)
        outer_tick_radius3 = int((self.size-self.size/9) * 0.40)

        for tick in range(divisions+1):
            angle_in_radians = (cmath.pi)+ tick/divisions * cmath.pi
            inner_point = cmath.rect(inner_tick_radius, angle_in_radians)
            outer_point = cmath.rect(outer_tick_radius, angle_in_radians)
            

            if (tick%10) == 0:
                self.canvas.create_line(
                    *self.to_absolute(inner_point.real, inner_point.imag),
                    *self.to_absolute(outer_point.real, outer_point.imag),
                    width=2,fill='blue')
            else:
                inner_point3 = cmath.rect(inner_tick_radius3, angle_in_radians)
                outer_point3 = cmath.rect(outer_tick_radius3, angle_in_radians)
                self.canvas.create_line(
                    *self.to_absolute(inner_point3.real, inner_point3.imag),
                    *self.to_absolute(outer_point3.real, outer_point3.imag),
                    width=1,fill='light blue')
            if (tick%10) == 0:
                inner_point2 = cmath.rect(inner_tick_radius2, angle_in_radians)
                outer_point2 = cmath.rect(outer_tick_radius2, angle_in_radians)
                x= outer_point2.real + self.size/2
                y= outer_point2.imag + self.size/2
                label = str(int(self.min_value + tick * (self.max_value-self.min_value)/100))
                self.canvas.create_text(x,y, font=("Arial",int(self.size/25)),fill="white", text=label)
    def set_value(self, number: (float, int)):
#        print("set_value")
        number = number if number <= self.max_value else self.max_value
        number = number if number > self.min_value else self.min_value
        degree = (number- self.min_value) / (self.max_value - self.min_value) * 180.0
#        degree = 90.0 + (number- self.min_value) / (self.max_value - self.min_value) * 180.0
        draw_dial(self.canvas,self.size/2,self.size/2,-1*degree,self.size/3,8)
        label = str('%.2f' % number)
        self.canvas.delete(self.readout)
        self.readout = self.canvas.create_text(self.size/3-5,self.size/2+5, font=("Arial",int(self.size/16),'bold'),fill="white", text=label,angle=0)
