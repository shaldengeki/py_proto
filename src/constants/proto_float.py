from enum import Enum
from typing import Optional

from src.constants.proto_identifier import ProtoIdentifier
from src.constants.proto_int import ProtoInt
from src.proto_node import ParsedProtoNode, ProtoNode


class ProtoFloatSign(Enum):
    POSITIVE = "+"
    NEGATIVE = "-"


class ParsedProtoFloatNode(ParsedProtoNode):
    node: "ProtoFloat"
    remaining_source: str


class ProtoFloat(ProtoNode):
    SIGNS = set("+-")
    DIGITS = ProtoInt.DECIMAL
    DECIMAL = DIGITS | set(".")
    EXPONENTIAL = set("eE")

    def __init__(self, parent: Optional[ProtoNode], value: float, sign: ProtoFloatSign):
        super().__init__(parent)
        self.value = value
        self.sign = sign

    def __eq__(self, other) -> bool:
        # Handle nan.
        if self.value != self.value:
            return other.value != other.value

        return self.value == other.value and self.sign == other.sign

    def __str__(self) -> str:
        return f"<ProtoFloat value={self.value} sign={self.sign}>"

    def __repr__(self) -> str:
        return str(self)

    def normalize(self) -> "ProtoFloat":
        return self

    @classmethod
    def match(
        cls, parent: Optional[ProtoNode], proto_source: str
    ) -> Optional["ParsedProtoFloatNode"]:
        if proto_source.startswith("inf"):
            proto_source = proto_source[3:]
            if proto_source and proto_source[0] in ProtoIdentifier.ALL:
                raise ValueError(
                    f"Proto has invalid float, invalid post-inf character: {proto_source}"
                )
            return ParsedProtoFloatNode(
                ProtoFloat(parent, float("inf"), ProtoFloatSign.POSITIVE),
                proto_source.strip(),
            )

        if proto_source.startswith("nan"):
            proto_source = proto_source[3:]
            if proto_source and proto_source[0] in ProtoIdentifier.ALL:
                raise ValueError(
                    f"Proto has invalid float, invalid post-nan character: {proto_source}"
                )
            return ParsedProtoFloatNode(
                ProtoFloat(parent, float("nan"), ProtoFloatSign.POSITIVE),
                proto_source.strip(),
            )

        if not proto_source[0] in ProtoFloat.DECIMAL:
            return None

        decimal_started = False
        precision = 0
        for i, c in enumerate(proto_source):
            if c not in ProtoFloat.DECIMAL:
                i -= 1
                break
            if c == ".":
                if decimal_started:
                    raise ValueError(
                        f"Proto has invalid float, duplicate decimal: {proto_source}"
                    )
                decimal_started = True
            elif decimal_started:
                precision += 1

        try:
            base = round(float(proto_source[: i + 1]), precision)
        except ValueError:
            return None

        proto_source = proto_source[i + 1 :]

        sign = 1
        if proto_source and proto_source[0] in ProtoFloat.EXPONENTIAL:
            proto_source = proto_source[1:]
            if proto_source and proto_source[0] in ProtoFloat.SIGNS:
                if proto_source[0] == "-":
                    sign *= -1
                proto_source = proto_source[1:]

            for i, c in enumerate(proto_source):
                if c in ProtoFloat.SIGNS:
                    raise ValueError(
                        f"Proto has invalid float, unexpected sign: {proto_source}"
                    )
                if c not in ProtoFloat.DIGITS:
                    if c in ProtoIdentifier.ALL:
                        raise ValueError(
                            f"Proto has invalid float, non-digit character: {proto_source}"
                        )
                    i -= 1
                    break
            base *= pow(10, sign * int(proto_source[: i + 1]))
            proto_source = proto_source[i + 1 :]

        return ParsedProtoFloatNode(
            ProtoFloat(parent, base, ProtoFloatSign.POSITIVE), proto_source.strip()
        )

    def serialize(self) -> str:
        if self.sign == ProtoFloatSign.NEGATIVE:
            return f"-{self.value}"

        return str(self.value)
