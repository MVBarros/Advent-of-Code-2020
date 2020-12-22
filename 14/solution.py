import itertools

def bin_or(x: str, y: str) -> str:
    return '{0:036b}'.format(int(x, 2) | int(y, 2))

def bin_and(x: str, y: str) -> str:
    return '{0:036b}'.format(int(x, 2) & int(y, 2))

class AbstractMask:
    def __init__(self, val: str):
        pass 
    
    def apply(self, val: str) -> list:
        pass

class NullMask(AbstractMask):
    def __init__(self, val: str):
        return

    def apply(self, val: str) -> list:
        return val

class Mask(AbstractMask):
    def __init__(self, val: str):
        self.__zero = "".join(('1' if char == 'X' else char for char in val))
        self.__one = "".join(('0' if char == 'X' else char for char in val))

    def apply(self, val: str) -> list:
        return [bin_or(self.__one, bin_and(val, self.__zero))]

class AddrMask(AbstractMask):
    def __init__(self, val: str):
        self.__x = "".join(('0' if char != 'X' else char for char in val))
        self.__one = "".join(('0' if char != '1' else char for char in val))

    def apply(self, val: str) -> list:
        val = bin_or(self.__one, val)
        val = "".join((x_val if x_val == 'X' else val for x_val, val in zip(self.__x, val)))
        return self._get_all_possible_addrs(val)
    
    def _get_all_possible_addrs(self, val: str) -> list:
        for i, char in enumerate(val):
            if char == 'X':
                prefixes = [val[:i] + '0',  val[:i] + '1']
                suffixes = [s for s in self._get_all_possible_addrs(val[i+1:])]
                return [val for val in itertools.product(prefixes, suffixes)]
        return [val]

class State:
    def __init__(self):
        self.__mask = NullMask("")
        self.mem = dict()
    
    def mem_sum(self) -> int:
        return sum([int(val, 2) for val in state.mem.values()])

class AbstractMaskDecoder:
    def __init__(self):
        pass

    def decode(self, state: State, rval: str):
        pass

class MaskDecoder(AbstractMaskDecoder):
    def __init__(self):
        return

    def decode(self, state: State, rval: str):
        state.mask = Mask(rval) 

class AddrMaskDecoder(AbstractMaskDecoder):
    def __init__(self):
        return
    
    def decode(self, state: State, rval: str):
        state.mask = AddrMask(rval)

class AbstractMemDecoder:
    def __init__(self):
        pass

    def decode(self, state: State, lval: str, rval: str):
        pass

class MemDecoder(AbstractMemDecoder):
    def __init__(self):
        return

    def decode(self, state: State, lval: str, rval: str):
        addr = f'{int(lval[4:-1]):036b}'
        val = f'{int(rval):036b}'
        for val in state.mask.apply(val):
            state.mem[addr] = val

class AddrMemDecoder(AbstractMemDecoder):
    def __init__(self):
        return

    def decode(self, state: State, lval: str, rval: str):
        addr = f'{int(lval[4:-1]):036b}'
        val = f'{int(rval):036b}'
        for addr in state.mask.apply(addr):
            state.mem[addr] = val            

class InstructionDecoder:
    def __init__(self, mem_decoder: AbstractMemDecoder, mask_decoder: AbstractMaskDecoder):
        self.__mem_decoder = mem_decoder
        self.__mask_decoder = mask_decoder
    
    def decode(self, state: State, instruction: str):
        lval, rval = instruction.split(' = ')
        if lval == 'mask':
            self.__mask_decoder.decode(state, rval)
        else:
            self.__mem_decoder.decode(state, lval, rval)

def parse_input(path: str) -> list:
    with open(path, 'r') as fd:
        return[line[:-1] for line in fd]
  
def process_program(state: State, program: list, decoder: InstructionDecoder):
    for instr in program:
        decoder.decode(state, instr)
        
program = parse_input('input.txt')
    
state = State()
decoder = InstructionDecoder(MemDecoder(), MaskDecoder())
process_program(state, program, decoder)

print(state.mem_sum())

state = State()
decoder = InstructionDecoder(AddrMemDecoder(), AddrMaskDecoder())
process_program(state, program, decoder)

print(state.mem_sum())
