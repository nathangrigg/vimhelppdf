#!/usr/bin/python

import sys
import os.path
import codecs
# import cProfile
from vimh2h import VimH2H

DOC_BEGIN = r"""\documentclass{article}
\usepackage{xcolor}
\definecolor{i}{RGB}{0,137,139}
\definecolor{t}{RGB}{250,0,250}
\definecolor{h}{RGB}{164,32,246}
\definecolor{k}{RGB}{106,89,205}
\definecolor{e}{RGB}{0,0,255}
\definecolor{s}{RGB}{106,89,205}
\definecolor{o}{RGB}{46,139,87}
\definecolor{c}{RGB}{165,42,42}
\usepackage[colorlinks=true]{hyperref}
\usepackage{fancyvrb}
\usepackage{fontspec}
\setmonofont{Source Code Pro}
\usepackage[margin=1in,left=1.25in]{geometry}
\renewcommand\ll[2]{\hyperref[#1]{\si{#2}}}
\newcommand\ld[2]{\hyperref[#1]{\color{black}#2}}
\newcommand\ls[2]{\hyperref[#1]{\ss{#2}}}
\newcommand\lo[2]{\hyperref[#1]{\so{#2}}}
\newcommand\lc[2]{\hyperref[#1]{\sc{#2}}}
\newcommand\st[1]{{\color{t}#1}}
\newcommand\si[1]{{\color{i}#1}}
\newcommand\sn[1]{{\color{n}#1}}
\newcommand\sh[1]{{\color{h}#1}}
\newcommand\sk[1]{{\color{k}#1}}
\newcommand\se[1]{{\color{e}#1}}
\renewcommand\ss[1]{{\color{s}#1}}
\renewcommand\sn[1]{{\color{blue}#1}}
\newcommand\so[1]{\textbf{\color{o}#1}}
\renewcommand\sc[1]{\textbf{\color{c}#1}}
\begin{document}
"""

SECTION_BEGIN = r"""\newpage
\phantomsection{}\addcontentsline{toc}{section}{%s}
\begin{Verbatim}[commandchars=\\\{\}]
"""

SECTION_END = """
\\end{Verbatim}
"""

DOC_END = """\\end{document}
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
    fout = codecs.open('vimdoc.tex', 'w', 'utf-8')
    fout.write(DOC_BEGIN)

    for row in contents:
        split_row = row.strip().split(None, 1)
        if len(split_row) != 2:
            continue
        filename, title = split_row
        fout.write(SECTION_BEGIN % title)

        print "Processing " + filename + "..."
        text = slurp(os.path.join('doc', filename))
        try:
            text = text.decode('UTF-8')
        except UnicodeError:
            text = text.decode('ISO-8859-1')
        fout.write(h2h.to_tex(filename, text))
        fout.write(SECTION_END)

    fout.write(DOC_END)

main()
# cProfile.run('main()')
