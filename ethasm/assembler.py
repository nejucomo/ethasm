import sys
import re
from pyethereum.opcodes import reverse_opcodes


class ParseError (Exception):
    def __init__(self, lineidx, reason):
        Exception.__init__(self, 'Invalid instruction on line {0}, {1}'.format(lineidx+1, reason))


def assemble(inf, outf):
    for (lineidx, line) in enumerate(inf.readlines()):
        instruction = _CommentRgx.sub('', line.rstrip())
        sys.stderr.write(
            'line {0}, line {1!r} -> instruction {2!r}\n'.format(
                lineidx+1, line, instruction))
        if instruction == '':
            continue

        m = _InstructionRgx.match(instruction)
        if m is None:
            raise ParseError(lineidx, 'could not parse: {0!r}'.format(instruction))
        else:
            label = m.group('label')
            sys.stderr.write(
                'line {0}, label {1!r} not implemented; ignored.\n'.format(
                    lineidx+1, label))

            pusharg = m.group('pusharg')
            if pusharg is None:
                outf.write(assemble_mnemonic(lineidx, m.group('mnemonic')))
            else:
                outf.write(assemble_pusharg(lineidx, pusharg))


def assemble_mnemonic(lineidx, mnemonic):
    try:
        return chr(reverse_opcodes[mnemonic.upper()])
    except KeyError:
        raise ParseError(lineidx, 'unknown mnemonic: {0!r}'.format(mnemonic))


def assemble_pusharg(lineidx, pusharg):
    sys.stderr.write(
        "line {0}, pusharg not implemented; substituting 'push<1> 0' for {1!r}\n".format(
            lineidx + 1, pusharg))
    return chr(reverse_opcodes['PUSH']) + '\0'



_InstructionRgx = re.compile(
    r'''
    ^
    # optional-whitespace-prefixed label (optional):
    [ \t]*
    ((?P<label>\w+):)?

    # optional-whitespace-prefixed mnemonic:
    [ \t]*

    (?P<mnemonic>
     ( # PUSH is followed whitespace then an argument specification:
      PUSH [ \t]+
      (?P<pusharg>
       \d+ # Decimal, or:
       |0x([a-f0-9][a-f0-9])+ # Hexadecimal, or:
       |"([^"\n]|\\")*(?<!\\)" # String literal.
      )
      | # -or if not push, a single-word mnemonic:
      [a-z][a-z0-9]*
     )
    )
    $ # End-of-line.  Note: comments are stripped prior to matching instructions.
    ''',
    re.VERBOSE | re.IGNORECASE)

_CommentRgx = re.compile(r'[ \t]*;.*$')


