def read_file(path):
    with open(path) as fd:
        return fd.read()

def response_union(response):
    response = response.replace('\n', '')
    return "".join(set(response)) 

def response_intersection(reponse):
    response_list = reponse.split('\n')
    response_list = [set(response) for response in response_list]
    response_intersection = response_list[0].intersection(*response_list)
    return "".join(response_intersection)
    
def parse_responses(contents):
    return contents.split("\n\n") # \n\n marks end of one group and beginning of another

responses = parse_responses(read_file('input.txt'))
responses_union = [response_union(response) for response in responses]
responses_intersection = [response_intersection(response) for response in responses]
print(sum(map(lambda x: len(x), responses_union)))
print(sum(map(lambda x: len(x), responses_intersection)))
