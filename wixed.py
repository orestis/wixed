

def observed(prop):
    def _setter(self, newvalue):
        setattr(self, prop, newvalue)
        self.updated()

    def _getter(self):
        return getattr(self, prop)

    return _getter, _setter

class Buffer(object):
    def __init__(self, name):
        self.name = name
        self._text = ''
        self._curpos = 0
        self._anchor = 0
        self.updateFunc = lambda : None

    text = property(*observed('_text'))
    curpos = property(*observed('_curpos'))
    anchor = property(*observed('_anchor'))

    def updated(self):
        self.updateFunc()

    



class BufferManager(object):
    pass
