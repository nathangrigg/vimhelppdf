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

letter: vimdoc.pdf
a4: vimdoc-a4.pdf
ipad: vimdoc-ipad.pdf
all: letter a4 ipad

update:
	./update.sh

$(docdir):
	./update.sh

%.pdf: %.tex body.tex preamble.tex
	latexmk $<

body.tex: $(helpfiles) $(docdir)
	./h2h.py

clean:
	latexmk -c
	rm body.tex
	rm -r $(docdir)

clobber:
	latexmk -C

help:
	@echo "$$TASKS"

.PHONY: letter a4 ipad all update help clean clobber
