.text


  .global main
  b main

main:
   mov r0, #1
   mov r1, #1
   ldrb r3, r0, r1
   ldrb r2, r1, r3




.end