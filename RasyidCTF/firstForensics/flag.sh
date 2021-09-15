#!/bin/bash
strings 2.jpg | grep -oE CTFR{.*}
