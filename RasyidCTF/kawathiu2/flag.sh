#!/bin/bash

cat flag.txt | tr -d " " | tr -d "\n" | grep -oE "CTFR{.*}"
