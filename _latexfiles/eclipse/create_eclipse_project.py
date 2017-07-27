#!/usr/bin/python
import os
import os.path
import re
import sys

scriptroot = os.path.dirname(sys.argv[0])

searchroot = '../..'
if len(sys.argv) > 1:
    searchroot = sys.argv[1]

watchOutList = []
for root, dirs, files in os.walk(searchroot):
    for r in ['.svn', '_layouts', '_old']:
        if r in dirs:
            dirs.remove(r)
    n = 0
    for f in files:
        if f == 'example.tex':
            continue
        
        m = re.match(r'^(.*)\.tex$', f)
        if m:
            txt = file(os.path.join(root, f)).read()
            if re.search(r'\\newcommand\{\\mypath', txt, re.MULTILINE):
                if n == 0:
                    print(root)
                else:
                    watchOutList += [root]
                print(f)
                for p in ['.project', '.texlipse', 'Makefile', 'Makefile.in']:
                    ptxt = file(os.path.join(scriptroot, '%s.tpl' % p)).read()
                    ptxt = ptxt % { 
                        'name': m.group(1), 
                        'projname': root.replace('.\\', '').replace('\\', '_'), 
                        }
                    file(os.path.join(root, p), 'w').write(ptxt)
                n = n + 1

print(watchOutList)
