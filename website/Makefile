.SUFFIXES: 
.SUFFIXES: .tmpl .html
RENDER = ../bin/render.py
GENERATE_DEPENDS = ../bin/render.py -d 

%.html:%.tmpl
	$(RENDER) $< > $@

%.d:%.tmpl
	$(GENERATE_DEPENDS) $< > $@

TEMPLATE_FILES=$(wildcard *.tmpl)
HTML_FILES=$(TEMPLATE_FILES:.tmpl=.html)
DEPENDS = $(HTML_FILES:.html=.d)
html: $(DEPENDS) $(HTML_FILES)
sinclude $(DEPENDS)

.PHONY: clean html
clean:
	rm *.html *.d
