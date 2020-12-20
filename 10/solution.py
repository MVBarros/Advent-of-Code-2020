def load_input(path):
    with open(path, 'r') as fd:
        # -1 needed here to remove trailling newline
        return [int(line[:-1]) for line in fd]

def calculate_chain_diffs(charges, prev_charge):
    charge_diffs = {1: 0, 3: 0}
    prev_charge = charges[0]
    for charge in charges[1:]:
        diff = charge - prev_charge
        prev_charge = charge
        if diff in {1, 3}:
            charge_diffs[diff] += 1
    return charge_diffs

def get_possible_connections(root, charges_sorted):
    charges_possible = []
    for index, charge in enumerate(charges_sorted):
        if charge > root + 3:
            break
        charges_possible.append((index, charge))
    return charges_possible

def count_possible_chains(root, charges_sorted, visited):
    if charges_sorted == []:  # End of chain
        visited[root] = 1
        return 1
    elif root in visited:  # Already know how many chains I can make from here, no need to repeat computation
        return visited[root]
    else:
        connections = get_possible_connections(root, charges_sorted)
        possibilities = sum([count_possible_chains(charge, charges_sorted[i + 1:], visited) for i, charge in connections])
        visited[root] = possibilities
        return possibilities

charges = load_input('input.txt')

charges.sort()
# add final charge of 3 plus than max
charges.append(charges[len(charges) - 1] + 3)

root = 0  # initial outlet with charge 0

diffs = calculate_chain_diffs(charges, root)

print(diffs[1] * diffs[3])

print(count_possible_chains(root, charges, {}))
