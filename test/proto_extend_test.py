import unittest
from textwrap import dedent

from src.proto_extend import ProtoExtend
from src.proto_identifier import ProtoIdentifier
from src.proto_int import ProtoInt, ProtoIntSign
from src.proto_message import ProtoMessageField, ProtoMessageFieldTypesEnum


class ExtendTest(unittest.TestCase):
    maxDiff = None

    def test_empty_extend(self):
        parsed_empty_extend = ProtoExtend.match("""extend FooMessage {}""")
        self.assertIsNotNone(parsed_empty_extend)
        self.assertEqual(
            parsed_empty_extend.node.message_type, ProtoIdentifier("FooMessage")
        )
        self.assertEqual(parsed_empty_extend.node.serialize(), "extend FooMessage {\n}")

        parsed_spaced_extend = ProtoExtend.match(
            dedent(
                """
            extend FooMessage {

            }
        """.strip()
            )
        )
        self.assertIsNotNone(parsed_spaced_extend)
        self.assertEqual(
            parsed_spaced_extend.node.message_type, ProtoIdentifier("FooMessage")
        )
        self.assertEqual(
            parsed_spaced_extend.node.serialize(), "extend FooMessage {\n}"
        )

    def test_extend_empty_statements(self):
        empty_statement_message = ProtoExtend.match(
            dedent(
                """
            extend FooMessage {
                ;
                ;
            }
        """.strip()
            )
        )
        self.assertIsNotNone(empty_statement_message)
        self.assertEqual(
            empty_statement_message.node.message_type, ProtoIdentifier("FooMessage")
        )
        self.assertEqual(
            empty_statement_message.node.serialize(), "extend FooMessage {\n}"
        )

    def test_extend_simple_field(self):
        parsed_extend_with_single_field = ProtoExtend.match(
            dedent(
                """
            extend FooMessage {
                string single_field = 1;
            }
        """.strip()
            )
        )
        self.assertEqual(
            parsed_extend_with_single_field.node,
            ProtoExtend(
                ProtoIdentifier("FooMessage"),
                [
                    ProtoMessageField(
                        ProtoMessageFieldTypesEnum.STRING,
                        ProtoIdentifier("single_field"),
                        ProtoInt(1, ProtoIntSign.POSITIVE),
                    )
                ],
            ),
        )
        self.assertEqual(
            parsed_extend_with_single_field.node.serialize(),
            dedent(
                """
            extend FooMessage {
            string single_field = 1;
            }
            """
            ).strip(),
        )


if __name__ == "__main__":
    unittest.main()
