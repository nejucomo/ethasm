#from pprint import pprint

from pyethereum.opcodes import opcodes, reverse_opcodes

PUSH1 = reverse_opcodes['PUSH1']
PUSH32 = reverse_opcodes['PUSH32']


class MalformedBytecode (Exception):
    def __init__(self, offset, reason):
        Exception.__init__(self, 'Malformed bytecode at byte offset {0}: {1}'.format(offset, reason))


def disassemble(inf, outf):
    for ix, instruction in iter_dis(inf):
        outf.write('{0: 3d}: {1}\n'.format(ix, instruction))


def iter_dis(inf):
    it = enumerate(iter_bytes(inf))
    for i, c in it:
        opcode = ord(c)
        yield i, dis_op(it, i, c, opcode)


def dis_op(it, i, c, opcode):
    if PUSH1 <= opcode <= PUSH32:
        return dis_push(it, c, opcode)
    else:
        return dis_other(i, opcode)


def dis_push(it, c, opcode):
    arglen = 1 + opcode - PUSH1
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

    return 'push 0x{0:s} ; {1} {2}'.format(argbehex, long(argbehex, 16), argstr)


def dis_other(i, opcode):
    try:
        return opcodes[opcode][0].lower()
    except KeyError:
        raise MalformedBytecode(i, 'Unknown opcode 0x{1:x}'.format(opcode))


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
