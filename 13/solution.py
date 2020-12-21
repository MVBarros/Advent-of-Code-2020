import math
from sympy import Matrix
from diophantine import solve

def load_bus_line(line):
    buses = {}
    line_elements = line.split(',')
    for count, el in enumerate(line_elements):
        if el != 'x':
            buses[int(el)] = count
    return buses

def load_input(path):
    with open(path, 'r') as fd:
        departure_time = int(fd.readline()[:-1])
        buses = load_bus_line(fd.readline())
        return departure_time, buses

def is_multiple(num, base):
    return not num % base

def first_multiple_at_least(min, base):
    return base * (math.ceil((min / base)))

def get_earliest_bus(departure, buses):
    return min(((first_multiple_at_least(departure, interval), interval) for interval in buses))

def build_diophantine_system(buses):
    system = []
    expected = []
    for i, first in enumerate(buses):
            equation = [0] * len(buses) + [-1] # extra dimension for t
            equation[i] = first
            system.append(equation)
            expected.append(buses[first])
    return (system, expected)

def solve_diophantine_system(system, expected): 
    system = Matrix(system)
    expected = Matrix(expected)
    return solve(system, expected)
    
departure_time, buses = load_input('input.txt')

print(get_earliest_bus(departure_time, buses))

system, expected = build_diophantine_system(buses)

print(solve_diophantine_system(system, expected))
