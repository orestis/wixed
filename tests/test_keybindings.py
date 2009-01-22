from nose.tools import assert_equal

from wixed.keybindings import translate, KeyMapper

import wx

class testKeybindings(object):
    def test_translate(self):
        assert_equal(translate(ord('a'), 0), 'a')
        assert_equal(translate(ord('z'), 0), 'z')
        assert_equal(translate(ord('Z'), 0), 'Z')

        assert_equal(translate(wx.WXK_TAB, 0), '<TAB>')
        assert_equal(translate(wx.WXK_RETURN, 0), '<RETURN>')

        assert_equal(translate(wx.WXK_RETURN, wx.MOD_SHIFT), 'S-<RETURN>')
        assert_equal(translate(wx.WXK_TAB, wx.MOD_CONTROL), 'C-<TAB>')

    def test_keymap(self):
        keyman = KeyMapper()
        keyman['<A-B>'] = 1
        assert_equal(keyman['<a-b>'], 1)
        
        keyman['<b-c>'] = 1
        assert_equal(keyman['<B-c>'], 1)
        


