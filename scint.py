import wx
import os
import wx.stc as stc
from PythonCtrl import PythonSTC
import keyword

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400, 400))
        self.control = PythonSTC(self, 1)
        self.CreateStatusBar()

        filemenu = wx.Menu()
        filemenu.Append(wx.ID_OPEN, "&Open", "Open file...")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_ABOUT, "&About", "info")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "exit")

        evalMenu = wx.Menu()
        evalMenu.Append(201, "Eval buffer")

        self.Bind(wx.EVT_MENU, self.OnEvalBuffer, id=201)

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(evalMenu, "E&val")
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, wx.ID_OPEN, self.OnOpen)

        self.Show(True)



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
frame = MainWindow(None, wx.ID_ANY, "Small editor")

app.MainLoop()
