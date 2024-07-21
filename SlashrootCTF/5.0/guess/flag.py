#!/usr/bin/env python3

a = "Smcplwih|<qx=`~c#N` bJ\'$+.g\""
for i in range(len(a)):
	print( chr(i^ord(a[i])), end = '')

