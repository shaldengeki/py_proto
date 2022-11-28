import unittest
from textwrap import dedent

from src.proto_bool import ProtoBool
from src.proto_constant import ProtoConstant
from src.proto_identifier import ProtoIdentifier
from src.proto_message import ProtoMessage
from src.proto_option import ProtoOption
from src.proto_string_literal import ProtoStringLiteral


class MessageTest(unittest.TestCase):
    maxDiff = None

    def test_message_all_features(self):
        parsed_message_multiple_fields = ProtoMessage.match(
            dedent(
                """
            message FooMessage {
                option (foo.bar).baz = "bat";
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
            ],
        )
        self.assertEqual(
            parsed_message_multiple_fields.node.serialize(),
            dedent(
                """
            message FooMessage {
            option (foo.bar).baz = "bat";
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


if __name__ == "__main__":
    unittest.main()
