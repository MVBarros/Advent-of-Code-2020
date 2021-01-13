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

def move(cups, idx):
    pick_up = get_pickup(cups, idx)
    pickup_set = set(pick_up)
    
    next_idx = (idx + len(pick_up) + 1) % len(cups)

    current_cup, next_cup = cups[idx], cups[next_idx]

    destination = get_destination(cups, current_cup, pickup_set)
    cups = remove_pickup(cups, pickup_set)
    destination_idx = get_cup_idx(cups, destination)
    cups = cups[:destination_idx + 1] + pick_up + cups[destination_idx + 1:]

    return (cups, next_cup)
    
def game(cups, rounds):
    idx = 0
    count = 0
    while count < rounds:
        cups, next_cup = move(cups, idx)
        idx = get_cup_idx(cups, next_cup)
        count += 1
    return cups
        
        
cups = parse_input('input.txt')
cups = game(cups, 100)

print(cups)
