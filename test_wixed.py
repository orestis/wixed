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

        b.delete(0, 0, 1, 0)
        assert_equal(b.text, '234567890\n')

        b.delete(0, 4, 1, 0)
        assert_equal(b.text, '23457890\n')

        b.delete(0, 7, 1, 0)
        assert_equal(b.text, '2345789\n')

        b.delete(0, 3, 2, 0)
        assert_equal(b.text, '23489\n')

        b.delete(0, 5, 1, -1)
        assert_equal(b.text, '23489')


    def test_delete_2(self):
        b = Buffer('test')
        b.write('123\n456\n789\n')

        b.delete(1, 1, 7, -2)
        assert_equal(b.text, '123\n4')


    def test_delete_3(self):
        b = Buffer('test')
        b.write('1234567890\nabcdefghij\nABCDEFGHIJ')

        b.delete(0, 10, 11, -1)
        assert_equal(b.text, '1234567890\nABCDEFGHIJ')

        b.delete(0, 4, 11, -1)
        assert_equal(b.text, '1234EFGHIJ')


    def test_delete_all(self):
        b = Buffer('test')
        b.write('a\n')
        b.delete(0, 0, 2, -1)
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
        b.delete(0, 0, 4, 0)
        assert_equal(b.text, '\n')
        assert_equal(b.lines, ['', ''])
        b.insert(0, 0, '\n', 1)
        assert_equal(b.text, '\n\n')
        assert_equal(b.lines, ['', '', ''])
        b.delete(1, 0, 1, -1)
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

        assert_equal(arglist, [(0, 0, 3, None), (0, 0, 'new!', None)])

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
        assert_equal(list(reversed(arglist)), [(i + 1, 0, len(line), None) for i, line in enumerate(previouslines)])






if __name__ == '__main__':
    unittest.main()
