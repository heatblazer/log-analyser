import json

class ConfUtil(object):
    db = {}
    Fname = str()
    Orms = []
    class ORMMixer:
        MainSeparator = "PacketRouter Statistics:"
        MainDelimiter = ":"
        OptSeparator = "====="
        TimeSeparator = "CAT_PDFE_STATISTICS"
        UiMode = False
        ShortExport = False
        TimeSort = True
        def __init__(self, entry_name, field_name, fields , plugin, mandatory):
            self.group_name = entry_name
            self.field_name = field_name
            self.fields = fields
            self.plugin = plugin
            self.mandatory = mandatory
        
        def group(self):
            return ConfUtil.db[self.group_name]

        def mode(self):
            return self.plugin

        def __str__(self):
            return "[group:{}]:[field:{}]:[fields:{}]:[plugin:{}]:[mandatory:{}]".format(self.group_name, self.field_name, self.fields, self.plugin, self.mandatory)     

    @staticmethod
    def load(fname):
        ConfUtil.Fname = fname
        try:
            with open(fname, 'r') as fp:
                ConfUtil.db = json.load(fp)    
                fp.close()
                return True
        except:
            return False
        pass

    @staticmethod
    def exists(name):
        if name in ConfUtil.db:
            return True
        return False

    @staticmethod
    def dumpall():
        if ConfUtil.db is not None:
            for record in ConfUtil.db:
                if record == "path":
                    continue
                elif record == "main-separator":
                    ConfUtil.ORMMixer.MainSeparator = ConfUtil.db['main-separator']
                    continue
                elif record == "main-delimiter":
                    ConfUtil.ORMMixer.MainDelimiter = ConfUtil.db['main-delimiter']
                    continue
                elif record == "ui-mode":
                    ConfUtil.ORMMixer.UiMode = ConfUtil.db['ui-mode']
                    continue
                elif record == "opt-separator":
                    ConfUtil.ORMMixer.OptSeparator = ConfUtil.db['opt-separator']
                    continue
                elif record == "time-sort":
                    ConfUtil.ORMMixer.TimeSort = ConfUtil.db['time-sort']
                    continue
                elif record == "time-delimiter":
                    ConfUtil.ORMMixer.TimeSeparator = ConfUtil.db['time-delimiter']
                    continue
                elif record == "short-export":
                    ConfUtil.ORMMixer.ShortExport = ConfUtil.db['short-export']
                    continue
                d = ConfUtil.db[record]
                plg = False
                mandatory = False
                if 'plugin'  in d:
                    plg = d['plugin']
                elif 'mandatory' in d:
                    mandatory = d['mandatory']

                ConfUtil.Orms.append(ConfUtil.ORMMixer(record, d["name"], d["fields"], plg, mandatory))


    @staticmethod
    def path():
        if ConfUtil.db is not None:
            return ConfUtil.db["path"]

    @staticmethod
    def grp_name():
        return ConfUtil.db["group_name"]

    @staticmethod
    def fname():
        return ConfUtil.Fname


if __name__ == "__main__":
    #unit test
    ConfUtil.load('db_ver1.json')
    ConfUtil.dumpall() 
    print(ConfUtil.path())

    for kv in ConfUtil.Orms:
        print("MODE: ", kv.mode())
        print(str(kv))
    pass
