
from db import ConfUtil

# given the dynamic expr from json file:   
# "dynamic-expression" : ["int", "int", "del/", "int", "int", "del/", "int", "int", "del ", "char", "char", "del:", "char", "char", "del:", "char", "char"],
# you will get 3 matches
# with low complexity !
TEST_DATA = "11/22/33 11:aa:bb some stuff that wont be matched  and other [11/11/11 Ca:Ab:ZZ] that will be! And that will be appended 22/11/33 aa:vv:zz and this one too 00/11/22 AA:XX:LL and nothing more..."


class DynamicEx:

    class Digit:
        def __init__(self):
            self.ok = True

        def __call__(self, d):
            return (d>='0' and d <='9') 
        
    class Separator:
        def __init__(self, sep='/'):
            self.opt = sep

        def __call__(self, d):
            return  d == self.opt or d == ' ' or d=='\t'

    class Char:

        def __call__(self, d):
            return d >= 'A' and d <= 'z'

        
    def __init__(self):
        self.dynamic_expressions = []
        dexpr = None
        for kv in ConfUtil.Orms:
            if kv.dyn_expr is not None:
                dexpr = kv.dyn_expr
        if dexpr is not None:
            for expr in dexpr:
                if expr == "int":
                    self.dynamic_expressions.append(DynamicEx.Digit())
                elif expr == "char":
                    self.dynamic_expressions.append(DynamicEx.Char())
                elif "del" in expr:
                    self.dynamic_expressions.append(DynamicEx.Separator(expr[len(expr)-1]))
                else:
                    pass

    def match(self, data):
        if data is None:
            return None

        i, j  = 0, 0
        s = str()
#        m = []
        while i < len(data):
            while j < len(self.dynamic_expressions) and i < len(data):
                if self.dynamic_expressions[j](data[i]) is False:
                    s = str()
                    break
                else:
                    s += data[i]
                    i+=1
                j+=1
            if j == len(self.dynamic_expressions):
                return s
#                j = 0
#                m.append(s)
#                s = str()
            j = 0
            i+=1
            
        return None
# <<<

#unit test !
if __name__ == "__main__":
    ConfUtil.load("db_ver1.json")
    ConfUtil.dumpall()

    d = DynamicEx()
    b = True

    i, j  = 0, 0
    s = str()
    m = []
    while i < len(TEST_DATA):
        while j < len(d.dynamic_expressions) and i < len(TEST_DATA):
            if d.dynamic_expressions[j](TEST_DATA[i]) is False:
                s = str()
                break
            else:
                s += TEST_DATA[i]
                i+=1
            j+=1
        if j == len(d.dynamic_expressions):
            j = 0
            m.append(s)
            s = str()
        j = 0
        i+=1

    print("Matches:  ", m)
    pass