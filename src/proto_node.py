import abc
from typing import NamedTuple, Optional

class ProtoNode(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def match(cls, proto_source: str) -> Optional["ParsedProtoNode"]:
        raise NotImplementedError

    @abc.abstractmethod
    def serialize(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def normalize(self) -> Optional["ProtoNode"]:
        raise NotImplementedError


class ParsedProtoNode(NamedTuple):
    node: ProtoNode
    remaining_source: str

    def __str__(self) -> str:
        return f"<ParsedProtoNode node={self.node} remaining_source={self.remaining_source} >"

    def __repr__(self) -> str:
        return str(self)
