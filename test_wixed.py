import unittest

from wixed import Buffer

class BufferTest(unittest.TestCase):
    def test_insert(self):
        b = Buffer('test')
        self.assertEquals(b.text, '', 'wrong initial text')

        b.insert(0, 0, 'hello', 0)
        self.assertEquals(b.text, 'hello', 'wrong text after simple insert')

        b.insert(0, 0, 'bye ', 0)
        self.assertEquals(b.text, 'bye hello', 'wrong text after simple insert')

        b.insert(0, len('bye hello'), '\n', 1)
        self.assertEquals(b.text, 'bye hello\n', 'wrong text after newline insert')

        b.insert(1, 0, 'newline', 0)
        self.assertEquals(b.text, 'bye hello\nnewline', 'wrong text after second insert')

        b.insert(0, 3, 'embolimo\nkeimeno\n', 2)
        self.assertEquals(b.text, 'byeembolimo\nkeimeno\n hello\nnewline')





if __name__ == '__main__':
    unittest.main()
