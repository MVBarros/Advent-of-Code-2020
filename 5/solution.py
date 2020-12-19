def load_input(path):
    with open(path, 'r') as fd:
        return [line[:-1] for line in fd] # -1 needed here to remove trailling newline

def get_seat_number(seat_id):
    binary_seat_number = seat_id.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    return int(binary_seat_number, 2)

def is_seat_empty(seats_taken, seat_number):
    seat_empty_cond = seat_number not in seats_taken
    adjacent_seats_full_cond = all(seat in seats_taken for seat in (seat_number-1, seat_number+1))
    return seat_empty_cond and adjacent_seats_full_cond

def get_empty_seat(seats_taken):
    return next(i for i in range(0, 2**10) if is_seat_empty(seats_taken, i))

seat_ids = load_input('input.txt')

seats_taken = set(map(lambda x: get_seat_number(x), seat_ids))

print(max(seats_taken))
print(get_empty_seat(seats_taken))
