.SUFFIXES: 
.SUFFIXES: .tmpl .html
RENDER = ../bin/render.py

%.html:%.tmpl
	$(RENDER) $< > $@

TEMPLATE_FILES=$(wildcard *.tmpl)
HTML_FILES=$(TEMPLATE_FILES:.tmpl=.html)
html: $(HTML_FILES)
website: tar html

*.html: $(wildcard templates/*.tmpl) $(wildcard */*/*/benchmark.dat) \
	$(wildcard */*/*/comments.txt) $(RENDER) 

tar:
	../bin/package.sh

.PHONY: clean html tar website
clean:
	rm *.html
