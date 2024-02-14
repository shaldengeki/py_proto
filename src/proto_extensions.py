from enum import Enum
from typing import Optional

from .proto_identifier import ProtoIdentifier
from .proto_node import ParsedProtoNode, ProtoNode
from .proto_range import ProtoRange


class ProtoExtensions(ProtoNode):
    def __init__(
        self,
        ranges: list[ProtoRange],
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.ranges = ranges
        for range in self.ranges:
            range.parent = self

    def __eq__(self, other) -> bool:
        return self.ranges == other.ranges

    def __str__(self) -> str:
        return f"<ProtoExtensions ranges={self.ranges}>"

    def __repr__(self) -> str:
        return str(self)

    def normalize(self) -> "ProtoExtensions":
        # sort the ranges.
        return ProtoExtensions(
            ranges=sorted(self.ranges, key=lambda r: int(r.min)),
            parent=self.parent,
        )

    @classmethod
    def match(
        cls, proto_source: str, parent: Optional[ProtoNode] = None
    ) -> Optional["ParsedProtoNode"]:
        if not proto_source.startswith("extensions "):
            return None

        proto_source = proto_source[11:].strip()

        ranges = []
        while True:
            if proto_source[0] == ";":
                proto_source = proto_source[1:].strip()
                break
            if not proto_source:
                raise ValueError(
                    "Proto source has invalid extensions syntax, does not contain ;"
                )
            if proto_source[0] == ",":
                proto_source = proto_source[1:].strip()
            match = ProtoRange.match(proto_source)
            if match is None:
                return None
            ranges.append(match.node)
            proto_source = match.remaining_source

        return ParsedProtoNode(
            ProtoExtensions(ranges=ranges, parent=parent), proto_source.strip()
        )

    def serialize(self) -> str:
        serialize_parts = ["extensions", ", ".join(r.serialize() for r in self.ranges)]
        return " ".join(serialize_parts) + ";"
