.text

_start: .global start
	.global main

	b main

main:

	mov r0, #0x1
	mov r1, #0x0
	and r3,r0,r1
	.end

