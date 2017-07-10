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

docdir = doc
helpfiles = $(wildcard $(docdir)/*.txt)

letter: vimhelp.pdf
a4: vimhelp-a4.pdf
ipad: vimhelp-ipad.pdf
all: letter a4 ipad

update:
	./update.sh

$(docdir):
	./update.sh

%.pdf: %.tex body.tex FORCE
	xelatex $<
ifndef SECOND_TIME_RUN
	$(MAKE) $(MAKECMDGOALS) SECOND_TIME_RUN=true
endif

body.tex: $(helpfiles) $(docdir) contents.txt
	python h2h.py

clean:
	-rm -f body.tex *.log *.aux *.toc *.out *.pyc
	-rm -f -r $(docdir)

clobber: clean
	-rm -f vimhelp{,-ipad,-a4}.pdf

distclean: clobber

help:
	@echo "$$TASKS"

.PHONY: letter a4 ipad all update help clean clobber distclean FORCE
