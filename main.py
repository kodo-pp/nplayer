#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess as sp
import sys
import os

def set_tty_mode(mode: str):
    if not os.isatty(0):
        return
    if mode not in ['raw', 'cooked', 'sane']:
        raise ValueError('terminal mode "{}" is not supported'.format(mode))
    if sp.call(['/usr/bin/env', 'stty', mode]) != 0:
        raise OSError('failed to set terminal mode to "{}"'.format(mode))

def tty_tune(tune: list):
    if not os.isatty(0):
        return
    for i in tune:
        if sp.call(['/usr/bin/env', 'stty', i]) != 0:
            raise OSError('failed to set terminal mode to "{}"'.format(i))

def ctrl_key(key: str) -> str:
    if key not in 'QWERTYUIOPASDFGHJKLZXCVBNM':
        raise ValueError('ctrl_key() is defined only for latin capital letters')
    return chr(ord(key) - ord('A') + 1)

def is_printable(key: str) -> bool:
    return ord(key) in range(32, 127)   # ASCII DEL (127) not included

fb1 = 30
fb2 = 18
fq1 = 1
fq2 = 0.75

def gen_freq(freq: float, duration: int):
    sp.call('./gen_freq.py {} {} | aplay 2>/dev/null &'.format(freq, duration), shell=True)

def get_note(char: str) -> tuple:
    if ord('A') <= ord(char) <= ord('Z'):
        return chr(ord(char) - ord('A') + ord('a')), 6000
    elif ord('a') <= ord(char) <= ord('z'):
        return char, 2000
    else:
        return None, None

def play(_char: str) -> bool:
    print('Playing: {}'.format(_char), end='\r\n')
    char, duration = get_note(_char)
    if char is None:
        return False
    freq_arr = list("qawsedrftgyhujikolp;[']\\")
    if char not in freq_arr:
        return False
    freq_map = {v: k for k, v in enumerate(freq_arr)}
    #print('Playing freq {} for {} ticks'.format(freq_map[char], duration), end='\r\n', file=sys.stderr)
    gen_freq(float(fb1 - freq_map[char] * fq1), duration)
    return True

def main():
    set_tty_mode('raw')
    tty_tune(['-echo'])

    while True:
        ch = sys.stdin.read(1)
        if (len(ch) < 1):
            break
        if ch == ctrl_key('C'):
            print('Exiting', end='\r\n', file=sys.stderr)
            return 0
        elif ch == chr(9):
            global fb1, fb2, fq1, fq2
            fb1, fb2 = fb2, fb1
            fq1, fq2 = fq2, fq1
            if fb1 == 30:
                print("\x1b[1;32mChanging mode: Normal\x1b[0m", end='\r\n')
            else:
                print("\x1b[1;31mChanging mode: HiFreq\x1b[0m", end='\r\n')
            continue
        play(ch)

def on_exit():
    set_tty_mode('sane')

if __name__ == '__main__':
    exit_status = 0
    try:
        exit_status = main()
    finally:
        on_exit()
    exit(exit_status)
