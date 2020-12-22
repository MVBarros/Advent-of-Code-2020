import collections as col
import itertools

def bin_or(x, y):
    return '{0:036b}'.format(int(x, 2) | int(y, 2))

class Mask:
    def __init__(self, val):
        self.__x = "".join(('0' if char != 'X' else char for char in val))
        self.__one = "".join(('0' if char != '1' else char for char in val))

    def apply(self, val):
        val = bin_or(self.__one, val)
        val = "".join((x_val if x_val == 'X' else val for x_val, val in zip(self.__x, val)))
        return self._get_all_possible_addrs(val)
    
    def _get_all_possible_addrs(self, val):
        for i, char in enumerate(val):
            if char == 'X':
                prefixes = [val[:i] + '0',  val[:i] + '1']
                suffixes = [s for s in self._get_all_possible_addrs(val[i+1:])]
                return [val for val in itertools.product(prefixes, suffixes)]
        return [val]

class MemInstruction:
    def __init__(self, lval, rval):
        self.__addr = f'{int(lval[4:-1]):036b}'
        self.__val = f'{int(rval):036b}'

    def exec(self, state):
        for addr in state.mask.apply(self.__addr):
            state.mem[addr] = self.__val    
        
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
