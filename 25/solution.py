SUBJECT = 7
MODULUS = 20201227

def parse_input(path: str) -> list:
    with open(path, 'r') as fd:
        return [int(line[:-1]) for line in fd]

def get_loop_size(pub_key):
    loop_size = 1
    val = SUBJECT
    while val != pub_key:
        val = (val * SUBJECT) % MODULUS
        loop_size += 1
    return loop_size

def produce_encryption_key(pub_key, loop_size):
    val = 1 
    for i in range(loop_size):
        val = (val * pub_key) % MODULUS
    return val


card_pub_key, door_pub_key = parse_input('input.txt')

card_loop = get_loop_size(card_pub_key)

print(f"Card loop size: {card_loop}")

print(f"Encryption key: {produce_encryption_key(door_pub_key, card_loop)}")