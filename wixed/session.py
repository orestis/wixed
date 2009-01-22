import os
from wixed.keybindings import KeyMapper

class Session(object):

    def __init__(self, buffers):
        self.buffers = buffers
        self.context = {
            'buffers': self.buffers,
            'current_buffer': None,
            'session': self,
        }
        self._cur_buf = None
        self._windows = None
        
        self.keymap = KeyMapper()
        scratch = self.buffers.new('* Scratch *')
        print >> scratch, '# use this buffer to scratch yourself'

    def init(self):
        if os.path.exists('init.py'):
            try:
                exec(open('init.py').read(), self.context)
            except Exception, e:
                print e

    def _set_windows(self, w):
        self._windows = w
        self.context['windows'] = self._windows

    windows = property(lambda s: s._windows, _set_windows)

    def _set_cur_buf(self, b):
        self._cur_buf = b
        self.context['current_buffer'] = self._cur_buf

    current_buffer = property(lambda s: s._cur_buf, _set_cur_buf)

    def keydown(self, key):
        command = self.keymap[key]
        try:
            command(self)
        except Exception, e:
            print e

        




