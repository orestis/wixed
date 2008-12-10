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
        self._lines = ['']
        self._curpos = 0
        self._anchor = 0
        self.pos_changed = EventHook()
        self.inserted = EventHook()
        self.deleted = EventHook()

    curpos = observed('_curpos', lambda s: s.pos_changed)
    anchor = observed('_anchor', lambda s: s.pos_changed)

    @property
    def text(self):
        return '\n'.join(self._lines)

    def write(self, v):
        self.insert(len(self._lines) - 1, # last line
                    len(self._lines[-1]), # after the last character
                    v,
                    v.count('\n'))

    def insert(self, lineno, col, text, linesadded, where=None):
        try:
            line = self._lines[lineno]
            front, back = line[:col], line[col:]
                
            if linesadded == 0:
                newline = ''.join([front, text, back])
                self._lines[lineno] = newline
            else:
                middle = text.split('\n') # splitlines doesn't return an empty new line
                first, rest = middle[0], middle[1:]

                newline = ''.join([front, first])
                self._lines[lineno] = newline

                if back:
                    rest[-1] = ''.join([rest[-1], back])

                for i, line in enumerate(rest):
                    self._lines.insert(i + lineno + 1, line)
            self.inserted.fire((lineno, col, text, where))
        except IndexError:
            print locals()
            print self._lines
            raise


    def delete(self, lineno, col, length, linesremoved, where=None):
        if linesremoved == 0:
            line = self._lines[lineno]
            front, back = line[:col], line[col+length:]
            self._lines[lineno] = front + back
        else:
            pass
        self.deleted.fire((lineno, col, length, where))
            

    def add_line(self, line):
        pass

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
        

