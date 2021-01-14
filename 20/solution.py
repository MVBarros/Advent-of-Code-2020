import itertools
import functools
import random

class Tile:
    contrary_sides = {'top': 'bot', 'bot': 'top', 'left': 'right', 'right': 'left'}
    flipped_sides = {'top': 'bot', 'bot': 'top', 'left': 'left', 'right': 'right'}
    rotated_sides = {'top': 'right', 'right': 'bot', 'bot': 'left', 'left': 'top'}
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
    
    def get_matching_side(self, other) -> str:
        for side, bound in self.bounds.items():
            if bound == other.bounds[Tile.contrary_sides[side]]:
                return side
        return None
    
    def connect(self, other):
        if other in self.neighbours.values():
            return

        for i in range(4):
            matching_side = self.get_matching_side(other)
            if matching_side is not None:
                self.neighbours[matching_side] = other
                other.neighbours[Tile.contrary_sides[matching_side]] = self
                return
            self.rotate(set())

        self.flip(set())

        for i in range(4):
            matching_side = self.get_matching_side(other)
            if matching_side is not None:
                self.neighbours[matching_side] = other
                other.neighbours[Tile.contrary_sides[matching_side]] = self
                return
            self.rotate(set())

    def rotate_image(self):
        self.image = ["".join(line) for line in zip(*self.image[::-1])]

    def rotate(self, visited):
        if self in visited:
            return
        visited.add(self)

        self.bounds = {Tile.rotated_sides[side]: bound for side, bound in self.bounds.items()}
        self.bounds['top'] = self.bounds['top'][::-1]
        self.bounds['bot'] = self.bounds['bot'][::-1]
        
        self.rotate_image()

        self.neighbours = {Tile.rotated_sides[side]: neighbour for side, neighbour in self.neighbours.items()}
        for neighbour in self.neighbours.values():
            if neighbour is not None:
                neighbour.rotate(visited)
        return
    
    def flip_image(self):
        self.image = self.image[::-1]

    def flip(self, visited):
        if self in visited:
            return
        visited.add(self)

        self.bounds = {Tile.flipped_sides[side]: bound for side, bound in self.bounds.items()}
        self.bounds['left'] = self.bounds['left'][::-1]
        self.bounds['right'] = self.bounds['right'][::-1]
        
        self.flip_image()

        self.neighbours = {Tile.flipped_sides[side]: neighbour for side, neighbour in self.neighbours.items()}
        for neighbour in self.neighbours.values():
            if neighbour is not None:
                neighbour.flip(visited)
        return
    
    def __repr__(self):
        return str(self.number)

    def print_image(self):
        for line in self.image:
            print(line)
        
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

def connect_tiles(connection_map: dict):
    for tile, connections in connection_map.items():
        for connection in connections:
            tile.connect(connection)

def get_borders(connection_map: dict) -> list:
    return [tile for tile, connections in connection_map.items() if len(connections) == 2]

tiles = parse_input('input.txt')

connection_map = get_connections(tiles)

border_tiles = get_borders(connection_map)

print(functools.reduce(lambda x, y: x * y, map(lambda x: x.number, border_tiles)))

connect_tiles(connection_map)

# tiles[0].flip(set())

for tile in tiles:
    print(f'tile:{tile.number}, neighbours: {tile.neighbours}')
    