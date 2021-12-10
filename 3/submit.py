#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE
from itertools import product

LD_LIBRARY_PATH = os.environ['LD_LIBRARY_PATH']

def mkdirs(*ds):
    for d in ds:
        if not os.path.isdir(d):
            os.makedirs(d)

cwd = os.getcwd()
mkdirs('condor')
os.chdir('condor')

for args in product(
    [32,64,128],
    [8,16],
    [8,16]
):
    args = [ str(x) for x in args ]
    name = '_'.join(args)
    print(name)
    with open(f'{name}.sh','w') as f:
        f.write(f'''\
#!/bin/bash
export LD_LIBRARY_PATH={LD_LIBRARY_PATH}
cd '{cwd}'
./test.py {' '.join(args)}
''')
    os.chmod(f'{name}.sh',0o775)

    p = Popen(
        ('condor_submit','-'),
        stdin=PIPE, stdout=PIPE
    )
    p.stdin.write(f'''\
Universe   = vanilla
Executable = {name}.sh
Output     = {name}.out
Error      = {name}.err
Log        = {name}.log
getenv = True
Queue
'''.encode())
    p.communicate()
    p.stdin.close()
