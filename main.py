import os
import sys
import keyword

import wx
import wx.stc as stc

from PythonCtrl import PythonSTC
from commandline import CommandLineControl
from wixed import BufferManager

ID_MAINPANEL = wx.NewId()

class MainWindow(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'title', size=(800, 600))
        self.buffers = BufferManager()
        self.buffers.updateFunc = self.CurrentBufferChanged
        self.messages_buffer = self.buffers.new('* Messages *')
        self.mainPanel = wx.Panel(self, wx.ID_ANY)
        self.mainPanel.SetBackgroundColour(wx.RED)
        self.editor = PythonSTC(self.mainPanel , self.messages_buffer)
        self.context = {
            'STC': self.editor, 'BUFFERS': self.buffers,
            'wx': wx, 'B': self.buffers.current
        }
        sys.stdout = self.messages_buffer
        sys.stderr = self.messages_buffer

        self.commandLine = CommandLineControl(self.mainPanel, wx.ID_ANY, size=(125, -1), context=self.context)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.editor, proportion=1, flag=wx.EXPAND)
        box.Add(self.commandLine, proportion=0, flag=wx.EXPAND)

        self.mainPanel.SetSizer(box)
        self.mainPanel.SetAutoLayout(True)

        self.CreateStatusBar()
        self.CreateMenu()

        self.CurrentBufferChanged()
        self.Show(True)

    def OnPreviousBuffer(self, _):
        self.buffers.previous()

    def OnNextBuffer(self, _):
        self.buffers.next()

    def CurrentBufferChanged(self):
        self.Title = self.buffers.current.name
        self.editor.buffer = self.buffers.current
        self.context['B'] = self.buffers.current


    def CreateMenu(self):
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_OPEN, "&Open", "Open file...")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_ABOUT, "&About", "info")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "exit")

        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)

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

    def OnOpen(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.py", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.editor.SetTextRaw(f.read())
            f.close()
        dlg.Destroy()

    def OnEvalBuffer(self, e):
        text = self.editor.GetTextRaw()
        exec(text.replace('\r\n', '\n'), self.context)


app = wx.PySimpleApp()
frame = MainWindow(None, wx.ID_ANY)

app.MainLoop()
