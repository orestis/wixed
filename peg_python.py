from keyword import kwlist
from pegparse import *

def expand(num):
    def token(tok):
        return [num] * len(tok)
    return token

keywords = map(lambda kw: Keyword(kw, token=expand(1)), kwlist)
keywords = reduce(Choice, keywords)

WS = Terminal(' ', token=expand(0))
CR = Terminal('\n', token=expand(0))
names = Regex('[a-zA-Z_][a-zA-Z0-9_]*', token=expand(2))

grammar = keywords / WS / names / CR

source = """\
def if orestis or hello class
"""
engine = Engine(grammar)
tokens = []
print list(engine.parse(source, tokens))
print tokens
tokens = []
print grammar.match(source, tokens)
print tokens
tokens = []
print Repeat(grammar).match(source, tokens)
print tokens

assert list(engine.parse(source)) == ['def', ' ', 'if', ' ', 'orestis', ' ', 'or', ' ', 'hello', ' ', 'class', '\n']
assert grammar.match(source) == ('def', ' if orestis or hello class\n')
assert Repeat(grammar).match(source) == ('def if orestis or hello class\n', '')

