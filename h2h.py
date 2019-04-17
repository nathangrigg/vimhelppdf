#!/usr/bin/python3

import os.path
# import cProfile
from vimh2h import VimH2H

SECTION_BEGIN = r"""\addcontentsline{toc}{%s}{%s}
\markright{%s}
\begin{Verbatim}[commandchars=\\\{\},formatcom=\fixurl]
"""

CHAPTER_BEGIN = r"""\addcontentsline{toc}{%s}{%s}
"""

SECTION_END = """
\\end{Verbatim}
\\newpage\\phantomsection{}
"""

DOC_END = r"""
\addcontentsline{toc}{%s}{About this pdf}
\markright{about this pdf}
"""

def main():

    print("Processing tags...")
    with open(os.path.join('doc', 'tags'),'r') as inputFile:
        h2h = VimH2H(inputFile.read())
    with open(os.path.join('doc', 'vim_faq.txt'),'r') as inputFile:
        h2h.add_tags(inputFile.read())
    with open('contents.txt','r') as inputFile:
        contents = inputFile.read().split('\n')

    with open('body.tex', 'w') as outputFile:
        level = "chapter"
        for row in contents:
            split_row = row.strip().split(None, 1)
            if len(split_row) != 2:
                continue
            filename, title = split_row
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
            outputFile.write(h2h.to_tex(filename, text))
            outputFile.write(SECTION_END)

        outputFile.write(DOC_END % level)

main()
# cProfile.run('main()')
