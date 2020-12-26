class Rule:
    def match(self, message: str) -> (bool, str):
        pass

class SimpleRule(Rule):
    def __init__(self, content: str):
        self.__content = content
    
    def match(self, message: str) -> (bool, str):
        if message.startswith(self.__content):
            return (True, message[len(self.__content):])
        else:
            return (False, None)
  
class ComplexRule(Rule):
    def __init__(self, content: list, rule_list):
        self.__content = content
        self.__rule_list = rule_list
    
    def match(self, message: str) -> (bool, str):
        for idx in self.__content:
            curr_rule = self.__rule_list[idx]
            match, message = curr_rule.match(message)
            if not match:
                return (False, None)
        return (True, message)

class OrRule(Rule):
    def __init__(self, rules: list,):
        self.__rules = rules
        
    def match(self, message: str) -> (bool, str):
        for rule in self.__rules:
            matched, possible_msg = rule.match(message)
            if matched is True:
                return (True, possible_msg)
        return (False, None)

def parse_rule_content(rule_content: str, rule_list: list) -> Rule:
    if rule_content.startswith('"'): #simple rule
        return SimpleRule(rule_content.strip('"'))
    elif '|' in rule_content:
        rules = [parse_rule_content(rule, rule_list) for rule in rule_content.split(' | ')]
        return OrRule(rules)
    else:
        return ComplexRule([int(rule) for rule in rule_content.split(' ')], rule_list)
    return rule_content

def parse_rules(rules: str) -> list:
    rule_list = rules.split('\n')
    ret = [None] * len(rule_list) * 10
    for rule in rule_list:
        rule_num, rule_content = rule.split(': ')
        ret[int(rule_num)] = parse_rule_content(rule_content, ret)
    return ret

def parse_messages(messages: str) -> list:
    #print(messages)
    return [message for message in messages.split('\n')]
    #for rule in rules.split('\n')


def parse_input(path: str):
    with open(path, 'r') as f:
        data = f.read()
        rules, messages = data.split('\n\n')
        return (parse_rules(rules), parse_messages(messages))

#rules, messages = parse_input('input.txt')

#print(len([message for message in messages if rules[0].match(message) and rules[0].apply(message) == '']))

rules, messages = parse_input('input2.txt')

print(len([message for message in messages if rules[0].match(message) == (True, '')]))
