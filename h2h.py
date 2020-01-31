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
    with open(os.path.join('doc', 'tags'),'r') as inputFile:
        h2h = VimH2H(inputFile.read())
    with open(os.path.join('doc', 'vim_faq.txt'),'r') as inputFile:
        h2h.add_tags(inputFile.read())
    with open('contents.txt','r') as inputFile:
        contents = inputFile.read().split('\n')
    if args.faq:
        with open('doc/vim_faq.txt','r') as inputFile:
            h2h.add_tags(inputFile.read())

    with open('body.tex', 'w') as outputFile:
        level = "chapter"
        for row in contents:
            split_row = row.strip().split(None, 1)
            if len(split_row) != 2:
                continue
            filename, title = split_row
            if not args.faq and filename == 'vim_faq.txt':
                continue
            if filename == "#":
                outputFile.write(CHAPTER_BEGIN % ("chapter", title))
                level = "section"
                continue
            if filename == "##":
                outputFile.write(CHAPTER_BEGIN % ("section", title))
                level = "subsection"
                continue

            print("Processing " + filename + "...")
            outputFile.write(SECTION_BEGIN % (level, title, filename.replace('_', r'\_')))

            with open(os.path.join('doc', filename),'r') as inputFile:
                text =inputFile.read()
            outputFile.write(h2h.to_tex(filename, text, args.faq))
            outputFile.write(SECTION_END)

        outputFile.write(DOC_END % level)

main()
# cProfile.run('main()')
