# converts vim documentation to html

import re

VIM_FAQ_LINE = """\
 \ll{76696d5f6661712e747874}{vim_faq.txt}       Frequently asked questions
"""

RE_TAGLINE = re.compile(r'(\S+)\s+(\S+)')

PAT_WORDCHAR = '[!#-)+-{}~\xC0-\xFF]'

PAT_HEADER   = r'(^.*~$)'
PAT_GRAPHIC  = r'(^.* `$)'
PAT_PIPEWORD = r'(?<!\\)\|([#-)!+-~]+)\|'
PAT_STARWORD = r'\*([#-)!+-~]+)\*(?:(?=\s)|$)'
PAT_COMMAND  = r'`([^` ]+)`'
PAT_OPTWORD  = r"('(?:[a-z]{2,}|t_..)')"
PAT_CTRL     = r'(CTRL-(?:W_)?(?:[\w\[\]^+-<>=@]|<[A-Za-z]+?>)?)'
PAT_SPECIAL  = r'(<.*?>|\{.*?}|' \
               r'\[(?:range|line|count|offset|\+?cmd|[-+]?num|\+\+opt|' \
               r'arg|arguments|ident|addr|group)]|' \
               r'(?<=\s)\[[-a-z^A-Z0-9_]{2,}])'
PAT_TITLE    = r'(Vim version [0-9.a-z]+|VIM REFERENCE.*)'
PAT_NOTE     = r'((?<!' + PAT_WORDCHAR + r')(?:note|NOTE|Notes?):?' \
                 r'(?!' + PAT_WORDCHAR + r'))'
PAT_URL      = r'((?:https?|ftp)://[^\'"<> \t]+[a-zA-Z0-9/])'
PAT_WORD     = r'((?<!' + PAT_WORDCHAR + r')' + PAT_WORDCHAR + r'+' \
                 r'(?!' + PAT_WORDCHAR + r'))'

RE_LINKWORD = re.compile(
        PAT_OPTWORD  + '|' +
        PAT_CTRL     + '|' +
        PAT_SPECIAL)
RE_TAGWORD = re.compile(
        PAT_HEADER   + '|' +
        PAT_GRAPHIC  + '|' +
        PAT_PIPEWORD + '|' +
        PAT_STARWORD + '|' +
        PAT_COMMAND  + '|' +
        PAT_OPTWORD  + '|' +
        PAT_CTRL     + '|' +
        PAT_SPECIAL  + '|' +
        PAT_TITLE    + '|' +
        PAT_NOTE     + '|' +
        PAT_URL      + '|' +
        PAT_WORD)
RE_NEWLINE   = re.compile(r'[\r\n]')
RE_HRULE     = re.compile(r'[-=]{3,}.*[-=]{3,3}$')
RE_EG_START  = re.compile(r'(?:.* )?>$')
RE_EG_END    = re.compile(r'\S')
RE_SECTION   = re.compile(r'[-A-Z .][-A-Z0-9 .()]*(?=\s+\*)')
RE_STARTAG   = re.compile(r'\s\*([^ \t|]+)\*(?:\s|$)')
RE_LOCAL_ADD = re.compile(r'LOCAL ADDITIONS:\s+\*local-additions\*$')
LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslashzzz'),
    (re.compile(r'([{}])'), r'\\\1'),
    (re.compile(r'[\x00-\x1f]'), '?'),
    (re.compile(r'\\textbackslashzzz'), r'\\textbackslash{}'),
)

class Link(object):
    __slots__ = 'link_pipe', 'link_plain'

    def __init__(self, link_pipe, link_plain):
        self.link_pipe = link_pipe
        self.link_plain = link_plain

