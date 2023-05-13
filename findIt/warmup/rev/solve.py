import string
import sys
from subprocess import PIPE, STDOUT, Popen

cmd = (
    "sudo /usr/lib/linux-tools/5.15.0-71-generic/perf stat -x, -e instructions:u "
    + sys.argv[1]
    + " 1>/dev/null"
)
key = ""

while True:
    maximum = 0, 0
    for i in string.printable:
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        stdout, _ = p.communicate(input=b"%s\n" % (key + i))
        nb_instructions = int(stdout.split(",")[0])
        if nb_instructions > maximum[0]:
            maximum = nb_instructions, i
    key += maximum[1]
    print(key)
