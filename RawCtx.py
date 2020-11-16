#create one file with raw matched ctx


from GridDataHolder import GridDataHolder
from Utils import Utils
from db import ConfUtil

class RawCtx:
    grid_data_holders = []
    def __init__(self, filename, fp):
        self.filename= filename
        self.graph_data_holder = GridDataHolder(filename)
        self.graph_data_holder.parse_saulog()
        for dn in self.graph_data_holder.data_nodes:
            RawCtx.grid_data_holders.append(dn)
        self._name = None 
        self._fp = fp

    
    def output_raw(self):
        RawCtx.grid_data_holders.sort()
        for gdh in RawCtx.grid_data_holders:
            for o in gdh.opt:
                self._fp.write("{}".format(o))



