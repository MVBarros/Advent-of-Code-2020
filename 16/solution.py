import copy
import functools

def flaten_list(l: list) -> list:
    return [item for sublist in l for item in sublist]

class Interval:
    def __init__(self, min: int, max: int):
        self.min = min 
        self.max = max 
    
    def contains(self, val: int) -> bool:
        return self.min <= val <= self.max 

class TicketElement:
    def __init__(self, name: str, intervals: list):
        self.intervals = intervals
        self.name = name
    
    def check(self, val: int) -> bool:
        return next((val for interval in self.intervals if interval.contains(val)), None) is not None
    
class TicketChecker:
    def __init__(self, elements: set):
        self.elements = elements
    
    def is_val_valid(self, val: int) -> bool:
        return next((el for el in self.elements if el.check(val)), None) is not None

    def get_ticket_faults(self, ticket: list) -> list:
        return (val for val in ticket if not self.is_val_valid(val))
    
    def is_ticket_valid(self, ticket: list) -> bool:
        return next((val for val in ticket if not self.is_val_valid(val)), None) is None
        
    def get_possible_elements(self, val: int) -> dict:
        return {element for element in self.elements if element.check(val)}
    
    def discard_invalid_tickets(self, tickets: list) -> list:
        return [ticket for ticket in tickets if checker.is_ticket_valid(ticket)]

class TicketFormat:
    def __init__(self, ticket_size: int, checker: TicketChecker):
        self.possible_elements = {i: checker.elements.copy() for i in range(ticket_size)}
        self.known_positions = dict()
        self.known_values = set()
        self.ticket_size = ticket_size
        
            
    def is_format_known(self):
        return len(self.known_positions) == self.ticket_size
    
    def process_ticket(self, ticket: list):
        for i, val in enumerate(ticket):
            possible_elements = self.possible_elements[i]
            possible_elements -= self.known_values
            possible_elements &= checker.get_possible_elements(val)
            if len(possible_elements) == 1:
                known_value = next(iter(possible_elements))
                self.known_positions[i] = known_value
                self.known_values.add(known_value)
                
    
    def process_tickets(self, tickets: list):
        while 1:
            for ticket in tickets:
                self.process_ticket(ticket)
                if self.is_format_known():
                    return
            

def parse_interval(interval: str) -> Interval:
    lower, upper = (int(val) for val in interval.split('-'))
    return Interval(lower, upper)

def parse_ticket_element(element: str) -> TicketElement:
    name, intervals = element.split(': ')
    intervals = [parse_interval(interval) for interval in intervals.split(' or ')]
    return TicketElement(name, intervals)

def parse_elments(elements: str) -> TicketChecker:
    elements = {parse_ticket_element(element) for element in elements.split('\n')}
    return TicketChecker(elements)

def parse_ticket(ticket: str) -> list:
    return [int(val) for val in ticket.split(',')]

def parse_tickets(tickets: str) -> list:
    tickets = tickets.split('\n')[1:]
    return [parse_ticket(ticket) for ticket in tickets]

def parse_input(path: str) -> (TicketChecker, list, list):
    with open(path, 'r') as fd:
        data = fd.read()
        elements, my_ticket, nearby_tickets = data.split('\n\n')
        
        checker = parse_elments(elements)
        my_ticket = parse_tickets(my_ticket)[0]
        nearby_tickets = parse_tickets(nearby_tickets)

        return (checker, my_ticket, nearby_tickets)

checker, my_ticket, nearby_tickets = parse_input('input.txt')

faults = flaten_list([checker.get_ticket_faults(ticket) for ticket in nearby_tickets])
print(sum(faults))

nearby_tickets = checker.discard_invalid_tickets(nearby_tickets)
ticket_size = len(my_ticket)
format = TicketFormat(ticket_size, checker)
format.process_tickets(nearby_tickets)

positions = {key for key, value in format.known_positions.items() if value.name.startswith('departure')}

print(functools.reduce(lambda x,y: x*y, (my_ticket[i] for i in positions)))