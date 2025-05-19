import unittest
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_heading(self):
        blocks = [
            "# this is a h1 heading",
            "## this is a h2 heading",
            "### this is a h3 heading",
            "#### this is a h4 heading",
            "##### this is a h5 heading",
            "###### this is a h6 heading"
        ]
        block_types = [block_to_block_type(block) for block in blocks]

        self.assertEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING
            ]
        )

    def test_block_code(self):
        block = "```this is a code block```"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.CODE)

    def test_block_quote(self):
        block = ">this is a quote block"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_unordered_list(self):
        block = "- this is an\n- unordered list with\n- some items"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_ordered_list(self):
        block = "1. this is an\n2. ordered list with\n3. three items"
        block_type = block_to_block_type(block)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_paragraph(self):
        blocks = [
            "this is a paragraph",
            "####### this is not a heading",
            "``` this is not a code block",
            "`` this is also not a code block```",
            "- this is not\n-an unordered list\n- for (some) reason ;)",
            "1. this is not\n2.an ordered\n3. list",
            "1. this is also\n3. not an\n2. ordered list"
        ]
        block_types = [block_to_block_type(block) for block in blocks]

        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH
            ]
        )


if __name__ == "__main__":
    unittest.main()
