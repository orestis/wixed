from utils import HistoryList

class CommandLineHandler(object):

    def __init__(self):
        self.command = ''
        self.history = HistoryList()

    def line_changed(self, line):
        if callable(line):
            line = line()
        self.command = line
        self.history.reset()

    def previous(self):
        try:
            self.history.previous()
        finally:
            self.command = self.history.current

    def next(self):
        try:
            self.history.next()
        finally:
            self.command = self.history.current

    def execute(self, context):
        if self.command == '':
            return
        self.history.append(self.command)
        try:
            exec(self.command, context)
        except Exception, e:
            print e


import wx
class CommandLineControl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context')
        self.context['CMD'] = self
        style = kwargs.get('style', 0)
        style |= wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_RICH2 # TE_RICH2 for windows
        kwargs ['style'] = style
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.handler = CommandLineHandler()
        self.handler.line_changed('')
        style = self.DefaultStyle
        if wx.Platform == '__WXMSW__':
            font = wx.SystemSettings.GetFont(wx.SYS_ANSI_FIXED_FONT)
        else:
            font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        style.SetFont(font)
        self.style = style
        self.SetDefaultStyle(style)

    def Flash(self):
        wx.Bell()

    def ChangeValue(self, v):
        wx.TextCtrl.ChangeValue(self, v)
        self.SetStyle(0, len(v), self.style)

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.handler.execute(self.context)
            self.ChangeValue('')
        elif key == wx.WXK_DOWN:
            try:
                self.handler.next()
                self.ChangeValue(self.handler.command)
                self.SetInsertionPoint(len(self.handler.command))
            except IndexError:
                self.handler.line_changed('')
                self.ChangeValue('')
        elif key == wx.WXK_UP:
            try:
                self.handler.previous()
            except IndexError:
                self.Flash()
            self.ChangeValue(self.handler.command)
            self.SetInsertionPoint(len(self.handler.command))

        elif key == wx.WXK_ESCAPE:
            self.handler.line_changed('')
            self.ChangeValue('')
        else:
            event.Skip()
            wx.CallAfter(self.handler.line_changed, self.GetValue)


