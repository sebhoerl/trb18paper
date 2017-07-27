#!/usr/bin/python
import sys
import subprocess
import re
import os

TMPDIR = 'wc'

def _writeWords(words):
    open('mywordcount.tex', 'w').write((r'\newcommand{\mytextwordcount}{%(words)s}%%' % locals()) + '\n')
    
def _printWords(words):
    print(words)
    
def compile(fdir, fname):
    subprocess.call([r'pdflatex',
                     r'-interaction=nonstopmode',
                     r'-output-directory=%s' % TMPDIR,
                     r'%(fname)s' % locals()],
                    cwd=fdir)

    tmpdir = TMPDIR
    subprocess.call([r'bibtex',
                     r'%(tmpdir)s/%(fname)s' % locals()],
                    cwd=fdir)

    subprocess.call([r'pdflatex',
                     r'-interaction=nonstopmode',
                     r'-output-directory=%s' % TMPDIR,
                     r'%(fname)s' % locals()],
                    cwd=fdir)

    subprocess.call([r'pdflatex',
                     r'-interaction=nonstopmode',
                     r'-output-directory=%s' % TMPDIR,
                     r'%(fname)s' % locals()],
                    cwd=fdir)

def countWords(scriptpath, fdir, fname):
    subprocess.call([r'pdflatex',
                     r'-interaction=nonstopmode',
                     r'-output-directory=%s' % TMPDIR,
                     r'\input{%(scriptpath)s/wordcount.inp}'
                      '\edef\wcFileName{%(fname)s}'
                      '\edef\jobname{\wcFileName}'
                      '\input{\wcFileName}' % locals()],
                    cwd=fdir)

    log = open(os.path.join(fdir, os.path.join(TMPDIR, 'wordcount.log')), 'rbU').read()
    countedwords = len(re.findall(r'3\.0863[35].*$', log, re.M))
    exhyphens = len(re.findall(r'3\.08632 -.*$', log, re.M))
    mathbreaks = len(re.findall(r'3\.08633 plus 3\.08633 minus .*$', log, re.M))
    undefwarnings = len(re.findall(r'There were undefined citations', log, re.M))
    return countedwords - exhyphens - mathbreaks, undefwarnings

def run():
    global fdir
    
    from optparse import OptionParser

    parser = OptionParser(usage="usage: %prog [main LaTeX file] [options]",
                          epilog="Writes word count for a LaTeX file into the file mywordcount.tex in the current directory.")

    parser.add_option("-p", "--print", dest="print_", action="store_true", default=False,
                      help="print to stdout instead of writing to mywordcount.tex")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Please specify the name of your LaTeX file as parameter.")
    if options.print_:
        _doWriteWords = _printWords
    else:
        _doWriteWords = lambda x: (_printWords(x), _writeWords(x))

    fname = args[0]
    fname = re.sub('\.tex$', '', fname)
    fdir, fname  = os.path.split(fname)
    if fdir == '':
        fdir = '.'
    
    scriptpath = sys.path[0]
    scriptpath = os.path.relpath(scriptpath)
    scriptpath = os.path.relpath(scriptpath, fdir)
    scriptpath = scriptpath.replace('\\', '/')
    
    _doWriteWords(0)
    
    wcdir = os.path.join(fdir, TMPDIR)
    if not os.path.isdir(wcdir):
        os.mkdir(wcdir)
    
    words, undefwarnings = countWords(scriptpath, fdir, fname)
    if undefwarnings > 0:
        compile(fdir, fname)
        words, _ = countWords(scriptpath, fdir, fname)
    
    _doWriteWords(words)
    
def cleanup():
    for f in ('wordcount.log', 'wordcount.pdf'):
        try:
            os.unlink(os.path.join(fdir, f))
        except:
            pass
            
def main():
    try:
        run()
    finally:
        cleanup()
    
if __name__=='__main__':
    main()

