
class CommandLineHandler(object):

    def __init__(self):
        self.command = ''
        self.history = []
        self._index = 0

    def line_changed(self, line):
        if callable(line):
            line = line()
        self.command = line
        self._index = 0

    def go_previous(self):
        self._index -= 1
        try:
            if self._index < 0:
                raise IndexError
            self.command = self.history[self._index]
        except IndexError:
            self._index = 0 # no more, go to the first

    def go_next(self):
        self._index += 1
        if self._index == 0 or self._index == len(self.history):
            self.command = ''
            self._index = len(self.history) - 1
        else:
            try:
                self.command = self.history[self._index]
            except IndexError:
                self._index = len(self.history) - 1

    def execute(self, context):
        self.history.append(self.command)
        self._index = len(self.history) - 1
        try:
            exec(self.command, context)
        except Exception, e:
            print e


import wx
class CommandLineControl(wx.TextCtrl):
    def __init__(self, *args, **kwargs):
        self.context = kwargs.pop('context')
        wx.TextCtrl.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.handler = CommandLineHandler()

    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
            self.handler.execute(self.context)
            self.SetValue('')
        elif key == wx.WXK_DOWN:
            wx.WXK_ESCAPE
            self.handler.go_next()
            self.SetValue(self.handler.command)
            self.SetInsertionPoint(len(self.handler.command))
        elif key == wx.WXK_UP:
            self.handler.go_previous()
            self.SetValue(self.handler.command)
            self.SetInsertionPoint(len(self.handler.command))
        elif key == wx.WXK_ESCAPE:
            self.handler.line_changed('')
            self.SetValue('')
        else:
            event.Skip()
            wx.CallAfter(self.handler.line_changed, self.GetValue)


