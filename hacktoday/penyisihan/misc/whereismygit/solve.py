import os
import subprocess

f = open("gitlog.txt")
flag = b""
os.chdir("./where-is-my-git")
for idx, line in enumerate(f.readlines()):
  if idx % 2 == 1 or idx == 126:
    continue

  info = line.split(" ")
  filename = info[-1].strip()
  commitId = info[1]

  print(commitId, filename)

  subprocess.run(["git", "checkout", commitId])
  res = subprocess.check_output(["cat", filename])
  flag += res

print(flag)