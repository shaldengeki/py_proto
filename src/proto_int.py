from enum import Enum
from typing import Optional

from src.proto_identifier import ProtoIdentifier
from src.proto_node import ParsedProtoNode, ProtoNode


class ProtoIntSign(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


class ProtoInt(ProtoNode):
    OCTAL = set("01234567")
    DECIMAL = OCTAL | set("89")
    HEX = DECIMAL | set("ABCDEFabcdef")

    def __init__(self, value: int, sign: ProtoIntSign):
        self.value = value
        self.sign = sign

    def __eq__(self, other: "ProtoInt") -> bool:
        return self.value == other.value

    def __str__(self) -> str:
        return f"<ProtoInt value={self.value} sign={self.sign}>"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def match(proto_source: str) -> Optional["ParsedProtoNode"]:
        if proto_source[0] not in ProtoInt.DECIMAL:
            return None

        if proto_source.startswith("0"):
            # Octal or hex.
            pass
        else:
            # Decimal.
            for i, c in enumerate(proto_source):
                if c not in ProtoInt.DECIMAL:
                    return ParsedProtoNode(
                        ProtoInt(int(proto_source[:i]), ProtoIntSign.POSITIVE),
                        proto_source[i:].strip(),
                    )
            return ParsedProtoNode(
                ProtoInt(int(proto_source), ProtoIntSign.POSITIVE), ""
            )

        if proto_source.startswith("true") and (
            len(proto_source) == 4 or proto_source[4] not in ProtoIdentifier.ALL
        ):
            return ParsedProtoNode(ProtoInt(True), proto_source[4:].strip())
        elif proto_source.startswith("false") and (
            len(proto_source) == 5 or proto_source[5] not in ProtoIdentifier.ALL
        ):
            return ParsedProtoNode(ProtoInt(False), proto_source[5:].strip())
        return None

    def serialize(self) -> str:
        if self.sign == ProtoIntSign.NEGATIVE:
            return f"-{self.value}"

        return str(self.value)
