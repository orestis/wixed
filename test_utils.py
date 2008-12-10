from nose.tools import assert_equal

from utils import EventHook

class testEventHooks(object):
    def test_add_remove(self):
        hook = EventHook()
        def func1():
            pass

        def func2():
            pass

        hook += func1
        assert_equal(hook._observers, [func1])

        hook += func2
        assert_equal(hook._observers, [func1, func2])

        hook -= func1
        assert_equal(hook._observers, [func2])

        hook -= func2
        assert_equal(hook._observers, [])


