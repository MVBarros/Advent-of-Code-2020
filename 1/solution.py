import itertools, functools

DESIRED_SUM = 2020

def load_input(path):
    with open(path) as fd:
        return [int(line) for line in fd]

def list_product(list):
    return functools.reduce(lambda x,y: x*y, list)

def generate_combinations(input, combination_size):
    return itertools.combinations(input, combination_size)

def check_combination(combination):
    combination_sum = sum(combination)
    return combination_sum == DESIRED_SUM

def get_correct_combination(combinations):
    return next(combination for combination in combinations if check_combination(combination))
 
input = load_input('input.txt')

first_problem_combinations = generate_combinations(input, 2)
second_problem_combinations = generate_combinations(input, 3)

first_problem_solution = get_correct_combination(first_problem_combinations)
second_problem_solution = get_correct_combination(second_problem_combinations)

print(list_product(first_problem_solution))
print(list_product(second_problem_solution))
