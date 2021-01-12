import functools
import collections

vectors = {'se': (-1, 0, 1), 'sw': (0, -1, 1), 'ne': (0, 1, -1), 'nw': (1, 0, -1), 'w': (1, -1, 0), 'e': (-1, 1, 0)}
vector_list =  [(-1, 0, 1), (0, -1, 1), (0, 1, -1), (1, 0, -1), (1, -1, 0), (-1, 1, 0)]


def parse_input(path: str) -> list:
    with open(path, 'r') as fd:
        return [line[:-1] for line in fd]

def get_steps(line: str) -> tuple:
    steps = []
    i = 0
    while i < len(line):
        char = line[i]
        if char in {'e', 'w'}:
            steps.append(vectors[char])
            i += 1
        else:
            steps.append(vectors[char + line[i + 1]])
            i += 2
    return steps

def walk_line(line: str) -> tuple:
    steps = get_steps(line)
    return functools.reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]), steps, (0, 0, 0))

def get_floor_bounds(tiles):
    x_coords = {tile[0] for tile in tiles}
    y_coords = {tile[1] for tile in tiles}
    z_coords = {tile[2] for tile in tiles}
    min_coord = (min(x_coords) - 1, min(y_coords) - 1, min(z_coords) - 1)
    max_coord = (max(x_coords) + 2, max(y_coords) + 2, max(z_coords) + 2)
    return min_coord, max_coord

def get_adjacent_pos(pos):
    return ((pos[0] + vector[0], pos[1] + vector[1], pos[2] + vector[2]) for vector in vector_list)
    

def check_white(tiles, pos, flips):
    adj = get_adjacent_pos(pos)
    num_blacks = sum((1 for pos in adj if tiles[pos] % 2))
    if num_blacks == 2:
        flips.add(pos)
    
def check_black(tiles, pos, flips):
    adj = get_adjacent_pos(pos)
    num_blacks = sum((1 for pos in adj if tiles[pos] % 2))
    if num_blacks == 0 or num_blacks > 2:
        flips.add(pos)

def check_pos(tile, pos, flips, visited):
    if pos in visited:
        return
    visited.add(pos)
    if not tiles[pos] % 2:
        check_white(tiles, pos, flips)
    else:
        check_black(tiles, pos, flips) 

def flip_ground(tiles):
    visited = set()
    flips = set()
    for pos in tiles:
        for adj_pos in get_adjacent_pos(pos):
            check_pos(tiles, adj_pos, flips, visited)
        check_pos(tiles, pos, flips, visited)

    for pos in flips:
        tiles[pos] += 1


def count_black(tiles):
    count = 0
    for pos in tiles:
        if tiles[pos] % 2:
            count += 1
    return count


lines = parse_input('input.txt')

tiles = collections.Counter([walk_line(line) for line in lines])
print(count_black(tiles))

for i in range(0, 100):
    tiles = collections.Counter([tile for tile, val in tiles.items() if val % 2 ])
    flip_ground(tiles)
    
print(count_black(tiles))
