import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        nodes = [
            TextNode("This is a bold text node", TextType.BOLD),
            TextNode("This is a bold text node", TextType.BOLD),
            TextNode("This is a new bold text node", TextType.BOLD),
            TextNode("This is an italic node", TextType.ITALIC),
            TextNode("This is an italic node", TextType.ITALIC),
            TextNode("This is a link node", TextType.LINK),
            TextNode("This is a image node", TextType.IMAGE),
        ]

        self.assertEqual(nodes[0], nodes[1])
        self.assertNotEqual(nodes[0], nodes[2])
        self.assertTrue(nodes[3] == nodes[4])
        self.assertFalse(nodes[5] == nodes[6])


if __name__ == "__main__":
    unittest.main()
