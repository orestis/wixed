from nose.tools import assert_equal
from nose import SkipTest
from mock import Mock

import threading
import time

import wx

from main import MainWindow

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
        frame = MainWindow(None, wx.ID_ANY)
 
        #define frame and release lock
        #The lock is used to make sure that SetData is defined.
        self.frame = frame
        self.app = app
        self.lock.release()
 
        app.MainLoop()
 
    def start_local(self):
        self.start_orig()
        #After thread has started, wait until the lock is released
        #before returning so that functions get defined.
        self.lock.acquire()


class GUITest(object):
    start_app = True
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

    def exit(self):
        self.frame.Destroy()
        self.thread.join(5)

    def get_notebook(self):
        return self.frame._nb

    def select_tab_with_title(self, title):
        nb = self.get_notebook()
        page_count = nb.GetPageCount()
        for i in range(page_count):
            if nb.GetPageText(i) == title:
                wx.CallAfter(lambda: nb.SetSelection(i))
                time.sleep(0.2)
                break

    def send_keys(self, keys):
        pass
                


class testMain(GUITest):

    def test_startup(self):
        # When wixed starts up, the title is * Messages *
        assert_equal(self.frame.Title, '* Messages *')

        # there is also another tab, called * Scratch *
        nb = self.get_notebook()
        assert_equal(nb.GetPageText(1), '* Scratch *')

        # clicking on the tab changes the title
        self.select_tab_with_title('* Scratch *')
        assert_equal(self.frame.Title, '* Scratch *')
        self.select_tab_with_title('* Messages *')
        assert_equal(self.frame.Title, '* Messages *')
