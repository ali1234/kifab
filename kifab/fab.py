from __future__ import absolute_import, print_function

import yaml

class Fab(object):
    def __init__(self, filename):
        with open(filename) as stream:
            self._yaml = yaml.load(stream)

    @property
    def plot(self):
        return self._yaml.get('plot', [])

    def execute(self, board, dest, suffix):
        for p in self.plot:
            board.plot(dest, suffix, **p)
