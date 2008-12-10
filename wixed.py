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
        self._lines = ['']
        self._curpos = 0
        self._anchor = 0
        self.changed = EventHook()

    curpos = observed('_curpos', lambda s: s.changed)
    anchor = observed('_anchor', lambda s: s.changed)

    #@property
    #def text(self):
    #    return '\n'.join(self._lines)
embolimo
keimeno

    def write(self, v):
        self.text += v
        self._curpos = len(self.text)
        self._anchor = len(self.text)
        self.changed.fire(v)

    def insert(self, lineno, col, text, linesadded):
        print locals()
        #import pdb; pdb.set_trace()
        try:
            if linesadded == 0:
                line = self._lines[lineno]
                front, back = line[:col], line[col:]
                newline = ''.join([front, text, back])
                self._lines[lineno] = newline
            else:
                #import pdb; pdb.set_trace()
                print 'before insert', self._lines
                middle = text.split('\n') # splitlines doesn't return the empty new line
                # the first line has to be joined with existing one
                first, rest = middle[0], middle[1:]
                print 'first, rest', first, rest
                line = self._lines[lineno]
                front, back = line[:col], line[col:]
                newline = ''.join([front, first])
                self._lines[lineno] = newline
                print 'newline', newline
                print 'after first line', self._lines

                #the rest we can just insert
                for i, line in enumerate(rest):
                    idx = i + lineno + 1
                    print 'inserting', repr(line), 'at', idx
                    self._lines.insert(idx, line)
                # finish off by writing the last line, the split one
                if back:
                    print 'inserting back', repr(back), 'at', idx + 1
                    self._lines.insert(idx + 1, back)
        except IndexError:
            print locals()
            print self._lines
            raise
        print self._lines


    def delete(self, line, col, length, linesremoved):
        print 'deleting'
        print locals()

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
        

