import unittest

from src.proto_file import ProtoFile
from src.proto_string_literal import ProtoStringLiteral
from src.proto_syntax import ProtoSyntax, ProtoSyntaxDiff


class ProtoFileTest(unittest.TestCase):
    def test_diff_empty_same_syntax_returns_empty(self):
        pf1 = ProtoFile(ProtoSyntax(ProtoStringLiteral("proto3")), [])
        pf2 = ProtoFile(ProtoSyntax(ProtoStringLiteral("proto3")), [])
        self.assertEqual(pf1.diff(pf2), [])

    def test_diff_empty_different_syntax_returns_syntax_diff(self):
        pf1 = ProtoFile(ProtoSyntax(ProtoStringLiteral("proto3")), [])
        pf2 = ProtoFile(ProtoSyntax(ProtoStringLiteral("proto2")), [])
        self.assertEqual(
            pf1.diff(pf2),
            [
                ProtoSyntaxDiff(
                    ProtoSyntax(ProtoStringLiteral("proto3")),
                    ProtoSyntax(ProtoStringLiteral("proto2")),
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
