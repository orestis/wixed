from Plex import *

def token(tok):
    def _token(self, text):
        return self.scope + [tok]
    return _token


class PythonScanner(Scanner):
    letter = Range("AZaz") | Any("_")
    digit = Range("09")
  
    name = letter + Rep(letter | digit)
    
    in_string = Rep(AnyBut('\\\n"') | (Str("\\") + AnyChar)) # line continuations? | escapes
    dq_string = Str('"') + in_string + Str('"')

    spaces = Rep1(Any(" \t"))
    operator = Any("=")

    def string_action(self, text):
        print 'string action'
        self.scope.append('string.quoted.double.single-line.python')
        self._produce('punctuation.definition.string.end.python', text[0])
        print 'none token, scope is', self.scope
        self._produce('', text[1:-1])
        print 'after none token, scope is', self.scope
        self._produce('punctuation.definition.string.begin.python', text[-1])
        self.scope.pop()

    def _produce(self, v, text):
        token = self.scope
        if v is not '':
            token = self.scope + [v]
        self.produce(token, text)


    def begin(self, state):
        if state != '':
            self.scope.append(state)
        Scanner.begin(self, state)

    lexicon = Lexicon([
        State('source.python', [
            (name, token('variable')),
            (dq_string, string_action),
            (spaces, IGNORE),
            (operator, token('keyword.operator.assignment.python')),
        ]),
    ])
    def __init__(self, file):
        Scanner.__init__(self, self.lexicon, file)
        self.scope = []
        self.begin('source.python')

