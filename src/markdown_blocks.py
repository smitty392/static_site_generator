from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph block"
    HEADING = "heading block"
    CODE = "code block"
    QUOTE = "quote block"
    UNORDERED_LIST = "unordered list block"
    ORDERED_LIST = "ordered list block"


def block_to_block_type(block):
    if block.find("# ") in range(6):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif False not in [line.startswith("- ") for line in block.split("\n")]:
        return BlockType.UNORDERED_LIST
    elif False not in [line.startswith(f"{i + 1}. ") for i, line in enumerate(block.split("\n"))]:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    def remove_whitespace_from_lines(block):
        lines = block.split("\n")
        new_lines = []
        for line in lines:
            line = line.strip()
            if line:
                new_lines.append(line)
        new_block = "\n".join(new_lines)
        return new_block

    blocks = list(map(remove_whitespace_from_lines, markdown.split("\n\n")))
    blocks = [block for block in blocks if block]
    return blocks

