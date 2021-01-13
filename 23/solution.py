def parse_input(path: str) -> list:
    with open(path, 'r') as f:
        return [int(cup) for cup in f.read()]

def get_successors(successors, begin, num):
    cups = [0] * num
    current = successors[begin]
    for i in range(num):
        cups[i] = current
        current = successors[current]
    return cups

def get_destination(current_cup, pick_up, num_cups):
    destination_cup = (current_cup - 1) % num_cups
    while destination_cup in pick_up or destination_cup == 0:
        destination_cup = (destination_cup - 1) % num_cups
    return destination_cup
    
def move(successors, current_cup):
    pick_up = get_successors(successors, current_cup, 3)
    next_cup = successors[pick_up[2]]

    destination_cup = get_destination(current_cup, pick_up, len(successors))
    
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
