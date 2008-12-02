import wx
import os
import wx.stc as stc
from PythonCtrl import PythonSTC
import keyword

from wixed import Buffer

class MainWindow(wx.Frame):
    def __init__(self, parent, id):
        self.buffers = [Buffer('Untitled buffer'), Buffer('another buffer')]
        self._currentBufferIndex = 0
        wx.Frame.__init__(self, parent, id, self.currentBuffer.name, size=(800, 600))
        self.control = PythonSTC(self , self.currentBuffer)
        self.CreateStatusBar()
        self.CreateMenu()
        self.Show(True)

    @property
    def currentBuffer(self):
        return self.buffers[self._currentBufferIndex]

    def OnPreviousBuffer(self, _):
        self._currentBufferIndex -= 1
        if self._currentBufferIndex < 0:
            self._currentBufferIndex = len(self.buffers) - 1
        self.CurrentBufferChanged()

    def OnNextBuffer(self, _):
        self._currentBufferIndex += 1
        if self._currentBufferIndex >= len(self.buffers):
            self._currentBufferIndex = 0
        self.CurrentBufferChanged()

    def CurrentBufferChanged(self):
        self.Title = self.currentBuffer.name
        self.control.buffer = self.currentBuffer


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
        print 'exiting'
        self.Close(True)

    def OnOpen(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.py", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            self.control.SetTextRaw(f.read())
            f.close()
        dlg.Destroy()

    def OnEvalBuffer(self, e):
        text = self.control.GetTextRaw()
        context = {'WIXED': self, 'wx': wx}
        exec(text.replace('\r\n', '\n'), context)


app = wx.PySimpleApp()
frame = MainWindow(None, wx.ID_ANY)

app.MainLoop()
