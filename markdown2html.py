#!/usr/bin/python3
"""
Markdown to HTML converter script.
"""

import sys
import os


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

    for line in lines:
        # Handle headings
        if line.startswith('#'):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            count = 0
            for char in line:
                if char == '#':
                    count += 1
                else:
                    break
            if count <= 6 and len(line) > count and line[count] == ' ':
                content = line[count + 1:].strip()
                html_line = "<h{}>{}</h{}>".format(count, content, count)
                html_lines.append(html_line)
        # Handle unordered list items
        elif line.startswith('- '):
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            content = line[2:].strip()
            html_lines.append("<li>{}</li>".format(content))
        else:
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False

    # Close any open list
    if in_ul:
        html_lines.append("</ul>")

    with open(output_file, 'w') as f:
        f.write('\n'.join(html_lines))
        if html_lines:
            f.write('\n')

    sys.exit(0)
