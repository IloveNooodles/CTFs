
minato_aqua:     file format elf64-x86-64


Disassembly of section .init:

0000000000401000 <.init>:
  401000:	f3 0f 1e fa          	endbr64 
  401004:	48 83 ec 08          	sub    rsp,0x8
  401008:	48 8b 05 e9 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fe9]        # 403ff8 <setvbuf@plt+0x2f58>
  40100f:	48 85 c0             	test   rax,rax
  401012:	74 02                	je     401016 <system@plt-0x5a>
  401014:	ff d0                	call   rax
  401016:	48 83 c4 08          	add    rsp,0x8
  40101a:	c3                   	ret    

Disassembly of section .plt:

0000000000401020 <.plt>:
  401020:	ff 35 e2 2f 00 00    	push   QWORD PTR [rip+0x2fe2]        # 404008 <setvbuf@plt+0x2f68>
  401026:	f2 ff 25 e3 2f 00 00 	bnd jmp QWORD PTR [rip+0x2fe3]        # 404010 <setvbuf@plt+0x2f70>
  40102d:	0f 1f 00             	nop    DWORD PTR [rax]
  401030:	f3 0f 1e fa          	endbr64 
  401034:	68 00 00 00 00       	push   0x0
  401039:	f2 e9 e1 ff ff ff    	bnd jmp 401020 <system@plt-0x50>
  40103f:	90                   	nop
  401040:	f3 0f 1e fa          	endbr64 
  401044:	68 01 00 00 00       	push   0x1
  401049:	f2 e9 d1 ff ff ff    	bnd jmp 401020 <system@plt-0x50>
  40104f:	90                   	nop
  401050:	f3 0f 1e fa          	endbr64 
  401054:	68 02 00 00 00       	push   0x2
  401059:	f2 e9 c1 ff ff ff    	bnd jmp 401020 <system@plt-0x50>
  40105f:	90                   	nop
  401060:	f3 0f 1e fa          	endbr64 
  401064:	68 03 00 00 00       	push   0x3
  401069:	f2 e9 b1 ff ff ff    	bnd jmp 401020 <system@plt-0x50>
  40106f:	90                   	nop

Disassembly of section .plt.sec:

0000000000401070 <system@plt>:
  401070:	f3 0f 1e fa          	endbr64 
  401074:	f2 ff 25 9d 2f 00 00 	bnd jmp QWORD PTR [rip+0x2f9d]        # 404018 <setvbuf@plt+0x2f78>
  40107b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000401080 <printf@plt>:
  401080:	f3 0f 1e fa          	endbr64 
  401084:	f2 ff 25 95 2f 00 00 	bnd jmp QWORD PTR [rip+0x2f95]        # 404020 <setvbuf@plt+0x2f80>
  40108b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

0000000000401090 <gets@plt>:
  401090:	f3 0f 1e fa          	endbr64 
  401094:	f2 ff 25 8d 2f 00 00 	bnd jmp QWORD PTR [rip+0x2f8d]        # 404028 <setvbuf@plt+0x2f88>
  40109b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

00000000004010a0 <setvbuf@plt>:
  4010a0:	f3 0f 1e fa          	endbr64 
  4010a4:	f2 ff 25 85 2f 00 00 	bnd jmp QWORD PTR [rip+0x2f85]        # 404030 <setvbuf@plt+0x2f90>
  4010ab:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

