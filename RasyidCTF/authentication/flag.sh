#!/bin/bash

curl -s --location --request POST 'https://web.ctf.rasyidmf.com/chal9/?flag=d69faaea338ac0073602593fc9416f76' | grep -oE CTFR{.*}
