import copy
import itertools
import functools

ORTOGONAL_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

def load_input(path):
    with open(path, 'r') as fd:
        return [line[:-1] for line in fd] # -1 needed here to remove trailling newline

def get_grid_limits(grid):
    return (len(grid) - 1, len(grid[0]) - 1)

def is_position_valid(grid, row, column):
    max_row, max_column = get_grid_limits(grid)
    valid_row = row >= 0 and row <= max_row
    valid_column = column >= 0 and column <= max_column
    return valid_row and valid_column

def move(row, column, direction):
    return (row + direction[0], column + direction[1])

def move_in_direction_simple(grid, row, column, direction):
    row, column = move(row, column, direction)
    if is_position_valid(grid, row, column):
        return (row, column)
    return None

def move_in_direction_complex(grid, row, column, direction):
    row, column = move(row, column, direction)
    while is_position_valid(grid, row, column):
        if grid[row][column] != '.':
            return (row, column)
        row, column = move(row, column, direction)
    return None

def get_adjacent_seats(grid, row, column, move_func):
    adj_seats = {move_func(grid, row, column, direction) for direction in ORTOGONAL_DIRECTIONS}
    adj_seats.discard(None) #in case an adjacent seat does not exist
    return adj_seats

def process_empty_seat(grid, row, column, move_func):
    adjacent_seats = get_adjacent_seats(grid, row, column, move_func)
    if all([grid[row][column] != '#' for row, column in adjacent_seats]):
        return '#'
    return 'L'
        
def process_occupied_seat(grid, row, column, move_func, occupied_tolerance):
    adjacent_seats = get_adjacent_seats(grid, row, column, move_func)
    if len([True for row, column in adjacent_seats if grid[row][column] == '#']) >= occupied_tolerance:
        return 'L'
    return '#'

def process_seat(grid, row, column, move_func, occupied_tolerance):
    if grid[row][column] == 'L':
        return process_empty_seat(grid, row, column, move_func)
    elif grid[row][column] == '#':
        return process_occupied_seat(grid, row, column, move_func, occupied_tolerance)
    return '.'

def process_row(grid, row, move_func, occupied_tolerance):
    new_seats = [process_seat(grid, row, column, move_func, occupied_tolerance) for column in range(len(grid[row]))]
    return "".join(new_seats)
            
def process_grid(grid, move_func, occupied_tolerance):
    return [process_row(grid, row, move_func, occupied_tolerance) for row in range(len(grid))]
    
def are_grids_different(grid1, grid2):
    for row1, row2 in zip(grid1, grid2):
        if row1 != row2:
            return True
    return False
    
def count_occupied_seats(grid):
    count = 0
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] == '#':
                count += 1
    return count
    
def process_until_stable(grid, move_func, occupied_tolerance):
    grid_processed = process_grid(grid, move_func, occupied_tolerance)
    while are_grids_different(grid, grid_processed):
        grid = grid_processed
        grid_processed = process_grid(grid, move_func, occupied_tolerance)
    return grid

grid = load_input('input.txt')

print(count_occupied_seats(process_until_stable(grid, move_in_direction_simple, 4)))
print(count_occupied_seats(process_until_stable(grid, move_in_direction_complex, 5)))