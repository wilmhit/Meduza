import unittest

from signal_processing import Signal


class TestSignalProcessing(unittest.TestCase):
    def setUp(self):
        self.code = b"PNG"
        self.two_byte = b"AA"
        self.rest = \
             b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

        self.message = \
            b"PNGAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def test_creating_message(self):
        message = Signal()
        message.code = self.code
        message.two_byte = self.two_byte

        self.assertEqual(message.get_message(), self.message)

    def test_parsing_message(self):
        message = Signal(self.message)

        self.assertEqual(self.code, message.code)
        self.assertEqual(self.two_byte, message.two_byte)
        self.assertEqual(self.rest, message.rest)

    def test_create_and_parse(self):
        message = Signal()
        message.code = self.code
        message.two_byte = self.two_byte
        decoded = Signal(message.get_message())

        self.assertEqual(decoded.code, self.code)
        self.assertEqual(decoded.two_byte, self.two_byte)
        self.assertEqual(decoded.rest, self.rest)
