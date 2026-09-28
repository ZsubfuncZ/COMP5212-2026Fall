.PHONY: all presentation handout clean
all: presentation handout
presentation:
	latexmk -pdf main.tex
handout:
	latexmk -pdf handout.tex
clean:
	latexmk -c main.tex
	latexmk -c handout.tex
