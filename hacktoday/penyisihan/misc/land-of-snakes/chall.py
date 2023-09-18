#!/usr/bin/env python3
import string as STRING
from infos import HEADER_TEXT, MORE_INFO # ignore this. it's not important

BLACKLISTED_CHARACTERS = "!\"#$%&',.;<>?@[\]^_`{|}~" + STRING.whitespace
BLACKLISTED_WORDS = 'breakpoint', 'compile', 'eval', 'exec', 'input', 'print', 'system'
MORE_INFORMATION = "help", "copyright", "credits", "license", "help()", "copyright()", "credits()", "license()"
IS_NOT_SAFE = False

print(HEADER_TEXT)
while 1:
    cal = input(">>> ").strip()
    if cal in MORE_INFORMATION:
      MORE_INFO(cal)
      continue
    assert len(cal) <= 20
    if not cal: continue

    for c in cal:
        if ord(c) > 1 << 7:
            IS_NOT_SAFE = True
        if c in BLACKLISTED_CHARACTERS:
            IS_NOT_SAFE = True

    for w in BLACKLISTED_WORDS:
        if w in cal.lower():
            IS_NOT_SAFE = True

    if IS_NOT_SAFE:
        print("Forbidden char or word found! Exiting...")
        exit(1)

    try:
        ans = eval(cal)
        assert type(ans) == float or type(ans) == int, "galat."
        print(ans)
    except Exception as e:
        print(e)
        exit(1)
