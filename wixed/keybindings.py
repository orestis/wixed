import wx

special_keys = [k for k in dir(wx) if k.startswith('WXK_')]

def _get_special(keycode):
    special = None
    for key in special_keys:
        if keycode == getattr(wx, key):
            special = key[4:]
            break
    if special:
        return '<%s>' % special

def translate(keycode, modifiers):
    mods = []
    if modifiers & wx.MOD_META:
        mods.append('M')
    if modifiers & wx.MOD_CONTROL:
        mods.append('C')
    if modifiers & wx.MOD_ALT:
        mods.append('A')
    if modifiers & wx.MOD_SHIFT:
        mods.append('S')
    if mods: mods.append('-')
    try:
        key = _get_special(keycode) or chr(keycode)
    except:
        key = _get_special(keycode)

    return '%s%s' % (''.join(mods), key)

class KeyMapper(object):

    def __init__(self):
        self._mappings = {}

    def __setitem__(self, item, value):
        self._mappings[item.lower()] = value

    def __getitem__(self, item):
        return self._mappings[item.lower()]

    def clear(self):
        self._mappings = {}

