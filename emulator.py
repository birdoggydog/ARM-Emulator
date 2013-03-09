

## ARM7 Emulator 
## by Nathaniel Waggoner
## Released under open source lisense,
## Order of operations:
import time, BarrellShifter, Instructions, elf
import sys
## initializiation
def condition_passed(cond,register):
	PC = 15
	if cond == extract_field(register[PC],31,28):
		return True
	else:
		return False
	
def regInit():
	global mode, usr, syst,svc,abt,und,irq,fiq, abtRegister, usrRegister, svcRegister, fiqRegister,irqRegister,undRegister,systRegister 
	usrRegister = [0 for i in range(31)]
	abtRegister = [0 for i in range(31)]
	systRegister = [0 for i in range(31)]
	fiqRegister = [0 for i in range(31)]
	svcRegister = [0 for i in range(31)]
	irqRegister = [0 for i in range(31)]
	undRegister = [0 for i in range(31)]
	register = [0 for i in range(31)]
	#register[13] = 0x03007f00
	#register[14] = 0x0
	#register[15] = 0x08000004
	#register[16] = 0x0000005f
	return register	

	


def readFile():
	
	counter = 0
	Memory = {}
	theFile = sys.stdin.readlines()
	for line in theFile:
		

		for word in line:
			
			##if hex(ord(word)) not in Memory.keys():
			Memory[hex(counter+0x8054)] = int(ord(word))	 #+0x8000000)
			counter = counter+1
	print(Memory)
	return Memory

def fetch(Memory, register):
	#print(register)
	#print(Memory)
	mem_loc = register[PC]
	mem_loc = hex(mem_loc)
	
	instruction = Memory[mem_loc]
	instruction = instruction + (Memory[hex(int(mem_loc,16)+1)] << 8)
	instruction = instruction + (Memory[hex(int(mem_loc,16)+2)] << 16)
	instruction = instruction + (Memory[hex(int(mem_loc,16)+3)] << 24)

	return instruction
## exception handling
def handleException(word,inst,addMode):
	print("Exception!",inst)
	pass

def setMode(curMode,newMode,register):
	
	global mode, usr, syst,svc,abt,und,irq,fiq, abtRegister, usrRegister, svcRegister, fiqRegister,irqRegister,undRegister,systRegister 
	if newMode == usr:
	
		if curMode != fiq and curMode != syst:

			for i in range(14):
				usrRegister[i] = register[i]
			
		elif curMode == fiq:
			for i in range(8):
				usrRegister[i] = register[i]
		
		else:
			usrRegister = register						
				
		usrRegister[PC] = register[PC]
		usrRegister[CPSR] = register[CPSR]
		register = usrRegister
		
		mode = usr
	
	elif newMode == abt:
		if curMode != fiq:
			for i in range(13):
		
				abtRegister[i] = register[i]
				
		else:
			for i in range(8):
				abtRegister[i] = register[i]	

		abtRegister[PC] = register[PC]
		abtRegister[CPSR] = register[CPSR]
		register = abtRegister	
		mode = abt	
		## 13 and 14 are special and 		
	# fiq	
	elif newMode == fiq:
		## 8-14, and SPSR are special	
		for i in range(8):
			fiqRegister = register[i]
		fiqRegister[PC] = register[PC]
		fiqRegister[CPSR] = register[CPSR]	
		register = fiqRegister
		mode = fiq
	elif newMode == svc:
		if curMode != fiq:
			for i in range(13):
		
				svcRegister[i] = register[i]
				
		else:
			for i in range(8):
				svcRegister[i] = register[i]	

		svcRegister[PC] = register[PC]
		svcRegister[CPSR] = register[CPSR]
		register = svcRegister
		mode = svc
	elif newMode == irq:

		## 13 and 14 are special and SPSR
		if curMode != fiq:
			for i in range(13):
		
				irqRegister[i] = register[i]
				
		else:
			for i in range(8):
				irqRegister[i] = register[i]
		irqRegister[PC] = register[PC]
		irqRegister[CPSR] = register[CPSR]
		register = irqRegister
		mode = irq

	elif newMode == und:
		if curMode != fiq:
			for i in range(13):
		
				undRegister[i] = register[i]
				
		else:
			for i in range(8):
				undRegister[i] = register[i]
		undRegister[PC] = register[PC]
		undRegister[CPSR] = register[CPSR]
		## 13 and 14 are special and SPSR
		register = undRegister
		mode = und
	elif newMode == syst:
		## 13 and 14 are special and SPSR
		if curMode != fiq:
			for i in range(13):
		
				systRegister[i] = register[i]
				
		else:
			for i in range(8):
				systRegister[i] = register[i]
		systRegister[PC]= register[PC]
		systRegister[CPSR] = register[CPSR]
		register = systRegister
		mode = syst

	return register

