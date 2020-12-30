import functools
import collections

alergens = {}
ingredients = collections.Counter()

class Alergen:
    def __init__(self, possibilities: set):
        self.possibilities = possibilities
    
    def add_possibilities(self, possibilities: set):
        self.possibilities &= possibilities
    
    def remove_possibilities(self, possibilities: set):
        self.possibilities -= possibilities
    
    def is_known(self):
        return len(self.possibilities) == 1
    
    def get_ingredient(self):
        return next(iter(self.possibilities))

def parse_recipe(line):
    recipe_ingredients, recipe_alergens = line.split(' (contains ')
    ingredient_set = set(recipe_ingredients.split(' '))
    for alergen in recipe_alergens.split(', '):
        if alergen in alergens:
            alergens[alergen].add_possibilities(ingredient_set)
        else:
            alergens[alergen] = Alergen(ingredient_set.copy())
    ingredients.update(ingredient_set)

def parse_input(path: str):
    with open(path, 'r') as fd:
        for line in fd: 
            parse_recipe(line[:-2]) # -2 to eat ')\n' at the end of the line

def are_all_alergens_known():
    for alergen in alergens.values():
        if not alergen.is_known():
            return False
    return True

def get_all_ingredients():
    return ingredients.keys()

def get_alergenic_ingredients():
    return {alergen.get_ingredient() for alergen in alergens.values() if alergen.is_known()}

def get_non_alergenic_ingredients():
    return get_all_ingredients() - get_alergenic_ingredients() 

def induce_alergenic_ingredients():
    while not are_all_alergens_known():
        known_ingredients = get_alergenic_ingredients()
        unknown_alergens = (alergen for alergen in alergens.values() if not alergen.is_known())
        for alergen in unknown_alergens:
            alergen.remove_possibilities(known_ingredients)

def count_non_alergenic_occurences():
    non_alergenics = get_non_alergenic_ingredients()
    return sum((count for ingredient, count in ingredients.items() if ingredient in non_alergenics))
    
def get_canonical_string():
    return ','.join((alergens[alergen].get_ingredient() for alergen in sorted(alergens)))

parse_input('input.txt')
induce_alergenic_ingredients()
print(count_non_alergenic_occurences())
print(get_canonical_string())