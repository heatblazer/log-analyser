#the application wrapper 
# connect data grid with drawing context here...
import sys
import os
import time
import datetime

from progress.bar import Bar
from db import ConfUtil
from GraphContext import GraphCtx # plotting 
from CsvContext import CsvContext #no ui mode


class Application:
    """
    Bring all blocks  toghether.
    1. Load .json
    2. use arguments to select mode
    3. prepare csv builder
    4. begin loading data to DataGrid
    5. start plot or export needed data
    """

    def __init__(self, jsonfile):
        ConfUtil.load(jsonfile)
        self.headers = []
        self.graphs = []
        self.log_folder = None
        ConfUtil.dumpall()


    def Run(self, uimode=True):
        """app runner"""
        import Utils 

        self.log_folder = ConfUtil.path()
        self.files = Utils.Utils.get_filesr(ConfUtil.path()) #array of files 
        os.chdir(self.log_folder)
        bar = Bar("Processing:", max=int(len(self.files) * 2))
        a = datetime.datetime.now()        
        if uimode == True:
            GraphCtx.SIZE = len(self.files)
            GraphCtx.load()
            for l in self.files:
                bar.next()
                self.graphs.append(GraphCtx(l))            
            for graph in self.graphs:
                bar.next()
                graph.plot_parsers()                                
            GraphCtx.plot_all()
        else: #no ui mode
            for l in self.files:
                bar.next()
                self.graphs.append(CsvContext(l))
            for gp in self.graphs:
                bar.next()
                gp.gen_csv()
                
        bar.finish()                    
        b = datetime.datetime.now()
        print ("\r\nTime elapsed : {}".format(b-a))
 
 #application entry point - not unit test !
if __name__ == "__main__":
    print (os.name)
    jsonfile = None 
    if len(sys.argv) >= 2:
        jsonfile = sys.argv[len(sys.argv)-1]
    else:
        jsonfile = "db_ver1.json"

    app = Application(jsonfile)
    app.Run(ConfUtil.ORMMixer.UiMode)
