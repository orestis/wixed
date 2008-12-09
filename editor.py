import time
from threading import Thread

import wx
from wx import stc

TABWIDTH = 4

class FundamentalEditor(stc.StyledTextCtrl):
    def __init__(self, parent, ID, buffer):
        stc.StyledTextCtrl.__init__(self, parent, ID, style=wx.BORDER_NONE)

        self._Setup()

        self._buffer = buffer
        self.SetText(self._buffer.text)
        t = Thread(target=self.QueryBuffer)
        t.start()
        
    def __set_buffer(self, newbuffer):
        self.SyncToBuffer()
        self._buffer = newbuffer
        self.SetText(self._buffer.text)
        self.SyncFromBuffer()

    buffer = property(lambda self: self._buffer, __set_buffer)

    def QueryBuffer(self):
        while True:
            try:
                if self.buffer.pending:
                    wx.CallAfter(self.SyncFromBuffer)
                time.sleep(0.1)
            except wx.PyDeadObjectError:
                break


    def SyncFromBuffer(self):
        self.AppendText(''.join(self.buffer.pending))
        self.buffer.synced()
        self.SetAnchor(self.buffer.anchor)
        self.GotoPos(self.buffer.curpos)

    def SyncToBuffer(self):
        self.buffer.text = self.GetText()
        self.buffer.synced()
        self.buffer.curpos = self.GetCurrentPos()
        self.buffer.anchor = self.GetAnchor()




    def _Setup(self):
        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.CmdKeyAssign(ord('W'), stc.STC_SCMOD_CTRL, stc.STC_CMD_WORDRIGHT)
        self.CmdKeyAssign(ord('W'), stc.STC_SCMOD_CTRL | stc.STC_SCMOD_SHIFT, stc.STC_CMD_WORDLEFT)

        self.SetBufferedDraw(True)
        self.SetUseAntiAliasing(True)

        # Set left and right margins
        self.SetMargins(2,2)

        # Set up the numbers in the margin for margin #1
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        # Reasonable value for, say, 4-5 digits using a mono font (40 pix)
        self.SetMarginWidth(1, 40)

        self.SetIndent(TABWIDTH)               # Proscribed indent size for wx
        self.SetBackSpaceUnIndents(True)# Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)        # Tab key indents
        self.SetTabWidth(TABWIDTH)             # Proscribed tab size for wx
        self.SetUseTabs(False)          # Use spaces rather than tabs, or

        self.SetEOLMode(wx.stc.STC_EOL_LF)
        self.SetViewEOL(False)

        # Global default style
        if wx.Platform == '__WXMSW__':
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier New')
        elif wx.Platform == '__WXMAC__':
            # and use this whenever OS != MSW.
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Monaco')
        else:
            defsize = wx.SystemSettings.GetFont(wx.SYS_ANSI_FIXED_FONT).GetPointSize()
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier,size:%d'%defsize)

        # Clear styles and revert to default.
        self.StyleClearAll()

        # The rest remains unchanged.

        # Line numbers in margin
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,'fore:#000000,back:#99A9C2')
        # Highlighted brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,'fore:#00009D,back:#FFFF00')
        # Unmatched brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,'fore:#00009D,back:#FF0000')
        # Indentation guide
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        # Caret color
        self.SetCaretForeground("BLUE")

        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
