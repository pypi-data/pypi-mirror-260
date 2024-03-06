import unittest

from escape_unk.unescape_unk import unescape

class TestUnescape(unittest.TestCase):
    def test_unescape1(self):
        text = '[c3a7]]'
        char = unescape(text)
        self.assertEqual(char, 'ç')

    def test_unescape2(self):
        text = '[[c3a7]'
        char = unescape(text)
        self.assertEqual(char, 'ç')

    def test_unescape3(self):
        text = '[c3a7]'
        char = unescape(text)
        self.assertEqual(char, '[c3a7]')
