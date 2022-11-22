from typing import Optional

from src.proto_node import ParsedProtoNode, ProtoNode


class ProtoIdentifier(ProtoNode):
    def __init__(self, identifier: str):
        self.identifier = identifier

    def __eq__(self, other) -> bool:
        return self.identifier == other.identifier

    def __str__(self) -> str:
        return f"<ProtoIdentifier identifier={self.identifier}>"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def match(proto_source: str) -> Optional["ParsedProtoNode"]:
        starting_characters = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.".split()
        )
        all_characters = set("0123456789".split()) + starting_characters
        part_characters = all_characters - "."

        if proto_source[0] not in starting_characters:
            return None

        in_part = True
        for i, c in enumerate(proto_source):
            if c == ".":
                if not in_part:
                    raise ValueError(f"Proto has invalid identifier: {proto_source}")
                in_part = False
            else:
                if c in part_characters:
                    in_part = True
                else:
                    return ParsedProtoNode(
                        ProtoIdentifier(proto_source[:i]), proto_source[i:]
                    )
        raise ValueError(f"Proto has invalid identifier: {proto_source}")

    def serialize(self) -> str:
        return self.identifier
