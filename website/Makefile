.SUFFIXES: 
.SUFFIXES: .tmpl .html
RENDER = ../bin/render.py

%.html:%.tmpl
	$(RENDER) $< > $@

%.d:%.tmpl
	$(GENERATE_DEPENDS) $< > $@

TEMPLATE_FILES=$(wildcard *.tmpl)
HTML_FILES=$(TEMPLATE_FILES:.tmpl=.html)
html: $(HTML_FILES)

*.html: $(wildcard templates/*.tmpl)
minimization.html: $(wildcard minimization/*/*/*.dat)

.PHONY: clean html
clean:
	rm *.html
