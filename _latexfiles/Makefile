LATEXFILES := $(dir $(lastword $(MAKEFILE_LIST)))

# We store the absolute path of the Makefile in MY_MAKEFILE
# $(realpath...) appends the cwd unconditionally, so we need
# to filter this to avoid duplicate prepend of the cwd
MY_MAKEFILE := $(lastword $(MAKEFILE_LIST))
MY_MAKEFILE := $(lastword $(wildcard $(MY_MAKEFILE) $(realpath $(MY_MAKEFILE))))

# make doesn't like file names containing spaces -- 
# we ignore them.
# If a directory contains a file named "a b" and two files
# c and d, $(wildcard *) expands to "a b c d". The second
# call to $(wildcard...) returns all files that match
# the patern "a b c d", i.e., only the files that exists.
# Thus, only "c d" are returned, and will be processed
# later on.
ALL_FILES := $(wildcard $(addsuffix /.,$(wildcard *)))

all: $(ALL_FILES)

-include Makefile.in

# look into latexmkrc for configuration options
LATEXMK := perl $(dir $(MY_MAKEFILE))latexmk.pl
OUTDIR_NAME := $(firstword $(OUTDIR_NAME) tmp)
ifneq ($(OUTDIR_NAME),.)
OUTDIR_SWITCH := -output-directory=$(OUTDIR_NAME)
OUTDIR_DELETE := $(OUTDIR_NAME)
endif
FMTDIR_NAME := $(firstword $(FMTDIR_NAME) fmt)
WORDCOUNT_TMPDIR_NAME := wc
export PDFLATEX := $(lastword pdflatex $(PDFLATEX))



clean: FORCE
	$(LATEXMK) -C -silent
	rm -rf .format.dependencies.* *.fmt *.synctex.gz *.pdf *.4ct *.4tc *.bbl *.css *.htm *.html *.idv *.lg *.odt *.tdo *.tmp *.xref $(OUTDIR_DELETE) $(WORDCOUNT_TMPDIR_NAME)

-include $(wildcard .format.dependencies.*)

.PHONY: all FORCE

%/.: %/Makefile.in FORCE
	$(MAKE) -C $(dir $@) -f $(MY_MAKEFILE)

%/.: $(addsuffix /.,%/*) FORCE ;

ifdef V
LATEXMK_FLAGS := -g
else
LATEXMK_FLAGS := -f -silent
endif

$(FMTDIR_NAME):
	mkdir -p $(FMTDIR_NAME)

%.fmt: %.ltx $(FMTDIR_NAME)
	pdflatex -recorder -ini -output-directory=$(FMTDIR_NAME) -interaction=nonstopmode "&pdflatex $*.ltx\dump" || true
	egrep '^INPUT ' $(FMTDIR_NAME)/$*.fls | sed 's/INPUT /$*.fmt: /' | sort | uniq | grep -v '.*\.pdf$$' > .format.dependencies.$*
	cp -u -v $(FMTDIR_NAME)/$@ .

$(OUTDIR_NAME):
	mkdir $(OUTDIR_NAME)

%.pdf: $(OUTDIR_NAME) %.tex FORCE
	[ ! -e $*.ltx ] || make $*.fmt
	$(LATEXMK) -pdf -recorder $(LATEXMK_FLAGS) $(OUTDIR_SWITCH) -r $(dir $(MY_MAKEFILE))latexmkrc $(basename $(abspath $*)) || tail -n 25 $(OUTDIR_NAME)/$*.log
	[ ! -e $(OUTDIR_NAME)/$@ ] || [ $@ -ef $(OUTDIR_NAME)/$@ ] || cp -u -v $(OUTDIR_NAME)/$@ .
	[ ! -e $(OUTDIR_NAME)/$*.synctex.gz ] || [ $*.synctex.gz -ef $(OUTDIR_NAME)/$*.synctex.gz ] || cp -u -v $(OUTDIR_NAME)/$*.synctex.gz .
	[ ! -e $(OUTDIR_NAME)/$*.log ] || [ $*.log -ef $(OUTDIR_NAME)/$*.log ] || cp -u -v $(OUTDIR_NAME)/$*.log .

%.html: %.tex FORCE
	make $*.pdf
	cp -u -v $(OUTDIR_NAME)/* .
	htlatex $(basename $(abspath $*)) "$(LATEXFILES)/tex2word/ivt.cfg,word" 'symbol/!' "-cvalidate -e$(LATEXFILES)/tex2word/tex4ht.env"

%.odt: %.pdf FORCE
	cp -u -v $(OUTDIR_NAME)/* .
	mk4ht oolatex $(basename $(abspath $*)) "$(LATEXFILES)/tex2word/ivt-oo.cfg,ooffice,bib-,hidden-ref"
	mk4ht oolatex $(basename $(abspath $*)) "$(LATEXFILES)tex2word/ivt-oo.cfg,ooffice,bib-,hidden-ref"

%-trr.odt: %.pdf FORCE
	[ "." = "$(OUTDIR_NAME)" ] || cp -u -v $(OUTDIR_NAME)/* .
	mk4ht oolatex $(basename $(abspath $*)) "$(LATEXFILES)/tex2word/trr.cfg,ooffice,bib-,hidden-ref"
	mv $*.odt $@

%.htm: %.tex FORCE
	make $*.pdf
	[ "." = "$(OUTDIR_NAME)" ] || cp -u -v $(OUTDIR_NAME)/* .
	htlatex $(basename $(abspath $*)) "$(LATEXFILES)/tex2word/simple.cfg,charset=utf-8,-css,NoFonts" ' -cunihtf -utf8' " -cvalidate"
	grep -A 10000000 '[<]html' $*.html > $@
	rm $*.html

%.Rtex %.dat: %.Rnw
	echo "library(knitr); knit('$<', output='$*.Rtex.utf8')" | R --no-save --no-restore || true
	iconv -t latin1 $*.Rtex.utf8 > $*.Rtex
	rm $*.Rtex.utf8

%.R: %.Rnw
	echo "library(knitr); purl('$<', output='$*.R')" | R --no-save --no-restore || true

%-flat.tex: %.tex
	latexpand --keep-comments $< | sed -r 's/\\makeatletter[{][}]//g' > $@

FORCE:

spin:
	make $(SPIN_TARGET); while true; do inotifywait -r . $(shell find . -type l -xtype d -printf '%p/*\n') $(shell find . -type l -xtype f) -e CREATE,MODIFY,DELETE; make -j2 $(SPIN_TARGET); done
