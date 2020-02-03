#!/usr/bin/python3

import argparse
import os.path
# import cProfile
from vimh2h import VimH2H

SECTION_BEGIN = r"""\addcontentsline{toc}{%s}{%s}
\markright{%s}
\begin{Verbatim}[commandchars=\\\{\},formatcom=\fixurl]
"""

CHAPTER_BEGIN = r"""\addcontentsline{toc}{%s}{%s}
\phantomsection{}
"""

SECTION_END = """
\\end{Verbatim}
\\cleardoublepage\\phantomsection{}
"""

DOC_END = r"""
\addcontentsline{toc}{%s}{About this pdf}
\markright{about this pdf}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--faq', dest='faq', action='store_true')
    parser.add_argument('--no-faq', dest='faq', action='store_false')
    parser.set_defaults(faq=True)
    args = parser.parse_args()

    print("Processing tags...")
    with open(os.path.join('doc', 'tags'), 'r') as input_file:
        h2h = VimH2H(input_file.read())
    if args.faq:
        with open(os.path.join('doc', 'vim_faq.txt'), 'r') as input_file:
            h2h.add_tags(input_file.read())
    with open('contents.txt', 'r') as input_file:
        contents = input_file.read().split('\n')

    with open('body.tex', 'w') as output_file:
        level = "chapter"
        for row in contents:
            split_row = row.strip().split(None, 1)
            if len(split_row) != 2:
                continue
            filename, title = split_row
            if not args.faq and filename == 'vim_faq.txt':
                continue
            if filename == "#":
                output_file.write(CHAPTER_BEGIN % ("chapter", title))
                level = "section"
                continue
            if filename == "##":
                output_file.write(CHAPTER_BEGIN % ("section", title))
                level = "subsection"
                continue

            print("Processing " + filename + "...")
            output_file.write(SECTION_BEGIN % (level, title, filename.replace('_', r'\_')))

            with open(os.path.join('doc', filename), 'r') as input_file:
                text = input_file.read()
            output_file.write(h2h.to_tex(filename, text, args.faq))
            output_file.write(SECTION_END)

        output_file.write(DOC_END % level)

main()
# cProfile.run('main()')
