.SUFFIXES: 
.SUFFIXES: .tmpl .html
RENDER = ../bin/render.py

%.html:%.tmpl
	$(RENDER) $< > $@

TEMPLATE_FILES=$(wildcard *.tmpl)
HTML_FILES=$(TEMPLATE_FILES:.tmpl=.html)
html: $(HTML_FILES)

*.html: $(wildcard templates/*.tmpl) $(wildcard */*/*/benchmark.dat) \
	$(wildcard */*/*/comments.txt) $(RENDER) 
minimization.html: $(wildcard minimization/*/*/*.dat)

.PHONY: clean html
clean:
	rm *.html
