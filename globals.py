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
            code.append(f"mul @{self.addr} #{other} @{t.addr}")
        elif isinstance(other, type(self)):
            code.append(f"mul @{self.addr} @{other.addr} @{t.addr}")
        return t
    def __add__(self, other):
        global numvars
        t = Variable(numvars)
        numvars += 1
        if isinstance(other, int):
            code.append(f"add @{self.addr} #{other} @{t.addr}")
        elif isinstance(other, type(self)):
            code.append(f"add @{self.addr} @{other.addr} @{t.addr}")
        return t
    
class Storage:
    def __init__(self):
        pass
    def __getitem__(self, key):
        global numvars
        v = Variable(numvars)
        code.append(f"load #{v.addr} #{key}")
        numvars += 1
        return v
    def __setitem__(self, key, value: Variable):
        code.append(f"store #{value.addr} #{key}")

storage = Storage()

def to_uint256(i: int):
    return i.to_bytes(32, "big")

def dump_code():
    bytecode = []
    def process_argument(arg):
        bytecode.append("7F")
        if arg.startswith("#"):
            bytecode.append(to_uint256(int(arg[1:])).hex())
        elif arg.startswith("@"):
            bytecode.append(to_uint256(32*int(arg[1:])).hex())
            bytecode.append("51")
    def process_argument2(arg):
        bytecode.append("7F")
        if arg.startswith("#"):
            bytecode.append(to_uint256(32*int(arg[1:])).hex())
        elif arg.startswith("@"):
            bytecode.append(to_uint256(32*int(arg[1:])).hex())
            bytecode.append("51")
    def dest_argument(arg):
        if arg.startswith("@"):
            bytecode.append("7F")
            bytecode.append(to_uint256(32*int(arg[1:])).hex())
            bytecode.append("52")

            
    for line in code:
        op = line.split()
        if op[0] == "add":
            process_argument(op[1])
            process_argument(op[2])
            bytecode.append("01")
            dest_argument(op[3])
        elif op[0] == "mul":
            process_argument(op[1])
            process_argument(op[2])
            bytecode.append("02")
            dest_argument(op[3])
        elif op[0] == "load":
            process_argument2(op[2])
            bytecode.append("54") # SLOAD
            process_argument2(op[1])
            bytecode.append("52") # MSTORE
        elif op[0] == "store":
            process_argument2(op[1])
            bytecode.append("51") # MLOAD
            process_argument2(op[2])
            bytecode.append("55") # SSTORE
    
    # process_argument("#0")
    # process_argument("#0")
    # bytecode.append("F3") # RETURN
    bytecode.append("00") # STOP

    return ''.join(bytecode)