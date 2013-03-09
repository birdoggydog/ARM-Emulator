.text


  .global main
  b main

main:
   mov r0, #1
   mov r1, #1
   smull r3, r0, r1
   smull r2, r1, r3




.end