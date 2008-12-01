import wx
import os
import wx.stc

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400, 400))
        self.control = wx.stc.StyledTextCtrl(self, 1, style=wx.TE_MULTILINE)
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

        faces = {
            'mono' : 'Consolas',
            'size' : 12,
            'size2' : 10,
        }
        
        # Global default styles for all languages
        self.control.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,     "face:%(mono)s,size:%(size)d" % faces)
        self.control.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(mono)s,size:%(size2)d" % faces)
        self.control.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "face:%(mono)s" % faces)
        self.control.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.control.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        # Python styles
        # White space
        self.control.StyleSetSpec(wx.stc.STC_P_DEFAULT, "fore:#808080,face:%(mono)s,size:%(size)d" % faces)
        # Comment
        self.control.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(mono)s,size:%(size)d" % faces)
        # Number
        self.control.StyleSetSpec(wx.stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.control.StyleSetSpec(wx.stc.STC_P_STRING, "fore:#7F007F,italic,face:%(mono)s,size:%(size)d" % faces)
        # Single quoted string
        self.control.StyleSetSpec(wx.stc.STC_P_CHARACTER, "fore:#7F007F,italic,face:%(mono)s,size:%(size)d" % faces)
        # Keyword
        self.control.StyleSetSpec(wx.stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.control.StyleSetSpec(wx.stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.control.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.control.StyleSetSpec(wx.stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.control.StyleSetSpec(wx.stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.control.StyleSetSpec(wx.stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.control.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, "fore:#808080,face:%(mono)s,size:%(size)d" % faces)
        # Comment-blocks
        self.control.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.control.StyleSetSpec(wx.stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        #self.control.SetViewWhiteSpace(wx.stc.STC_WS_VISIBLEAFTERINDENT)

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
            self.control.SetLexer(wx.stc.STC_LEX_PYTHON)
            f.close()
        dlg.Destroy()

    def OnEvalBuffer(self, e):
        text = self.control.GetTextRaw()
        context = {'WIXED': self, 'wx': wx}
        exec(text.replace('\r\n', '\n'), context)


app = wx.PySimpleApp()
frame = MainWindow(None, wx.ID_ANY, "Small editor")

app.MainLoop()
