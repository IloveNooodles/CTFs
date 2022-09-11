
.def temp = r16
.def EW = r23 
.def PB = r24 
.def A  = r25
.def count = r21

MAIN:
	ldi temp, low(0x025f)
	ldi temp, high(0x025f)
	out 0x3e, temp

rjmp INIT1

EXIT:
	rjmp EXIT

DATA1:
	ldi ZH,high(2*key)
	ldi ZL,low(2*key)
	ret

DATA2:
	ldi ZH,high(2*MAIN)
	ldi ZL,low(2*MAIN)
	ret

INIT1:
	ser temp
	out 0x1a,temp
	out 0x17,temp
	cbi 0x1b,1
	ldi PB,0x38 
	out 0x18,PB
	sbi 0x1b,0 
	cbi 0x1b,0 
	cbi 0x1b,1 
	ldi PB,$0E 
	out 0x18,PB
	sbi 0x1b,0 
	cbi 0x1b,0 
	cbi 0x1b,1 
	ldi PB,$01 
	out 0x18,PB
	sbi 0x1b,0 
	cbi 0x1b,0 
	cbi 0x1b,1 
	ldi PB,$06 
	out 0x18,PB
	sbi 0x1b,0 
	cbi 0x1b,0 

LOAD1: 
	cpi count, 16 
	breq PAUSE 
	rcall DATA1
	add ZL, count
	lpm 
	mov A, r0 
	rcall DATA2
	add ZL, count
	lpm 
	add A, r0
	sbi 0x1b,1 
	out 0x18, A
	sbi 0x1b,0 
	cbi 0x1b,0 
	inc count
	rjmp LOAD1

PAUSE:
	cbi 0x1b,1 
	ldi PB, $C0 
	out 0x18,PB
	sbi 0x1b,0 
	cbi 0x1b,0 

LOAD2: 
	cpi count, 32
	breq EXIT
	rcall DATA1
	add ZL, count
	lpm 
	mov A, r0 
	rcall DATA2
	add ZL, count
	lpm 
	add A, r0
	sbi 0x1b,1 
	out 0x18, A
	sbi 0x1b,0 
	cbi 0x1b,0 
	inc count
	rjmp LOAD2

key:
