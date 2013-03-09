.text

_start: .global _start
	.global main


	b main

main:
	mov r0, #1
	mov r1, #1
	adc r3, r0, r1
	adc r2, r1, r3
	
	.end
