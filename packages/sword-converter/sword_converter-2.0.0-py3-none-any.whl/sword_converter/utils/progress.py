import time


class Progress(object):
    def __init__(self, title, size=None):
        super().__init__()
        self._title = title
        if size is not None:
            self._size = size
            self.update(0)

    def infinite(self, event):
        while not event.is_set():
            for state in ('|', '/', '-', '\\'):
                print(f"{self._title} {state}", end="\r")
                time.sleep(.25)
        print(f"{self._title} ✔")

    def update(self, iteration):
        if self._size == iteration:
            print(f"{self._title} {'✔':<4}")
        else:
            print(f"{self._title} {(iteration / self._size):.0%}", end="\r")
