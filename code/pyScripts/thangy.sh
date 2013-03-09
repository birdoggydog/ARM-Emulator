#! /bin/bash

for file in 
do
	arm-linux-gnueabi-as -o "${file}/${file}.o" "${file}/${file}"
	arm-linux-gnuabi-ld -o "${file}/${file}.elf" "${file}/${file}.o" 
done
