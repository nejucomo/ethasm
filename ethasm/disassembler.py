#from pprint import pprint

from pyethereum.opcodes import opcodes, reverse_opcodes

PUSH_BASE = reverse_opcodes['PUSH']
PUSH_CEIL = PUSH_BASE + 32


def disassemble(inf, outf):
    for ix, instruction in iter_dis(inf):
        outf.write('{0: 3d}: {1}\n'.format(ix, instruction))


def iter_dis(inf):
    it = enumerate(iter_bytes(inf))
    for i, c in it:
        opcode = ord(c)

        if PUSH_BASE <= opcode < PUSH_CEIL:
            arglen = 1 + opcode - PUSH_BASE
            arglelist = read_push_arg(it, arglen)
            argbehex = ''.join(reversed(arglelist)).encode('hex')
            argchars = []
            for c in arglelist:
                b = ord(c)
                if 0x20 <= b < 0x80:
                    argchars.append(c)
                else:
                    argchars = None
                    break

            if argchars is None:
                argstr = ''
            else:
                argstr = repr(''.join(argchars))

            yield i, 'push 0x{0:s} = {1} {2}'.format(
                        argbehex,
                        long(argbehex, 16),
                        argstr)
        else:
            try:
                yield i, opcodes[opcode][0].lower()
            except KeyError:
                raise ValueError('Unknown opcode at byte index {0}: 0x{1:x}'.format(i, opcode))


def iter_bytes(f, bufsize=2**16):
    buf = f.read(bufsize)
    while buf:
        for c in buf:
            yield c
        buf = f.read(bufsize)


def read_push_arg(it, count):
    bytes = []
    while len(bytes) < count:
        (_, byte) = it.next()
        bytes.append(byte)
    return bytes
