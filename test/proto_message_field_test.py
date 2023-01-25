import unittest

from src.proto_identifier import ProtoFullIdentifier, ProtoIdentifier
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

    def test_message_field_starts_with_underscore(self):
        parsed_undescored_field = ProtoMessageField.match("string _test_field = 1;")
        self.assertEqual(
            parsed_undescored_field.node,
            ProtoMessageField(
                ProtoMessageFieldTypesEnum.STRING,
                ProtoIdentifier("_test_field"),
                ProtoInt(1, ProtoIntSign.POSITIVE),
            ),
        )
        parsed_double_undescored_field = ProtoMessageField.match(
            "bool __test_field = 1;"
        )
        self.assertEqual(
            parsed_double_undescored_field.node,
            ProtoMessageField(
                ProtoMessageFieldTypesEnum.STRING,
                ProtoIdentifier("__test_field"),
                ProtoInt(1, ProtoIntSign.POSITIVE),
            ),
        )

    def test_field_repeated(self):
        parsed_message_with_repeated_field_simple = ProtoMessageField.match(
            "repeated bool repeated_field = 3;"
        )
        self.assertEqual(
            parsed_message_with_repeated_field_simple.node,
            ProtoMessageField(
                ProtoMessageFieldTypesEnum.BOOL,
                ProtoIdentifier("repeated_field"),
                ProtoInt(3, ProtoIntSign.POSITIVE),
                True,
            ),
        )

    def test_message_field_enum_or_message(self):
        parsed_message_with_repeated_field_simple = ProtoMessageField.match(
            "foo.SomeEnumOrMessage enum_or_message_field = 1;"
        )
        self.assertEqual(
            parsed_message_with_repeated_field_simple.node,
            ProtoMessageField(
                ProtoMessageFieldTypesEnum.ENUM_OR_MESSAGE,
                ProtoIdentifier("enum_or_message_field"),
                ProtoInt(1, ProtoIntSign.POSITIVE),
                False,
                False,
                ProtoFullIdentifier("foo.SomeEnumOrMessage"),
            ),
        )
