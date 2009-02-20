from nose.tools import assert_equal
import sys

import threading
import time
from StringIO import StringIO

import wx

from wixed.main import init_session

sys.path.append('Lib') # also needs to have libeventsim.dylib _directly_ on the root.
from eventsim import UIEventSimulator

_keys_to_codes = {
    u'\x08': 51, u'\t': 48, u'\r': 76, u'\x10': 112, u'\x1b': 71, u' ': 49,
    u"'": 39, u'*': 67, u'+': 69, u',': 43, u'-': 78, u'.': 65, u'/': 75, u'0':
    82, u'1': 83, u'2': 84, u'3': 85, u'4': 86, u'5': 87, u'6': 88, u'7': 89,
    u'8': 91, u'9': 92, u';': 41, u'=': 81, u'[': 33, u'\\': 42, u']': 30,
    u'`': 50, u'a': 0, u'b': 11, u'c': 8, u'd': 2, u'e': 14, u'f': 3, u'g': 5,
    u'h': 4, u'i': 34, u'j': 38, u'k': 40, u'l': 37, u'm': 46, u'n': 45, u'o':
    31, u'p': 35, u'q': 12, u'r': 15, u's': 1, u't': 17, u'u': 32, u'v': 9,
    u'w': 13, u'x': 7, u'y': 16, u'z': 6, u'\x7f': 117, u'\xa4': 10, u'\u0138':
    119, u'\u0139': 115, u'\u013a': 123, u'\u013b': 126, u'\u013c': 124,
    u'\u013d': 125, u'\u0143': 114, u'\u0154': 122, u'\u0155': 120, u'\u0156':
    99, u'\u0157': 118, u'\u0158': 96, u'\u0159': 97, u'\u015a': 98, u'\u0160':
    105, u'\u016e': 116, u'\u016f': 121
}

def mainloop(app):
    app.MainLoop()

class MainThread(threading.Thread):
    def __init__(self, autoStart=True):
        threading.Thread.__init__(self)
        self.setDaemon(1)
        self.start_orig = self.start
        self.start = self.start_local
        self.frame = None # to be defined in self.run
        self.app = None # ditto
        self.lock = threading.Lock()
        self.lock.acquire() #lock until variables are set
        if autoStart:
             self.start() #automatically start thread on init

    def run(self):
        app = wx.PySimpleApp()
        s = init_session()
        f = s.make_frame()
 
        #define frame and release lock
        #The lock is used to make sure that SetData is defined.
        self.frame = f
        self.app = app
        self.session = s
        self.lock.release()
 
        app.MainLoop()
 
    def start_local(self):
        self.start_orig()
        #After thread has started, wait until the lock is released
        #before returning so that functions get defined.
        self.lock.acquire()


class GUITest(object):
    start_app = True
    def __init__(self):
        self.events = UIEventSimulator()

    def setup(self):
        if self.start_app:
            self.launch()

    def teardown(self):
        if self.start_app:
            self.exit()

    def launch(self):
        self.thread = MainThread()
        self.app = self.thread.app
        self.frame = self.thread.frame
        self.session = self.thread.session

    def exit(self):
        self.frame.Destroy()
        self.thread.join(5)

    def get_notebook(self):
        return self.frame._nb

    def select_tab(self, title):
        nb = self.get_notebook()
        i = self._nb_title_to_index(title)
        wx.CallAfter(lambda: nb.SetSelection(i))
        time.sleep(0.2)

    def _nb_title_to_index(self, title):
        nb = self.get_notebook()
        page_count = nb.GetPageCount()
        for i in range(page_count):
            if nb.GetPageText(i) == title:
                return i

    def get_tab(self, title):
        return self.get_notebook().GetPage(self._nb_title_to_index(title))


    def send_keys(self, keys, shift=False, cmd=False, alt=False):
        for key in keys:
            self.events.KeyChar(_keys_to_codes[key], shift, cmd, alt)
        time.sleep(0.2)


class testMain(GUITest):
    GUI = True

    def test_startup(self):
        # When wixed starts, a frame appears
        # When wixed starts up, the title is * Messages *
        assert_equal(self.frame.Title, '* Messages *')

        # there is also another tab, called * Scratch *
        nb = self.get_notebook()
        assert_equal(nb.GetPageText(0), '* Messages *')
        assert_equal(nb.GetPageText(1), '* Scratch *')

        # the first tab has keyboard focus

        assert_equal(self.frame.FindFocus(), nb.GetPage(0))

        # clicking on the tab changes the title
        self.select_tab('* Scratch *')
        assert_equal(self.frame.Title, '* Scratch *')
        self.select_tab('* Messages *')
        assert_equal(self.frame.Title, '* Messages *')

        # typing something in the scratch buffer produces some text
        self.select_tab('* Scratch *')
        # abc in mac way - need to implement that in eventsim
        self.send_keys('abc')

        scratch = self.session.buffers['* Scratch *']
        assert 'abc' in scratch.text

    def test_commandline(self):
        # hitting m-x should focus commandline
        cmdLine = self.frame.commandLine
        self.select_tab('* Scratch *')
        assert cmdLine != cmdLine.FindFocus(), 'should not have focus by default'
        self.send_keys('x', cmd=True)
        assert cmdLine == cmdLine.FindFocus() 

        self.send_keys("print 'commandline'\r")
        messages = self.session.buffers['* Messages *']
        assert 'commandline' in messages.text

        self.send_keys('\x1b') # ESC
        assert_equal(self.frame.FindFocus(), self.get_tab('* Scratch *'))




