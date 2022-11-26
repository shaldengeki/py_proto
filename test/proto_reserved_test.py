import unittest
from textwrap import dedent

from src.proto_reserved import ProtoReserved, ProtoReservedRange


class ReservedTest(unittest.TestCase):
    def test_reserved_range_single_int(self):
        self.assertEqual(ProtoReservedRange.match("42").node.serialize(), "42")

    def test_reserved_range_invalid_non_ints(self):
        self.assertIsNone(ProtoReservedRange.match("42.5"))
        self.assertIsNone(ProtoReservedRange.match("a"))
        self.assertIsNone(ProtoReservedRange.match("-"))

    def test_reserved_range_int_range(self):
        self.assertEqual(ProtoReservedRange.match("1 to 1").node.serialize(), "1 to 1")
        self.assertEqual(ProtoReservedRange.match("1 to 7").node.serialize(), "1 to 7")

    def test_reserved_range_invalid_range(self):
        with self.assertRaises(ValueError):
            ProtoReservedRange.match("8 to 2")

        with self.assertRaises(ValueError):
            ProtoReservedRange.match("3 to 0")

        with self.assertRaises(ValueError):
            ProtoReservedRange.match("1 to -1")

    def test_reserved_range_invalid_range_non_int(self):
        with self.assertRaises(ValueError):
            ProtoReservedRange.match("1 to c")

        with self.assertRaises(ValueError):
            ProtoReservedRange.match("1 to -bc3")

    def test_reserved_range_max(self):
        self.assertEqual(
            ProtoReservedRange.match("7 to max").node.serialize(), "7 to max"
        )


if __name__ == "__main__":
    unittest.main()
