
from db import ConfUtil

class GenericParser:
    
    @staticmethod
    def extract_digit(data):
        #also clamps floats...
        dgt = []
        for d in data:
            if d == '\t' or d == '\n' or d == '\r' or d == ' ':
                continue
            if d >= '0' and d <= '9':
                dgt.append(d)
            else:
                break
        res = int("".join(dgt))
        return res


    def __init__(self, data, jobj=None):

        def exact_match(src, dst):
            if len(src) != len(dst):
                return False
            for i in range(0, len(src)):
                if src[i] != dst[i]:
                    return False
            return True

        self.filed_name = jobj.field_name
        self.matchers = jobj.fields
        self.group = jobj.group_name
        self.plugin = jobj.plugin
        self.matched = {}
        self.array = []
        i, j = 0, 0
        while i <  len(data):            
            if self.filed_name not in data[i] and i < len(data):
                i += 1
                continue           
            j = i+1 #save one check by moving ptr to the next element
            while j < len(data):# and self.filed_name not in data[j]:
                if j+1 >= len(data):
                    break            

                if data[j+1].find(ConfUtil.ORMMixer.OptSeparator) is not -1: #!strstr(...)
                    break

                spl = data[j].split(ConfUtil.ORMMixer.MainDelimiter)                
                if len(spl) > 1:
                    spl[0] = spl[0].replace("\n", "").replace("\r", "").replace("\t", "").rstrip(' ')
                    for m in self.matchers:
                        if exact_match(m, spl[0]) is True:
                            if m not in self.matched:
                                self.matched[m] = []
                                self.matched[m].append(GenericParser.extract_digit(spl[1]))
                            else:
                                self.matched[m].append(GenericParser.extract_digit(spl[1]))                    
                j += 1
            i += 1


    def set_time(self, time):
        self.time = time

    def valid(self):        
        """check if we have a valid fields. Ex. No field can be None"""
        if ConfUtil.ORMMixer.UiMode is True:
            for m in self.matchers:
                if m not in self.matched:
                    return False
        return True

    def matched_data(self):
        class tmpnode:
            def __init__(self, group, time, name, data):
                self.name = name
                self.data = data
                self.group = group
                self.time = time

        tmpnodes = []
        for m in self.matched:
            #print("[{}]: {},{}".format(self.group, m,self.matched[m]))
            tmpnodes.append(tmpnode(self.group, self.time, m, self.matched[m]))
        return tmpnodes

    def __str__(self):
        return "[GParser @ field:{}, matchers: {}, plugin: {}]".format(self.filed_name,self.matchers,self.plugin)
    