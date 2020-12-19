def parse_line(line):
    bag_colour_string, bag_content_string = line.split(" contain ")
    bag_colour = bag_colour_string[:-5]
    bag_content = []
    for content in bag_content_string.split(", "):
        if content == "no other bags.":
            break
        number, adjective, colour, _ = content.split(" ")
        colour = f"{adjective} {colour}"
        bag_content.append((colour, int(number)))
    return (bag_colour, bag_content)


def load_input(path):
    with open(path) as fd:
        bag_graph = {}
        for line in fd:
            bag_color, bag_content = parse_line(line[:-1])
            bag_graph[bag_color] = bag_content
        return bag_graph


def reverse_graph(original):
    reversed = {}
    for node in original:
        reversed[node] = []
    for source_node, vertice_list in original.items():
        for destination_node, _ in vertice_list: # for our use case we do not need the number entry, so just ignore it
            reversed[destination_node].append(source_node) 
    return reversed 


def generate_discovered_map(graph):
    discovered = {}
    for node in graph:
        discovered[node] = False
    return discovered

''' bfs with count of nodes reached'''
def reachable_node_count(graph, source): 
    node_count = 0
    discovered_map = generate_discovered_map(graph)
    queue = []    
    discovered_map[source] = True
    queue.append(source)
    while len(queue) != 0:
        current_node = queue.pop(0)
        node_count += 1
        adjacent_nodes = graph[current_node]
        for node in adjacent_nodes:
            if not discovered_map[node]:
                discovered_map[node] = True
                queue.append(node)
    return node_count - 1 # remove source node count

def inner_bag_count(graph, source):
    if len(graph[source]) == 0:
        return 0
    else:
        count = 0
        for colour, number in graph[source]:
            count += number * (inner_bag_count(graph, colour) + 1) 
        return count

graph = load_input("input.txt")
print(reachable_node_count(reverse_graph(graph), "shiny gold"))
print(inner_bag_count(graph, "shiny gold"))