from __future__ import absolute_import, print_function

import argparse
import os
import pcbnew

from kifab.fab import Fab
from kifab.board import Board


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pcb', type=str, metavar='PCBFILE',
                        help='Kicad PCB file.')
    parser.add_argument('fab', type=str, metavar='FABFILE',
                        help='Kifab FAB file.')
    parser.add_argument('-o', '--outdir', type=str, default='.',
                        help='Generate files in this directory.')
    parser.add_argument('-s', '--suffix', type=str, default='',
                        help='Common suffix for generated files.')

    args = parser.parse_args()

    board = Board(args.pcb)
    fab = Fab(args.fab)
    fab.execute(board, args.outdir, args.suffix)

if __name__ == '__main__':
    main()