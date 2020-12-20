import functools

def load_input(path):
    with open(path, 'r') as fd:
        return [line[:-1] for line in fd] # -1 needed here to remove trailling newline

def find_slope_solution(input, step_x, step_y):
    num_trees = 0
    curr_x, curr_y = (0,0)
    num_lines = len(input)
    num_columns = len(input[0])
    while curr_y < num_lines:
        if input[curr_y][curr_x] == '#':
            num_trees += 1
        curr_x = (curr_x + step_x) % num_columns
        curr_y += step_y
    return num_trees    

def list_product(list):
    return functools.reduce(lambda x,y: x*y, list)

def multiple_slope_solutions(input, slopes):
    return [find_slope_solution(input, *slope) for slope in slopes]

input = load_input('input.txt')

second_problem_slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))

print(find_slope_solution(input, 3, 1))
print(list_product(multiple_slope_solutions(input, second_problem_slopes)))
