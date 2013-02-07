#!/usr/bin/env python
from jinja2 import Environment, FileSystemLoader
from jinja2.meta import find_referenced_templates
from sys import argv, exit
from os.path import dirname, basename, isdir
from os import listdir
from os.path import isfile, join

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


def load_benchmarks(suite):
    benchmarks = {}
    index = 0
    for benchmark in listdir(suite):
        benchmark_path = join(suite, benchmark)
        if isfile(benchmark_path) or benchmark[0] == '.':
            continue
        
        benchmarks[benchmark] = []
        for entry_name in listdir(join(suite, benchmark)):
            run_path = join(suite, benchmark, entry_name)
            if isfile(run_path) or entry_name[0] == '.':
                continue

            benchmark_dat = join(run_path, 'benchmark.dat')
            if not isfile(benchmark_dat):
                continue

            data = {}
            comments_txt = join(run_path, 'comments.txt')
            if isfile(comments_txt):
                data['comments'] = open(comments_txt).read()


            input_files = join(run_path, entry_name+'.tgz')
            if isfile(input_files):
                data['input_files'] = input_files

            data['entry_name'] = entry_name
            data['id'] = '%s-%i' % (benchmark,index)
            index += 1
            f = open(benchmark_dat)
            for line in f:
                fields = line.strip().split()
                key = fields[0]
                value = ' '.join(fields[1:])
                data[key] = value

                try:
                    data[key] = float(value)
                except:
                    pass

            if 'code_file' in data and not isfile(join('codes',data['code_file'])):
                del data['code_file']

            benchmarks[benchmark].append(data)
            
        if len(benchmarks[benchmark]) == 0:
            del benchmarks[benchmark]
    return benchmarks

if len(argv) < 2:
    usage()
    exit(1)
if '-h' in argv:
    usage()
    exit(0)

template_path = argv[1]
env = Environment(loader=FileSystemLoader(dirname(template_path)))
template = env.get_template(basename(template_path))

suite_folder = template_path[:template_path.rfind('.')]
if isdir(suite_folder):
    benchmarks = load_benchmarks(suite_folder)
else:
    benchmarks = None
print template.render(benchmarks=benchmarks)