## usefull shit - sign Extension, find bit, extract field, etc...
	
	
		
def signExtend(num, msb, size):
	
	if extract_field(num, msb, msb) == 1:
		numberOfOnes = 32-size
		for i in range(numberOfOnes):
			num = (1<< (size+i))+ num
		return num
	else:
		return num
	

def carryFrom(value):
	if value > 2**32 != 0:
		return 1
	else:
		return 0
def overflowFrom(value, operand):
	if extract_field(value,32,32) != extract_field(operand,32,32):
		return 1
	else:
		return 0
def setMemory(Memory, value, numLocs):
	pass
	
	
def findBit(word,bit):
	i = 31
	while i >= 0:
		if extractBit(word,i,i) == bit:
			return i
	return i

#def do_data_proc(word,addMode,inst,register):
	#shifter_operand, shifter_carry_out,register = data_shift_opp(addMode,word,register)	
	#if inst == ADD:
def setInstString(inst):
	insts = {1:'ADC',2:'ADD',3:'AND',4:'BIC',5:'CMN',6:'CMP',7:'EOR',8:'MOV',9:'MVN',10:'ORR',11:'RSB',12:'RSC',
						13:'SBC',14:'SUB',15:'TEQ',16:'TST',
						17:'MRS',18:'MSR',19:'BX',20:'CLZ',21:'BLX2',22:'BLX1',48:'BBL',
						23:'MLA',24:'MUL',25:'SMLAL',26:'SMULL',27:'UMLAL',28:'UMULL',
						29:'LDM1',30:'LDM2',31:'LDM3',32:'STM1',33:'STM2',
						34:'LDR',35:'LDRB',36:'LDRBT',37:'LDRH',38:'LDRSB',
						39:'LDRSH',40:'LDRT',41:'STR',42:'STRB',43:'STRBT',44:'STRH',45:'STRT',
						96:'UND',97:'SWI'}
	return insts[inst]

