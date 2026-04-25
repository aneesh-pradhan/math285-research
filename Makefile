MAIN     := main
BUILDDIR := build
HTMLDIR  := docs
HTMLBUILD := $(BUILDDIR)/html
LATEXMK  := latexmk
LATEX    := pdflatex
PYTHON   := python3

.PHONY: all
all: $(BUILDDIR)/$(MAIN).pdf

$(BUILDDIR)/$(MAIN).pdf: $(MAIN).tex $(wildcard content/*.tex) $(wildcard bibliography/*.bib)
	mkdir -p $(BUILDDIR)
	$(LATEXMK) -pdf -pdflatex="$(LATEX) -interaction=nonstopmode" \
	            -outdir=$(BUILDDIR) $(MAIN).tex

.PHONY: watch
watch:
	$(LATEXMK) -pdf -pvc -pdflatex="$(LATEX) -interaction=nonstopmode" \
	            -outdir=$(BUILDDIR) $(MAIN).tex

.PHONY: html
html: $(HTMLDIR)/index.html

$(HTMLDIR)/index.html: $(MAIN).tex $(wildcard content/*.tex) \
                        $(wildcard styles/*.sty) $(wildcard bibliography/*.bib) \
                        $(wildcard figures/*) styles/web.css \
                        scripts/postprocess_html.py $(BUILDDIR)/$(MAIN).pdf
	mkdir -p $(HTMLDIR) $(HTMLBUILD)
	make4ht -d $(HTMLDIR) -B $(HTMLBUILD) -j index $(MAIN).tex "mathjax,NoFonts"
	make4ht -d $(HTMLDIR) -B $(HTMLBUILD) -j index $(MAIN).tex "mathjax,NoFonts"
	cp $(BUILDDIR)/$(MAIN).pdf $(HTMLDIR)/$(MAIN).pdf
	cp styles/web.css $(HTMLDIR)/site.css
	touch $(HTMLDIR)/.nojekyll
	$(PYTHON) scripts/postprocess_html.py $(HTMLDIR)/index.html

.PHONY: open
open: all
	xdg-open $(BUILDDIR)/$(MAIN).pdf &

.PHONY: clean
clean:
	$(LATEXMK) -C -outdir=$(BUILDDIR)
	rm -rf $(BUILDDIR)

.PHONY: wc
wc:
	texcount content/*.tex
