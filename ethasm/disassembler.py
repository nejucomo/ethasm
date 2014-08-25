from pyethereuem.opcodes import opcodes, reverse_opcodes

PUSH_BASE = reverse_opcodes['PUSH']
PUSH_CEIL = PUSH_BASE + 32


def disassemble(inf, outf):
    for instruction in iter_dis(inf):
        outf.write('{0}\n'.format(instruction))


def iter_dis(inf):
    it = enumerate(iter_bytes(inf))
    for i, c in it:
        opcode = ord(c)

        if PUSH_BASE <= opcode < PUSH_CEIL:
            arg = read_push_arg(it, opcode - PUSH_BASE)
            yield 'PUSH 0x{0:s}'.format(arg)
        else:
            try:
                yield opcodes[c][0]
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
    return ''.join(bytes)
