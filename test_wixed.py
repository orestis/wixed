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






if __name__ == '__main__':
    unittest.main()
