from typing import Optional

from src.proto_node import ParsedProtoNode, ProtoNode, ProtoNodeDiff


class ProtoPackage(ProtoNode):
    def __init__(self, parent: Optional[ProtoNode], package: str):
        super().__init__(parent)
        self.package = package

    def __eq__(self, other) -> bool:
        return hasattr(other, "package") and self.package == other.package

    def __str__(self) -> str:
        return f"<ProtoPackage package={self.package}>"

    def __repr__(self) -> str:
        return str(self)

    def normalize(self) -> "ProtoPackage":
        return self

    @classmethod
    def match(
        cls, parent: Optional[ProtoNode], proto_source: str
    ) -> Optional["ParsedProtoNode"]:
        if not proto_source.startswith("package"):
            return None

        if not proto_source.startswith("package "):
            raise ValueError(f"Proto has invalid package: {proto_source}")

        proto_source = proto_source[8:]
        parts = proto_source.split(";")
        package = parts[0]

        if len(parts) == 1:
            raise ValueError(
                f"Proto has invalid package declaration syntax: {';'.join(parts)}"
            )

        if not package:
            raise ValueError(f"Proto cannot have empty package: {proto_source}")

        proto_source = ";".join(parts[1:])

        if package.startswith(".") or package.endswith("."):
            raise ValueError(f"Proto has invalid package: {package}")

        return ParsedProtoNode(ProtoPackage(parent, package), proto_source.strip())

    def serialize(self) -> str:
        return f"package {self.package};"

    @staticmethod
    def diff(
        left: Optional["ProtoPackage"], right: Optional["ProtoPackage"]
    ) -> list["ProtoNodeDiff"]:
        if left == right:
            return []
        elif left is not None and right is None:
            return [ProtoPackageAdded(left)]
        elif left is None and right is not None:
            return [ProtoPackageRemoved(right)]

        assert left is not None and right is not None
        return [ProtoPackageChanged(left, right)]


class ProtoPackageChanged(ProtoNodeDiff):
    def __init__(self, left: ProtoPackage, right: ProtoPackage):
        self.left = left
        self.right = right

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ProtoPackageChanged)
            and self.left == other.left
            and self.right == other.right
        )


class ProtoPackageAdded(ProtoNodeDiff):
    def __init__(self, left: ProtoPackage):
        self.left = left

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ProtoPackageAdded) and self.left == other.left


class ProtoPackageRemoved(ProtoNodeDiff):
    def __init__(self, right: ProtoPackage):
        self.right = right

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ProtoPackageRemoved) and self.right == other.right
