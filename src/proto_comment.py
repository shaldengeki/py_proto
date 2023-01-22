import abc
from typing import Optional

from src.proto_identifier import ProtoFullIdentifier
from src.proto_node import ParsedProtoNode, ProtoNode


class ProtoComment(ProtoNode):
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __str__(self) -> str:
        return f"<ProtoComment value={self.value}>"

    def __repr__(self) -> str:
        return str(self)

    def normalize(self) -> Optional["ProtoComment"]:
        return None

    @classmethod
    def match(cls, proto_source: str) -> Optional["ParsedProtoNode"]:
        return None

    def serialize(self) -> str:
        return ""

class ProtoSingleLineComment(ProtoComment):
    def __str__(self) -> str:
        return f"<ProtoSingleLineComment value={self.value}>"

    @classmethod
    def match(cls, proto_source: str) -> Optional["ParsedProtoNode"]:
        if not proto_source.startswith("//"):
            return None

        proto_source = proto_source[2:]
        newline_pos = proto_source.find("\n")
        if newline_pos == -1:
            newline_pos = len(proto_source)
        return ParsedProtoNode(
            ProtoSingleLineComment(proto_source[:newline_pos]),
            proto_source[newline_pos+1:]
        )

    def serialize(self) -> str:
        return f"//{self.value}"

# class ProtoMultiLineComment(ProtoNode):
#     def __init__(self, value: bool):
#         self.value = value

#     def __bool__(self) -> bool:
#         return self.value

#     def __eq__(self, other) -> bool:
#         return bool(self) == bool(other)

#     def __str__(self) -> str:
#         return f"<ProtoBool value={self.value}>"

#     def __repr__(self) -> str:
#         return str(self)

#     def normalize(self) -> "ProtoBool":
#         return self

#     @classmethod
#     def match(cls, proto_source: str) -> Optional["ParsedProtoNode"]:
#         if proto_source.startswith("true") and (
#             len(proto_source) == 4 or proto_source[4] not in ProtoFullIdentifier.ALL
#         ):
#             return ParsedProtoNode(ProtoBool(True), proto_source[4:].strip())
#         elif proto_source.startswith("false") and (
#             len(proto_source) == 5 or proto_source[5] not in ProtoFullIdentifier.ALL
#         ):
#             return ParsedProtoNode(ProtoBool(False), proto_source[5:].strip())
#         return None

#     def serialize(self) -> str:
#         return str(self.value).lower()
