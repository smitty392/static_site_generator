from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_nodes.append(block_to_html_node(block))

    parent_node = ParentNode("div", html_nodes)
    return parent_node


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            block_node = text_to_html_node(block, "p")
        case BlockType.HEADING:
            find_space = block.find(" ")
            new_text = block[find_space + 1:]
            tag = f"h{find_space}"
            block_node = text_to_html_node(new_text, tag)
        case BlockType.CODE:
            new_text = block[3:-3]
            code_node = LeafNode("code", new_text)
            block_node = ParentNode("pre", [code_node])
        case BlockType.QUOTE:
            find_space = block.find(">")
            new_text = block[find_space + 1:]
            block_node = text_to_html_node(new_text, "blockquote")
        case BlockType.UNORDERED_LIST:
            block_node = list_block_to_html_node(block, "ul")
        case BlockType.ORDERED_LIST:
            block_node = list_block_to_html_node(block, "ol")
    return block_node


def text_to_html_node(text, tag):
    text_nodes = text_to_textnodes(text.replace("\n", " "))
    html_nodes = map(text_node_to_html_node, text_nodes)
    node = ParentNode(tag, html_nodes)
    return node


def list_block_to_html_node(block, tag):
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        find_space = line.find(" ")
        new_line = line[find_space + 1:]
        node = text_to_html_node(new_line, "li")
        list_nodes.append(node)
    return ParentNode(tag, list_nodes)