def main():
	
	global mode, usr, syst,svc,abt,und,irq,fiq, abtRegister, usrRegister, svcRegister, fiqRegister,irqRegister,undRegister,systRegister 

	global ADC, ADD, AND, BIC, CMN, CMP, EOR, MOV, MVN,ORR, RSB, RSC, SBC, SUB, TEQ, TST, ADC, ADD, AND, BIC, CMN, CMP, EOR, MOV, MVN,ORR, RSB, RSC, SBC, SUB, TEQ, TST,COND
	global MRS, MSR , BX, CLZ, BLX2, BLX1,LDR, LDRB
	global LDRBT,LDRH,LDRSB,LDRSH,LDRT,STR,STRB,STRBT,STRH,STRTMLA,MUL,SMLAL,SMULL,UMLAL,UMULL, LDM1, LDM2, LDM3, STM1, STM2 
	global LR,PC,CPSR,SPSR
	addMode = 0
	
	usr = 0
	syst = 1
	svc = 2
	abt = 3
	und = 4
	irq = 5
	fiq = 6
	mode = usr
	LR = 14
	PC = 15     
	CPSR = 16
	SPSR = 17	

	## will add ability to pass in file name as arguement.	
	#filename = 'code/template.machine'
	#filename = 'code/instTests/adc/adc.test'
	# inits our regs	
	register = regInit()
	# inits our memory
	
	# sets the registers up
	register = setMode(mode, usr, register)
	# ganks a binary, converts to hex

	#g = g[0].strip("\n")
	#	print()
	#	print(g)
	
	Memory, register[PC] = elf.loadfile(sys.stdin.readlines()[0].strip("\n"))

	#print(hex(entry))
	#print(Memory)

	ADC, ADD, AND, BIC, CMN, CMP, EOR, MOV, MVN,ORR, RSB, RSC, SBC, SUB, TEQ, TST = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
			# Misc Insts, Branching.

	MRS, MSR , BX, CLZ, BLX2, BLX1, BBL = 17,18,19,20,21,22,48
			# Multiplies:

	MLA,MUL,SMLAL,SMULL,UMLAL,UMULL = 23,24,25,26,27,28
			## load/store mults:
	
	LDM1, LDM2, LDM3, STM1, STM2 = 29,30,31,32,33
			# extra load/store instructions:
	
	LDR, LDRB, LDRBT,LDRH,LDRSB,LDRSH,LDRT,STR,STRB,STRBT,STRH,STRT= 34,35,36,37,38,39,40,41,42,43,44,45
	DP32BitImmediate = 0
	DPImmediateShift= 1 
	DPRegShift = 2
	MLSImmOffIndex = 3
	MLSRegOffIndex = 4
	LSImmOffIndex = 5
	LSRegOffIndex = 6
	LSScaleRegOffIndex = 7		
	LSMultiple = 8
	UND = 96
	IRREL = 10
	UNPRED = 99
	BKPT = 98
	SWI = 97
	PC = 15
	CPSR = 16
	SPSR = 17
	COND = 0
	#barrelShifter = BarrellShifter()
	#register[PC] = 0x8054
	while True:  # represents the main loop
		
		for i in range(16):
			print("R[{0}] :".format(i),hex(register[i]))
		word = fetch(Memory, register)

		addMode = BarrellShifter.determineMode(word)
		inst = Instructions.parseInstruction(word)
		
		register[PC] = register[PC] +4
		instStr = setInstString(inst)
		if inst == BKPT or inst == SWI:
			handleException(word,inst,addMode)

		else:
			if addMode == DP32BitImmediate or addMode == DPImmediateShift or addMode == DPRegShift:
				shifter_operand, shifter_carry_out, register = BarrellShifter.do_data_proc(word,addMode,inst,register)
				register = Instructions.do_dp(shifter_operand,shifter_carry_out,register,inst,word)
			
			elif addMode == MLSImmOffIndex or addMode == MLSRegOffIndex:
				address,register = BarrellShifter.do_misc_l_s(word,addMode,inst,register)
				register, Memory = Instructions.do_LS(address,Memory,register,inst,word)

			elif addMode == LSMultiple:
				start_address,end_address,register = BarrellShifter.do_l_s_mult(word,addMode,inst,register)
				Memory, register = Instructions.do_LSM(start_address,end_address,Memory,register,inst,word)
			
			elif addMode == LSImmOffIndex or addMode == LSRegOffIndex or addMode == LSScaleRegOffIndex:
				address, register = BarrellShifter.do_l_s(word,addMode,inst,register)
				register, Memory = Instructions.do_LS(address,Memory,register,inst,word)
			elif inst >22 and inst <29:
				register =  Instructions.do_multiplies(Memory,register,word,inst,addMode)
			else: 
				register = Instructions.do_misc(Memory,register,word,inst,addMode)
			print("Word: ", bin(word),". Add Mode: ", addMode, "Inst: ", instStr)
main()
