from TimeParser import TimeFraction
from GenericParser import GenericParser
from db import ConfUtil
from threading import Thread

class GridDataHolder:
    """data aggregator for the log file, separates data from render context"""

    class AddIf:

        def __init__(self):
            pass

        def __call__(self):
            pass



    class DataNode:
        """data node to put desired data for parsing.
        Minimum is time fraction so we can sort cyclic files.
        No need to find EOF also 
        """
        def __init__(self, time_, opt_=[]):
            self.time = time_
            self.opt = opt_

        def __eq__(self, rhs):
            return self.time == rhs.time


        def __lt__(self, rhs):
            return self.time < rhs.time


    def __init__(self, filename=None, sau_stat=True):
        """init parsers here"""     
        self.filename = filename       
        self.data_nodes =[]
        self.main_separator = ConfUtil.ORMMixer.MainSeparator
    

    def data(self):
        return self.data_nodes


    def parse_saulog(self, add_if=None):
        with open(self.filename, "r") as fp:
            lines = 0
            grid = []
            #don't do recursion! on huge file python interpreter max depth exceeds 3000 calls on stack!
            while True:
                line = fp.readline()                
                if not line:
                    break
                if line == "\n" or line == "\r":
                    continue
                lines += 1
                if self.main_separator in line:
                    bStop = False
                    while bStop is False:
                        next = fp.readline()                        
                        if next == "\n" or next == "\r" or next == "\r\n":
                            continue
                        if not next or self.main_separator in next: 
                            break
                        for kv in ConfUtil.Orms:
                            if kv.field_name in next:
                                grid.append([])
                                grid[len(grid)-1].append(line)
                                grid[len(grid)-1].append(next)
                                bStop = True
                                break
            
            for d in grid:
                tf = TimeFraction(d)
                if TimeFraction.valid(tf):
                    self.data_nodes.append(GridDataHolder.DataNode(tf, d))
                else:
                    print("Invalid!!!")
                    break
            #self.data_nodes.sort()
            


    def parse_statistics(self):
        with open(self.filename, "r") as fp:
            lines = 0
            datagrid = []
            last = False
            #don't do recursion! on huge file python interpreter max depth exceeds 3000 calls on stack!
            while True:
                line = fp.readline()                
                if not line:
                    break
                if line == "\n" or line == "\r":
                    continue
                lines += 1
                if self.main_separator in line or last is True:
                    datagrid.append([])
                    #datagrid[len(datagrid)-1].append(main_separator)
                    while True:
                        next = fp.readline()
                        if next == "\n" or next == "\r" or next == "\r\n":
                            continue
                        if self.main_separator in next:
                            last = True    
                            break
                        if not next: 
                            break
                        datagrid[len(datagrid)-1].append(next)
        for elem in datagrid:
            tfract = TimeFraction(elem)
            optparsers = []
            for orm in ConfUtil.Orms:
                gp = GenericParser(elem, orm)
                if TimeFraction.valid(tfract):
                    gp.set_time(tfract)
                if gp.valid():
                    optparsers.append(gp)
                else:
                    continue
                #removed log for dirty data

            if TimeFraction.valid(tfract):
                datNode = GridDataHolder.DataNode(tfract, optparsers)
                self.data_nodes.append(datNode)

        #sort by time :)         
        self.data_nodes.sort()
