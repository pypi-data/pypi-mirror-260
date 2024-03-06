import datetime


class Waiting:
    def __init__(self):
        self._times = []

    def add(self, start, end):
        self._times.append((start, end))
        if len(self._times) > 5:
            self._times.pop(0)

    @property
    def x_more_time(self):
        i = 0
        tt = datetime.timedelta(seconds=0)
        for t in self._times:
            i += 1
            tt += datetime.timedelta(seconds=t[1] - t[0])
        return tt / i
