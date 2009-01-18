import wx
from wixed.window import MainWindow

if __name__ == '__main__':
    app = wx.PySimpleApp()
    app.AppName = u'Wixed'
    frame = MainWindow(None, wx.ID_ANY)

    app.MainLoop()
