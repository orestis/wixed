from wixed.utils import HistoryList, EventHook
from wixed.core import Process

class CommandDispatcher(object):
    def execute(self, command, context):
        if command.startswith('!'):
            if '>>' in command:
                command, pipe = command.split('>>')
                output_buf = context[pipe.strip()]
            else:
                output_buf = context['BUFFERS'].new('* output *')
                
            Process(command[1:].split(), buffer=output_buf)


class CommandLineHandler(object):

    def __init__(self):
        self.command = ''
        self.history = HistoryList()
        self.dispatcher = CommandDispatcher()
        self.execute = EventHook()

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

    def finish(self):
        if self.command == '':
            return
        self.history.append(self.command)
        self.execute.fire(self.command)



import wx
class CommandLineControl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
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
        self.unfocus = EventHook()

    def Flash(self):
        wx.Bell()

    def ChangeValue(self, v):
        wx.TextCtrl.ChangeValue(self, v)
        self.SetStyle(0, len(v), self.style)

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.handler.finish()
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
            self.unfocus.fire()
        else:
            event.Skip()
            wx.CallAfter(self.handler.line_changed, self.GetValue)


