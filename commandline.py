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
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.handler = CommandLineHandler()
        self.handler.line_changed('')
        style = self.DefaultStyle
        font = style.GetFont()
        font.SetFamily(wx.TELETYPE)
        font.SetFaceName('Monaco')
        font.SetPointSize(12)
        style.SetFont(font)
        self.SetDefaultStyle(style)

    def Flash(self):
        wx.Bell()

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.handler.execute(self.context)
            self.SetValue('')
        elif key == wx.WXK_DOWN:
            try:
                self.handler.next()
                self.SetValue(self.handler.command)
                self.SetInsertionPoint(len(self.handler.command))
            except IndexError:
                self.handler.line_changed('')
                self.SetValue('')
        elif key == wx.WXK_UP:
            try:
                self.handler.previous()
            except IndexError:
                self.Flash()
            self.SetValue(self.handler.command)
            self.SetInsertionPoint(len(self.handler.command))

        elif key == wx.WXK_ESCAPE:
            self.handler.line_changed('')
            self.SetValue('')
        else:
            event.Skip()
            wx.CallAfter(self.handler.line_changed, self.GetValue)


