"""
from wixed import *
p = Process(['python', 'chatty.py'], buffer=B)
"""

count = 0
for _ in range(10000):
    print '.',
    count += 1
    if count % 50 == 0:
        print
