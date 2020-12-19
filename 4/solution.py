import re

expected_passport_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'] # cid is not needed since a passport is valid with or without it
valid_eye_colors = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

MIN_BYR = 1920
MAX_BYR = 2002
MIN_IYR = 2010
MAX_IYR = 2020
MIN_EYR = 2020
MAX_EYR = 2030
HGT_SUFFIX_CM = "cm"
HGT_SUFFIX_IN = "in"
MIN_HGT_CM = 150
MAX_HGT_CM = 193
MIN_HGT_IN = 59
MAX_HGT_IN = 76
HCL_SUFFIX_REGEXP = '[0-9a-f]*'
PID_REGEXP = '[0-9]*'
PID_LEN = 9
HCL_SUFFIX_LEN = 6
HCL_PREFIX = "#"

def read_file(path):
    with open(path) as fd:
        return fd.read()

def parse_passport_string(passport_string):
    passport_string = passport_string.replace('\n', ' ')
    passport_contents = passport_string.split(' ')
    passport = {}
    for passport_entry in passport_contents:
        passport_entry = passport_entry.split(':')
        passport[passport_entry[0]] = passport_entry[1]
    return passport


def get_passport_strings(contents):
    return contents.split("\n\n") # \n\n marks end of one passport and beginning of another

def parse_passports(contents):
    passport_strings = get_passport_strings(contents) 
    return [parse_passport_string(string) for string in passport_strings]

def get_matching_passports(passports, matching_function):
    return [passport for passport in passports if matching_function(passport)]

def check_passport_complete(passport):
    return all(key in passport for key in expected_passport_keys)

def get_complete_passports(passports):
    return get_matching_passports(passports, check_passport_complete)
   
def validate_year(year, min, max):
    num_digits_cond = len(year) == 4
    value_bound_cond = int(year) >= min and int(year) <= max
    return num_digits_cond and value_bound_cond    

def validate_passport_byr(passport):
    return validate_year(passport['byr'], MIN_BYR, MAX_BYR)

def validate_passport_iyr(passport):
    return validate_year(passport['iyr'], MIN_IYR, MAX_IYR)

def validate_passport_eyr(passport):
    return validate_year(passport['eyr'], MIN_EYR, MAX_EYR)

def validate_passport_hgt(passport):
    hgt = passport['hgt']
    hgt_suffix = hgt[-2:]
    hgt_value = int(hgt[:-2])
    correct_value_cond = False
    if hgt_suffix == HGT_SUFFIX_CM:
        correct_value_cond = hgt_value >= MIN_HGT_CM and hgt_value <= MAX_HGT_CM
    elif hgt_suffix == HGT_SUFFIX_IN:
        correct_value_cond = hgt_value >= MIN_HGT_IN and hgt_value <= MAX_HGT_IN
    return correct_value_cond

def validate_passport_hcl(passport):
    hcl = passport['hcl']
    hcl_prefix = hcl[0]
    hcl_suffix  = hcl[1:]
    correct_prefix_cond = hcl_prefix == HCL_PREFIX
    correct_suffix_cond = len(hcl_suffix) == HCL_SUFFIX_LEN and re.match(HCL_SUFFIX_REGEXP, hcl_suffix)
    return correct_prefix_cond and correct_suffix_cond

def validate_passport_ecl(passport):
    return passport['ecl'] in valid_eye_colors

def validate_passport_pid(passport):
    pid = passport['pid']
    return len(pid) == PID_LEN and re.match(PID_REGEXP, pid)

validate_passport_functions = [validate_passport_byr, validate_passport_iyr, validate_passport_eyr \
    , validate_passport_hgt, validate_passport_hcl, validate_passport_ecl, validate_passport_pid]

def check_passport_valid(passport):
    return all(function(passport) for function in validate_passport_functions)

def get_valid_passports(passports):
    return get_matching_passports(passports, check_passport_valid)

passports = parse_passports(read_file('input.txt'))

complete_passports = get_complete_passports(passports)
valid_passports = get_valid_passports(complete_passports)

print(len(complete_passports))
print(len(valid_passports))
