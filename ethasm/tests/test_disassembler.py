import unittest
from cStringIO import StringIO
import string

from pyethereum import opcodes
from ethasm import disassembler


class dis_push_Tests (unittest.TestCase):

    def test_push1_nonprintable(self):
        self._test_push1('\x17', 'push 0x17 ; 23 ')

    def test_push1_printable(self):
        self._test_push1('*', 'push 0x2a ; 42 "*"')

    def test_push1_printable_dquote(self):
        self._test_push1('*', r'push 0x2a ; 42 "\""')

    def _test_push1(self, char, expectedinstruction):
        opcode = opcodes.reverse_opcodes['PUSH1']
        it = iter([(43, char)])
        inst = disassembler.dis_push(it, 42, chr(opcode), opcode)
        self.assertEqual(inst, expectedinstruction)


class dis_other_Tests (unittest.TestCase):

    def test_known_opcodes(self):
        self.assertEqual('stop', disassembler.dis_other(None, 0x00))
        self.assertEqual('suicide', disassembler.dis_other(None, 0xff))

    def test_unknown_opcode(self):
        self.assertRaises(
            disassembler.MalformedBytecode,
            disassembler.dis_other,
            42,
            -1)


class iter_bytes_Tests (unittest.TestCase):

    def test_single_buf(self):
        self._test_iter_bytes(input='foo', bufsize=10)

    def test_boundary_neg1(self):
        self._test_iter_bytes(input='foo', bufsize=2)

    def test_boundary_eq(self):
        self._test_iter_bytes(input='foo', bufsize=3)

    def test_boundary_pos1(self):
        self._test_iter_bytes(input='foo', bufsize=4)

    def test_multi_buf(self):
        self._test_iter_bytes(input=string.letters, bufsize=5)

    def _test_iter_bytes(self, input, bufsize):
        f = StringIO(input)
        output = ''.join(disassembler.iter_bytes(f, bufsize))
        self.assertEqual(output, input)


class read_push_arg_Tests (unittest.TestCase):

    def test_well_formed(self):
        bytesin = [1, 2, 3]
        it = enumerate(iter(bytesin))
        bytesout = disassembler.read_push_arg(it, 42, len(bytesin))
        self.assertEqual(bytesin, bytesout)

    def test_early_eof(self):
        bytesin = [1, 2, 3]
        it = enumerate(iter(bytesin))

        self.assertRaises(
            disassembler.MalformedBytecode,
            disassembler.read_push_arg,
            it,
            42,
            len(bytesin) + 1)
