import copy
import operator

operator_lookup_table = {'+': operator.add, '-': operator.sub } 

def load_input(path):
    with open(path, 'r') as fd:
        return [line[:-1] for line in fd] # -1 needed here to remove trailling newline

def exec_nop(operand, state):
    state['ip'] += 1
    

def exec_acc(operand, state):
    operator = operand[0]
    val = int(operand[1:])
    state['acc'] = operator_lookup_table[operator](state['acc'], val)
    state['ip'] += 1
    

def exec_jmp(operand, state):
    operator = operand[0]
    val = int(operand[1:])
    state['ip'] = operator_lookup_table[operator](state['ip'], val)
    

instr_lookup_table = {'nop': exec_nop, 'acc': exec_acc, 'jmp': exec_jmp}

def exec_line(line, state):
    instr, operand = line.split(' ')
    instr_lookup_table[instr](operand, state)
    
def is_state_repeated(state, executed_instrs):
    return state['ip'] in executed_instrs

def has_program_terminated(program, state):
    return state['ip'] == len(program)

def execution_should_continue(program, state, executed_instrs):
    state_repeated_cond = is_state_repeated(state, executed_instrs)
    program_terminated_cond = has_program_terminated(program, state)
    return not (state_repeated_cond or program_terminated_cond)

def exec(program):
    state = {'acc': 0, 'ip': 0}
    executed_instrs = set()
    while execution_should_continue(program, state, executed_instrs):
        executed_instrs.add(state['ip'])
        line = program[state['ip']]
        exec_line(line, state)
    return state

def is_jmp_instr(line):
    return line[0:3] == 'jmp'

def is_nop_instr(line):
    return line[0:3] == 'nop'

def get_matching_lines(program, matching_func):
    return [line_no for line_no, line in enumerate(program) if matching_func(line)]
    
def replace_line_instr(program, line_no, new_instr):
    program = copy.deepcopy(program)
    program[line_no] = new_instr + program[line_no][3:]
    return program

def test_corruption(program, matching_func, replace_instruction):
    jmp_lines = get_matching_lines(program, matching_func)
    for line_no in jmp_lines:
        new_program = replace_line_instr(program, line_no, replace_instruction)
        state = exec(new_program)
        if has_program_terminated(new_program, state):
            return state
    return None
        
program = load_input('input.txt')

print(exec(program))

print(test_corruption(program, is_nop_instr, 'jmp'))
print(test_corruption(program, is_jmp_instr, 'nop'))