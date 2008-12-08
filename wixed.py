import subprocess
import os
import signal

from utils import Pipe, CircleList


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
        self._buffers = CircleList()
        self.updateFunc = lambda : None

    def new(self, *args, **kwargs):
        b = Buffer(*args, **kwargs)
        self._buffers.append(b)
        return b

    def __repr__(self):
        return 'BufferManager: <%r>' % self._buffers

    @property
    def current(self):
        return self._buffers.current

    def next(self):
        self._buffers.next()
        self.updateFunc()

    def previous(self):
        self._buffers.previous()
        self.updateFunc()


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
        

