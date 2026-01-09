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
    for line in lines:
        if line.startswith('#'):
            count = 0
            for char in line:
                if char == '#':
                    count += 1
                else:
                    break
            if count <= 6 and len(line) > count and line[count] == ' ':
                content = line[count + 1:].strip()
                html_lines.append("<h{}>{}</h{}>".format(count, content, count))

    with open(output_file, 'w') as f:
        f.write('\n'.join(html_lines))
        if html_lines:
            f.write('\n')

    sys.exit(0)