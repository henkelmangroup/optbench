#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
from jinja2.meta import find_referenced_templates
from sys import argv, exit
from os.path import dirname, basename

def get_dependencies(env, path):
    text = env.loader.get_source(env, path)[0]
    ast = env.parse(text)
    tpls = find_referenced_templates(ast)
    deps = []
    for dep in tpls:
        deps.append(dep)
    return list(set(deps))

def usage():
    print 'usage: render.py template'

if len(argv) < 2:
    usage()
    exit(1)
if '-h' in argv:
    usage()
    exit(0)

if '-d' in argv:
    template_path = argv[2]
else:
    template_path = argv[1]
env = Environment(loader=FileSystemLoader(dirname(template_path)))
if '-d' in argv:
    deps = get_dependencies(env, basename(template_path))
    print basename(template_path)[:basename(template_path).rfind('.')]+'.html:\\'
    for dep in deps:
        print dep+' \\'
else:
    template = env.get_template(basename(template_path))
    print template.render()
