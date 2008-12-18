from keyword import kwlist
import re
from pegparse import *

T = Terminal

def expand(num):
    def token(tok):
        return [num] * len(tok)
    return token

keywords = map(lambda kw: Keyword(kw).set_token(expand(1)), kwlist)
keywords = reduce(Choice, keywords)

WS = Terminal(' ').set_token(expand(0))
CR = Terminal('\n').set_token(expand(0))
CONT = Terminal('\\')
QUOTE_S = Terminal("'")
QUOTE_D = Terminal('"')
identifier = Regex('[a-zA-Z_][a-zA-Z0-9_]*').set_token(expand(2))

# strings
escapeseq = Regex(r'\\[a-z]') # grammar says any ASCII
longstringchar = Regex('.', re.DOTALL)
shortstringchar_s = Regex(r"[^']")
shortstringchar_d = Regex(r'[^"]')
longstringitem = longstringchar / escapeseq
shortstringitem_s = shortstringchar_s / escapeseq
shortstringitem_d = shortstringchar_d / escapeseq
longstring = Group(
    (Terminal("'''") + Group(Repeat(Not(T("'''")) + longstringitem)) + Terminal("'''")) /
    (Terminal('"""') + Group(Repeat(Not(T('"""')) + longstringitem)) + Terminal('"""'))
)
shortstring = Group(
    (Terminal("'") + Repeat(shortstringitem_s) + Terminal("'")) /
    (Terminal('"') + Repeat(shortstringchar_d) + Terminal('"'))
)
stringprefix = oneOf('r u ur R U UR Ur uR'.split())
stringliteral = ZeroOrOne(stringprefix) + (longstring / shortstring)

# numbers
intpart = Regex('[0-9]+')
fraction = Group(Terminal(".") + intpart)
exponent = Group(oneOf("e", "E") + ZeroOrOne(oneOf('+', '-')) + intpart)
pointfloat = Group((ZeroOrOne(intpart) + fraction) / (intpart + Terminal('.')))
exponentfloat = Group((intpart / pointfloat) + exponent)
floatnumber = pointfloat / exponentfloat
imagnumber = Group((floatnumber / intpart) + (T('j')/T('J')))
hexinteger = Group(T('0') + (T('x') / T('X')) + Regex('[0-9a-zA-Z]+'))
octinteger = Group(T('0') + Regex('[0-7]+'))
decimalinteger = Regex('[1-9][0-9]*') / T('0')
integer = hexinteger / octinteger / decimalinteger
longinteger = Group(integer + (T('l') / T('L')))

number = Group(imagnumber / floatnumber / floatnumber / longinteger / integer).set_token(expand(3))
literal = stringliteral / number

grammar = literal / WS / CR

source = """\
123L 234523
0.13
1e-12
0xDEADBEEF
01231237
123.5j
.123
123.
"""
from pprint import pprint
result, rest = Repeat(grammar).match(source)
print noempties(flatten(result)), `rest`

source = """\
'a string'
'''
my 
"nasty
'even nastier
'nested'
"string"
name is orestis 
'''
"irellevant"
"123"
123
'''
"""
result, rest = Repeat(grammar).match(source)
print flatten(result), `rest`


