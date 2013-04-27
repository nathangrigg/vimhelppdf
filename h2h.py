#!/usr/bin/python

import sys
import os.path
import codecs
# import cProfile
from vimh2h import VimH2H

SECTION_BEGIN = r"""\addcontentsline{toc}{%s}{%s}
\markright{%s}
\begin{Verbatim}[commandchars=\\\{\}]
"""

CHAPTER_BEGIN = r"""\addcontentsline{toc}{%s}{%s}
"""

SECTION_END = """
\\end{Verbatim}
\\newpage\\phantomsection{}
"""

DOC_END = r"""
\vspace*{\stretch{4}}
\markright{about this pdf}
\addcontentsline{toc}{%s}{About this pdf}
\begin{minipage}{5in}
The text of this document is taken from the Vim
help pages and the Vim FAQ.

\bigskip

The files are converted to pdf using \XeLaTeX with the hyperref package.
The \href{https://github.com/nathangrigg/vimdocpdf}{conversion script}
is written by Nathan Grigg, based on the HTML conversion script written
by Carlo Teubner.
\end{minipage}
\vspace{\stretch{1}}
"""

def slurp(filename):
    f = open(filename)
    c = f.read()
    f.close()
    return c

def main():

    print "Processing tags..."
    h2h = VimH2H(slurp('doc/tags'))
    h2h.add_tags(slurp('doc/vim_faq.txt'))

    contents = slurp('contents.txt').split('\n')
    fout = codecs.open('body.tex', 'w', 'utf-8')

    level = "chapter"
    for row in contents:
        split_row = row.strip().split(None, 1)
        if len(split_row) != 2:
            continue
        filename, title = split_row
        if filename == "#":
            fout.write(CHAPTER_BEGIN % ("chapter", title))
            level = "section"
            continue
        if filename == "##":
            fout.write(CHAPTER_BEGIN % ("section", title))
            level = "subsection"
            continue

        fout.write(SECTION_BEGIN % (level, title, filename.replace('_', r'\_')))

        print "Processing " + filename + "..."
        text = slurp(os.path.join('doc', filename))
        try:
            text = text.decode('UTF-8')
        except UnicodeError:
            text = text.decode('ISO-8859-1')
        fout.write(h2h.to_tex(filename, text))
        fout.write(SECTION_END)

    fout.write(DOC_END % level)

main()
# cProfile.run('main()')
