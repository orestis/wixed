import subprocess
import os
import signal

from utils import Pipe, CircleList

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
        self._text = ''
        self.curpos = 0
        self.anchor = 0
        self.pending = []

    def __set_text(self, newtext):
        self._text = newtext
        self.synced()

    text = property(lambda self: self._text, __set_text)

    def write(self, v):
        self._text += v
        self.pending.append(v)
        self.curpos = len(self._text)
        self.anchor = len(self._text)

    def updated(self):
        self.updateFunc()

    def synced(self):
        self.pending = []

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
        

