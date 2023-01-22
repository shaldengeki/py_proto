import unittest

from src.proto_comment import ProtoSingleLineComment


class ProtoSingleLineCommentTest(unittest.TestCase):
    def test_matches_normal_comment(self):
        node = ProtoSingleLineComment.match("// hello there, this is a comment").node
        self.assertEqual(node.value, " hello there, this is a comment")
        self.assertEqual(node.serialize(), "// hello there, this is a comment")

    def test_matches_without_space(self):
        node = ProtoSingleLineComment.match("//comment without space").node
        self.assertEqual(node.value, "comment without space")
        self.assertEqual(node.serialize(), "//comment without space")

    def test_does_not_match_multiple_lines(self):
        node = ProtoSingleLineComment.match("//line one\nbut not this").node
        self.assertEqual(node.value, "line one")
        self.assertEqual(node.serialize(), "//line one")

    def test_does_not_match_single_slash(self):
        self.assertIsNone(ProtoSingleLineComment.match("/hello there, this is a comment"))
        self.assertIsNone(ProtoSingleLineComment.match("/ /hello there, this is a comment"))


if __name__ == "__main__":
    unittest.main()
