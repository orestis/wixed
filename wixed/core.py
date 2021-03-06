import subprocess
import os
import signal

import wx

from wixed.utils import Pipe, CircleList, EventHook, observed
from wixed.editor import FundamentalEditor, PythonEditor


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
        self._lines = [u'']
        self._obs_lines = ObservedList(self._lines, self._observe_list)
        self._curpos = 0
        self._anchor = 0
        self.pos_changed = EventHook()
        self.inserted = EventHook()
        self.deleted = EventHook()
        self.events = []
        self.read_pos = 0

    def _observe_list(self, method, *args):
        if method == '__setitem__':
            lineno, line = args
            self.delete(lineno, 0, self._lines[lineno], 0)
            self.insert(lineno, 0, line, 0)
        elif method == '__delslice__':
            start, end = args
            if end > len(self._lines) - 1:
                end = len(self._lines) - 1

            for idx in range(end, start - 1, -1):
                self.delete(idx, 0, self._lines[idx], -1)
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

    def read(self, length):
        text = self.text[self.read_pos:length]
        self.read_pos += len(text)
        return text

    def write(self, v):
        u_v = v.decode('utf-8').replace('\r\n', '\n')
        self.insert(len(self._lines) - 1, # last line
                    len(self._lines[-1]), # after the last character
                    u_v,
                    u_v.count('\n'))
        self.scroll_to_end()

    def scroll_to_end(self):
        self._anchor = len(self.text)
        self.curpos = len(self.text)

    def insert(self, lineno, col, text, linesadded, where=None):
        self._insert(lineno, col, text, linesadded, where)
        self.inserted.fire((lineno, col, text, where))

    def _insert(self, lineno, col, text, linesadded, where):
        self.events.append(('insert', self.text, self._lines, locals()))
        
        line = self._lines[lineno]
        front, back = line[:col], line[col:]
            
        if linesadded == 0:
            newline = u''.join([front, text, back])
            self._lines[lineno] = newline
        else:
            middle = text.split('\n') # splitlines doesn't return an empty new line
            first, rest = middle[0], middle[1:]

            newline = u''.join([front, first])
            self._lines[lineno] = newline

            if back:
                rest[-1] = u''.join([rest[-1], back])

            for i, line in enumerate(rest):
                self._lines.insert(i + lineno + 1, line)


    def delete(self, lineno, col, text, linesremoved, where=None):
        self._delete(lineno, col, text, linesremoved, where)
        self.deleted.fire((lineno, col, text, where))


    def _delete(self, lineno, col, text, linesremoved, where):
        self.events.append(('delete', self.text, self._lines, locals()))
        length = len(text)
        if linesremoved == 0:
            line = self._lines[lineno]
            front, back = line[:col], line[col+length:]
            self._lines[lineno] = front + back
        else:
            changedlines = self._lines[lineno : lineno + abs(linesremoved) + 1]
            afterlines = self._lines[lineno + abs(linesremoved) + 1:]
            text = u'\n'.join(changedlines)
            front, back = text[:col], text[col+length:]
            newtext = front + back
            newlines = newtext.splitlines()
            if not newlines:
                newlines.append(u'')
            del self._lines[lineno:]
            self._lines.extend(newlines)
            self._lines.extend(afterlines)
        if not self._lines:
            self._lines.append(u'')

            

    def __repr__(self):
        return 'Buffer <%r>' % self.name

class FileBuffer(Buffer):
    def __init__(self, filepath):
        name = os.path.basename(filepath)
        super(FileBuffer, self).__init__(name)
        self.filepath = filepath
        f = open(filepath)
        self.write(f.read())
        f.close()

    def save(self):
        tempfilepath = self.filepath + '.__wixedsave__'
        tempfile = open(tempfilepath, 'wb')
        tempfile.write(self.text)
        tempfile.close()
        os.rename(tempfilepath, self.filepath)


class BufferManager(object):
    def __init__(self):
        self._buffers = []
        self._names_to_bufs = {}
        self._bufs_to_indexes = {}
        self.buffer_created = EventHook()

    @property
    def buffers(self):
        return self._buffers

    def _register_buffer(self, b):
        self._buffers.append(b)
        self._bufs_to_indexes[b] = len(self._buffers) - 1
        self._names_to_bufs[b.name] = b
        self.buffer_created.fire(b)

    def visit(self, *args, **kwargs):
        b = FileBuffer(*args, **kwargs)
        self._register_buffer(b)
        return b

    def new(self, *args, **kwargs):
        b = Buffer(*args, **kwargs)
        self._register_buffer(b)
        return b

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._buffers[item]
        else:
            return self._names_to_bufs[item]

    def __len__(self):
        return len(self._buffers)

    def __iter__(self):
        return iter(self._buffers)

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
        

class Shell(object):
    def __init__(self, shell, buffer, args=None):
        try:
            import pexpect
        except ImportError:
            from external import wexpect as pexpect
        self._buffer = buffer
        if args is None:
            args = []
        self.popen = pexpect.spawn(shell, args)
        self.popen.setecho(False)
        Pipe(self.popen, self._buffer)

    def kill(self):
        self.popen.close(True)

