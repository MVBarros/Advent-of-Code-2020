import math

DIRECTION_VECTORS = {'N': (0,1), 'S': (0, -1), 'W': (-1, 0), 'E': (1, 0)}

def load_input(path):
    with open(path, 'r') as fd:
        return [line[:-1] for line in fd] # -1 needed here to revector_add trailling newline

def vector_add(v1, v2):
    return tuple(el1 + el2 for el1, el2 in zip(v1, v2))

def vector_multiply(vector, units):
    return tuple(units * el for el in vector)

def vector_rotate(vector, angle):
    x, y = vector
    angle =  math.radians(angle)
    return (round(math.cos(angle) * x - math.sin(angle) * y), round(math.sin(angle) * x + math.cos(angle) * y))

def process_component_rotation(ship, component, angle):
    ship[component] = vector_rotate(ship[component], angle)

def process_component_direction(ship, direction, units, component):
    delta = vector_multiply(direction, units)
    ship[component] = vector_add(ship[component], delta)

def process_component_forward(ship, units, component):
    delta = vector_multiply(ship[component], units)
    ship['position'] = vector_add(ship['position'], delta)

def process_direction(ship, direction, units): 
    process_component_direction(ship, direction, units, 'position')   
    
def process_forward(ship, units):
    process_component_forward(ship, units, 'direction')

def process_rotation(ship, angle):
    process_component_rotation(ship, 'direction', angle)

def process_direction_waypoint(ship, direction, units):
    process_component_direction(ship, direction, units, 'waypoint')   

def process_forward_waypoint(ship, units):
    process_component_forward(ship, units, 'waypoint')

def process_rotation_waypoint(ship, angle):
    process_component_rotation(ship, 'waypoint', angle)

def process_instruction(ship, instruction, direction_funct, forward_funct, rotation_funct):
    units = int(instruction[1:])
    direction = instruction[0]
    if direction in DIRECTION_VECTORS:
        direction = DIRECTION_VECTORS[direction]
        direction_funct(ship, direction, units)
    elif direction == 'F':
        forward_funct(ship, units)
    else:
        angle = units if direction == 'L' else 360 - units
        rotation_funct(ship, angle)
        
def process_instructions(ship, instructions, direction_funct, forward_funct, rotation_funct):
    for instruction in instructions:
        process_instruction(ship, instruction, direction_funct, forward_funct, rotation_funct)
        
instructions = load_input('input.txt')

ship = {'position': (0, 0), 'direction': (1, 0), 'waypoint': (10, 1)}

process_instructions(ship, instructions, process_direction, process_forward, process_rotation)
print(ship['position'])

process_instructions(ship, instructions, process_direction_waypoint, process_forward_waypoint, process_rotation_waypoint)
print(ship['position'])
