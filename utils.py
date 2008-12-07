from threading import Thread

class Pipe(object):
    def __init__(self, readStream, writeStream):
        self.readStream = readStream
        self.writeStream = writeStream
        t = Thread(target=self.do_piping)
        t.start()

    def do_piping(self):
        while True:
            c = self.readStream.read(10)
            if c == '':
                break
            self.writeStream.write(c)


class CircleList(list):
    index = None

    def append(self, v):
        list.append(self, v)
        if self.index is None:
            self.index = 0

    @property
    def current(self):
        if self.index is not None:
            return self[self.index]

    def next(self):
        if self.index >= len(self) - 1: #end of list
            self.index = 0
        else:
            self.index += 1

    def previous(self):
        if self.index <= 0: # start of list
            self.index = len(self) - 1
        else:
            self.index -= 1



class HistoryList(list):
    index = None
    def append(self, v):
        list.append(self, v)
        self.reset()

    @property
    def current(self):
        if self.index is not None:
            return self[self.index]

    def reset(self):
        self.index = len(self)

    def next(self):
        if self.index >= len(self) - 1: #end of list
            raise IndexError('end of list')
        else:
            self.index += 1

    def previous(self):
        if self.index <= 0: # start of list
            raise IndexError('start of list')
        else:
            self.index -= 1


