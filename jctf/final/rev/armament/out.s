.data
    .align 4
    input: .asciz "JCTF{"
    output: .space 26

.text
.global main
main:
    push {r4-r7, lr}
    ldr r0, =input
    ldr r1, =output
    mov r2, #0
loop:
    ldrb r3, [r0], #1
    cmp r3, #0
    beq done
    and r4, r3, #1
    cmp r4, #1
    subeq r3, r3, #11
    cmp r3, #100
    subgt r3, r3, #10
    lsr r3, r3, #1
    and r4, r2, #1
    cmp r4, #1
    addne r3, r3, #3
    subeq r3, r3, #3
    lsl r3, r3, #1
    strb r3, [r1], #1
    add r2, r2, #1
    b loop
done:
    pop {r4-r7, pc}
