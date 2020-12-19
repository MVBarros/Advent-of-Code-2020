import itertools, functools

def parse_line(line):
    separated_line = line.split(' ')
    line_nums = separated_line[0].split('-')
    first_num, second_num = (int(val) for val in line_nums) 
    desired_char = separated_line[1][0]
    password = separated_line[2]
    return (first_num, second_num, desired_char, password)

def load_input(path):
    with open(path) as fd:
        return [parse_line(line) for line in fd]

def first_solution_cond(min_val, max_val, desired_char, password):
    higher_cond = password.count(desired_char) >= min_val
    lower_cond = password.count(desired_char) <= max_val
    return higher_cond and lower_cond

def second_solution_cond(first_index, second_index, desired_char, password):
    first_cond = password[first_index -1] == desired_char
    second_cond = password[second_index -1] == desired_char
    return first_cond ^ second_cond

def get_matching_entries(input, cond_function):
    return (entry for entry in input if cond_function(*entry))

def count_matching_entries(input, cond_function):
    return sum(1 for _ in get_matching_entries(input, cond_function))
    
input = load_input('input.txt')

print(count_matching_entries(input, first_solution_cond))
print(count_matching_entries(input, second_solution_cond))
