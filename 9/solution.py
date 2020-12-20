import itertools

def load_input(path):
    with open(path, 'r') as fd:
        return [int(line[:-1]) for line in fd] # -1 needed here to remove trailling newline

def get_preamble_combinations(preamble):
    return itertools.combinations(preamble, 2)

def get_preamble_sums(preamble):
    combinations = get_preamble_combinations(preamble)
    return {sum(combination) for combination in combinations}

def is_number_weakness(number, preamble):
    return number not in get_preamble_sums(preamble)

def find_first_weakness(data):
    return next(data[i] for i in range(25, len(data)) if is_number_weakness(data[i], data[i-25: i]))

def get_fixed_size_data_ranges(data, size):
    return [data[i:i+size] for i in range(0, len(data)) if len(data[i:i+size]) == size] # remove unfinished ranges at the end of the input
    
def get_data_ranges_sum(ranges):
    return {sum(range) for range in ranges}

def ranges_contain_sum(ranges, expected_sum):
    return expected_sum in get_data_ranges_sum(ranges)

def get_data_ranges(data):
    for range_size in range(2, len(data)):
        yield get_fixed_size_data_ranges(data, range_size)
        
def search_range_collection_with_sum(data, sum):
    return next(ranges for ranges in get_data_ranges(data) if ranges_contain_sum(ranges, sum))

def find_range_with_sum(ranges, expected_sum):
    return next(range for range in ranges if sum(range) == expected_sum)

def get_range_with_sum(data, sum):
    ranges = search_range_collection_with_sum(data, sum)
    return find_range_with_sum(ranges, sum) 

encrypted_data = load_input('input.txt')

first_weakness = find_first_weakness(encrypted_data)

print(first_weakness)

range = get_range_with_sum(encrypted_data, first_weakness)
min, max = min(range), max(range)

print(min + max)
