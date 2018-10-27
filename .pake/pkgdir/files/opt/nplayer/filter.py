#!/usr/bin/env python3
import time
import sys

def putc(c):
    print(c, end='')
    sys.stdout.flush()

tk = 0.25
nlk = 4
sk = 2
uk = 2
dk = 1

with open(sys.argv[1]) as f:
    s = f.read()

for i in s:
    if i == '!':
        putc('\t')
    elif i == '0':
        tk = 0.25
    elif i == '-':
        tk -= 0.02
    elif i == '+':
        tk += 0.02
    elif i == ' ':
        time.sleep(tk * sk)
    elif i == '\n':
        time.sleep(tk * nlk)
    elif i.upper() == i:
        putc(i)
        time.sleep(tk * uk)
    else:
        putc(i)
        time.sleep(tk * dk)
