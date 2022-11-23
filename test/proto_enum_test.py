import unittest
from textwrap import dedent

from src.proto_bool import ProtoBool
from src.proto_constant import ProtoConstant
from src.proto_enum import ProtoEnum, ProtoEnumValue
from src.proto_identifier import ProtoIdentifier
from src.proto_int import ProtoInt, ProtoIntSign
from src.proto_option import ProtoOption
from src.proto_string_literal import ProtoStringLiteral


class EnumTest(unittest.TestCase):
    def test_enum_all_features(self):
        parsed_enum_multiple_values = ProtoEnum.match(
            dedent(
                """
            enum FooEnum {
                FE_NEGATIVE = -1;
                FE_UNDEFINED = 0;
                option java_package = "foobar";
                FE_VALONE = 1;
                FE_VALTWO = 2;
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_enum_multiple_values.node.nodes,
            [
                ProtoEnumValue(
                    ProtoIdentifier("FE_NEGATIVE"), ProtoInt(1, ProtoIntSign.NEGATIVE)
                ),
                ProtoEnumValue(
                    ProtoIdentifier("FE_UNDEFINED"), ProtoInt(0, ProtoIntSign.POSITIVE)
                ),
                ProtoOption(
                    ProtoIdentifier("java_package"),
                    ProtoConstant(ProtoStringLiteral("foobar")),
                ),
                ProtoEnumValue(
                    ProtoIdentifier("FE_VALONE"), ProtoInt(1, ProtoIntSign.POSITIVE)
                ),
                ProtoEnumValue(
                    ProtoIdentifier("FE_VALTWO"), ProtoInt(2, ProtoIntSign.POSITIVE)
                ),
            ],
        )

    def test_empty_enum(self):
        parsed_empty_enum = ProtoEnum.match("""enum FooEnum {}""")
        self.assertIsNotNone(parsed_empty_enum)
        self.assertEqual(parsed_empty_enum.node.name, ProtoIdentifier("FooEnum"))

        parsed_spaced_enum = ProtoEnum.match(
            dedent(
                """
            enum FooEnum {

            }
        """.strip()
            )
        )
        self.assertIsNotNone(parsed_spaced_enum)
        self.assertEqual(parsed_spaced_enum.node.name, ProtoIdentifier("FooEnum"))

    def test_enum_empty_statements(self):
        empty_statement_enum = ProtoEnum.match(
            dedent(
                """
            enum FooEnum {
                ;
                ;
            }
        """.strip()
            )
        )
        self.assertIsNotNone(empty_statement_enum)
        self.assertEqual(empty_statement_enum.node.name, ProtoIdentifier("FooEnum"))

    def test_enum_optionals(self):
        parsed_enum_with_optionals = ProtoEnum.match(
            dedent(
                """
            enum FooEnum {
                option java_package = "foobar";
                option (foo.bar).baz = false;
            }
        """.strip()
            )
        )
        self.assertIsNotNone(
            parsed_enum_with_optionals.node.options,
            [
                ProtoOption(
                    ProtoIdentifier("java_package"),
                    ProtoConstant(ProtoStringLiteral("foobar")),
                ),
                ProtoOption(
                    ProtoIdentifier("(foo.bar).baz"),
                    ProtoConstant(ProtoBool(False)),
                ),
            ],
        )
        self.assertEqual(
            parsed_enum_with_optionals.node.name, ProtoIdentifier("FooEnum")
        )

    def test_enum_single_value(self):
        parsed_enum_single_value = ProtoEnum.match(
            dedent(
                """
            enum FooEnum {
                FE_UNDEFINED = 0;
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_enum_single_value.node.nodes,
            [
                ProtoEnumValue(
                    ProtoIdentifier("FE_UNDEFINED"), ProtoInt(0, ProtoIntSign.POSITIVE)
                )
            ],
        )

    def test_enum_multiple_values(self):
        parsed_enum_multiple_values = ProtoEnum.match(
            dedent(
                """
            enum FooEnum {
                FE_NEGATIVE = -1;
                FE_UNDEFINED = 0;
                FE_VALONE = 1;
                FE_VALTWO = 2;
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_enum_multiple_values.node.nodes,
            [
                ProtoEnumValue(
                    ProtoIdentifier("FE_NEGATIVE"), ProtoInt(1, ProtoIntSign.NEGATIVE)
                ),
                ProtoEnumValue(
                    ProtoIdentifier("FE_UNDEFINED"), ProtoInt(0, ProtoIntSign.POSITIVE)
                ),
                ProtoEnumValue(
                    ProtoIdentifier("FE_VALONE"), ProtoInt(1, ProtoIntSign.POSITIVE)
                ),
                ProtoEnumValue(
                    ProtoIdentifier("FE_VALTWO"), ProtoInt(2, ProtoIntSign.POSITIVE)
                ),
            ],
        )


if __name__ == "__main__":
    unittest.main()
