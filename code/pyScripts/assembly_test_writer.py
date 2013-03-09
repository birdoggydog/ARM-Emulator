def main():
	
	import sys

	comds = ['adc', 'bic', 'eor', ' ldr', '', 'ldrsb', 'lmd3', 'mul', 'rsb', 'smlal', 'stm2', 'strbt', 'sub', 'umlal', 'add', 'cmn', 'ldm1', 'ldrb', ' ldrsh', 'mla', ' mvn', 'rsc', 'smull', 'str', ' strh', ' teq', 'umull'
'and', 'cmp', 'ldm2', 'ldrbt', 'ldrt', ' mov', ' orr', 'sbc', 'stm1', ' strb', 'strt', ' tst']

	
	for i in comds:
		filename = "{0}.s".format(i)
		print(filename)
		theFile = open(filename,"w")
		
		theFile.write(".text\n")
		theFile.write("\n")
		theFile.write("\n")
		theFile.write("  .global main\n")
		theFile.write("  b main\n")
		theFile.write("\n")
		theFile.write("main:\n")
		theFile.write("   mov r0, #1\n")
		theFile.write("   mov r1, #1\n")
		theFile.write("   {0} r3, r0, r1\n".format(i))
		theFile.write("   {0} r2, r1, r3\n".format(i))
		theFile.write("\n")
		theFile.write("\n")
		theFile.write("\n")
		theFile.write("\n")
		theFile.write(".end")
		theFile.flush()
		theFile.close()

	
main()

