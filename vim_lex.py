from keyword import kwlist

from pyparsing import Regex, Keyword, Or, SkipTo, WordEnd, alphanums, LineEnd


def pos(s, loc, tokens):
    actual_loc = s.index(tokens[0], loc)
    return (actual_loc, len(tokens[0]) + actual_loc, tokens)

def contains(expr):
    expr.setParseAction(pos)
    def parse_contained_expr(s, loc, tok):
        substr = s[loc+len(tok[0]):]
        print expr.parseString(substr)

    return parse_contained_expr

kwlist = set(kwlist)
def_class = set('def class'.split())
kwlist -= def_class

pythonFunction = Regex("[a-zA-Z_][a-zA-Z0-9_]*") + WordEnd(alphanums + '_').suppress() # how to do this?
def_class = Or(map(Keyword, def_class)).setParseAction(contains(pythonFunction), pos) # nextgroup=pythonFunction skipwhite

keywords = Or(map(Keyword, kwlist))

pythonComment = Regex("#.*$")

pythonString = Regex('"""') + SkipTo('"""', include=True) # contains=pythonEscape

test = """\
def something():
    pass

"""

print def_class.parseString(test)
