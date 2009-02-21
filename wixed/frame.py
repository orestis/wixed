import wx.aui

from wixed.commandline import CommandLineControl
from wixed.editor import PythonEditor
from wixed.utils import EventHook

ID_MAINPANEL = wx.NewId()

class Frame(wx.Frame):
    def _setup(self):
        self.CreateMenu()

        mainPanel = wx.Panel(self, wx.ID_ANY)
        mainPanel.SetBackgroundColour(wx.RED)

        notebookstyle = (
            wx.aui.AUI_NB_DEFAULT_STYLE | wx.aui.AUI_NB_TAB_EXTERNAL_MOVE
            | wx.aui.AUI_NB_WINDOWLIST_BUTTON | wx.aui.AUI_NB_SCROLL_BUTTONS
            | wx.aui.AUI_NB_TAB_FIXED_WIDTH
        )
        self._nb= wx.aui.AuiNotebook(mainPanel, style=notebookstyle)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnPageClose)

        self.commandLine = CommandLineControl(mainPanel, wx.ID_ANY, size=(125, -1))
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._nb, proportion=1, flag=wx.EXPAND)
        box.Add(self.commandLine, proportion=0, flag=wx.EXPAND)

        mainPanel.SetSizer(box)
        mainPanel.SetAutoLayout(True)

        self.CreateStatusBar()


    def __init__(self, session):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'title', size=(800, 600))

        self.session = session
        self._setup()

        self.buffer_changed = EventHook()
        self.session.buffers.buffer_created += self.OnNewBuffer

        for b in session.buffers:
            self.OnNewBuffer(b)
            ed = PythonEditor(self._nb, wx.NewId(), b, session.keydown)
            self._nb.AddPage(ed, b.name)

        self.current_window_index = self._nb.Selection
        self.CurrentBufferChanged(self.current_window.buffer)

        self.session.keymap['m-x'] = lambda _: self.commandLine.SetFocus()
        self.commandLine.handler.execute += self.session.execute
        self.commandLine.unfocus += lambda: self.current_window.SetFocus()

        self.Show(True)


    @property
    def current_window(self):
        return self._nb.GetPage(self.current_window_index)

    def OnPageClose(self, event):
        ed = self._nb.GetPage(event.Selection)
        self.windows.remove(ed)
        event.Skip()

    def OnPageChanged(self, event):
        sel = self._nb.GetSelection()
        self.current_window_index = sel
        self.Title = self.current_window.buffer.name
        self.buffer_changed.fire(self.current_window.buffer)
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
        self.current_window.SetFocus()
        self.buffer_changed.fire(newbuffer)

    def OnNewBuffer(self, newbuf):
        mb = self.GetMenuBar()
        theid = mb.FindMenu('Buffers')
        menu = mb.GetMenu(theid)
        menuitem = menu.Append(wx.NewId(), newbuf.name)
        self.Bind(wx.EVT_MENU, lambda _: self.CurrentBufferChanged(newbuf), menuitem)

    def CreateMenu(self):
        filemenu = wx.Menu()
        filemenu.Append(wx.ID_OPEN, "&Open", "Open file...")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_ABOUT, "&About", "info")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT, "E&xit", "exit")

        wx.EVT_MENU(self, wx.ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnExit)

        evalMenu = wx.Menu()
        evalMenu.Append(201, "Eval buffer")
        self.Bind(wx.EVT_MENU, self.OnEvalBuffer, id=201)

        bufferMenu = wx.Menu()
        bufferMenu.Append(301, "&Next buffer")
        bufferMenu.Append(302, "&Previous buffer")
        bufferMenu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.OnNextBuffer, id=301)
        self.Bind(wx.EVT_MENU, self.OnPreviousBuffer, id=302)

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(evalMenu, "E&val")
        menuBar.Append(bufferMenu, "&Buffers")
        self.SetMenuBar(menuBar)

    def OnAbout(self, e):
        d = wx.MessageDialog(self, "Wicked!", 'About Wixed', wx.OK)
        d.ShowModal()
        d.Destroy()

    def OnExit(self, e):
        self.Close(True)

    def OnEvalBuffer(self, e):
        text = self.current_window.buffer.text
        exec(text.replace('\r\n', '\n'), self.session.context)



