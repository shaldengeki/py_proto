from typing import Optional

from src.proto_identifier import ProtoIdentifier
from src.proto_node import ParsedProtoNode, ProtoNode
from src.proto_string_literal import ProtoStringLiteral


class ProtoConstant(ProtoNode):
    # constant = fullIdent | ( [ "-" | "+" ] intLit ) | ( [ "-" | "+" ] floatLit ) | strLit | boolLit
    def __init__(
        self, value: ProtoIdentifier | ProtoStringLiteral | int | float | bool
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
        # TODO: handle bool
        # TODO: handle float
        # TODO: handle int
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

    def serialize(self) -> str:
        if isinstance(self.value, ProtoIdentifier) or isinstance(
            self.value, ProtoStringLiteral
        ):
            return self.value.serialize()
        elif isinstance(self.value, int) or isinstance(self.value, float):
            return str(self.value)
        elif isinstance(self.value, bool):
            return str(self.value).lower()
        raise ValueError(f"Proto has invalid constant: {self.value}")
