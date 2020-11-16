import csv 

from GridDataHolder import GridDataHolder
from Utils import Utils
from db import ConfUtil


class CsvContext:

    class ConstFields:
        FrameNumber = 'Frame Number'
        Time = 'Time'
        GroupName = 'Group Name'
        Field = 'Field'
        Value = 'Value'
        SauInstance = 'Instance'


    def __init__(self, filename):
        self.graph_data_holder = GridDataHolder(filename)
        self.graph_data_holder.parse_statistics()
        self._name = None 
        if Utils.unix() == False:
            tmp = filename.split("\\")
        else:
            tmp = filename.split("/")            
        if (len(tmp) > 0):
            self._name = tmp[len(tmp)-1].split('.')[0]
        else :
            self._name = filename.split('.')[0]
        if Utils.unix() == False:
            self._name = self._name.replace("\\", ".")
        else:
            self._name = self._name.replace("/", ".")
        self.csv_name = "-".join(tmp[1:])
        self.csv_file = open("{}.csv".format(self.csv_name), 'w', newline='')
        fieldnames = [CsvContext.ConstFields.FrameNumber, CsvContext.ConstFields.Time, \
            CsvContext.ConstFields.SauInstance, CsvContext.ConstFields.GroupName, \
                CsvContext.ConstFields.Field,CsvContext.ConstFields.Value]

        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)
        self.csv_writer.writeheader()
    
    def gen_csv(self):
        i = 0
        for gdh in self.graph_data_holder.data_nodes:
            i+=1
            for o in gdh.opt:
                matched = o.matched_data()
                for item in matched:
                    for j in range(0, len(item.data)):
                        if ConfUtil.ORMMixer.ShortExport is True:
                            self.csv_writer.writerow({CsvContext.ConstFields.FrameNumber:i, \
                            CsvContext.ConstFields.Time : str(item.time), \
                            CsvContext.ConstFields.SauInstance : self._name, \
                            CsvContext.ConstFields.GroupName : item.group, \
                            CsvContext.ConstFields.Field : item.name,  \
                            CsvContext.ConstFields.Value : item.data[len(item.data)-1]})
                            break
                        else:        
                            self.csv_writer.writerow({CsvContext.ConstFields.FrameNumber:i, \
                            CsvContext.ConstFields.Time : str(item.time), \
                            CsvContext.ConstFields.SauInstance : self._name, \
                            CsvContext.ConstFields.GroupName : item.group, \
                            CsvContext.ConstFields.Field : item.name,  \
                            CsvContext.ConstFields.Value : item.data[j]})
        self.csv_file.close()


if __name__ == "__main__":
    from db import  ConfUtil

    ConfUtil.load("db_ver1.json")
    ConfUtil.dumpall()
    csv = CsvContext("C:\\Users\\izapryanov.VERINT\\Desktop\\Samba\\Moov\\215.1.17.31\\MoovSAU_IM_2_2\\SAUStatMoovSAU_IM_2_2.ltf")
    csv.gen_csv()
    pass

