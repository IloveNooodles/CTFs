#!/bin/bash

strings First.NET.exe | grep -oE CTFR{.*}
