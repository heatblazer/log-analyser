#sau log parser

import sys
import os
import time
import datetime

from TimeParser import TimeFraction
from GenericParser import GenericParser

from progress.bar import Bar
from db import ConfUtil
from RawCtx import RawCtx



class SauLogApp:
    def __init__(self, jsonfile):
        ConfUtil.load(jsonfile)
        self.headers = []
        self.graphs = []
        self.log_folder = None
        ConfUtil.dumpall()

    def Run(self):

        """app runner"""
        import Utils 

        self.log_folder = ConfUtil.path()
        self.files = Utils.Utils.get_filesr(ConfUtil.path()) #array of files 
        os.chdir(self.log_folder)
        bar = Bar("Processing:", max=int(len(self.files) * 2))
        begin = datetime.datetime.now()        
        self._fp = open(ConfUtil.ORMMixer.SauLogFileTrunk, "w")
        for f in self.files:
            bar.next()
            self.raw_ctx = RawCtx(f, self._fp)
        
        self.raw_ctx.output_raw()
        self._fp.close()
        #<<<
        bar.finish()                    
        end = datetime.datetime.now()
        print ("\r\nTime elapsed : {}".format(end-begin))



if __name__ == "__main__":
    salog = SauLogApp("db_ver1.json")
    salog.Run()