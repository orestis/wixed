from pyparsing import *


def action(s, loc, tokens):
    actual_loc = s.index(tokens[0], loc)
    return (actual_loc, len(tokens[0]) + actual_loc, tokens)

string = QuotedString('"', escChar='\\').setResultsName('string').setParseAction(action)
valid_names = Word(alphas, alphanums + '_').setParseAction(action)
op_assign = Keyword('=').setParseAction(action)


assignment = valid_names + op_assign + string

test = 's     =    "Hello, World!"'
print assignment.parseString(test)

class Scanner(object):
    def __init__(self):
        self.scope = []
