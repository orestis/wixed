from wixed import BufferManager
from wixed.frame import Frame

from wixed.keybindings import KeyMapper

class Session(object):
    def __init__(self):
        self.frames = []
        self.buffers = BufferManager()
        self.current_buffer = None
        self.context = dict(
            buffers = self.buffers,
            session = self,
        )
        self.keymap = KeyMapper()
        
    def make_frame(self):
        f = Frame(self)
        f.buffer_changed += self.buffer_changed
        self.frames.append(f)
        if self.current_buffer is None:
            self.current_buffer = f.current_window.buffer
        return f

    def keydown(self, key):
        command = self.keymap[key]
        try:
            command(self)
        except Exception, e:
            print e

    def buffer_changed(self, b):
        self.current_buffer = b
        
    def execute(self, statement):
        try:
            exec(statement, self.context)
        except Exception, e:
            print e



