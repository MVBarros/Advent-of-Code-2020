import collections as col

def bin_or(x, y):
    return '{0:b}'.format(int(x, 2) | int(y, 2))

def bin_and(x, y):
    return '{0:b}'.format(int(x, 2) & int(y, 2))

class Mask:
    def __init__(self, val):
        self.__zero = "".join(('1' if char == 'X' else char for char in val))
        self.__one = "".join(('0' if char == 'X' else char for char in val))

    def apply(self, val):
        return bin_or(self.__one, bin_and(val, self.__zero))

class MemInstruction:
    def __init__(self, lval, rval):
        self.__addr = int(lval[4:-1])
        self.__val = f'{int(rval):036b}'

    def exec(self, state):
        state.mem[self.__addr] = state.mask.apply(self.__val)

class MaskInstruction:
    def __init__(self, rval):
        self.__mask = Mask(rval)
        
    def exec(self, state):
        state.mask = self.__mask 
        
class State:
    def __init__(self):
        self.__mask = None
        self.mem = {}
    
    def mem_sum(self):
        return sum([int(val, 2) for val in state.mem.values()])

def parse_line(line):
    lval, rval = line.split(' = ')
    if lval == 'mask':
        return MaskInstruction(rval)
    else:
        return MemInstruction(lval, rval)
    
def parse_input(path):
    with open(path, 'r') as fd:
        return[parse_line(line[:-1]) for line in fd]
  
def process_program(state, program):
    for instr in program:
        instr.exec(state)
        
program = parse_input('input.txt')
    
state = State()

process_program(state, program)

print(state.mem_sum())
