from typing import Optional

from src.constants.proto_string_literal import ProtoStringLiteral
from src.proto_node import ParsedProtoNode, ProtoNode, ProtoNodeDiff


class ProtoImport(ProtoNode):
    def __init__(
        self,
        parent: Optional[ProtoNode],
        path: ProtoStringLiteral,
        weak: bool = False,
        public: bool = False,
    ):
        super().__init__(parent)
        self.path = path
        self.path.parent = self
        self.weak = weak
        self.public = public

    def __eq__(self, other) -> bool:
        return (
            (hasattr(other, "path") and self.path == other.path)
            and (hasattr(other, "weak") and self.weak == other.weak)
            and (hasattr(other, "public") and self.public == other.public)
        )

    def __str__(self) -> str:
        return f"<ProtoImport path={self.path.serialize()} weak={self.weak} public={self.public}>"

    def __repr__(self) -> str:
        return str(self)

    def __dict__(self):
        return {
            "path": self.path.serialize(),
            "weak": self.weak,
            "public": self.public,
        }

    def normalize(self) -> "ProtoImport":
        return self

    @classmethod
    def match(
        cls, parent: Optional[ProtoNode], proto_source: str
    ) -> Optional["ParsedProtoNode"]:
        if not proto_source.startswith("import "):
            return None
        proto_source = proto_source[7:]

        weak = False
        if proto_source.startswith("weak "):
            weak = True
            proto_source = proto_source[5:]

        public = False
        if proto_source.startswith("public "):
            if weak:
                raise ValueError(f"Proto has invalid import syntax: {proto_source}")
            public = True
            proto_source = proto_source[7:]

        match = ProtoStringLiteral.match(None, proto_source)
        if match is None:
            raise ValueError(f"Proto has invalid import syntax: {proto_source}")

        if not match.remaining_source.startswith(";"):
            raise ValueError(
                f"Proto has invalid import syntax: {match.remaining_source}"
            )

        return ParsedProtoNode(
            ProtoImport(parent, match.node, weak=weak, public=public),
            match.remaining_source[1:].strip(),
        )

    def serialize(self) -> str:
        parts = ["import"]
        if self.weak:
            parts.append("weak")
        elif self.public:
            parts.append("public")
        parts.append(f"{self.path.serialize()};")
        return " ".join(parts)

    @staticmethod
    def diff_sets(
        left: list["ProtoImport"], right: list["ProtoImport"]
    ) -> list["ProtoNodeDiff"]:
        diffs: list[ProtoNodeDiff] = []
        left_names = set(i.path for i in left)
        right_names = set(i.path for i in right)
        for name in left_names - right_names:
            diffs.append(ProtoImportAdded(next(i for i in left if i.path == name)))
        for name in right_names - left_names:
            diffs.append(ProtoImportRemoved(next(i for i in right if i.path == name)))
        for name in left_names & right_names:
            left_import = next(i for i in left if i.path == name)
            right_import = next(i for i in right if i.path == name)
            if left_import.weak and not right_import.weak:
                diffs.append(ProtoImportMadeWeak(right_import))
            if not left_import.weak and right_import.weak:
                diffs.append(ProtoImportMadeNonWeak(right_import))
            if left_import.public and not right_import.public:
                diffs.append(ProtoImportMadePublic(right_import))
            if not left_import.public and right_import.public:
                diffs.append(ProtoImportMadeNonPublic(right_import))

        return diffs


class ProtoImportAdded(ProtoNodeDiff):
    def __init__(self, proto_import: ProtoImport):
        self.proto_import = proto_import

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ProtoImportAdded)
            and self.proto_import == other.proto_import
        )


class ProtoImportRemoved(ProtoImportAdded):
    pass


class ProtoImportMadeWeak(ProtoImportAdded):
    pass


class ProtoImportMadeNonWeak(ProtoImportAdded):
    pass


class ProtoImportMadePublic(ProtoImportAdded):
    pass


class ProtoImportMadeNonPublic(ProtoImportAdded):
    pass
