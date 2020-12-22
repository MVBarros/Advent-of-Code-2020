def load_input(path: str) -> list:
    with open(path, 'r') as fd:
        line = fd.readline()
        return [int(el) for el in line.split(',')]

def elf_game(nums_starting: list, turns: int) -> int:
    # there will never be more than turn number spokens and the number spoken
    # will never be larger than the number of turns, therefore this can be a 
    # fixed size list, there is no need to use a dictionary and lose time hashing 
    nums_spoken = [turns] * turns 
    for i, num in enumerate(nums_starting):
        nums_spoken[num] = i + 1

    # next turn will always be zero since the starting numbers do not repeat
    num_current = 0
    num_next = 0
    for turn_current in range(len(nums_starting) + 1, turns):
        num_current = num_next
        # 0 if the number is new, diff otherwise, since we started
        # the array with the highest possible number spoken in the game
        num_next = max(turn_current - nums_spoken[num_current], 0)
        nums_spoken[num_current] = turn_current
    return num_next

    
nums_starting = load_input('input.txt')
print(elf_game(nums_starting, 2020))
print(elf_game(nums_starting, 30000000))

    