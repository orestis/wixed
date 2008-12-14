from collections import defaultdict

class SyntaxGroup(object):
    def __init__(self):
        self.keywords = defaultdict(list)
        self.contained_keywords = defaultdict(list)
        self.matches = defaultdict(list)
        self.contained_matches = defaultdict(list)

    def keyword(self, name, kwlist, nextgroup=None, skipwhite=False, contained=False):
        if contained:
            self.contained_keywords[name].extend(kwlist.split())
        else:
            self.keywords[name].extend(kwlist.split())

    def match(self, name, regex, contained=False, contains=None):
        if contained:
            self.contained_matches[name].append(regex)
        else:
            self.matches[name].append(regex)


syn = SyntaxGroup()

syn.keyword('pythonStatement', 'as assert break continue del except exec finally')
syn.keyword('pythonStatement', 'global lambda pass print raise return try with')
syn.keyword('pythonStatement', 'yield')

syn.keyword('pythonStatement', 'def class', nextgroup='pythonFunction', skipwhite=True)

syn.match('pythonFunction', "[a-zA-Z_][a-zA-Z0-9_]*", contained=True)

syn.keyword('pythonRepeat', 'for while')

syn.keyword('pythonConditional', 'if elif else')

syn.keyword('pythonOperator', 'and in is not or')

syn.keyword('pythonPreCondit', 'import from')

syn.match('pythonComment', "#.*$", contains='pythonTodo')

syn.keyword('pythonTodo', 'TODO FIXME XXX', contained=True)


#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\=\'+ end=+\'+ skip=+\\\\\|\\'+ contains=pythonEscape')
#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\="+ end=+"+ skip=+\\\\\|\\"+ contains=pythonEscape')
#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\="""+ end=+"""+  contains=pythonEscape')
#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\='''+ end=+'''+  contains=pythonEscape')
#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\=[rR]'+ end=+'+ skip=+\\\\\|\\'+ ')
#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\=[rR]"+ end=+"+ skip=+\\\\\|\\"+ ')
#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\=[rR]"""+ end=+"""+  ')
#syn.region('pythonString', 'matchgroup=Normal start=+[uU]\=[rR]'''+ end=+'''+  ')


syn.match('pythonEscape', r'\\[abfnrtv\'"\\]', contained=True)
syn.match('pythonEscape', r"\\[0-7]{1,3}", contained=True) #\123 octal escapes
syn.match('pythonEscape', r"\\x[0-9a-fA-F]{2}", contained=True) #\x escapes
syn.match('pythonEscape', r"(\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8})", contained=True)

syn.match('pythonEscape', "\\$")


syn.match('pythonNumber', r"\<0x\x\+[Ll]\=\>")
syn.match('pythonNumber', r"\<\d\+[LljJ]\=\>")
syn.match('pythonNumber', r"\.\d\+\([eE][+-]\=\d\+\)\=[jJ]\=\>")
syn.match('pythonNumber', r"\<\d\+\.\([eE][+-]\=\d\+\)\=[jJ]\=\>")
syn.match('pythonNumber', r"\<\d\+\.\d\+\([eE][+-]\=\d\+\)\=[jJ]\=\>")



syn.keyword('pythonBuiltin', 'Ellipsis False None NotImplemented True __debug__')
syn.keyword('pythonBuiltin', '__import__ abs all any apply basestring bool')
syn.keyword('pythonBuiltin', 'buffer bytes callable chr classmethod cmp coerce')
syn.keyword('pythonBuiltin', 'compile complex copyright credits delattr dict')
syn.keyword('pythonBuiltin', 'dir divmod enumerate eval execfile exit file')
syn.keyword('pythonBuiltin', 'filter float frozenset getattr globals hasattr')
syn.keyword('pythonBuiltin', 'hash help hex id input int intern isinstance')
syn.keyword('pythonBuiltin', 'issubclass iter len license list locals long map')
syn.keyword('pythonBuiltin', 'max min object oct open ord pow property quit')
syn.keyword('pythonBuiltin', 'range raw_input reduce reload repr reversed round')
syn.keyword('pythonBuiltin', 'set setattr slice sorted staticmethod str sum')
syn.keyword('pythonBuiltin', 'super trunc tuple type unichr unicode vars xrange')
syn.keyword('pythonBuiltin', 'zip')



syn.keyword('pythonException', 'ArithmeticError AssertionError AttributeError')
syn.keyword('pythonException', 'BaseException DeprecationWarning EOFError')
syn.keyword('pythonException', 'EnvironmentError Exception FloatingPointError')
syn.keyword('pythonException', 'FutureWarning GeneratorExit IOError ImportError')
syn.keyword('pythonException', 'ImportWarning IndentationError IndexError')
syn.keyword('pythonException', 'KeyError KeyboardInterrupt LookupError')
syn.keyword('pythonException', 'MemoryError NameError NotImplementedError')
syn.keyword('pythonException', 'OSError OverflowError PendingDeprecationWarning')
syn.keyword('pythonException', 'ReferenceError RuntimeError RuntimeWarning')
syn.keyword('pythonException', 'StandardError StopIteration SyntaxError')
syn.keyword('pythonException', 'SyntaxWarning SystemError SystemExit TabError')
syn.keyword('pythonException', 'TypeError UnboundLocalError UnicodeDecodeError')
syn.keyword('pythonException', 'UnicodeEncodeError UnicodeError')
syn.keyword('pythonException', 'UnicodeTranslateError UnicodeWarning')
syn.keyword('pythonException', 'UserWarning ValueError Warning')
syn.keyword('pythonException', 'ZeroDivisionError')


#  syn match pythonSpaceError    display excludenl "\S\s\+$"ms=s+1
#  syn match pythonSpaceError    display " \+\t"
#  syn match pythonSpaceError    display "\t\+ "
#
#  hi def link pythonStatement Statement
#  hi def link pythonStatement Statement
#  hi def link pythonFunction Function
#  hi def link pythonRepeat Repeat
#  hi def link pythonConditional Conditional
#  hi def link pythonOperator Operator
#  hi def link pythonPreCondit PreCondit
#  hi def link pythonComment Comment
#  hi def link pythonTodo Todo
#  hi def link pythonString String
#  hi def link pythonEscape Special
#  hi def link pythonEscape Special
#
#  if exists("python_highlight_numbers")
#    hi def link pythonNumber Number
#  endif
#
#  if exists("python_highlight_builtins")
#    hi def link pythonBuiltin Function
#  endif
#
#  if exists("python_highlight_exceptions")
#    hi def link pythonException Exception
#  endif
#
#  if exists("python_highlight_space_errors")
#    hi def link pythonSpaceError Error
#  endif


#" Uncomment the 'minlines' statement line and comment out the 'maxlines'
#" statement line; changes behaviour to look at least 2000 lines previously for
#" syntax matches instead of at most 200 lines
#syn sync match pythonSync grouphere NONE "):$"
#"syn sync maxlines=200
#syn sync minlines=2000

#let b:current_syntax = "python"


print syn.matches
print syn.contained_matches

