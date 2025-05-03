import unittest
from textnode import TextType, TextNode
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestHTMLNode(unittest.TestCase):
    def test_delim_start_and_end(self):
        old_nodes = [
            TextNode("**this is bold text**", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "this is bold text")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_no_delimiters(self):
        old_nodes = [
            TextNode("there are no delimiters here", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "there are no delimiters here")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_multiple_delimiters(self):
        old_nodes = [
            TextNode("this code is mixed with _italic_, **bold**, and `code` text", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(old_nodes, "_", TextType.ITALIC),
                "**",
                TextType.BOLD
            ),
            "`",
            TextType.CODE
        )

        self.assertEqual(len(result), 7)
        self.assertEqual(
            [node.text for node in result],
            [
                "this code is mixed with ",
                "italic",
                ", ",
                "bold",
                ", and ",
                "code",
                " text"
            ]
        )
        self.assertEqual(
            [node.text_type for node in result],
            [
                TextType.NORMAL,
                TextType.ITALIC,
                TextType.NORMAL,
                TextType.BOLD,
                TextType.NORMAL,
                TextType.CODE,
                TextType.NORMAL
            ]
        )

    def test_unmatched_delimiter(self):
        old_nodes = [
            TextNode("this is **not closed", TextType.NORMAL)
        ]
        with self.assertRaises(Exception) as content:
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(str(content.exception), "invalid Markdown")

    def test_adjacent_delimiters(self):
        old_nodes = [
            TextNode("there is **bold****text** here", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(result), 4)
        self.assertEqual(
            [node.text for node in result],
            [
                "there is ",
                "bold",
                "text",
                " here"
            ]
        )
        self.assertEqual(
            [node.text_type for node in result],
            [
                TextType.NORMAL,
                TextType.BOLD,
                TextType.BOLD,
                TextType.NORMAL
            ]
        )

    def test_nothing_between_delimiters(self):
        old_nodes = [
            TextNode("something **** here", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(result), 2)
        self.assertEqual(
            [node.text for node in result],
            [
                "something ",
                " here"
            ]
        )
        self.assertEqual(
            [node.text_type for node in result],
            [
                TextType.NORMAL,
                TextType.NORMAL
            ]
        )

    def test_delimiters_inside_text(self):
        old_nodes = [
            TextNode("before **bold** after", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            [node.text for node in result],
            [
                "before ",
                "bold",
                " after"
            ]
        )
        self.assertEqual(
            [node.text_type for node in result],
            [
                TextType.NORMAL,
                TextType.BOLD,
                TextType.NORMAL
            ]
        )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_images(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(result[0], ("image", "https://i.imgur.com/zjjcJKZ.png"))

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        result = extract_markdown_links(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(result[0], ("link", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

    def test_extract_multiple_markdown_links(self):
        text = "This is text with a [link](https://github.com/smitty392) and a [second link](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        result = extract_markdown_links(text)

        self.assertEqual(len(result), 2)
        self.assertEqual([len(tup) for tup in result], [2 for x in result])
        self.assertEqual(
            result,
            [
                ("link", "https://github.com/smitty392"),
                ("second link", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            ]
        )

    def test_split_image_from_text(self):
        old_nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
                TextType.NORMAL
            )
        ]
        result = split_nodes_image(old_nodes)

        self.assertEqual(len(result), 2)
        self.assertEqual(
            [(node.text, node.text_type, node.url) for node in result],
            [
                (
                    "This is text with an ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png"
                )
            ]
        )

    def test_split_link_from_text(self):
        old_nodes = [
            TextNode(
                "This is text with a [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
                TextType.NORMAL
            )
        ]
        result = split_nodes_link(old_nodes)

        self.assertEqual(len(result), 2)
        self.assertEqual(
            [(node.text, node.text_type, node.url) for node in result],
            [
                (
                    "This is text with a ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "link",
                    TextType.LINK,
                    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                )
            ]
        )

    def test_split_image_from_middle_of_text(self):
        old_nodes = [
            TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in middle of string",
                TextType.NORMAL
            )
        ]
        result = split_nodes_image(old_nodes)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            [(node.text, node.text_type, node.url) for node in result],
            [
                (
                    "This is text with an ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png"
                ),
                (
                    " in middle of string",
                    TextType.NORMAL,
                    None
                )
            ]
        )

    def test_split_link_from_middle_of_text(self):
        old_nodes = [
            TextNode(
                "This is text with a [link](https://github.com/smitty392) in middle of string",
                TextType.NORMAL
            )
        ]
        result = split_nodes_link(old_nodes)

        self.assertEqual(len(result), 3)
        self.assertEqual(
            [(node.text, node.text_type, node.url) for node in result],
            [
                (
                    "This is text with a ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "link",
                    TextType.LINK,
                    "https://github.com/smitty392"
                ),
                (
                    " in middle of string",
                    TextType.NORMAL,
                    None
                )
            ]
        )

    def test_split_multiple_links_from_text(self):
        old_nodes = [
            TextNode(
                "This is text with a [link](https://github.com/smitty392) and a [second link](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
                TextType.NORMAL
            )
        ]
        result = split_nodes_link(old_nodes)

        self.assertEqual(len(result), 4)
        self.assertEqual(
            [(node.text, node.text_type, node.url) for node in result],
            [
                (
                    "This is text with a ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "link",
                    TextType.LINK,
                    "https://github.com/smitty392"
                ),
                (
                    " and a ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "second link",
                    TextType.LINK,
                    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                )
            ]
        )

    def test_split_link_from_multiple_nodes(self):
        old_nodes = [
            TextNode(
                "This is text with a [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
                TextType.NORMAL
            ),
            TextNode(
                "This is text with [another link](https://github.com/smitty392)",
                TextType.NORMAL
            )
        ]
        result = split_nodes_link(old_nodes)

        self.assertEqual(len(result), 4)
        self.assertEqual(
            [(node.text, node.text_type, node.url) for node in result],
            [
                (
                    "This is text with a ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "link",
                    TextType.LINK,
                    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                ),
                (
                    "This is text with ",
                    TextType.NORMAL,
                    None
                ),
                (
                    "another link",
                    TextType.LINK,
                    "https://github.com/smitty392"
                )
            ]
        )

    def test_string_with_no_link(self):
        old_nodes = [
            TextNode(
                "This is text with no link",
                TextType.NORMAL
            )
        ]
        result = split_nodes_link(old_nodes)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            [(node.text, node.text_type, node.url) for node in result],
            [
                (
                    "This is text with no link",
                    TextType.NORMAL,
                    None
                )
            ]
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)

        self.assertEqual(len(result), 10)
        self.assertEqual(
            [node.text for node in result],
            [
                "This is ",
                "text",
                " with an ",
                "italic",
                " word and a ",
                "code block",
                " and an ",
                "obi wan image",
                " and a ",
                "link"
            ]
        )
        self.assertEqual(
            [node.text_type for node in result],
            [
                TextType.NORMAL,
                TextType.BOLD,
                TextType.NORMAL,
                TextType.ITALIC,
                TextType.NORMAL,
                TextType.CODE,
                TextType.NORMAL,
                TextType.IMAGE,
                TextType.NORMAL,
                TextType.LINK
            ]
        )
        self.assertEqual(
            [node.url for node in result],
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                "https://i.imgur.com/fJRm4Vk.jpeg",
                None,
                "https://boot.dev"
            ]
        )


if __name__ == "__main__":
    unittest.main()

