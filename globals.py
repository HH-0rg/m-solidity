code = []
numvars = 0

class Variable:
    def __init__(self, addr):
        self.addr = addr
    def __mul__(self, other):
        global numvars
        t = Variable(numvars)
        numvars += 1
        if isinstance(other, int):
            code.append(f"mul @{self.addr}, #{other}, @{t.addr}") # mul @self.addr, #other, @t.addr
        elif isinstance(other, type(self)):
            code.append(f"mul @{self.addr}, @{other.addr}, @{t.addr}") # mul @self.addr, @other.addr, @t.addr
        return t
    def __add__(self, other):
        global numvars
        t = Variable(numvars)
        numvars += 1
        if isinstance(other, int):
            code.append(f"add @{self.addr}, #{other}, @{t.addr}") # mul @self.addr, #other, @t.addr
        elif isinstance(other, type(self)):
            code.append(f"add @{self.addr}, @{other.addr}, @{t.addr}") # mul @self.addr, @other.addr, @t.addr
        return t
    
class Storage:
    def __init__(self):
        pass
    def __getitem__(self, key):
        global numvars
        v = Variable(numvars)
        code.append(f"load @{v.addr}, {key}") # load @v.addr, key
        numvars += 1
        return v
    def __setitem__(self, key, value: Variable):
        code.append(f"store @{value.addr}, {key}") # store @value.addr, key

storage = Storage()

def dump_code():
    for line in code:
        print(line)