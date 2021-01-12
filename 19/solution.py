class Rule:
    def match(self, message: str) -> (bool, str):
        pass

class SimpleRule(Rule):
    def __init__(self, content: str):
        self.__content = content
    
    def match(self, message: str) -> (bool, str):
        return (message.startswith(self.__content), message[len(self.__content):])
        
class CompositeRule(Rule):
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
    if rule_content.startswith('"'):
        return SimpleRule(rule_content.strip('"'))
    elif '|' in rule_content:
        rules = [parse_rule_content(rule, rule_list) for rule in rule_content.split(' | ')]
        return OrRule(rules)
    else:
        return CompositeRule([int(rule) for rule in rule_content.split(' ')], rule_list)
    return rule_content

def parse_rules(rules: str) -> list:
    rule_list = rules.split('\n')
    ret = [None] * len(rule_list)
    for rule in rule_list:
        rule_num, rule_content = rule.split(': ')
        ret[int(rule_num)] = parse_rule_content(rule_content, ret)
    return ret

def parse_messages(messages: str) -> list:
    return [message for message in messages.split('\n')]
    
def parse_input(path: str):
    with open(path, 'r') as f:
        data = f.read()
        rules, messages = data.split('\n\n')
        return (parse_rules(rules), parse_messages(messages))

# Trick is that message will always be some arbitrary number of 42 followed by an iteration of n 42 ten n 31
# So we just need to match all 42, then all 31, and see if the number of 42 is higher then 31 
# (meaning there was a prefix of 42 matching rule 8 and then it was all rule 31)
def second_match(rules, message):
    left = rules[42]
    right = rules[31]
    matched_left, matched_right = 0, 0
    while left.match(message)[0] == True:
        message = left.match(message)[1]
        matched_left += 1
    while right.match(message)[0] == True:
        message = right.match(message)[1]
        matched_right += 1
    matched = matched_left > matched_right and matched_right != 0
    return (matched, message)


rules, messages = parse_input('input.txt')
print(len([message for message in messages if rules[0].match(message) == (True, '')]))

print(len([message for message in messages if second_match(rules, message) == (True, '')]))