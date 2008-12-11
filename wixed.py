import subprocess
import os
import signal

import wx

from utils import Pipe, CircleList, EventHook, observed
from editor import FundamentalEditor

class WindowManager(object):
    def __init__(self, parent, onnew):
        self._windows = []
        self._parent = parent
        self._eds_to_windows = {}
        self.onnew = onnew

    @property
    def windows(self):
        return self._windows

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._windows[item]
        else:
            return self._eds_to_windows[item]


    def __len__(self):
        return len(self._windows)

    def remove(self, ed):
        w = self._eds_to_windows[ed]
        self._windows.remove(w)
        del self._eds_to_windows[ed]


    def new(self, buffer):
        try:
            editor = FundamentalEditor(self._parent, wx.NewId(), buffer)
            w = Window(buffer, editor)
            self._eds_to_windows[editor] = w
            self._windows.append(w)
            self.onnew(w)
            return w
        except Exception, e:
            print e


class Window(object):
    def __init__(self, buffer, editor):
        self._buffer = buffer
        self.editor = editor

    def __set_buffer(self, newbuffer):
        self._buffer = newbuffer
        self.editor.buffer = newbuffer

    buffer = property(lambda self: self._buffer, __set_buffer)

    def __repr__(self):
        return 'Window <%r>' % self.buffer

def notifier(field):
    def func(self, *args):
        self._notify(field, *args)
    func.__name__ = field
    return func

def delegate(field):
    def func(self, *args):
        return getattr(self._l, field)(*args)
    func.__name__ = field
    return func

class ObservedList(object):
    def __init__(self, l, notify):
        self._l = l
        self._notify = notify

    append = notifier('append')
    insert = notifier('insert')
    extend = notifier('extend')
    sort = notifier('sort')
    reverse = notifier('reverse')
    remove = notifier('remove')
    __contains__ = delegate('__contains__')
    __delslice__ = notifier('__delslice__')
    __delitem__ = notifier('__delitem__')
    __reversed__ = delegate('__reversed__')
    __rmul__ = notifier('__rmul__')
    __setslice__ = notifier('__setslice__')
    __setitem__ = notifier('__setitem__')
    __eq__ = delegate('__eq__')
    __ne__ = delegate('__ne__')
    __iter__ = delegate('__iter__')
    __len__ = delegate('__len__')
    __str__ = delegate('__str__')
    __repr__ = delegate('__repr__')
    __getslice__ = delegate('__getslice__')
    __getitem__ = delegate('__getitem__')


class Buffer(object):
    def __init__(self, name):
        self.name = name
        self._lines = ['']
        self._obs_lines = ObservedList(self._lines, self._observe_list)
        self._curpos = 0
        self._anchor = 0
        self.pos_changed = EventHook()
        self.inserted = EventHook()
        self.deleted = EventHook()
        self.events = []

    def _observe_list(self, method, *args):
        if method == '__setitem__':
            lineno, line = args
            self.delete(lineno, 0, len(self._lines[lineno]), 0)
            self.insert(lineno, 0, line, 0)
        elif method == '__delslice__':
            start, end = args
            if end > len(self._lines) - 1:
                end = len(self._lines) - 1

            for idx in range(end, start - 1, -1):
                self.delete(idx, 0, len(self._lines[idx]), -1)
        elif method == 'extend':
            iterable = args[0]
            lineno = len(self._lines) - 1
            for idx, line in enumerate(iterable):
                self.insert(lineno + idx, 0, line+'\n', 1)
        elif method == 'insert':
            lineno, line = args
            self.insert(lineno, 0, line+'\n', 1)
        elif method == 'append':
            line = args[0]
            self.insert(len(self._lines) - 1, 0, line+'\n', 1)
        else:
            raise Exception('Sorry; Unknown modification to list: %s' % method)

    curpos = observed('_curpos', lambda s: s.pos_changed)
    anchor = observed('_anchor', lambda s: s.pos_changed)

    @property
    def text(self):
        return '\n'.join(self._lines)

    @property
    def lines(self):
        return self._obs_lines

    def write(self, v):
        u_v = v.decode('utf-8').replace('\r\n', '\n')
        self.insert(len(self._lines) - 1, # last line
                    len(self._lines[-1]), # after the last character
                    u_v,
                    u_v.count('\n'))
        self.scroll_to_end()

    def scroll_to_end(self):
        self._anchor = -1
        self.curpos = -1

    def insert(self, lineno, col, text, linesadded, where=None):
        self.events.append(('insert', self.text, self._lines, locals()))
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


    def delete(self, lineno, col, length, linesremoved, where=None):
        self.events.append(('delete', self.text, self._lines, locals()))
        if linesremoved == 0:
            line = self._lines[lineno]
            front, back = line[:col], line[col+length:]
            self._lines[lineno] = front + back
        else:
            changedlines = self._lines[lineno : lineno + abs(linesremoved) + 1]
            afterlines = self._lines[lineno + abs(linesremoved) + 1:]
            text = '\n'.join(changedlines)
            front, back = text[:col], text[col+length:]
            newtext = front + back
            newlines = newtext.splitlines()
            if not newlines:
                newlines.append('')
            del self._lines[lineno:]
            self._lines.extend(newlines)
            self._lines.extend(afterlines)
        if not self._lines:
            self._lines.append('')


        self.deleted.fire((lineno, col, length, where))
            

    def __repr__(self):
        return 'Buffer <%r>' % self.name



class BufferManager(object):
    def __init__(self, onnew=None):
        self._buffers = []
        self._names_to_bufs = {}
        self._bufs_to_indexes = {}
        self.onnew = onnew

    @property
    def buffers(self):
        return self._buffers

    def new(self, *args, **kwargs):
        b = Buffer(*args, **kwargs)
        self._buffers.append(b)
        self._bufs_to_indexes[b] = len(self._buffers) - 1
        self._names_to_bufs[b.name] = b
        if self.onnew:
            self.onnew(b)
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
        

