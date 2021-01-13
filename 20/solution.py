import itertools
import functools

class Tile:
    def __init__(self, name: str, image: list):
        self.number = int(name[-6:-1])
        self.image = image
        self.bounds = {'top': self.image[0], 'bot': self.image[-1]}
        self.bounds['left'] = "".join(line[0] for line in self.image)
        self.bounds['right'] = "".join(line[-1] for line in self.image)
        self.possible_bounds = set()
        for bound in self.bounds.values():
            self.possible_bounds.add(bound)
            self.possible_bounds.add(bound[::-1])
        self.neighbours = {'top': None, 'bot': None, 'left': None, 'right': None}
        
    def connects_to(self, other) -> bool:
        return self.possible_bounds & other.possible_bounds
    
    def __repr__(self):
        return str(self.number)

def parse_tile(tile: str) -> Tile:
    name, *image = tile.split('\n') 
    return Tile(name, image)
    
def parse_input(path: str) -> list:
    with open(path, 'r') as fd:
        data = fd.read()
        return [parse_tile(tile) for tile in data.split('\n\n')]

def get_connections(tiles: list) -> dict:
    connection_map = {tile: [] for tile in tiles}
    for first, second in itertools.combinations(tiles, 2):
        if first.connects_to(second):
            connection_map[first].append(second)
            connection_map[second].append(first)
    return connection_map

def get_borders(connection_map: dict) -> list:
    return [tile for tile, connections in connection_map.items() if len(connections) == 2]

tiles = parse_input('input.txt')

connection_map = get_connections(tiles)

border_tiles = get_borders(connection_map)

print(functools.reduce(lambda x, y: x * y, map(lambda x: x.number, border_tiles)))
