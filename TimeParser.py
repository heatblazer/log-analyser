from datetime import datetime
from db import ConfUtil
from DynamicExpression import DynamicEx


tdata = [
"14/04/20 03:56:00.898 (00) CAT_PDFE_STATISTICS Informational StatisticsCollector.cpp 36",
"PdfeLoggerSAU131_IM_SN_VoIP12/11/20 11:20:48.096 (00) CAT_PDFE_SDK_INIT Informational SdkStunRTP::EventsHandlerTCP::OnStaticConn 83 [7796711]: New connection for Application VoIP TCP [conn: 10.164.85.30:45376 - 64.233.164.188:5228",
"PdfeLoggerSAU149_IM_SN_VoIP	SdkStunRTP::EventsHandlerTCP::HandleTlsData	210	12/09/20 19:00:57.208 (00)	CAT_PDFE_SDK_LOGICS	Informational	2504	5320",
"PdfeLoggerSAU149_IM_SN_VoIP SdkStunRTP::EventsHandlerTCP::HandleTlsData	210		CAT_PDFE_SDK_LOGICS	Informational	250412/09/20 19:19:54.158 (00)	5320",
"PdfeLoggerSAU149_IM_SN_VoIP	SdkStunRTP::EventsHandlerTCP::HandleTlsData	210	12/09/20 19:19:54.158 (00)	CAT_PDFE_SDK_LOGICS	Informational	2504	5320",
"PdfeLoggerSAU149_IM_SN_VoIP	12/09/20 19:19:54.158 (00) SdkStunRTP::EventsHandlerTCP::HandleTlsData	210		CAT_PDFE_SDK_LOGICS	Informational	2504	5320",
"12/09/20 19:19:54.158 (00) PdfeLoggerSAU149_IM_SN_VoIP	 SdkStunRTP::EventsHandlerTCP::HandleTlsData	210		CAT_PDFE_SDK_LOGICS	Informational	2504	5320"
]

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return int(unix_time(dt) * 1000)



class TimeFraction:

    monthslookup = {
        1 : "01",
        2 : "02", 
        3 : "03", 
        4 : "04", 
        5 : "05",
        6 : "06",
        7 : "07",
        8 : "08",
        9 : "09",
        10 : "10",
        11 : "11",
        12 : "12" 
    }

    @staticmethod
    def valid(tf):
        return tf.utc > 0


#    dynamic_arr = [DynamicEx.Digit(), DynamicEx.Digit(), DynamicEx.Separator(), 
#                DynamicEx.Digit(), DynamicEx.Digit(), DynamicEx.Separator(), 
#                DynamicEx.Digit(), DynamicEx.Digit(), DynamicEx.Separator(), 
#                DynamicEx.Digit(), DynamicEx.Digit(), DynamicEx.Separator(':'), 
#                DynamicEx.Digit(), DynamicEx.Digit(), DynamicEx.Separator(':'), 
#                DynamicEx.Digit(), DynamicEx.Digit(), DynamicEx.Separator()]

    class Day:

        def __init__(self, data=None):
            if data is not None:
                spl = data.split("/")
                if len(spl) == 3:
                    self.day = int (spl[0])
                    self.month = int(spl[1])
                    self.year = int(spl[2])
        
        def __eq__(self, other):
            if self.day == other.day and self.month == other.month and self.year == other.year:
                return True
            return False

        def __lt__(self, other):
            if self.day < other.day or self.month < other.month or self.year < other.year:
                return True
            return False
        
        def __str__(self):
            return "20{0}-{1}-{2}".format(self.year, TimeFraction.monthslookup[self.month], self.day)



    class Hour:

        def __init__(self, data=None):
            self.original = data
            if data is not None:
                spl = data.split(":")
                if len(spl) >= 3:
                    self.hour = int (spl[0])
                    self.minute = int(spl[1])
                    self.secunds = int(float(spl[2]))

        def __eq__(self, other):
            if self.hour == other.hour and self.minute == other.minute and self.secunds == other.secunds:
                return True
            return False

        def __lt__(self, other):
            pass 
        
        def __str__(self):
            return self.original

    TimeOffset = -1

    dynamic_expr = None

    def __init__(self, data=None):
        if TimeFraction.dynamic_expr is None:
            TimeFraction.dynamic_expr = DynamicEx()
        ############################################################
        self.day = None
        self.hour = None
        self.utc = -1
        self.spl = None
        self.ok = True
        for d in data:
            timestr = TimeFraction.dynamic_expr.match(d)
            if timestr is not None:
                s = timestr.split(" ")#self.spl[c].split(" ")
                self.day = TimeFraction.Day(s[0])
                self.hour = TimeFraction.Hour(s[1])
                if self.day is not None and self.hour is not None:
                    a = datetime.strptime(str(self), "%Y-%m-%dT%H:%M:%SZ")
                    self.utc = int(unix_time_millis(a))
                break      


    def __eq__(self, other):
        return self.utc == other.utc        

    def __lt__(self, other):
        return self.utc < other.utc

    def __str__(self):
        s = "{0}T{1}Z".format(str(self.day), str(self.hour))
        return s



#unit test
if __name__ == "__main__":

    ConfUtil.load("db_ver1.json")
    ConfUtil.dumpall()



    tf1 = TimeFraction(tdata)
    tf2 = TimeFraction(tdata)
    
    if TimeFraction.valid(tf1) and TimeFraction.valid(tf2):

        if tf1 == tf2:
            print("Same")
        else:
            print("Not same")

