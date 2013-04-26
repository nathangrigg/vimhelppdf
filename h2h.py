#!/usr/bin/python

import sys
import os.path
import codecs
# import cProfile
from vimh2h import VimH2H

DOC_BEGIN = r"""\documentclass{article}
% \documentclass[a4paper]{article} %a4
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
\setromanfont{Avenir Next}
\setmonofont{Source Code Pro}
\usepackage[margin=1in]{geometry}
% \usepackage[margin=0.9in]{geometry} % a4
% \usepackage[margin=.4in,bottom=.8in,paperwidth=7.3in,paperheight=9.73in]{geometry} % ipad
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0in}
\cfoot{\rightmark{} \textemdash{} \thepage}
\renewcommand\ll[2]{\hyperlink{#1}{\si{#2}}}
\newcommand\ld[2]{\hyperlink{#1}{\color{black}#2}}
\newcommand\ls[2]{\hyperlink{#1}{\ss{#2}}}
\newcommand\lo[2]{\hyperlink{#1}{\so{#2}}}
\newcommand\lc[2]{\hyperlink{#1}{\sc{#2}}}
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
\begin{document}\phantomsection{}
"""

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

    fout.write(DOC_END)

main()
# cProfile.run('main()')
