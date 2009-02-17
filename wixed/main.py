import wx
import sys

from wixed.session import Session
from wixed.utils import Tee

def init_session():
    s = Session()
    messages_buffer = s.buffers.new('* Messages *')
    scratch_buffer = s.buffers.new('* Scratch *')
    if len(sys.argv) == 1:
        oldstdout = sys.stdout
        oldstderr = sys.stderr
        sys.stdout = Tee(oldstdout, messages_buffer)
        sys.stderr = Tee(oldstderr, messages_buffer)

    print >> messages_buffer, '# Hello!'
    print >> messages_buffer, '# Use python in the command line below'
    print >> messages_buffer, '# Output goes into this buffer (and in stdout, for post mortems!)'
    print >> messages_buffer, '# B is the current buffer'
    print >> messages_buffer
    print >> messages_buffer, '# You can also eval this buffer'
    print >> messages_buffer, '# Try this:'
    print >> messages_buffer, 'print >> B, "\'Hello world!\'"'
    print >> messages_buffer
    print >> messages_buffer, '# Use BUFFERS.new(name) to create a new buffer'
    print >> messages_buffer, '# import wixed and utils for handy stuff!'
    print >> messages_buffer

    print >> scratch_buffer, '# Use this buffer for scratching'
    return s

if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.AppName = u'Wixed'

    s = init_session()

    s.make_frame()
    app.MainLoop()
