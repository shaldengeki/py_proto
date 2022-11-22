import unittest

from src.proto_int import ProtoInt, ProtoIntSign


class IntTest(unittest.TestCase):
    def test_int(self):
        self.assertEqual(
            ProtoInt.match("1").node.value, ProtoInt(1, ProtoIntSign.POSITIVE)
        )
        self.assertEqual(
            ProtoInt.match("158912938471293847").node.value,
            ProtoInt(158912938471293847, ProtoIntSign.POSITIVE),
        )
        self.assertEqual(
            ProtoInt.match("+1").node.value, ProtoInt(1, ProtoIntSign.POSITIVE)
        )
        self.assertEqual(
            ProtoInt.match("+158912938471293847").node.value,
            ProtoInt(158912938471293847, ProtoIntSign.POSITIVE),
        )
        self.assertEqual(
            ProtoInt.match("-1").node.value, ProtoInt(1, ProtoIntSign.NEGATIVE)
        )
        self.assertEqual(
            ProtoInt.match("-248713857").node.value,
            ProtoInt(248713857, ProtoIntSign.NEGATIVE),
        )

    def test_octal(self):
        self.assertEqual(
            ProtoInt.match("072342").node.value,
            ProtoInt(0o72342, ProtoIntSign.POSITIVE),
        )
        with self.assertRaises(ValueError):
            ProtoInt.match("072942")

    def test_hex(self):
        self.assertEqual(
            ProtoInt.match("0x72342").node.value,
            ProtoInt(0x72342, ProtoIntSign.POSITIVE),
        )
        self.assertEqual(
            ProtoInt.match("0x7A3d2").node.value,
            ProtoInt(0x7A3D2, ProtoIntSign.POSITIVE),
        )
        with self.assertRaises(ValueError):
            ProtoInt.match("0x72G42")


if __name__ == "__main__":
    unittest.main()