00000000004010b0 <.text>:
  4010b0:	f3 0f 1e fa          	endbr64 
  4010b4:	31 ed                	xor    ebp,ebp
  4010b6:	49 89 d1             	mov    r9,rdx
  4010b9:	5e                   	pop    rsi
  4010ba:	48 89 e2             	mov    rdx,rsp
  4010bd:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
  4010c1:	50                   	push   rax
  4010c2:	54                   	push   rsp
  4010c3:	45 31 c0             	xor    r8d,r8d
  4010c6:	31 c9                	xor    ecx,ecx
  4010c8:	48 c7 c7 12 12 40 00 	mov    rdi,0x401212
  4010cf:	ff 15 1b 2f 00 00    	call   QWORD PTR [rip+0x2f1b]        # 403ff0 <setvbuf@plt+0x2f50>
  4010d5:	f4                   	hlt    
  4010d6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  4010dd:	00 00 00 
  4010e0:	f3 0f 1e fa          	endbr64 
  4010e4:	c3                   	ret    
  4010e5:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  4010ec:	00 00 00 
  4010ef:	90                   	nop
  4010f0:	b8 48 40 40 00       	mov    eax,0x404048
  4010f5:	48 3d 48 40 40 00    	cmp    rax,0x404048
  4010fb:	74 13                	je     401110 <setvbuf@plt+0x70>
  4010fd:	b8 00 00 00 00       	mov    eax,0x0
  401102:	48 85 c0             	test   rax,rax
  401105:	74 09                	je     401110 <setvbuf@plt+0x70>
  401107:	bf 48 40 40 00       	mov    edi,0x404048
  40110c:	ff e0                	jmp    rax
  40110e:	66 90                	xchg   ax,ax
  401110:	c3                   	ret    
  401111:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  401118:	00 00 00 00 
  40111c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  401120:	be 48 40 40 00       	mov    esi,0x404048
  401125:	48 81 ee 48 40 40 00 	sub    rsi,0x404048
  40112c:	48 89 f0             	mov    rax,rsi
  40112f:	48 c1 ee 3f          	shr    rsi,0x3f
  401133:	48 c1 f8 03          	sar    rax,0x3
  401137:	48 01 c6             	add    rsi,rax
  40113a:	48 d1 fe             	sar    rsi,1
  40113d:	74 11                	je     401150 <setvbuf@plt+0xb0>
  40113f:	b8 00 00 00 00       	mov    eax,0x0
  401144:	48 85 c0             	test   rax,rax
  401147:	74 07                	je     401150 <setvbuf@plt+0xb0>
  401149:	bf 48 40 40 00       	mov    edi,0x404048
  40114e:	ff e0                	jmp    rax
  401150:	c3                   	ret    
  401151:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  401158:	00 00 00 00 
  40115c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  401160:	f3 0f 1e fa          	endbr64 
  401164:	80 3d e5 2e 00 00 00 	cmp    BYTE PTR [rip+0x2ee5],0x0        # 404050 <stdout@GLIBC_2.2.5+0x8>
  40116b:	75 13                	jne    401180 <setvbuf@plt+0xe0>
  40116d:	55                   	push   rbp
  40116e:	48 89 e5             	mov    rbp,rsp
  401171:	e8 7a ff ff ff       	call   4010f0 <setvbuf@plt+0x50>
  401176:	c6 05 d3 2e 00 00 01 	mov    BYTE PTR [rip+0x2ed3],0x1        # 404050 <stdout@GLIBC_2.2.5+0x8>
  40117d:	5d                   	pop    rbp
  40117e:	c3                   	ret    
  40117f:	90                   	nop
  401180:	c3                   	ret    
  401181:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  401188:	00 00 00 00 
  40118c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  401190:	f3 0f 1e fa          	endbr64 
  401194:	eb 8a                	jmp    401120 <setvbuf@plt+0x80>
  401196:	f3 0f 1e fa          	endbr64 
  40119a:	55                   	push   rbp
  40119b:	48 89 e5             	mov    rbp,rsp
  40119e:	48 8b 05 a3 2e 00 00 	mov    rax,QWORD PTR [rip+0x2ea3]        # 404048 <stdout@GLIBC_2.2.5>
  4011a5:	b9 00 00 00 00       	mov    ecx,0x0
  4011aa:	ba 02 00 00 00       	mov    edx,0x2
  4011af:	be 00 00 00 00       	mov    esi,0x0
  4011b4:	48 89 c7             	mov    rdi,rax
  4011b7:	e8 e4 fe ff ff       	call   4010a0 <setvbuf@plt>
  4011bc:	90                   	nop
  4011bd:	5d                   	pop    rbp
  4011be:	c3                   	ret    
  4011bf:	f3 0f 1e fa          	endbr64 
  4011c3:	55                   	push   rbp
  4011c4:	48 89 e5             	mov    rbp,rsp
  4011c7:	48 83 ec 10          	sub    rsp,0x10
  4011cb:	48 89 7d f8          	mov    QWORD PTR [rbp-0x8],rdi
  4011cf:	48 8b 45 f8          	mov    rax,QWORD PTR [rbp-0x8]
  4011d3:	48 89 c7             	mov    rdi,rax
  4011d6:	e8 95 fe ff ff       	call   401070 <system@plt>
  4011db:	90                   	nop
  4011dc:	c9                   	leave  
  4011dd:	c3                   	ret    
  4011de:	f3 0f 1e fa          	endbr64 
  4011e2:	55                   	push   rbp
  4011e3:	48 89 e5             	mov    rbp,rsp
  4011e6:	48 83 ec 20          	sub    rsp,0x20
  4011ea:	48 8d 05 13 0e 00 00 	lea    rax,[rip+0xe13]        # 402004 <setvbuf@plt+0xf64>
  4011f1:	48 89 c7             	mov    rdi,rax
  4011f4:	b8 00 00 00 00       	mov    eax,0x0
  4011f9:	e8 82 fe ff ff       	call   401080 <printf@plt>
  4011fe:	48 8d 45 e0          	lea    rax,[rbp-0x20]
  401202:	48 89 c7             	mov    rdi,rax
  401205:	b8 00 00 00 00       	mov    eax,0x0
  40120a:	e8 81 fe ff ff       	call   401090 <gets@plt>
  40120f:	90                   	nop
  401210:	c9                   	leave  
  401211:	c3                   	ret    
  401212:	f3 0f 1e fa          	endbr64 
  401216:	55                   	push   rbp
  401217:	48 89 e5             	mov    rbp,rsp
  40121a:	48 83 ec 10          	sub    rsp,0x10
  40121e:	89 7d fc             	mov    DWORD PTR [rbp-0x4],edi
  401221:	48 89 75 f0          	mov    QWORD PTR [rbp-0x10],rsi
  401225:	b8 00 00 00 00       	mov    eax,0x0
  40122a:	e8 67 ff ff ff       	call   401196 <setvbuf@plt+0xf6>
  40122f:	b8 00 00 00 00       	mov    eax,0x0
  401234:	e8 a5 ff ff ff       	call   4011de <setvbuf@plt+0x13e>
  401239:	b8 00 00 00 00       	mov    eax,0x0
  40123e:	c9                   	leave  
  40123f:	c3                   	ret    

Disassembly of section .fini:

0000000000401240 <.fini>:
  401240:	f3 0f 1e fa          	endbr64 
  401244:	48 83 ec 08          	sub    rsp,0x8
  401248:	48 83 c4 08          	add    rsp,0x8
  40124c:	c3                   	ret    
