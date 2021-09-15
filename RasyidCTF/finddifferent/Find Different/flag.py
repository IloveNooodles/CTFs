#!/usr/bin/env python2
import sys

apple = open('apple.txt', 'r').read()
coconut = open('coconut.txt', 'r').read()

for i in range(len(apple)):
  if apple[i] != coconut[i]:
    sys.stdout.write(apple[i])
