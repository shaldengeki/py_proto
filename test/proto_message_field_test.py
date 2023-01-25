import unittest

from src.proto_identifier import ProtoIdentifier
from src.proto_int import ProtoInt, ProtoIntSign
from src.proto_message_field import ProtoMessageField, ProtoMessageFieldTypesEnum


class MessageFieldTest(unittest.TestCase):
    maxDiff = None

    def test_field_optional_default_false(self):
        string_field = ProtoMessageField.match("string single_field = 1;")
        self.assertEqual(
            string_field.node,
            ProtoMessageField(
                ProtoMessageFieldTypesEnum.STRING,
                ProtoIdentifier("single_field"),
                ProtoInt(1, ProtoIntSign.POSITIVE),
                False,
                False,
            ),
        )

    def test_field_optional_set(self):
        string_field = ProtoMessageField.match(
            "optional string single_field = 1;".strip()
        )
        self.assertEqual(
            string_field.node,
            ProtoMessageField(
                ProtoMessageFieldTypesEnum.STRING,
                ProtoIdentifier("single_field"),
                ProtoInt(1, ProtoIntSign.POSITIVE),
                False,
                True,
            ),
        )

    def test_field_cannot_have_repeated_and_optional(self):
        with self.assertRaises(ValueError):
            ProtoMessageField(
                ProtoMessageFieldTypesEnum.STRING,
                ProtoIdentifier("single_field"),
                ProtoInt(1, ProtoIntSign.POSITIVE),
                True,
                True,
            )
