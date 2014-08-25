#! /usr/bin/env python

import sys
import argparse

from assembler import assemble
from disassembler import disassemble



DESCRIPTION = """
Ethereum contract assembler / disassembler.
"""


def main(args = sys.argv[1:]):
    opts = parse_args(args)
    if opts.disassemble:
        cmd = disassemble
    else:
        cmd = assemble

    cmd(sys.stdin, sys.stdout)


def parse_args(args):
    p = argparse.ArgumentParser(description=DESCRIPTION)

    p.add_argument('-d', '--disassemble',
                   dest='disassemble',
                   action='store_true',
                   default=False,
                   help='Disassemble rather than assemble.')

    return p.parse_args(args)


if __name__ == '__main__':
    main()
