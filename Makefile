define TASKS
letter  make letter-sized version
a4      make a4-sized version
ipad    make ipad-sized version
all     make all versions
update  update vim help and vim-faq from repository
clean   delete intermediate files
clobber delete all files
endef
export TASKS

SHELL=/bin/bash

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

%.pdf: %.tex body.tex FORCE
	xelatex $<

body.tex: $(helpfiles) $(docdir) contents.txt
	python h2h.py $(faq)

clean:
	-rm body.tex *.log *.aux *.toc *.out
	-rm -r $(docdir)

clobber: clean
	-rm vimhelp{,-ipad,-a4}.pdf

help:
	@echo "$$TASKS"

.PHONY: letter a4 ipad all update help clean clobber FORCE
