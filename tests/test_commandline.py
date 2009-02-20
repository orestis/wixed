from mock import Mock
from nose.tools import assert_equal

from wixed.commandline import CommandLineHandler

class testCommandLine(object):
    def test_execute_event(self):
        cmd_handler = CommandLineHandler()
        listener = Mock()
        cmd_handler.execute += listener
        cmd_handler.line_changed('a command')
        cmd_handler.finish()
        listener.assert_called_with('a command')

    def test_command_line_handler(self):
        cmd_handler = CommandLineHandler()

        cmd_handler.line_changed('a command')
        cmd_handler.finish()
        assert cmd_handler.command == 'a command'
        assert_equal(list(cmd_handler.history), ['a command'])
