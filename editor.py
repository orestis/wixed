import time
from threading import Thread

import wx
from wx import stc

TABWIDTH = 4
DEBUG = True


def GetModificationType(mask):
    valid_masks = [m for m in dir(stc) if m.startswith('STC_MOD')
        or m.startswith('STC_PERFORMED')
        or m.startswith('STC_LASTSTEP')]

    actual_masks = []
    for m in valid_masks:
        if getattr(stc, m) & mask:
            actual_masks.append(m)
    return actual_masks

class FundamentalEditor(stc.StyledTextCtrl):
    def __init__(self, parent, ID, buffer):
        stc.StyledTextCtrl.__init__(self, parent, ID, style=wx.BORDER_NONE)

        self._Setup()

        self._buffer = buffer
        self._just_modified = True
        self.SetText(self._buffer.text)
        self.HookBuffer(self._buffer)
        self.Bind(stc.EVT_STC_MODIFIED, self.OnModified)
        self.Bind(stc.EVT_STC_UPDATEUI, self.UpdateUI)
        self._just_modified = False

    def UnhookBuffer(self, b):
        b.pos_changed -= self.SyncPosFromBuffer
        b.inserted -= self.SyncInsertFromBuffer
        b.deleted -= self.SyncDeleteFromBuffer

    def HookBuffer(self, b):
        b.pos_changed += self.SyncPosFromBuffer
        b.inserted += self.SyncInsertFromBuffer
        b.deleted += self.SyncDeleteFromBuffer

    def OnModified(self, event):
        isdelete = event.ModificationType & stc.STC_MOD_DELETETEXT
        isinsert = event.ModificationType & stc.STC_MOD_INSERTTEXT
        if (isinsert or isdelete):
            if self._just_modified:
                self._just_modified = False
                return
            pos = event.Position
            lineno = self.LineFromPosition(pos)
            col = self.GetColumn(pos)
            text = event.Text
            linesadded = event.LinesAdded
            try:
                if isinsert:
                    self.buffer.insert(lineno, col, text, linesadded, self)
                else:
                    self.buffer.delete(lineno, col, len(text), linesadded, self)
            except Exception, e:
                print e
                import pdb; pdb.set_trace()
            if DEBUG:
                assert (self.buffer.text == self.GetText(),
                    'buffer is out of sync, last locals where %r' % locals())


    def UpdateUI(self, _):
        self.buffer._curpos = self.GetCurrentPos()
        self.buffer._anchor = self.GetAnchor()
        
    def __set_buffer(self, newbuffer):
        if self._buffer is not None:
            self.UnhookBuffer(self._buffer)
        self._buffer = newbuffer
        self.HookBuffer(self._buffer)
        self._just_modified = True
        self.ClearAll()
        self._just_modified = True
        self.SetText(self._buffer.text) # SetText does a ClearAll behind the scenes, but we can't set the _just_modified flag then
        self.SyncPosFromBuffer()


    buffer = property(lambda self: self._buffer, __set_buffer)


    def SyncDeleteFromBuffer(self, event_args):
        lineno, col, length, where = event_args
        if where != self:
            pos = self.PositionFromLine(lineno) + col
            self._just_modified = True
            self.SetTargetStart(pos)
            self.SetTargetEnd(pos + length)
            self.ReplaceTarget('')


    def SyncInsertFromBuffer(self, event_args):
        lineno, col, text, where = event_args
        if where != self:
            pos = self.PositionFromLine(lineno) + col
            self._just_modified = True
            self.InsertText(pos, text)


    def SyncPosFromBuffer(self):
        self.GotoPos(self.buffer.curpos)
        self.SetAnchor(self.buffer.anchor)


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
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
