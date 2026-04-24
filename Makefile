MAIN     := main
BUILDDIR := build
LATEXMK  := latexmk
LATEX    := pdflatex

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
