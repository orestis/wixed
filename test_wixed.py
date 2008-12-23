from nose.tools import assert_equal

from wixed import Buffer

class testBuffer(object):
    def test_insert(self):
        b = Buffer('test')
        assert_equal(b.text, '', 'wrong initial text')

        b.insert(0, 0, 'hello', 0)
        assert_equal(b.text, 'hello', 'wrong text after simple insert')

        b.insert(0, 0, 'bye ', 0)
        assert_equal(b.text, 'bye hello', 'wrong text after simple insert')

        b.insert(0, len('bye hello'), '\n', 1)
        assert_equal(b.text, 'bye hello\n', 'wrong text after newline insert')

        b.insert(1, 0, 'newline', 0)
        assert_equal(b.text, 'bye hello\nnewline', 'wrong text after second insert')

        b.insert(0, 3, 'embolimo\nkeimeno\n', 2)
        assert_equal(b.text, 'byeembolimo\nkeimeno\n hello\nnewline')

    def test_insert_2(self):
        b = Buffer('test')
        b.insert(0, 0, 'minime', 0)

        b.insert(0, 4, '\n', 1)
        assert_equal(b.text, 'mini\nme')

        b.insert(0, 2, 'mee\nmoo', 1)
        assert_equal(b.text, 'mimee\nmooni\nme')


    def test_write(self):
        b = Buffer('test')
        b.write('123')
        assert_equal(b.text, '123')

        b.write('456\n\n789\n000')
        assert_equal(b.text, '123456\n\n789\n000')

        b = Buffer('test')
        print >> b, 'Hello!'
        assert_equal(b.text, 'Hello!\n')


    def test_delete(self):
        b = Buffer('test')
        b.write('1234567890\n')

        b.delete(0, 0, '1', 0)
        assert_equal(b.text, '234567890\n')

        b.delete(0, 4, '6', 0)
        assert_equal(b.text, '23457890\n')

        b.delete(0, 7, '0', 0)
        assert_equal(b.text, '2345789\n')

        b.delete(0, 3, '57', 0)
        assert_equal(b.text, '23489\n')

        b.delete(0, 5, '\n', -1)
        assert_equal(b.text, '23489')


    def test_delete_2(self):
        b = Buffer('test')
        b.write('123\n456\n789\n')

        b.delete(1, 1, '56\n789\n', -2)
        assert_equal(b.text, '123\n4')


    def test_delete_3(self):
        b = Buffer('test')
        b.write('1234567890\nabcdefghij\nABCDEFGHIJ')

        b.delete(0, 10, 'abcdefghij\n', -1)
        assert_equal(b.text, '1234567890\nABCDEFGHIJ')

        b.delete(0, 4, '567890\nABCD', -1)
        assert_equal(b.text, '1234EFGHIJ')


    def test_delete_all(self):
        b = Buffer('test')
        b.write('a\n')
        b.delete(0, 0, 'a\n', -1)
        assert_equal(b.text, '')
        b.insert(0, 0, 'a', 0)
        assert_equal(b.text, 'a')

    def test_delete_4(self):
        b = Buffer('test')
        assert_equal(b.text, '')
        assert_equal(b.lines, [''])
        b.lines.append('asdf')
        assert_equal(b.text, 'asdf\n')
        assert_equal(b.lines, ['asdf', ''])
        b.delete(0, 0, 'asdf', 0)
        assert_equal(b.text, '\n')
        assert_equal(b.lines, ['', ''])
        b.insert(0, 0, '\n', 1)
        assert_equal(b.text, '\n\n')
        assert_equal(b.lines, ['', '', ''])
        b.delete(1, 0, '\n', -1)
        assert_equal(b.text, '\n')
        assert_equal(b.lines, ['', ''])


    
    def test_lines(self):
        b = Buffer('test')
        arglist = []

        def observer(args):
            arglist.append(args)

        b.inserted += observer
        b.deleted += observer

        assert_equal(b.lines, [''])

        b.write('123\n')
        assert_equal(b.lines, ['123', ''])
        assert_equal(len(b.lines), 2)
        assert_equal(arglist, [(0, 0, '123\n', None)])

        del arglist[:]
        b.lines[0] = 'new!'

        assert_equal(arglist, [(0, 0, '123', None), (0, 0, 'new!', None)])

        del arglist[:]
        copy = b.lines[:]
        copy[0] = 'noooo'
        assert_equal(arglist, [])

        assert_equal(b.text, 'new!\n') #sanity
        b.lines.append('nice!')
        assert_equal(b.text, 'new!\nnice!\n')
        assert_equal(arglist, [(1, 0, 'nice!\n', None)])

        del arglist[:]
        b.lines.extend(['an', 'other'])
        assert_equal(b.text, 'new!\nnice!\nan\nother\n')
        assert_equal(arglist, [(2, 0, 'an\n', None), (3, 0, 'other\n', None)])

        previouslines = b.lines[:][1:]
        del arglist[:]
        del b.lines[1:]
        assert_equal(b.text, 'new!')
        assert_equal(len(b._lines), 1)
        assert_equal(len(b.lines), 1)
        assert_equal(list(reversed(arglist)),
            [(0, 4, 1, None)] + [(i + 1, 0, len(line), None) for i, line in enumerate(previouslines)])


    def test_scopes(self):
        b = Buffer('test')

        s = 's = "Hello, world!"'
        b.write(s)
        b.scope.parse()

        sp = 'source.python'
        assert_equal(b.scope[0, 0], [sp, 'variable'])
        assert_equal(b.scope[0, 2], [sp, 'keyword.operator.assignment.python'])
        s_len= len('"Hello, world!"')
        assert_equal(b.scope[0, 4], [sp, 'string.quoted.double.single-line.python',
            'punctuation.definition.string.begin.python'])
        for i in range(5,  s_len + 3):
            assert_equal(b.scope[0, i], [sp, 'string.quoted.double.single-line.python'], 'wrong scope at %d' % i)
        assert_equal(b.scope[0, s_len + 4], ['string.quoted.double.single-line.python',
            'punctuation.definition.string.end.python'])

        #   0123456789012345
        s2 = dedent("""\
            def some(a1, b2):
                f_1 = 123
        """)
        #   0123456789012345
        b.write(s2)
        mf = 'meta.function.python'
        mfp = 'meta.function.parameters.python'
        assert_scope(b.scope, (1, 0), (1, 2), [sp, mf, 'storage.type.function.python'])
        assert_scope(b.scope, (1, 4), (1, 7), [sp, mf, 'entity.name.function.python'])
        assert_scope(b.scope, (1, 8), (1, 8), [sp, mf, mfp, 'punctuation.definition.parameters.begin.python'])
        assert_scope(b.scope, (1, 9), (1, 10), [sp, mf, mfp, 'variable.parameter.function.python'])
        assert_scope(b.scope, (1, 11), (1, 11), [sp, mf, mfp, 'punctuation.separator.parameters.python'])
        assert_scope(b.scope, (1, 13), (1, 14), [sp, mf, mfp, 'variable.parameter.function.python'])
        assert_scope(b.scope, (1, 15), (1, 15), [sp, mf, mfp, 'punctuation.definition.parameters.end.python'])
        assert_scope(b.scope, (1, 16), (1, 16), [sp, mf, mfp, 'punctuation.section.function.begin.python'])

        assert_scope(b.scope, (2, 4), (2, 6), [sp, mf, 'variable'])
        assert_equal(b.scope, (2, 7), (2, 7), [sp, mf, 'keyword.operator.assignment.python'])
        assert_equal(b.scope, (2, 9), (2, 11), [sp, mf, 'constant.numeric.integer.decimal.python'])


def assert_scope(scope, start, end, expected):
    for line in range(start[0], end[0] + 1):
        for col in range(start[1], end[1] + 1):
            assert_equal(scope[line, col], expected)




if __name__ == '__main__':
    unittest.main()
