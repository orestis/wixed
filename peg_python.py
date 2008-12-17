from keyword import kwlist
from pegparse import *

def expand(num):
    def token(tok):
        return [num] * len(tok)
    return token

keywords = map(lambda kw: Keyword(kw).set_token(expand(1)), kwlist)
keywords = reduce(Choice, keywords)

WS = Terminal(' ').set_token(expand(0))
CR = Terminal('\n').set_token(expand(0))
names = Regex('[a-zA-Z_][a-zA-Z0-9_]*').set_token(expand(2))

grammar = keywords / WS / names / CR

source = """\
def if orestis or hello class
"""
from pprint import pprint
result = Repeat(grammar).match(source)
pprint(result)

def flatten(x):
    result = []
    for el in x:
        #if isinstance(el, (list, tuple)):
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

flat = [t for t in flatten(result) if t != '']
assert len(flat) == len(source), '%d != %d' % (len(flat), len(source))

print flat
