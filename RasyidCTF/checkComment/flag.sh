#!/bin/bash

exiftool kepiting.jpg | grep -oE CTFR{.*}
