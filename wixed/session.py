from wixed import BufferManager
from wixed.frame import Frame

from wixed.keybindings import KeyMapper

class Session(object):
    def __init__(self):
        self.frames = []
        self.buffers = BufferManager()
        self.context = dict(
            buffers = self.buffers,
            current_buffer = None,
            session = self,
        )
        self.keymap = KeyMapper()
        
    def make_frame(self):
        f = Frame(self)
        self.frames.append(f)
        return f

    def keydown(self, key):
        command = self.keymap[key]
        try:
            command(self)
        except Exception, e:
            print e
        
    def execute(self, statement):
        try:
            exec(statement, self.context)
        except Exception, e:
            print e



