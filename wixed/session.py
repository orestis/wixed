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
        

class _Session(object):

    def __init__(self, buffers):
        self._cur_buf = None
        self._windows = None
        

    def _set_windows(self, w):
        self._windows = w
        self.context['windows'] = self._windows

    windows = property(lambda s: s._windows, _set_windows)

    def _set_cur_buf(self, b):
        self._cur_buf = b
        self.context['current_buffer'] = self._cur_buf

    current_buffer = property(lambda s: s._cur_buf, _set_cur_buf)





