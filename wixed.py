import subprocess
import os
import signal

from utils import Pipe, CircleList, EventHook, observed

class Window(object):
    def __init__(self, buffer, editor, buf_idx):
        self._buffer = buffer
        self.editor = editor

    def __set_buffer(self, newbuffer):
        self._buffer = newbuffer
        self.editor.buffer = newbuffer

    buffer = property(lambda self: self._buffer, __set_buffer)

    def __repr__(self):
        return 'Window <%r>' % self.buffer

class Buffer(object):
    def __init__(self, name):
        self.name = name
        self.text = ''
        self._curpos = 0
        self._anchor = 0
        self.changed = EventHook()

    curpos = observed('_curpos', lambda s: s.changed)
    anchor = observed('_anchor', lambda s: s.changed)

    def write(self, v):
        self.text += v
        self._curpos = len(self.text)
        self._anchor = len(self.text)
        self.changed.fire(v)

    def __repr__(self):
        return 'Buffer <%r>' % self.name



class BufferManager(object):
    def __init__(self):
        self._buffers = []
        self._names_to_bufs = {}
        self._bufs_to_indexes = {}

    @property
    def buffers(self):
        return self._buffers

    def new(self, *args, **kwargs):
        b = Buffer(*args, **kwargs)
        self._buffers.append(b)
        self._bufs_to_indexes[b] = len(self._buffers) - 1
        self._names_to_bufs[b.name] = b
        return b

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._buffers[item]
        else:
            return self._names_to_bufs[item]

    def __len__(self):
        return len(self._buffers)

    def __repr__(self):
        return 'BufferManager: <%r>' % self._buffers

    def next(self, frombuf):
        fromidx = self._bufs_to_indexes[frombuf]
        if fromidx >= len(self._buffers) - 1: # end of list
            return self._buffers[0]
        return self._buffers[fromidx + 1]

    def previous(self, frombuf):
        fromidx = self._bufs_to_indexes[frombuf]
        if fromidx <= 0: # start of list
            return self._buffers[-1]
        return self._buffers[fromidx - 1]


class Process(object):
    def __init__(self, *args, **kwargs):
        self._buffer = kwargs.pop('buffer')
        kwargs['stdout'] = subprocess.PIPE
        #kwargs['stdin'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.STDOUT
        kwargs['bufsize'] = 0 #unbuffered
        self.popen = subprocess.Popen(*args, **kwargs)
        Pipe(self.popen.stdout, self._buffer)

    def kill(self):
        try:
            import win32api
            win32api.TerminateProcess(int(self.popen._handle), -1)
        except ImportError:
            os.kill(self.popen.pid, signal.SIGKILL)
        

