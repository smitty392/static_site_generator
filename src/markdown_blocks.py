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

