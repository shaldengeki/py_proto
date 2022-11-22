from typing import Optional

from src.proto_bool import ProtoBool
from src.proto_identifier import ProtoIdentifier
from src.proto_int import ProtoInt, ProtoIntSign
from src.proto_node import ParsedProtoNode, ProtoNode
from src.proto_string_literal import ProtoStringLiteral


class ProtoConstant(ProtoNode):
    # constant = fullIdent | ( [ "-" | "+" ] intLit ) | ( [ "-" | "+" ] floatLit ) | strLit | boolLit
    def __init__(
        self, value: ProtoIdentifier | ProtoStringLiteral | int | float | ProtoBool
    ):
        # TODO: handle floats and ints
        self.value = value

    def __eq__(self, other: "ProtoConstant") -> bool:
        return self.value == other.value

    def __str__(self) -> str:
        return f"<ProtoConstant value={self.serialize()}>"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def match(proto_source: str) -> Optional["ParsedProtoNode"]:
        match = ProtoBool.match(proto_source)
        if match is not None:
            return ParsedProtoNode(
                ProtoConstant(match.node),
                match.remaining_source.strip(),
            )

        # TODO: handle float
        sign = ProtoIntSign.POSITIVE
        if proto_source.startswith("+") or proto_source.startswith("-"):
            sign = next(x for x in ProtoIntSign if x.value == proto_source[0])
            match = ProtoInt.match(proto_source[1:])
        else:
            match = ProtoInt.match(proto_source)
        if match is not None:
            return ParsedProtoNode(
                ProtoInt(match.node, sign),
                match.remaining_source.strip(),
            )

        match = ProtoIdentifier.match(proto_source)
        if match is not None:
            return ParsedProtoNode(
                ProtoConstant(match.node),
                match.remaining_source.strip(),
            )

        match = ProtoStringLiteral.match(proto_source)
        if match is not None:
            return ParsedProtoNode(
                ProtoConstant(match.node),
                match.remaining_source.strip(),
            )

        return None

    def serialize(self) -> str:
        if isinstance(self.value, ProtoNode):
            return self.value.serialize()
        elif isinstance(self.value, int) or isinstance(self.value, float):
            return str(self.value)
        raise ValueError(f"Proto has invalid constant: {self.value}")
