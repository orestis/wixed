import subprocess
import os
import signal
from threading import Thread
import time


class CircleList(list):
    index = None

    def append(self, v):
        list.append(self, v)
        if self.index is None:
            self.index = 0

    @property
    def current(self):
        if self.index is not None:
            return self[self.index]

    def next(self):
        if self.index >= len(self) - 1: #end of list
            self.index = 0
        else:
            self.index += 1

    def previous(self):
        if self.index <= 0: # start of list
            self.index = len(self) - 1
        else:
            self.index -= 1



def observed(prop):
    def _setter(self, newvalue):
        setattr(self, prop, newvalue)
        self.updated()

    def _getter(self):
        return getattr(self, prop)

    return _getter, _setter

class Buffer(object):
    def __init__(self, name):
        self.name = name
        self._text = ''
        self._curpos = 0
        self._anchor = 0
        self.updateFunc = lambda : None

    text = property(*observed('_text'))
    curpos = property(*observed('_curpos'))
    anchor = property(*observed('_anchor'))

    def write(self, v):
        self.text += v

    def updated(self):
        self.updateFunc()

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
        #kwargs['bufsize'] = 0 #unbuffered
        self.popen = subprocess.Popen(*args, **kwargs)
        Pipe(self.popen.stdout, self._buffer)

    def kill(self):
        os.kill(self.popen.pid, signal.SIGKILL)
        

class Pipe(object):
    def __init__(self, readStream, writeStream):
        self.readStream = readStream
        self.writeStream = writeStream
        t = Thread(target=self.do_piping)
        t.start()

    def do_piping(self):
        while True:
            c = self.readStream.read(100)
            if c == '':
                break
            self.writeStream.write(c)
            time.sleep(0.1)


