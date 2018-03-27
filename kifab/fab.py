from __future__ import absolute_import, print_function

import yaml

class Fab(object):
    def __init__(self, filename):
        with open(filename) as stream:
            self._yaml = yaml.load(stream)

    @property
    def plots(self):
        return self._yaml.get('plots', [])

    def execute(self, board, dest, suffix):
        for p in self.plots:
            board.plot(dest, suffix, **p)

        if 'drill' in self._yaml:
            board.drill(dest, suffix, **self._yaml['drill'])