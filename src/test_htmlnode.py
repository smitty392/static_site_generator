import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        nodes = [
            HTMLNode("p", "This is a paragraph."),
            HTMLNode("p", "This is a paragraph."),
            HTMLNode("h1", "This is a first level header."),
            HTMLNode(
                "h1",
                children=[
                    HTMLNode("p", "This is a paragraph."),
                    HTMLNode("h1", "This is a first level header.")
                ]
            ),
            HTMLNode(
                "a",
                "This node has props",
                props={
                    "href": "https://www.google.com",
                    "target": "_blank"
                }
            )
        ]

        self.assertEqual(nodes[0], nodes[1])
        self.assertNotEqual(nodes[0], nodes[2])
        self.assertEqual(len(nodes[3].children), 2)
        self.assertEqual(
            nodes[4].props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_leaf_to_html_p(self):
        nodes = [
            LeafNode("p", "Hello, world!"),
            LeafNode("h1", "Hello, cool world!"),
        ]
        self.assertEqual(nodes[0].to_html(), "<p>Hello, world!</p>")
        self.assertEqual(nodes[1].to_html(), "<h1>Hello, cool world!</h1>")


if __name__ == "__main__":
    unittest.main()