class VimH2H(object):
    def __init__(self, tags, version=None):
        self._urls = { }
        self._version = version
        for line in RE_NEWLINE.split(tags):
            m = RE_TAGLINE.match(line)
            if m:
                tag, filename = m.group(1, 2)
                self.do_add_tag(tag)

    def add_tags(self, contents):
        for match in RE_STARTAG.finditer(contents):
            tag = match.group(1).replace('\\', '\\\\').replace('/', '\\/')
            self.do_add_tag(tag)

    def do_add_tag(self, tag):
        args = "{" + tag.encode("hex") + "}{" + tex_escape[tag] + "}"
        link_pipe = '\\ll' + args
        classattr = '\\ld'
        m = RE_LINKWORD.match(tag)
        if m:
            opt, ctrl, special = m.groups()
            if opt is not None: classattr = '\\lo'
            elif ctrl is not None: classattr = '\\lc'
            elif special is not None: classattr = '\\ls'
        link_plain = classattr + args
        self._urls[tag] = Link(link_pipe, link_plain)

    def maplink(self, tag, css_class=None):
        links = self._urls.get(tag)
        if links is not None:
            if css_class == 'l': return links.link_pipe
            else: return links.link_plain
        elif css_class is not None:
            return '\\s' + css_class + '{' + tex_escape[tag] + '}'
        else: return tex_escape[tag]

    def to_tex(self, filename, contents):
        out = [ ]

        inexample = 0
        filename = str(filename)
        is_help_txt = (filename == 'help.txt')
        faq_line = False
        for line in RE_NEWLINE.split(contents):
            line = line.rstrip('\r\n')
            line_tabs = line
            line = line.expandtabs()
            if RE_HRULE.match(line):
                out.extend((r'\sh{', line, '}', '\n'))
                continue
            if inexample == 2:
                if RE_EG_END.match(line):
                    inexample = 0
                    if line[0] == '<': line = line[1:]
                else:
                    out.extend((r'\se{', tex_escape[line], '}', '\n'))
                    continue
            if RE_EG_START.match(line_tabs):
                inexample = 1
                line = line[0:-1]
            if RE_SECTION.match(line_tabs):
                m = RE_SECTION.match(line)
                out.extend((r'\sc{', m.group(0), r'}'))
                line = line[m.end():]
            if is_help_txt and RE_LOCAL_ADD.match(line_tabs):
                faq_line = True
            lastpos = 0
            for match in RE_TAGWORD.finditer(line):
                pos = match.start()
                if pos > lastpos:
                    out.append(tex_escape[line[lastpos:pos]])
                lastpos = match.end()
                header, graphic, pipeword, starword, command, opt, ctrl, \
                        special, title, note, url, word = match.groups()
                if pipeword is not None:
                    out.extend((' ', self.maplink(pipeword, 'l'), ' '))
                elif starword is not None:
                    out.extend((' \\hypertarget{', starword.encode("hex"),
                            '}{\\st{', tex_escape[starword], '}} '))
                elif command is not None:
                    out.extend(('`\\se{', tex_escape[command], '}`'))
                elif opt is not None:
                    out.append(self.maplink(opt, 'o'))
                elif ctrl is not None:
                    out.append(self.maplink(ctrl, 'k'))
                elif special is not None:
                    out.append(self.maplink(special, 's'))
                elif title is not None:
                    out.extend(('\\si{', tex_escape[title], '}'))
                elif note is not None:
                    out.extend(('\\sn{', tex_escape[note], '}'))
                elif header is not None:
                    out.extend(('\\sh{', tex_escape[header[:-1]], '}'))
                elif graphic is not None:
                    out.append(tex_escape[graphic[:-2]])
                elif url is not None:
                    out.extend(('\\url{', url, '}'))
                elif word is not None:
                    out.append(self.maplink(word))
            if lastpos < len(line):
                out.append(tex_escape[line[lastpos:]])
            out.append('\n')
            if inexample == 1: inexample = 2
            if faq_line:
                out.append(VIM_FAQ_LINE)
                faq_line = False

        return ''.join(out)

class TexEscCache(dict):
    def __missing__(self, key):
        r = key
        for pattern, replacement in LATEX_SUBS:
            r = pattern.sub(replacement, r)
        self[key] = r
        return r

tex_escape = TexEscCache()
