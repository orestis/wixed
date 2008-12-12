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
        self._just_modified_pos = False


    def __del__(self):
        if self._buffer is not None:
            self.UnhookBuffer(self._buffer)


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
                raise
            if DEBUG:
                assert (self.buffer.text == self.GetText(),
                    'buffer is out of sync, last locals where %r' % locals())


    def UpdateUI(self, _):
        if self._just_modified_pos:
            self._just_modified_pos = False
            return
        self.buffer._curpos = self.GetCurrentPos()
        self.buffer.anchor = self.GetAnchor()
        
    
    def _SyncPosFromBuffer(self):
        start, end = self.GetSelection()
        if (start, end) != (self.buffer.anchor, self.buffer.curpos):
            self._just_modified_pos = True
            self.SetSelection(self.buffer.anchor, self.buffer.curpos)

    def SyncPosFromBuffer(self):
        wx.CallAfter(self._SyncPosFromBuffer)


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
            if DEBUG:
                assert (self.buffer.text == self.GetText(),
                    'buffer is out of sync, last locals where %r' % locals())


    def SyncInsertFromBuffer(self, event_args):
        lineno, col, text, where = event_args
        if where != self:
            pos = self.PositionFromLine(lineno) + col
            self._just_modified = True
            self._just_modified_pos = True # InsertText invokes UpdateUI on the Mac, not on windows.
            self.InsertText(pos, text)
            if DEBUG:
                assert (self.buffer.text == self.GetText(),
                    'buffer is out of sync, last locals where %r' % locals())


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
        
STYLE_BLACK = 11
STYLE_ORANGE = 12
STYLE_PURPLE = 13
STYLE_BLUE = 14

class StyledEditor(FundamentalEditor):
    def __init__(self, parent, ID, buffer):
        super(StyledEditor, self).__init__(parent, ID, buffer)
        self.SetLexer(stc.STC_LEX_CONTAINER)
        self.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyleNeeded)

        self.StyleSetSpec(STYLE_BLACK, 'fore:#000000')
        self.StyleSetSpec(STYLE_ORANGE, 'fore:#FFF000')
        self.StyleSetSpec(STYLE_PURPLE, 'fore:#FF00FF')
        self.StyleSetSpec(STYLE_BLUE, 'fore:#0000FF')


    def OnStyleNeeded(self, event):
        line_number = self.LineFromPosition(self.EndStyled)
        print 'styling', line_number
        start_pos = self.PositionFromLine(line_number)
        end_pos = event.Position


        line_length = self.LineLength(line_number)
        if line_length > 0:

            from parsers import simpleSQL
            try:
                tokens = simpleSQL.parseString(self.GetLine(line_number))
                print tokens
            except Exception, e:
                print e
                start_col = e.loc
                print 'start_col', start_col
                print 'start_pos', start_pos
                print 'end_pos', end_pos
                error_length = len(e.pstr)
                print e.pstr
                self.StartStyling(start_pos, stc.STC_INDICS_MASK)
                if start_col != 0:
                    self.SetStyling(start_pos + start_col, 0)
                self.SetStyling(start_pos + start_col + error_length, stc.STC_INDIC0_MASK)
                return

            first_char = chr(self.GetCharAt(start_pos))

            # The SCI_STARTSTYLING here is important
            self.StartStyling(start_pos, 0x1f)

            if first_char == '-':
                self.SetStyling(line_length, STYLE_ORANGE)
            elif first_char == '/':
                self.SetStyling(line_length, STYLE_PURPLE)
            elif first_char == '*':
                self.SetStyling(line_length, STYLE_BLUE)
            else:
                self.SetStyling(line_length, STYLE_BLACK)




