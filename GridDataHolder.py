from TimeParser import TimeFraction
from GenericParser import GenericParser
from db import ConfUtil

class GridDataHolder:
    """data aggregator for the log file, separates data from render context"""

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


    def __init__(self, filename=None):
        """init parsers here"""            
        self.data_nodes =[]
        main_separator = ConfUtil.ORMMixer.MainSeparator
        with open(filename, "r") as fp:
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
                if main_separator in line or last is True:
                    datagrid.append([])
                    datagrid[len(datagrid)-1].append(main_separator)
                    while True:
                        next = fp.readline()
                        if next == "\n" or next == "\r" or next == "\r\n":
                            continue
                        if main_separator in next:
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
                if TimeFraction.valid(tfract) and ConfUtil.ORMMixer.TimeSort is True:
                    gp.set_time(tfract)
                if gp.valid():
                    optparsers.append(gp)
                else:
                    print ("Parser {} missmatch for file {}".format(str(gp), filename))
                #removed log for dirty data

            if TimeFraction.valid(tfract) and ConfUtil.ORMMixer.TimeSort is True:
                datNode = GridDataHolder.DataNode(tfract, optparsers)
                self.data_nodes.append(datNode)

        #sort by time :)         
        self.data_nodes.sort()
        pass
