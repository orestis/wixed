import wx
from wx import stc
from wixed.keybindings import translate

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
    def __init__(self, parent, ID, buffer, session):
        stc.StyledTextCtrl.__init__(self, parent, ID, style=wx.BORDER_NONE)

        self._setup()

        self._buffer = buffer
        self._just_modified = True
        self._session = session
        self.SetText(self._buffer.text)
        self.HookBuffer(self._buffer)
        self.Bind(stc.EVT_STC_MODIFIED, self.OnModified)
        self.Bind(stc.EVT_STC_UPDATEUI, self.UpdateUI)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
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

    def OnKeyDown(self, event):
        trans = translate(event.KeyCode, event.Modifiers)
        try:
            self._session.keydown(trans)
        except KeyError:
            event.Skip()

    def OnModified(self, event):
        event.Skip()
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
                    self.buffer.delete(lineno, col, text, linesadded, self)
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
        lineno, col, text, where = event_args
        if where != self:
            pos = self.FindColumn(lineno, col)
            endpos = pos + len(text.encode('utf-8'))

            self._just_modified = True
            self.SetTargetStart(pos)
            self.SetTargetEnd(endpos)
            self.ReplaceTarget('')
            if DEBUG:
                assert (self.buffer.text == self.GetText(),
                    'buffer is out of sync, last locals where %r' % locals())


    def SyncInsertFromBuffer(self, event_args):
        lineno, col, text, where = event_args
        if where != self:
            pos = self.FindColumn(lineno, col)
            self._just_modified = True
            self._just_modified_pos = True # InsertText invokes UpdateUI on the Mac, not on windows.
            self.InsertText(pos, text)
            if DEBUG:
                assert (self.buffer.text == self.GetText(),
                    'buffer is out of sync, last locals where %r' % locals())



    def _setup(self):
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
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,'fore:#000000,back:#99A9C2')
        # Highlighted brace
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,'fore:#00009D,back:#FFFF00')
        # Unmatched brace
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,'fore:#00009D,back:#FF0000')
        # Indentation guide
        self.StyleSetSpec(stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        # Caret color
        self.SetCaretForeground("BLUE")
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        

class PythonEditor(FundamentalEditor):
    def __init__(self, *args):
        super(PythonEditor, self).__init__(*args)
        self._setup_styles()


    def _setup_styles(self):
        # set lexers - remove this
        import keyword
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        # Python styles
        self.StyleSetSpec(stc.STC_P_DEFAULT, 'fore:#000000')
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE,  'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, 'fore:#008000,back:#F0FFF0')
        # Numbers
        self.StyleSetSpec(stc.STC_P_NUMBER, 'fore:#008080')
        # Strings and characters
        self.StyleSetSpec(stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(stc.STC_P_CHARACTER, 'fore:#800080')
        # Keywords
        self.StyleSetSpec(stc.STC_P_WORD, 'fore:#000080,bold')
        # Triple quote
        self.StyleSetSpec(stc.STC_P_TRIPLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, 'fore:#800080,back:#FFFFEA')
        # Class names
        self.StyleSetSpec(stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Function names
        self.StyleSetSpec(stc.STC_P_DEFNAME, 'fore:#008080,bold')
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, 'fore:#800000,bold')
        # Identifiers. I leave this as not bold because everything seems
        # to be an identifier if it doesn't match the above criterae
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, 'fore:#000000')


