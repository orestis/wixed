import os
import sys
import keyword

import wx
import wx.aui
import wx.stc as stc

from PythonCtrl import PythonSTC
from editor import FundamentalEditor
from commandline import CommandLineControl
from wixed import BufferManager
from utils import Tee

ID_MAINPANEL = wx.NewId()

class MainWindow(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'title', size=(800, 600))
        self.buffers = BufferManager()
        self.messages_buffer = self.buffers.new('* Messages *')
        scratch = self.buffers.new('* Scratch *')
        self.context = {
            'BUFFERS': self.buffers,
            'wx': wx
        }

        mainPanel = wx.Panel(self, wx.ID_ANY)
        mainPanel.SetBackgroundColour(wx.RED)

        notebookstyle = (
            wx.aui.AUI_NB_DEFAULT_STYLE | wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
            | wx.aui.AUI_NB_WINDOWLIST_BUTTON | wx.aui.AUI_NB_SCROLL_BUTTONS
        )
        self._nb= wx.aui.AuiNotebook(mainPanel, style=notebookstyle)
        self.windows = []
        for b in self.buffers:
            ed = FundamentalEditor(self._nb, wx.NewId(), b)
            self._nb.AddPage(ed, b.name)

        self.current_window_index = self._nb.Selection
        self.CurrentBufferChanged(self.current_window.buffer)

        self.context['NB'] = self._nb
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)

        self.commandLine = CommandLineControl(mainPanel, wx.ID_ANY, size=(125, -1), context=self.context)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._nb, proportion=1, flag=wx.EXPAND)
        box.Add(self.commandLine, proportion=0, flag=wx.EXPAND)

        mainPanel.SetSizer(box)
        mainPanel.SetAutoLayout(True)

        if len(sys.argv) == 1:
            oldstdout = sys.stdout
            oldstderr = sys.stderr
            sys.stdout = Tee(oldstdout, self.messages_buffer)
            sys.stderr = Tee(oldstderr, self.messages_buffer)

        self.CreateStatusBar()
        self.CreateMenu()

        self.Show(True)
        print >> self.messages_buffer, '# Hello!'
        print >> self.messages_buffer, '# Use python in the command line below'
        print >> self.messages_buffer, '# Output goes into this buffer (and in stdout, for post mortems!)'
        print >> self.messages_buffer, '# B is the current buffer'
        print >> self.messages_buffer
        print >> self.messages_buffer, '# You can also eval this buffer'
        print >> self.messages_buffer, '# Try this:'
        print >> self.messages_buffer, 'print >> B, "\'Hello world!\'"'
        print >> self.messages_buffer
        print >> self.messages_buffer, '# Use BUFFERS.new(name) to create a new buffer'
        print >> self.messages_buffer, '# import wixed and utils for handy stuff!'
        print >> self.messages_buffer

        print >> scratch, '# use this buffer to scratch yourself'

    @property
    def current_window(self):
        return self._nb.GetPage(self.current_window_index)

    def OnPageChanged(self, event):
        sel = self._nb.GetSelection()
        self.current_window_index = sel
        self.Title = self.current_window.buffer.name
        self.context['B'] = self.current_window.buffer
        event.Skip()

    def OnPreviousBuffer(self, _):
        newbuf = self.buffers.previous(frombuf=self.current_window.buffer)
        self.CurrentBufferChanged(newbuf)

    def OnNextBuffer(self, _):
        newbuf = self.buffers.next(frombuf=self.current_window.buffer)
        self.CurrentBufferChanged(newbuf)

    def CurrentBufferChanged(self, newbuffer):
        self.Title = newbuffer.name
        self.current_window.buffer = newbuffer
        self._nb.SetPageText(self.current_window_index, newbuffer.name)
        self.context['B'] = self.current_window.buffer


    def CreateMenu(self):
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_OPEN, "&Open", "Open file...")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_ABOUT, "&About", "info")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "exit")

        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)
        #wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)

        evalMenu = wx.Menu()
        evalMenu.Append(201, "Eval buffer")
        self.Bind(wx.EVT_MENU, self.OnEvalBuffer, id=201)

        bufferMenu = wx.Menu()
        bufferMenu.Append(301, "&Next buffer")
        bufferMenu.Append(302, "&Previous buffer")
        self.Bind(wx.EVT_MENU, self.OnNextBuffer, id=301)
        self.Bind(wx.EVT_MENU, self.OnPreviousBuffer, id=302)

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(evalMenu, "E&val")
        menuBar.Append(bufferMenu, "&Buffers")
        self.SetMenuBar(menuBar)

    def OnAbout(self, e):
        d = wx.MessageDialog(self, "sample editor", 'about', wx.OK)
        d.ShowModal()
        d.Destroy()

    def OnExit(self, e):
        self.Close(True)

    #def OnOpen(self, e):
    #    self.dirname = ''
    #    dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.py", wx.OPEN)
    #    if dlg.ShowModal() == wx.ID_OK:
    #        self.filename = dlg.GetFilename()
    #        self.dirname = dlg.GetDirectory()
    #        f = open(os.path.join(self.dirname, self.filename), 'r')
    #        self.editor.SetTextRaw(f.read())
    #        f.close()
    #    dlg.Destroy()

    def OnEvalBuffer(self, e):
        text = self.current_window.buffer.text
        exec(text.replace('\r\n', '\n'), self.context)


app = wx.PySimpleApp()
frame = MainWindow(None, wx.ID_ANY)

app.MainLoop()
