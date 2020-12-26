import operator

def is_token_val(token):
    return '1' <= token <= '9'
 
class PostfixEvaluator:
    operator_lookup = {'+': operator.add, '*': operator.mul}

    def __init__(self, tokens):
        self.__tokens = tokens
        self.__vals = []
        self.__ops = []
    
    def eval(self):
        for token in self.__tokens:
            if is_token_val(token):
                self.__vals.append(token)
            else:
                left = int(self.__vals.pop())
                right = int(self.__vals.pop())
                res = PostfixEvaluator.operator_lookup[token](left, right)
                self.__vals.append(res)   
        return self.__vals[0]   


'''
Implementation of https://en.wikipedia.org/wiki/Shunting-yard_algorithm
Since we have no function calls in our expressions and each expression
is well formed, the code is simpler.
'''
class ShuntingYard:
    def __init__(self, tokens: list, precedences):
        self.__tokens = tokens
        self.__precedences = precedences
        self.__out = []
        self.__op_stack = []
        
    def _get_op_precedence(self, token):
        return self.__precedences[token]

    def _top_operator(self):
        return self.__op_stack[-1]
    
    def _pop_top_operator_onto_out(self):
        op = self.__op_stack.pop()
        self.__out.append(op)

    def run(self):
        for token in self.__tokens:
            if is_token_val(token):
                self.__out.append(token)
            elif token == ')':
                while self._top_operator() != '(':
                    self._pop_top_operator_onto_out()
                self.__op_stack.pop()
            elif token == '(':
                self.__op_stack.append(token)
            else:
                while (len(self.__op_stack) != 0 and self._top_operator() != '('
                and self._get_op_precedence(token) <= self._get_op_precedence(self._top_operator())):
                    self._pop_top_operator_onto_out()
                self.__op_stack.append(token)
        while len(self.__op_stack) != 0:
            self._pop_top_operator_onto_out()
        return self.__out

def lex_expression(expression: str) -> list:
    expression = expression.replace(' ', '')
    return [char for char in expression]
    
def parse_input(path: str) -> list:
    with open(path, 'r') as fd:
        return [lex_expression(line[:-1]) for line in fd]

res = 0

for expression in parse_input('input.txt'):
    expression_postfix = ShuntingYard(expression, {'+': 1, '*': 1}).run()
    res += PostfixEvaluator(expression_postfix).eval()
    
print(res)

res = 0

for expression in parse_input('input.txt'):
    expression_postfix = ShuntingYard(expression, {'+': 2, '*': 1}).run()
    res += PostfixEvaluator(expression_postfix).eval()
    
print(res)