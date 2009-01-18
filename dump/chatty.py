"""
from wixed import *
p = Process(['python', 'chatty.py'], buffer=B)
"""
import sys
count = 0
char = 'A'
if len(sys.argv) > 1:
    if sys.argv[1] == 'dots':
        char = '. '
if not char == '. ':
    print '"""'
for _ in range(100000):
    sys.stdout.write(char)
    count += 1
    if count % 50 == 0:
        print
if not char == '. ':
    print '"""'
