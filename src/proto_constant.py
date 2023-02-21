from typing import Optional

from src.proto_bool import ProtoBool
from src.proto_float import ProtoFloat, ProtoFloatSign
from src.proto_identifier import ProtoFullIdentifier
from src.proto_int import ProtoInt, ProtoIntSign
from src.proto_node import ParsedProtoNode, ProtoNode
from src.proto_string_literal import ProtoStringLiteral

ProtoConstantTypes = (
    ProtoFullIdentifier | ProtoStringLiteral | ProtoInt | ProtoFloat | ProtoBool
)


class ParsedProtoConstantNode(ParsedProtoNode):
    node: "ProtoConstant"
    remaining_source: str


class ProtoConstant(ProtoNode):
    def __init__(self, value: ProtoConstantTypes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
        self.value.parent = self

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __str__(self) -> str:
        return f"<ProtoConstant value={self.value}>"

    def __repr__(self) -> str:
        return str(self)

    def normalize(self) -> "ProtoConstant":
        return self

    @classmethod
    def match(
        cls, proto_source: str, parent: Optional[ProtoNode] = None
    ) -> Optional["ParsedProtoConstantNode"]:
        match = ProtoBool.match(proto_source=proto_source, parent=None)
        if match is not None:
            proto_constant = ProtoConstant(value=match.node, parent=parent)
            return ParsedProtoConstantNode(
                proto_constant,
                match.remaining_source.strip(),
            )

        sign = ProtoIntSign.POSITIVE
        if proto_source.startswith("+") or proto_source.startswith("-"):
            sign = next(x for x in ProtoIntSign if x.value == proto_source[0])
            proto_int_match = ProtoInt.match(proto_source=proto_source[1:], parent=None)
        else:
            proto_int_match = ProtoInt.match(proto_source=proto_source, parent=None)
        if proto_int_match is not None:
            proto_constant = ProtoConstant(value=proto_int_match.node, parent=parent)
            proto_int_match.node.sign = sign
            return ParsedProtoConstantNode(
                proto_constant,
                proto_int_match.remaining_source.strip(),
            )

        float_sign = ProtoFloatSign.POSITIVE
        if proto_source.startswith("+") or proto_source.startswith("-"):
            float_sign = next(x for x in ProtoFloatSign if x.value == proto_source[0])
            float_match = ProtoFloat.match(proto_source=proto_source[1:], parent=None)
        else:
            float_match = ProtoFloat.match(proto_source=proto_source, parent=None)
        if float_match is not None:
            proto_constant = ProtoConstant(value=float_match.node, parent=parent)
            float_match.node.sign = float_sign
            return ParsedProtoConstantNode(
                proto_constant,
                float_match.remaining_source.strip(),
            )

        identifier_match = ProtoFullIdentifier.match(
            proto_source=proto_source, parent=None
        )
        if identifier_match is not None:
            return ParsedProtoConstantNode(
                ProtoConstant(value=identifier_match.node, parent=parent),
                identifier_match.remaining_source.strip(),
            )

        string_literal_match = ProtoStringLiteral.match(
            proto_source=proto_source, parent=None
        )
        if string_literal_match is not None:
            return ParsedProtoConstantNode(
                ProtoConstant(value=string_literal_match.node, parent=parent),
                string_literal_match.remaining_source.strip(),
            )

        return None

    def serialize(self) -> str:
        if not isinstance(self.value, ProtoNode):
            raise ValueError(
                f"Proto has invalid constant: {self.value} with class: {self.value.__class__.__name__}"
            )

        return self.value.serialize()
