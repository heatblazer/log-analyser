#graph context
import os
from math import sqrt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import numpy as np
import time
import datetime
import threading
from GridDataHolder import GridDataHolder
from matplotlib.widgets import Slider


class GraphCtx:
    GROWS = 1
    GCOLS = 1
    CNT = 0
    SIZE = 0
    Figure = plt.figure()
    ax = []

    #TODO: confiugre it dynamically 
    Colormap = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', '#e377c2', '#bcbd22', '#e377c2', '#17becf']
    
    @staticmethod
    def plot_all():
        
#       plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=2,ncol=1, mode="expand", borderaxespad=0.)
        #plt.legend(bbox_to_anchor=(-GraphCtx.GCOLS, 1., 0., GraphCtx.GROWS+1), loc=1,ncol=1, mode="expand", borderaxespad=0.)
        plt.legend(bbox_to_anchor=(1,0), loc="lower right", bbox_transform=GraphCtx.Figure.transFigure, ncol=3)
        plt.show() 

    @staticmethod
    def load():
        def rowcol(size):
            i = 0
            j = 0
            t = size
            while (i <= size):
                size -= 3
                j += 1

            print(t / j)
            print(j)
            GraphCtx.GROWS = 3 
            GraphCtx.GCOLS = j - 1
            coef = GraphCtx.SIZE - (GraphCtx.GROWS * GraphCtx.GCOLS)
            GraphCtx.GCOLS += coef
            pass

        if GraphCtx.SIZE == 1:
            GraphCtx.GROWS = GraphCtx.GCOLS = 1
        else:
            rowcol(GraphCtx.SIZE)

        for i in range(0, GraphCtx.SIZE):
            GraphCtx.ax.append(GraphCtx.Figure.add_subplot(GraphCtx.GROWS, GraphCtx.GCOLS, i+1))
        
        font = None 

        if GraphCtx.SIZE <= 9:
            font = {'family' : 'normal',
                    'size'   : 12}
        elif GraphCtx.SIZE >= 12:
            font = {'family' : 'normal',
                    'size'   : 8}

        matplotlib.rc('font', **font)
 


    def __init__(self, filename=None):
        #now separates data from rendering context, so data not dependant on matpltlib, pandas, etc...
        self.graph_data_holder = GridDataHolder(filename)
        self.graph_data_holder.parse_statistics()
        self._name = None #filename.split(".")[0]
        tmp = filename.split("\\")
        if (len(tmp) > 0):
            self._name = tmp[len(tmp)-1].split('.')[0]
        else :
            self._name = filename.split('.')[0]



    def plot_parsers(self):
        x = []
        y = {}
        xidx = 0
        if True: #no normals
            for dn in self.graph_data_holder.data_nodes:
                for kv in dn.opt:
                    for kv2 in kv.matched:
                        if kv2 not in y:
                            y[kv2] = []
                        y[kv2].append(kv.matched[kv2][len(kv.matched[kv2])-1])
                
                x.append(xidx)
                xidx+=1
            ################################################
        colcnt = 0
        for assocarr in y:
            if len(y[assocarr]) != len(x): # will not plot if x axis not corresponding to y
                continue
            plt.subplots_adjust(hspace=0.40)
            GraphCtx.ax[GraphCtx.CNT].grid(True)
            GraphCtx.ax[GraphCtx.CNT].set_title(self._name)
            GraphCtx.ax[GraphCtx.CNT].plot(x, y[assocarr], GraphCtx.Colormap[colcnt % len(GraphCtx.Colormap)], label=assocarr)
            colcnt += 1

        GraphCtx.CNT+=1
            
