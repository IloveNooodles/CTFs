#!/usr/bin/env python3
import re

restricted = '!"#$%&\'+,-/\\;<>?@*^`|()~0123456789'
code = input('>>> ')

assert (code.count('_') < 30)
assert (len(code) < 150)

if not re.findall('[%s]' % re.escape(restricted), code):
    try:
        eval(code, {'__builtins__': None, '_': {}.__class__.__subclasses__()})
    except:
        pass