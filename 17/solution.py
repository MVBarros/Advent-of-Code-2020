import itertools

def parse_cubes(cubes: str, dimensions) -> dict:
    coords = set()
    for y, line in enumerate(cubes):
        for x, char in enumerate(line):
            if  char == '#':
                coords.add((x, y, *([0] * (dimensions - 2))))
    return coords

def parse_input(path: str, dimensions) -> list:
    with open(path, 'r') as fd:
        return parse_cubes([line[:-1] for line in fd.readlines()], dimensions)

def get_neighbours(point: tuple) -> tuple:
    bounds = ((i-1, i, i+1) for i in point)
    return (neighbour for neighbour in itertools.product(*bounds) if neighbour != point)

def is_cube_active(cubes: dict, point: tuple) -> bool:
    return point in cubes

def process_active_cube(cubes_read, cubes, point: tuple):
    neighbours = get_neighbours(point)
    num_active_neighbours = sum((1 for cube in neighbours if is_cube_active(cubes_read, cube)))
    if num_active_neighbours not in {2, 3}:
        cubes.remove(point)

def process_inactive_cube(cubes_read, cubes, point: tuple):
    neighbours = get_neighbours(point)
    num_active_neighbours = sum((1 for cube in neighbours if is_cube_active(cubes_read, cube)))
    if num_active_neighbours == 3:
        cubes.add(point)

def process_cube(cubes_read, cubes, point: tuple):
    if is_cube_active(cubes_read, point):
        process_active_cube(cubes_read, cubes, point)
    else:
        process_inactive_cube(cubes_read, cubes, point)
    
def traverse(cubes, bounds):
    cubes_read = cubes.copy()
    for point in itertools.product(*bounds):
        process_cube(cubes_read, cubes, point)
    
def get_bounds(cubes, dimensions):
    return (range(min((k[i] for k in cubes)) - 1, max((k[i] for k in cubes)) + 2) for i in range(dimensions))
    
for dimensions in (3, 4):
    cubes = parse_input('input.txt', dimensions)
    for _ in range(6):
        bounds = get_bounds(cubes, dimensions)
        traverse(cubes, bounds)
    print(len(cubes))
