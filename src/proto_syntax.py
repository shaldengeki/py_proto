from enum import Enum
from typing import Optional

from src.proto_node import ParsedProtoNode, ProtoNode
from src.proto_string_literal import ProtoStringLiteral


class ProtoSyntaxType(Enum):
    PROTO2 = "proto2"
    PROTO3 = "proto3"


class ProtoSyntax(ProtoNode):
    def __init__(self, syntax: ProtoSyntaxType):
        self.syntax = syntax

    def __eq__(self, other) -> bool:
        return self.syntax == other.syntax

    def __str__(self) -> str:
        return f"<ProtoSyntax syntax={self.syntax}>"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def match(proto_source: str) -> Optional["ParsedProtoNode"]:
        if not proto_source.startswith("syntax = "):
            return None
        parts = proto_source.split(";")
        proto_source = ";".join(parts[1:])
        syntax_line = parts[0][9:]
        match = ProtoStringLiteral.match(syntax_line)
        if match is None:
            raise ValueError(f"Proto has invalid syntax syntax: {';'.join(parts)}")
        try:
            syntax_type = ProtoSyntaxType[match.node.val.upper()]
        except KeyError:
            raise ValueError(
                f"Proto has unknown syntax type: {match.node.val}, must be one of: {[proto_type.name for proto_type in ProtoSyntaxType]}"
            )

        return ParsedProtoNode(
            ProtoSyntax(syntax_type),
            proto_source.strip(),
        )

    def serialize(self) -> str:
        return f'syntax = "{self.syntax.value}";'
