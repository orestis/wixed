# more reading
# http://www.iam.unibe.ch/~scg/Teaching/CC/11PEGs.pdf
# http://en.wikipedia.org/wiki/Parsing_expression_grammar
# http://www.brynosaurus.com/pub/lang/peg-slides.pdf


class Expr(object):
    def __add__(self, other):
        return Concat(self, other)

    def __div__(self, other):
        return Choice(self, other)

    def __invert__(self):
        return Not(self)

    def match(self, s, tokens=None):
        return self.e.match(s, tokens)

    def __repr__(self):
        return str(self.e)


class Variable(Expr):
    def __init__(self):
        self.e = None


class Empty(Expr):

    def match(self, s, tokens=None):
        return '', s

    def __repr__(self):
        return 'EMPTY'

EMPTY = Empty()

class Terminal(Expr):
    def __init__(self, e, token=lambda x: 'terminal'):
        self.e = e
        self.token = token
    
    def match(self, s, tokens=None):
        if s.startswith(self.e):
            tok, news = s[:len(self.e)], s[len(self.e):]
            if tokens is not None:
                tokens.append(self.token(tok))
            return tok, news
        return None, s

class Concat(Expr):
    def __init__(self, e, b, token=lambda x: 'concat'):
        self.e = e
        self.b = b
        self.token = token

    def match(self, s, tokens=None):
        toka, news = self.e.match(s)
        if toka is not None:
            tokb, news = self.b.match(news)
            if tokb is not None:
                if tokens is not None:
                    tokens.append(self.token(toka+tokb))
                return toka + tokb, news
        return None, s

    def __repr__(self):
        return '( ' + str(self.e) + ' + ' + str(self.b) + ' )'
 
class Choice(Expr):
    def __init__(self, e, b):
        self.e = e
        self.b = b

    def match(self, s, tokens=None):
        tok, news = self.e.match(s, tokens)
        if tok is None:
            return self.b.match(s, tokens)
        return tok, news

    def __repr__(self):
        return '( ' + str(self.e) + ' / ' + str(self.b) + ' )'
 

class Not(Expr):
    def __init__(self, e):
        self.e = e

    def match(self, s, tokens=None):
        tok, news = self.e.match(s) # do not pass in tokens, should not consume
        if tok is not None: # if e succeeds
            return None, s # fails with no consuming
        return '', s # if not, succeed with no consuming

    def __repr__(self):
        return '! (' + str(self.e) + ')'
 
class Repeat(Expr):
    def __init__(self, e):
        v = Variable()
        self.e = (e + v) / EMPTY
        v.e = self.e #dang! recursion! Thanks, pyparsing

    def __repr__(self):
        return '(' + str(self.e) + ')*'
 
class ZeroOrOne(Expr):
    def __init__(self, e):
        self.e = e / EMPTY

class OneOrMore(Expr):
    def __init__(self, e):
        self.e = e + Repeat(e)

class And(Expr):
    def __init__(self, e): # succeeds when e succeeds, but does not consume
        self.e = ~(~(e))

class Engine(object):
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, input, tokens=None):
        while input:
            token, input = self.grammar.match(input, tokens)
            if token is None:
                yield ('<<<%s>>>' % input)
                return
            yield token


# NON-STANDARD STUFF

import re
class Regex(Expr):
    def __init__(self, e, token=lambda x: 'regex'):
        self.e = re.compile(e)
        self._regex = e
        self.token = token

    def match(self, s, tokens=None):
        match = self.e.match(s)
        if match is not None:
            end = match.end()
            tok, news = s[:end], s[end:]
            if tokens is not None:
                tokens.append(self.token(tok))
            return tok, news
        return None, s

class Keyword(Expr):
    def __init__(self, e, token=lambda x: 'keyword'):
        self.e = Terminal(e, token)
        self.check = And(self.e + Terminal(' '))
        self.token = token

    def match(self, s, tokens=None):
        tok, news = self.check.match(s) # check but don't consume
        if tok is not None:
            return self.e.match(s, tokens) # consume the original expression
        return None, s


    
if __name__ == '__main__':
    simple = Terminal('a')
    eng = Engine(simple)
    assert list(eng.parse('aaaa')) == ['a', 'a', 'a', 'a']

    repeat = Repeat(Terminal('a'))
    eng = Engine(repeat)
    assert list(eng.parse('aaaa')) == ['aaaa']

    simple = Terminal('a') / Terminal('b')
    eng = Engine(simple)
    assert list(eng.parse('abba')) == ['a', 'b', 'b', 'a']

    simple = Terminal('a') + Terminal('b')
    eng = Engine(simple)
    assert list(eng.parse('ababcc')) == ['ab', 'ab', '<<<cc>>>']

    simple = ZeroOrOne(Terminal('a')) + Terminal('b')
    eng = Engine(simple)
    assert list(eng.parse('abb')) == ['ab', 'b']

    simple = Terminal('foo') + ~(Terminal('bar'))
    eng = Engine(simple)
    assert list(eng.parse('foobie')) == ['foo', '<<<bie>>>']
    assert list(eng.parse('foobar')) == ['<<<foobar>>>']

    simple = Terminal('foo') + And(Terminal('bar'))
    eng = Engine(simple)
    assert list(eng.parse('foobar')) == ['foo', '<<<bar>>>']
    assert list(eng.parse('foobie')) == ['<<<foobie>>>']

    simple = Repeat(Terminal('a') + Terminal('c')) + Terminal('b')
    eng = Engine(simple)
    assert list(eng.parse('bbacacbbddd')) == ['b', 'b', 'acacb', 'b', '<<<ddd>>>']

    simple = OneOrMore(Terminal('a') + Terminal('c')) + Terminal('b')
    eng = Engine(simple)
    assert list(eng.parse('bbacacbbddd')) == ['<<<bbacacbbddd>>>']
    assert list(eng.parse('acacbbddd')) == ['acacb', '<<<bddd>>>']

    print 'assertions pass'
