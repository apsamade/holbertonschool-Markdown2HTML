#!/usr/bin/python3
"""
Markdown to HTML converter script.
"""

import sys
import os
import re
import hashlib


def parse_inline(text):
    """Parse inline markdown syntax: bold, emphasis, MD5, remove c."""
    # MD5 conversion [[text]] -> md5 hash
    pattern = r'\[\[(.+?)\]\]'
    while re.search(pattern, text):
        match = re.search(pattern, text)
        md5_hash = hashlib.md5(match.group(1).encode()).hexdigest()
        text = text[:match.start()] + md5_hash + text[match.end():]

    # Remove c ((text)) -> text without c
    pattern = r'\(\((.+?)\)\)'
    while re.search(pattern, text):
        match = re.search(pattern, text)
        content = match.group(1).replace('c', '').replace('C', '')
        text = text[:match.start()] + content + text[match.end():]

    # Bold **text** -> <b>text</b>
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)

    # Emphasis __text__ -> <em>text</em>
    text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)

    return text


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        sys.stderr.write("Missing {}\n".format(markdown_file))
        sys.exit(1)

    with open(markdown_file, 'r') as f:
        lines = f.readlines()

    html_lines = []
    in_ul = False
    in_ol = False
    in_p = False
    p_lines = []

    for line in lines:
        line_stripped = line.strip()

        # Check if line is empty
        if not line_stripped:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if in_p:
                html_lines.append("<p>")
                html_lines.append("<br/>\n".join(p_lines))
                html_lines.append("</p>")
                in_p = False
                p_lines = []
            continue

        # Handle headings
        if line.startswith('#'):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if in_p:
                html_lines.append("<p>")
                html_lines.append("<br/>\n".join(p_lines))
                html_lines.append("</p>")
                in_p = False
                p_lines = []
            count = 0
            for char in line:
                if char == '#':
                    count += 1
                else:
                    break
            if count <= 6 and len(line) > count and line[count] == ' ':
                content = parse_inline(line[count + 1:].strip())
                heading = "<h{}>{}</h{}>".format(count, content, count)
                html_lines.append(heading)

        # Handle unordered list items
        elif line.startswith('- '):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if in_p:
                html_lines.append("<p>")
                html_lines.append("<br/>\n".join(p_lines))
                html_lines.append("</p>")
                in_p = False
                p_lines = []
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            content = parse_inline(line[2:].strip())
            html_lines.append("<li>{}</li>".format(content))

        # Handle ordered list items
        elif line.startswith('* '):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_p:
                html_lines.append("<p>")
                html_lines.append("<br/>\n".join(p_lines))
                html_lines.append("</p>")
                in_p = False
                p_lines = []
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            content = parse_inline(line[2:].strip())
            html_lines.append("<li>{}</li>".format(content))

        # Handle paragraph text
        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_p:
                in_p = True
            p_lines.append(parse_inline(line_stripped))

    # Close any open tags
    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")
    if in_p:
        html_lines.append("<p>")
        html_lines.append("<br/>\n".join(p_lines))
        html_lines.append("</p>")

    with open(output_file, 'w') as f:
        f.write('\n'.join(html_lines))
        if html_lines:
            f.write('\n')

    sys.exit(0)
