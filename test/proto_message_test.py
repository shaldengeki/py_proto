import unittest
from textwrap import dedent

from src.proto_bool import ProtoBool
from src.proto_constant import ProtoConstant
from src.proto_enum import ProtoEnum, ProtoEnumValue
from src.proto_identifier import ProtoFullIdentifier, ProtoIdentifier
from src.proto_int import ProtoInt, ProtoIntSign
from src.proto_message import (
    ProtoMessage,
    ProtoMessageField,
    ProtoMessageFieldOption,
    ProtoMessageFieldTypesEnum,
    ProtoOneOf,
)
from src.proto_option import ProtoOption
from src.proto_reserved import ProtoReserved, ProtoReservedRange, ProtoReservedRangeEnum
from src.proto_string_literal import ProtoStringLiteral


class MessageTest(unittest.TestCase):
    maxDiff = None

    def test_message_all_features(self):
        parsed_message_multiple_fields = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                option (foo.bar).baz = "bat";
                enum MyEnum {
                    ME_UNDEFINED = 0;
                    ME_VALONE = 1;
                    ME_VALTWO = 2;
                }
                message NestedMessage {}
                reserved "a";
                reserved 1 to 3;
                repeated string some_field = 4 [ (bar.baz).bat = "bat", baz.bat = -100 ];
                bool some_bool_field = 5;
                oneof one_of_field {
                    string name = 4;
                    option java_package = "com.example.foo";
                    SubMessage sub_message = 9;
                }
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_message_multiple_fields.node.nodes,
            [
                ProtoOption(
                    ProtoIdentifier("(foo.bar).baz"),
                    ProtoConstant(ProtoStringLiteral("bat")),
                ),
                ProtoEnum(
                    ProtoIdentifier("MyEnum"),
                    [
                        ProtoEnumValue(
                            ProtoIdentifier("ME_UNDEFINED"),
                            ProtoInt(0, ProtoIntSign.POSITIVE),
                        ),
                        ProtoEnumValue(
                            ProtoIdentifier("ME_VALONE"),
                            ProtoInt(1, ProtoIntSign.POSITIVE),
                        ),
                        ProtoEnumValue(
                            ProtoIdentifier("ME_VALTWO"),
                            ProtoInt(2, ProtoIntSign.POSITIVE),
                        ),
                    ],
                ),
                ProtoMessage(ProtoIdentifier("NestedMessage"), []),
                ProtoReserved(fields=[ProtoIdentifier("a")]),
                ProtoReserved(
                    ranges=[
                        ProtoReservedRange(
                            ProtoInt(1, ProtoIntSign.POSITIVE),
                            ProtoInt(3, ProtoIntSign.POSITIVE),
                        )
                    ]
                ),
                ProtoMessageField(
                    ProtoMessageFieldTypesEnum.STRING,
                    ProtoIdentifier("some_field"),
                    ProtoInt(4, ProtoIntSign.POSITIVE),
                    True,
                    None,
                    [
                        ProtoMessageFieldOption(
                            ProtoIdentifier("(bar.baz).bat"),
                            ProtoConstant(ProtoStringLiteral("bat")),
                        ),
                        ProtoMessageFieldOption(
                            ProtoIdentifier("baz.bat"),
                            ProtoConstant(ProtoInt(100, ProtoIntSign.NEGATIVE)),
                        ),
                    ],
                ),
                ProtoMessageField(
                    ProtoMessageFieldTypesEnum.BOOL,
                    ProtoIdentifier("some_bool_field"),
                    ProtoInt(5, ProtoIntSign.POSITIVE),
                    False,
                    None,
                ),
                ProtoOneOf(
                    ProtoIdentifier("one_of_field"),
                    [
                        ProtoMessageField(ProtoMessageFieldTypesEnum.STRING, ProtoIdentifier("name"), ProtoInt(4, ProtoIntSign.POSITIVE), False, None, []),
                        ProtoOption(ProtoIdentifier("java_package"), ProtoConstant(ProtoStringLiteral("com.example.foo"))),
                        ProtoMessageField(ProtoMessageFieldTypesEnum.ENUM_OR_MESSAGE, ProtoIdentifier("sub_message"), ProtoInt(9, ProtoIntSign.POSITIVE), False, ProtoFullIdentifier("SubMessage"), []),
                    ],
                ),
            ],
        )
        self.assertEqual(
            parsed_message_multiple_fields.node.serialize(),
            dedent(
                """
            message FooMessage {
            option (foo.bar).baz = "bat";
            enum MyEnum {
            ME_UNDEFINED = 0;
            ME_VALONE = 1;
            ME_VALTWO = 2;
            }
            message NestedMessage {
            }
            reserved "a";
            reserved 1 to 3;
            repeated string some_field = 4 [ (bar.baz).bat = "bat", baz.bat = -100 ];
            bool some_bool_field = 5;
            oneof one_of_field {
            string name = 4;
            option java_package = "com.example.foo";
            SubMessage sub_message = 9;
            }
            }
            """
            ).strip(),
        )

    def test_empty_message(self):
        parsed_empty_message = ProtoMessage.match("""message FooMessage {}""")
        self.assertIsNotNone(parsed_empty_message)
        self.assertEqual(parsed_empty_message.node.name, ProtoIdentifier("FooMessage"))

        parsed_spaced_message = ProtoMessage.match(
            dedent(
                """
            message FooMessage {

            }
        """.strip()
            )
        )
        self.assertIsNotNone(parsed_spaced_message)
        self.assertEqual(parsed_spaced_message.node.name, ProtoIdentifier("FooMessage"))

    def test_message_empty_statements(self):
        empty_statement_message = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                ;
                ;
            }
        """.strip()
            )
        )
        self.assertIsNotNone(empty_statement_message)
        self.assertEqual(
            empty_statement_message.node.name, ProtoIdentifier("FooMessage")
        )

    def test_message_optionals(self):
        parsed_message_with_optionals = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                option java_package = "foobar";
                option (foo.bar).baz = false;
            }
        """.strip()
            )
        )
        self.assertIsNotNone(
            parsed_message_with_optionals.node.options,
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
            parsed_message_with_optionals.node.name, ProtoIdentifier("FooMessage")
        )

    def test_message_nested_enum(self):
        parsed_message_with_enum = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                enum MyEnum {
                    ME_UNDEFINED = 0;
                    ME_NEGATIVE = -1;
                    ME_VALONE = 1;
                }
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_message_with_enum.node,
            ProtoMessage(
                ProtoIdentifier("FooMessage"),
                [
                    ProtoEnum(
                        ProtoIdentifier("MyEnum"),
                        [
                            ProtoEnumValue(
                                ProtoIdentifier("ME_UNDEFINED"),
                                ProtoInt(0, ProtoIntSign.POSITIVE),
                            ),
                            ProtoEnumValue(
                                ProtoIdentifier("ME_NEGATIVE"),
                                ProtoInt(1, ProtoIntSign.NEGATIVE),
                            ),
                            ProtoEnumValue(
                                ProtoIdentifier("ME_VALONE"),
                                ProtoInt(1, ProtoIntSign.POSITIVE),
                            ),
                        ],
                    )
                ],
            ),
        )

    def test_message_nested_message(self):
        parsed_message_with_enum = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                message NestedMessage {}
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_message_with_enum.node,
            ProtoMessage(
                ProtoIdentifier("FooMessage"),
                [
                    ProtoMessage(ProtoIdentifier("NestedMessage"), []),
                ],
            ),
        )

    def test_message_reserved_single_field(self):
        parsed_message_with_reserved_single_field = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                reserved 38, 48 to 100, 72 to max;
                reserved "foo", "barBaz";
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_message_with_reserved_single_field.node,
            ProtoMessage(
                ProtoIdentifier("FooMessage"),
                [
                    ProtoReserved(
                        ranges=[
                            ProtoReservedRange(ProtoInt(38, ProtoIntSign.POSITIVE)),
                            ProtoReservedRange(
                                ProtoInt(48, ProtoIntSign.POSITIVE),
                                ProtoInt(100, ProtoIntSign.POSITIVE),
                            ),
                            ProtoReservedRange(
                                ProtoInt(72, ProtoIntSign.POSITIVE),
                                ProtoReservedRangeEnum.MAX,
                            ),
                        ]
                    ),
                    ProtoReserved(
                        fields=[
                            ProtoIdentifier("foo"),
                            ProtoIdentifier("barBaz"),
                        ]
                    ),
                ],
            ),
        )

    def test_message_simple_field(self):
        parsed_message_with_single_field_simple = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                string single_field = 1;
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_message_with_single_field_simple.node,
            ProtoMessage(
                ProtoIdentifier("FooMessage"),
                [
                    ProtoMessageField(
                        ProtoMessageFieldTypesEnum.STRING,
                        ProtoIdentifier("single_field"),
                        ProtoInt(1, ProtoIntSign.POSITIVE),
                        False,
                        None,
                    )
                ],
            ),
        )

    def test_message_repeated_field(self):
        parsed_message_with_repeated_field_simple = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                repeated bool repeated_field = 3;
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_message_with_repeated_field_simple.node,
            ProtoMessage(
                ProtoIdentifier("FooMessage"),
                [
                    ProtoMessageField(
                        ProtoMessageFieldTypesEnum.BOOL,
                        ProtoIdentifier("repeated_field"),
                        ProtoInt(3, ProtoIntSign.POSITIVE),
                        True,
                        None,
                    )
                ],
            ),
        )

    def test_message_field_enum_or_message(self):
        parsed_message_with_repeated_field_simple = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                foo.SomeEnumOrMessage enum_or_message_field = 1;
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_message_with_repeated_field_simple.node,
            ProtoMessage(
                ProtoIdentifier("FooMessage"),
                [
                    ProtoMessageField(
                        ProtoMessageFieldTypesEnum.ENUM_OR_MESSAGE,
                        ProtoIdentifier("enum_or_message_field"),
                        ProtoInt(1, ProtoIntSign.POSITIVE),
                        False,
                        ProtoFullIdentifier("foo.SomeEnumOrMessage"),
                    )
                ],
            ),
        )

    def test_oneof_empty(self):
        parsed_oneof_empty = ProtoOneOf.match(
            dedent("oneof one_of_field {}".strip())
        )
        self.assertEqual(
            parsed_oneof_empty.node,
            ProtoOneOf(
                ProtoIdentifier("one_of_field"),
                [],
            ),
        )

    def test_oneof_empty_statements(self):
        parsed_oneof_empty = ProtoOneOf.match(
            dedent("""oneof one_of_field {
                ;
                ;
            }""".strip())
        )
        self.assertEqual(
            parsed_oneof_empty.node,
            ProtoOneOf(
                ProtoIdentifier("one_of_field"),
                [],
            ),
        )

    def test_oneof_basic_fields(self):
        parsed_oneof_basic_fields = ProtoOneOf.match(
            dedent("""oneof one_of_field {
                string name = 4;
                SubMessage sub_message = 9;
            }""".strip())
        )
        self.assertEqual(
            parsed_oneof_basic_fields.node,
            ProtoOneOf(
                ProtoIdentifier("one_of_field"),
                [
                    ProtoMessageField(ProtoMessageFieldTypesEnum.STRING, ProtoIdentifier("name"), ProtoInt(4, ProtoIntSign.POSITIVE), False, None, []),
                    ProtoMessageField(ProtoMessageFieldTypesEnum.ENUM_OR_MESSAGE, ProtoIdentifier("sub_message"), ProtoInt(9, ProtoIntSign.POSITIVE), False, ProtoFullIdentifier("SubMessage"), []),
                ],
            ),
        )

    def test_oneof_options(self):
        parsed_oneof_options = ProtoOneOf.match(
            dedent("""oneof one_of_field {
                option java_package = "com.example.foo";
            }""".strip())
        )
        self.assertEqual(
            parsed_oneof_options.node,
            ProtoOneOf(
                ProtoIdentifier("one_of_field"),
                [
                    ProtoOption(ProtoIdentifier("java_package"), ProtoConstant(ProtoStringLiteral("com.example.foo"))),
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
