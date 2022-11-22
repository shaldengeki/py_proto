import unittest
from textwrap import dedent

from src.proto_bool import ProtoBool
from src.proto_constant import ProtoConstant
from src.proto_identifier import ProtoIdentifier
from src.proto_int import ProtoInt, ProtoIntSign
from src.proto_string_literal import ProtoStringLiteral


class ConstantTest(unittest.TestCase):
    # constant = fullIdent | ( [ "-" | "+" ] intLit ) | ( [ "-" | "+" ] floatLit ) | strLit | boolLit
    def test_ident(self):
        self.assertEqual(ProtoConstant.match("a").node.value, ProtoIdentifier("a"))
        self.assertEqual(ProtoConstant.match("a0").node.value, ProtoIdentifier("a0"))
        self.assertEqual(ProtoConstant.match("a_").node.value, ProtoIdentifier("a_"))
        self.assertEqual(ProtoConstant.match("aa").node.value, ProtoIdentifier("aa"))
        self.assertEqual(ProtoConstant.match("ab").node.value, ProtoIdentifier("ab"))
        self.assertEqual(
            ProtoConstant.match("a0b_f_aj").node.value, ProtoIdentifier("a0b_f_aj")
        )
        self.assertEqual(
            ProtoConstant.match("a.bar").node.value, ProtoIdentifier("a.bar")
        )
        self.assertEqual(
            ProtoConstant.match("a.bar.baz").node.value, ProtoIdentifier("a.bar.baz")
        )

    def test_str(self):
        self.assertEqual(
            ProtoConstant.match("'a'").node.value, ProtoStringLiteral("a", quote="'")
        )
        self.assertEqual(
            ProtoConstant.match("'.a'").node.value, ProtoStringLiteral(".a", quote="'")
        )
        self.assertEqual(
            ProtoConstant.match('"a"').node.value, ProtoStringLiteral("a", quote='"')
        )

    def test_bool(self):
        self.assertEqual(ProtoConstant.match("true").node.value, ProtoBool(True))
        self.assertEqual(ProtoConstant.match("false").node.value, ProtoBool(False))

    def test_int(self):
        self.assertEqual(
            ProtoConstant.match("1").node.value, ProtoInt(1, ProtoIntSign.POSITIVE)
        )
        self.assertEqual(
            ProtoConstant.match("158912938471293847").node.value,
            ProtoInt(158912938471293847, ProtoIntSign.POSITIVE),
        )
        self.assertEqual(
            ProtoConstant.match("+1").node.value, ProtoInt(1, ProtoIntSign.POSITIVE)
        )
        self.assertEqual(
            ProtoConstant.match("+158912938471293847").node.value,
            ProtoInt(158912938471293847, ProtoIntSign.POSITIVE),
        )
        self.assertEqual(
            ProtoConstant.match("-1").node.value, ProtoInt(1, ProtoIntSign.NEGATIVE)
        )
        self.assertEqual(
            ProtoConstant.match("-248713857").node.value,
            ProtoInt(248713857, ProtoIntSign.NEGATIVE),
        )

        # Octal
        self.assertEqual(
            ProtoConstant.match("072342").node.value,
            ProtoInt(0o72342, ProtoIntSign.POSITIVE),
        )
        with self.assertRaises(ValueError):
            ProtoConstant.match("072942")

        # Hex
        self.assertEqual(
            ProtoConstant.match("0x72342").node.value,
            ProtoInt(0x72342, ProtoIntSign.POSITIVE),
        )
        self.assertEqual(
            ProtoConstant.match("0x7A3d2").node.value,
            ProtoInt(0x7A3D2, ProtoIntSign.POSITIVE),
        )
        with self.assertRaises(ValueError):
            ProtoConstant.match("0x72G42")

    def test_float(self):
        self.assertEqual(ProtoConstant.match("2834.235928").node.value, 2834.235928)
        self.assertEqual(ProtoConstant.match("2834.e2").node.value, 283400)
        self.assertEqual(ProtoConstant.match("2834e2").node.value, 283400)
        self.assertEqual(ProtoConstant.match("2834.e0").node.value, 2834)
        self.assertEqual(ProtoConstant.match("2834e0").node.value, 2834)
        self.assertEqual(ProtoConstant.match("2834.E3").node.value, 2834000)
        self.assertEqual(ProtoConstant.match("2834E3").node.value, 2834000)
        self.assertEqual(ProtoConstant.match("2834.e+2").node.value, 283400)
        self.assertEqual(ProtoConstant.match("2834e+2").node.value, 283400)
        self.assertEqual(ProtoConstant.match("2834.e-2").node.value, 28.34)
        self.assertEqual(ProtoConstant.match("2834e-2").node.value, 28.34)
        self.assertEqual(ProtoConstant.match(".0").node.value, 0.0)
        self.assertEqual(ProtoConstant.match(".0e-1").node.value, 0.00)
        self.assertEqual(ProtoConstant.match(".0E1").node.value, 0)
        self.assertEqual(ProtoConstant.match(".0E2").node.value, 0)
        self.assertEqual(ProtoConstant.match(".3265").node.value, 0.3265)
        self.assertEqual(ProtoConstant.match(".3265e1").node.value, 3.265)
        self.assertEqual(ProtoConstant.match("inf").node.value, float("inf"))
        self.assertEqual(ProtoConstant.match("nan").node.value, float("nan"))


if __name__ == "__main__":
    unittest.main()
