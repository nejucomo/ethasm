import unittest

from ethasm import disassembler


class DisassemblerTests (unittest.TestCase):

    def test_read_push_arg(self):
        bytesin = [1, 2, 3]
        it = enumerate(iter(bytesin))
        bytesout = disassembler.read_push_arg(it, len(bytesin))
        self.assertEqual(bytesin, bytesout)

    def test_read_push_arg_early_eof(self):
        bytesin = [1, 2, 3]
        it = enumerate(iter(bytesin))

        self.assertRaises(
            disassembler.MalformedBytecode,
            disassembler.read_push_arg,
            it,
            len(bytesin) + 1)
