from datetime import datetime


tdata = ["21/03/20 14:35:23.454 () CAT_PDFE_STATISTICS Informational StatisticsCollector.cpp 36"]

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


    def __init__(self, data=None):
        self.day = None
        self.hour = None
        self.utc = -1
        self.spl = None
        if data is not None:
            for d in data:
                if "CAT_PDFE_STATISTICS" in d:
                    self.spl = d.split(" ")
                    if len(self.spl) > 1:
                        self.day = TimeFraction.Day(self.spl[0])
                        self.hour = TimeFraction.Hour(self.spl[1])
                        if self.day is not None and self.hour is not None:
                            a = datetime.strptime(str(self), "%Y-%m-%dT%H:%M:%S.%fZ")
                            self.utc = int(unix_time_millis(a))


    def __eq__(self, other):
        return self.utc == other.utc        

    def __lt__(self, other):
        return self.utc < other.utc

    def __str__(self):
        s = "{0}T{1}Z".format(str(self.day), str(self.hour))
        return s



#unit test
if __name__ == "__main__":

    tf1 = TimeFraction(tdata)
    tf2 = TimeFraction(tdata)
    
    TimeFraction.valid(tf1)
    TimeFraction.valid(tf2)

    if tf1 == tf2:
        print("Same")
    else:
        print("Not same")



