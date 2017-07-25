-include _latexfiles/Makefile

all: _latexfiles

PARENT_LATEXFILES=$(firstword $(wildcard ../_latexfiles ../../_latexfiles ../../../_latexfiles ../../../../_latexfiles ../../../../../_latexfiles ../../../../../../_latexfiles ../../../../../../../_latexfiles ../../../../../../../../_latexfiles ../../../../../../../../../_latexfiles ../../../../../../../../../../_latexfiles))


_latexfiles:
	[ -n "$(PARENT_LATEXFILES)" ] # If failing here, no _latexfiles directory exists above this directory
	ln -s $(PARENT_LATEXFILES) _latexfiles
	make
