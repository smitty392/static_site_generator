import re
from textnode import TextType, TextNode


def text_to_textnodes(text):
    initial_node = [TextNode(text, TextType.NORMAL)]
    bold_results = split_nodes_delimiter(initial_node, "**", TextType.BOLD)
    italic_results = split_nodes_delimiter(bold_results, "_", TextType.ITALIC)
    code_results = split_nodes_delimiter(italic_results, "`", TextType.CODE)
    image_results = split_nodes_image(code_results)
    link_results = split_nodes_link(image_results)
    return link_results


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    def split_node(old_node):
        if old_node.text_type != TextType.NORMAL:
            return [old_node]
        text_split = old_node.text.split(delimiter)
        if len(text_split) % 2 == 0:
            raise Exception("invalid Markdown")
        result = []
        for i, value in enumerate(text_split):
            if not value:
                continue
            if i % 2 == 0:
                result.append(TextNode(value, TextType.NORMAL))
            else:
                result.append(TextNode(value, text_type))
        return result

    result = []
    for sublist in map(split_node, old_nodes):
        result.extend(sublist)
    return result


def split_nodes_image(old_nodes):
    def split_node(old_node):
        original_text = old_node.text
        original_text_type = old_node.text_type
        images = extract_markdown_images(original_text)
        if not images or original_text_type == TextType.IMAGE:
            return [old_node]

        text_to_split = original_text
        result = []
        for image in images:
            if len(image) != 2:
                raise Exception("invalid Markdown")
            alt_text = image[0]
            url = image[1]
            text_split = text_to_split.split(f"![{alt_text}]({url})")
            if text_split[0]:
                result.append(TextNode(text_split[0], original_text_type))
            result.append(TextNode(alt_text, TextType.IMAGE, url))
            text_to_split = text_split[1]
        if text_to_split:
            result.append(TextNode(text_to_split, original_text_type))
        return result

    result = []
    for sublist in map(split_node, old_nodes):
        result.extend(sublist)
    return result


def split_nodes_link(old_nodes):
    def split_node(old_node):
        original_text = old_node.text
        original_text_type = old_node.text_type
        links = extract_markdown_links(original_text)
        if not links or original_text_type == TextType.LINK:
            return [old_node]

        text_to_split = original_text
        result = []
        for link in links:
            if len(link) != 2:
                raise Exception("invalid Markdown")
            anchor_text = link[0]
            url = link[1]
            text_split = text_to_split.split(f"[{anchor_text}]({url})")
            if text_split[0]:
                result.append(TextNode(text_split[0], original_text_type))
            result.append(TextNode(anchor_text, TextType.LINK, url))
            text_to_split = text_split[1]
        if text_to_split:
            result.append(TextNode(text_to_split, original_text_type))
        return result

    result = []
    for sublist in map(split_node, old_nodes):
        result.extend(sublist)
    return result


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\[\]]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\[\]]*)\)", text)
    return matches

