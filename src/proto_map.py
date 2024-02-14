from enum import Enum
from typing import Optional, Sequence

from .proto_identifier import ProtoEnumOrMessageIdentifier, ProtoIdentifier
from .proto_int import ProtoInt
from .proto_message_field import ProtoMessageFieldOption, ProtoMessageFieldTypesEnum
from .proto_node import ParsedProtoNode, ProtoNode, ProtoNodeDiff


class ProtoMapKeyTypesEnum(Enum):
    INT32 = "int32"
    INT64 = "int64"
    UINT32 = "uint32"
    UINT64 = "uint64"
    SINT32 = "sint32"
    SINT64 = "sint64"
    FIXED32 = "fixed32"
    FIXED64 = "fixed64"
    SFIXED32 = "sfixed32"
    SFIXED64 = "sfixed64"
    BOOL = "bool"
    STRING = "string"


ProtoMapValueTypesEnum = ProtoMessageFieldTypesEnum


class ProtoMap(ProtoNode):
    def __init__(
        self,
        key_type: ProtoMapKeyTypesEnum,
        value_type: ProtoMapValueTypesEnum,
        name: ProtoIdentifier,
        number: ProtoInt,
        enum_or_message_type_name: Optional[ProtoEnumOrMessageIdentifier] = None,
        options: Optional[list[ProtoMessageFieldOption]] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.key_type = key_type
        self.value_type = value_type
        self.name = name
        self.name.parent = self
        self.number = number
        self.number.parent = self
        self.enum_or_message_type_name = enum_or_message_type_name
        if self.enum_or_message_type_name is not None:
            self.enum_or_message_type_name.parent = self

        if options is None:
            options = []
        self.options = options
        for option in self.options:
            option.parent = self

    def __eq__(self, other) -> bool:
        return (
            self.key_type == other.key_type
            and self.value_type == other.value_type
            and self.name == other.name
            and self.number == other.number
            and self.enum_or_message_type_name == other.enum_or_message_type_name
            and self.options == other.options
        )

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} key_type={self.key_type} value_type={self.value_type} name={self.name} number={self.number} enum_or_message_type_name={self.enum_or_message_type_name} options={self.options}>"

    def __repr__(self) -> str:
        return str(self)

    def normalize(self) -> "ProtoMap":
        return ProtoMap(
            parent=self.parent,
            key_type=self.key_type,
            value_type=self.value_type,
            name=self.name,
            number=self.number,
            enum_or_message_type_name=self.enum_or_message_type_name,
            options=sorted(self.options, key=lambda o: str(o.normalize())),
        )

    @classmethod
    def match(
        cls, proto_source: str, parent: Optional[ProtoNode] = None
    ) -> Optional["ParsedProtoNode"]:
        if proto_source.startswith("map "):
            proto_source = proto_source[4:].strip()
        elif proto_source.startswith("map<"):
            proto_source = proto_source[3:].strip()
        else:
            return None

        # Try to match the map key type.
        proto_source = proto_source[1:].strip()
        key_type = None
        for potential_key_type in ProtoMapKeyTypesEnum:
            if proto_source.startswith(potential_key_type.value):
                key_type = potential_key_type
                proto_source = proto_source[len(potential_key_type.value) :].strip()
                break
        if key_type is None:
            return None

        if not proto_source.startswith(","):
            return None
        proto_source = proto_source[1:].strip()

        # Next, try to match the map value type.
        value_type: Optional[ProtoMapValueTypesEnum] = None
        for potential_value_type in ProtoMapValueTypesEnum:
            if potential_value_type == ProtoMapValueTypesEnum.ENUM_OR_MESSAGE:
                # This is special-cased below.
                break
            if proto_source.startswith(potential_value_type.value):
                value_type = potential_value_type
                proto_source = proto_source[len(potential_value_type.value) :].strip()

        # If this is an enum or message type, try to match a name.
        enum_or_message_type_name = None
        if value_type is None:
            # See if this is an enum or message type.
            match = ProtoEnumOrMessageIdentifier.match(proto_source)
            if match is None:
                return None
            value_type = ProtoMessageFieldTypesEnum.ENUM_OR_MESSAGE
            enum_or_message_type_name = match.node
            proto_source = match.remaining_source.strip()

        if not proto_source.startswith(">"):
            return None
        proto_source = proto_source[1:].strip()

        # Try to match the map field's name.
        identifier_match = ProtoIdentifier.match(proto_source)
        if identifier_match is None:
            return None
        name = identifier_match.node
        proto_source = identifier_match.remaining_source.strip()

        if not proto_source.startswith("="):
            return None
        proto_source = proto_source[1:].strip()

        # Try to match the map field number.
        int_match = ProtoInt.match(proto_source)
        if int_match is None:
            return None
        number = int_match.node
        proto_source = int_match.remaining_source.strip()

        # Try to match map field options, if any.
        options = []
        if proto_source.startswith("["):
            proto_source = proto_source[1:].strip()
            end_bracket = proto_source.find("]")
            if end_bracket == -1:
                raise ValueError(
                    f"Proto has invalid map field option syntax, cannot find ]: {proto_source}"
                )
            for option_part in proto_source[:end_bracket].strip().split(","):
                message_field_option_match = ProtoMessageFieldOption.match(
                    option_part.strip()
                )
                if message_field_option_match is None:
                    raise ValueError(
                        f"Proto has invalid map field option syntax: {proto_source}"
                    )
                options.append(message_field_option_match.node)
            proto_source = proto_source[end_bracket + 1 :].strip()

        if not proto_source.startswith(";"):
            raise ValueError(
                f"Proto has invalid map field syntax, missing ending ;:{proto_source}"
            )

        return ParsedProtoNode(
            ProtoMap(
                key_type=key_type,
                value_type=value_type,
                name=name,
                number=number,
                enum_or_message_type_name=enum_or_message_type_name,
                options=options,
                parent=parent,
            ),
            proto_source[1:].strip(),
        )

    def serialize(self) -> str:
        serialized_parts = [
            f"map",
            f"<{self.key_type.value},",
        ]

        if self.value_type == ProtoMessageFieldTypesEnum.ENUM_OR_MESSAGE:
            if self.enum_or_message_type_name is None:
                raise ValueError(
                    f"Enum or message type name was not set for: {str(self)}"
                )
            serialized_parts.append(f"{self.enum_or_message_type_name.serialize()}>")
        else:
            serialized_parts.append(f"{self.value_type.value}>")

        serialized_parts = serialized_parts + [
            self.name.serialize(),
            "=",
            self.number.serialize(),
        ]

        if self.options:
            serialized_parts.append("[")
            serialized_parts.append(
                ", ".join(option.serialize() for option in self.options)
            )
            serialized_parts.append("]")

        return " ".join(serialized_parts) + ";"

    @staticmethod
    def diff(
        parent: Optional[ProtoNode], before: "ProtoMap", after: "ProtoMap"
    ) -> list["ProtoNodeDiff"]:
        if before is None and after is not None:
            return [ProtoMapAdded(parent, after)]
        elif before is not None and after is None:
            return [ProtoMapRemoved(parent, before)]
        elif before is None and after is None:
            return []
        elif before.name != after.name:
            return []
        elif before == after:
            return []
        diffs: list["ProtoNodeDiff"] = []
        return diffs

    @staticmethod
    def diff_sets(
        parent: Optional[ProtoNode], before: list["ProtoMap"], after: list["ProtoMap"]
    ) -> Sequence["ProtoNodeDiff"]:
        diffs: list[ProtoNodeDiff] = []
        before_names = set(o.name.identifier for o in before)
        after_names = set(o.name.identifier for o in after)
        for name in before_names - after_names:
            diffs.append(
                ProtoMapRemoved(
                    parent, next(i for i in before if i.name.identifier == name)
                )
            )
        for name in after_names - before_names:
            diffs.append(
                ProtoMapAdded(
                    parent, next(i for i in after if i.name.identifier == name)
                )
            )
        for name in before_names & after_names:
            before_enum = next(i for i in before if i.name.identifier == name)
            after_enum = next(i for i in after if i.name.identifier == name)
            diffs.extend(ProtoMap.diff(parent, before_enum, after_enum))

        return diffs


class ProtoMapDiff(ProtoNodeDiff):
    def __init__(self, parent: Optional[ProtoNode], map: ProtoMap):
        self.parent = parent
        self.map = map

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ProtoMapDiff) and self.map == other.map

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} parent={self.parent} map={self.map}>"


class ProtoMapAdded(ProtoMapDiff):
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and isinstance(other, ProtoMapAdded)


class ProtoMapRemoved(ProtoMapDiff):
    def __eq__(self, other: object) -> bool:
        return super().__eq__(other) and isinstance(other, ProtoMapRemoved)
