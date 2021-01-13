import copy

def parse_input(path: str) -> list:
    with open(path, 'r') as f:
        return [int(cup) for cup in f.read()]

def get_destination(cups, current, pick_up):
    destination = current - 1
    while destination in pick_up or destination == 0:
        if destination == 0:
            destination = len(cups)
        else:
            destination = (destination - 1) % len(cups)
    return destination

def get_pickup(cups, idx):
    num_cups = len(cups)
    return [cups[(idx + n) % num_cups] for n in (1, 2, 3)]
    
def get_cup_idx(cups, val):
    return cups.index(val)

def remove_pickup(cups, pick_up):
    return [cup for cup in cups if cup not in pick_up]

def get_successors(successors, begin, num):
    cups = []
    current = successors[begin]
    for i in range(num):
        cups.append(current)
        current = successors[current]
    return cups

def get_destination(current_cup, pick_up, num_cups):
    destination_cup = current_cup - 1
    if destination_cup == 0:
        destination_cup = num_cups    
    while destination_cup in pick_up:
        destination_cup -= 1
        if destination_cup == 0:
            destination_cup = num_cups
    return destination_cup
    
def move(successors, current_cup):
    *pick_up, next_cup = get_successors(successors, current_cup, 4)
    
    destination_cup = get_destination(current_cup, pick_up, len(successors) - 1)
    
    successors[current_cup] = next_cup
    successors[pick_up[2]] = successors[destination_cup]
    successors[destination_cup] = pick_up[0]
    return next_cup
    
def game(cups, rounds):
    cup_size = len(cups)
    successors = [0] * (cup_size + 1)
    for i in range(0, cup_size):
        successors[cups[i]] = cups[(i + 1) % cup_size]
    current_cup = cups[0]

    for i in range(rounds):
       current_cup = move(successors, current_cup)
    return successors

cups = parse_input('input.txt')
successors = game(cups, 100)

print(get_successors(successors, 1, 8))

for i in range(len(cups), 1000000):
    cups.append(i + 1)

successors = game(cups, 10000000)

print(get_successors(successors, 1, 2))
