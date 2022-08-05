define TASKS
letter     make letter-sized version
a4         make a4-sized version
ipad       make ipad-sized version
all        make all versions
update     update vim help and vim-faq from repository
clean      delete intermediate files
clobber    delete all files
distclean  same as clobber
endef
export TASKS

SHELL=/bin/bash

ifeq ($(OS),Windows_NT)  # Windows, MinGW, Cygwin, etc...
    OS := Windows
    subst_text := \\setmainfont{Arial}\n\\setmonofont{Courier New}
else
    OS := $(shell sh -c 'uname -s 2>/dev/null || echo not')
    ifeq ($(OS),Darwin)  # Mac OS X
        OS := Darwin
        subst_text := \\setromanfont{Avenir Next}\n\\setmonofont{Source Code Pro}
    else                 # Linux, GNU Hurd, *BSD, Haiku, Android, etc...
        OS := Linux
        subst_text := \\setmainfont{Liberation Sans}\n\\setmonofont{Liberation Mono}
    endif
endif

docdir = doc
helpfiles = $(wildcard $(docdir)/*.txt)

# If you use this you are going to want to do a `make clean` because
# it will mess up the dependencies.
ifeq (no, ${FAQ})
faq := --no-faq
endif

letter: vimhelp.pdf
a4: vimhelp-a4.pdf
ipad: vimhelp-ipad.pdf
all: letter a4 ipad

update:
	./update.sh

$(docdir):
	./update.sh

vimhelp.tex vimhelp-a4.tex vimhelp-ipad.tex: preamble.tex

preamble.tex: FORCE
	sed -i -e '/^\\usepackage{fontspec}/ {n;N;s/.*/$(subst_text)/}' preamble.tex

%.pdf: %.tex body.tex FORCE
	xelatex $<
ifndef SECOND_TIME_RUN
	$(MAKE) $(MAKECMDGOALS) SECOND_TIME_RUN=true
endif

body.tex: $(helpfiles) $(docdir) contents.txt
	python3 h2h.py $(faq)

clean:
	-rm -f body.tex *.log *.aux *.toc *.out *.pyc
	-rm -f -r $(docdir)

clobber: clean
	-rm -f vimhelp{,-ipad,-a4}.pdf

distclean: clobber

help:
	@echo "$$TASKS"

.PHONY: letter a4 ipad all update help clean clobber distclean FORCE
