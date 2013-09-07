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

body.tex: $(helpfiles) $(docdir) contents.txt
	python h2h.py

clean:
	-rm body.tex *.log *.aux *.toc *.out
	-rm -r $(docdir)

clobber: clean
	-rm vimhelp{,-ipad,-a4}.pdf

help:
	@echo "$$TASKS"

.PHONY: letter a4 ipad all update help clean clobber FORCE
