#class Instructions():
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
def condition_passed(cond,register):
	N = extract_field(register[CPSR],31,31)
	Z = extract_field(register[CPSR],30,30)
	C = extract_field(register[CPSR],29,29)
	V = extract_field(register[CPSR],28,28)
	#print(cond)
	if cond == 0:
		#equal
		if Z == 1:
			return True
	elif cond == 1:
		#not equal
		if Z == 0:
			return True
	elif cond == 2:
			#Carry set unsigned higher or same
			if C == 1:
				return True
	elif cond == 3:
		# carry clear, unsigned lower
		if C == 0:
			return True
	elif cond == 4:
		# MI Minus/Negative
		if N == 1:
			return True
	elif cond == 5:
		#plus postitove or zero
		if N == 0:
			return True
	elif cond == 6:
		#Overflow
		if V == 1:
			return True
	elif cond == 7:
		#No overflow
		if V == 0:
			return True
	elif cond == 8:
		#unsigned Higher
		if C== 1 and Z == 0:
			return True
	elif cond == 9:
		#Unsigned lower or same
		if C == 0 or Z == 1:
			return True
	elif cond == 10:
		#signed greater than or equal
		if (N == 1 and V ==1) or N == 0 and V == 0:
			return True
	elif cond == 11:
		#signed lessthen
		if (N == 1 and V == 0) or N == 0 and V == 1:
			return True
	elif cond == 12:
		#signed greater than:>
		if Z == o and ((N== 1 and V== 1)or (N == 0 and V == 0)):
			return True
	elif cond == 13:
		#signed less than or equal:
		if Z == 1 or (N == 1 and V == 0) or (N == 0 and V == 1):
			return True
	elif cond == 14:
		#always
		print('AL')
		return True
	else:
		return False
	return False

def set_memory(Memory,address,val,numLocs):
			for i in range(numLocs):
				Memory[address+i] = extract_field(val,i*8+8,i*8) 
			return Memory
def set_bit(num, shift, bit):
	
			mask = num&(~(1<<shift))
			returnVal = (bit<<shift) | num
	
			return returnVal&0xffffffff

def signExtend(num, msb, size):
	
			if extract_field(num, msb, msb) == 1:
				numberOfOnes = 32-size
				for i in range(numberOfOnes):
					num = (1<< (size+i))+ num
				return num
			else:
				return num
	

def fetch_inst(Memory, mem_loc,num):
			#print(register)
			mem_loc = hex(mem_loc)
			instruction = 0
			for i in range(num):
				instruction = instruction + ((Memory[mem_loc+i]) << (8*i))
			#instruction = Memory[mem_loc]
			#instruction = instruction + (Memory[hex(int(mem_loc,16)+1)] << 8)
			#instruction = instruction + (Memory[hex(int(mem_loc,16)+2)] << 16)
			#instruction = instruction + (Memory[hex(int(mem_loc,16)+3)] << 24)

def carry_from(value):
			if value > 2**32 != 0:
				return 1
			else:
				return 0
def overflow_from(value, operand):
			if extract_field(value,32,32) != extract_field(operand,32,32):
				return 1
			else:
				return 0
def do_misc(Memory,register,word,inst,addMode):
		cond = extract_field(word,31,28) 
		L = extract_field(word,31,28) 
		signed_immed24 = extract_field(word,23,0)

		if inst == 48:
			# bbl

			LR = 14
			if condition_passed(cond,register):
				if L == 1:
					register[LR] = register[PC]
				#print(signed_immed24)
				register[PC] = int((register[PC] + (signExtend(signed_immed24,23,24)<<2)+4)& 0xffffffff)
				#print(signExtend(signed_immed24,23,24)<<2)
		elif inst == 96:
			print("undefined")
		else:

			print("well...")
		return register
def do_LSM(start_address,end_address,Memory,register,inst,word):
			#LDM1, LDM2, LDM3, STM1, STM2 = 28,29,30,31,32
			register_list = extract_field(word,15,0)
			
			cond = extract_field(word,31,28)
			if inst == 28:
				if condition_passed(cond,register):
					address = start_address
					for i in range(15): # 0 to 14
						if extract_field(register_list,i,i) == 1:
							register[i] = fetch_inst(Memory,address,4)
							address = address +4
					if extract_field(register_list,15,15) == 1:
						value = fetch_inst(Memory,address,4)
						if version >= 5:
							register[PC] = value&0xfffffffe
							#T bit = value[0]
						else:
							register[PC] = value& 0xfffffffc
						address = address+4
					assert end_address == address-4
			elif inst == 29:
				# ldm2
				if condition_passed(cond,register):
					adress = start_address
					for i in range(15):
						if extract_field(register_list,i,i) == 1:
							register[i] = fetch_inst(Memory,address,4)
							address = address +4
					assert end_address == address-4
			elif inst == 30:
				# LDM 3
				if condition_passed(cond,register):
					address = start_address
					for i in range(15): # 0 to 14
						if extract_field(register_list,i,i) == 1:
							register[i] = fetch_inst(Memory,address,4)
							address = address +4
					register[CPSR] = register[SPSR]
					value = fetch_inst(Memory,address,4)
					if (version == FOURT or version > 5) and T == 1:
						regiister[PC] = value & oxfffffffe
					else:
						register[PC] = value&0xfffffffc
					address = address +4
					assert end_address == address-4
			elif inst == 31:
				# STM
				if condition_passed(cond,register):
					address = start_address
					for i in range(15):
						if extract_field(register_list,i,i) == 1:
							Memory = set_memory(Memory,address,register[i],4)
							address = address+4
						assert end_address == address-4
			elif inst == 32:
				# STM 2
				if condition_passed(cond,register):
					address = start_address
					for i in range(15):
						if extract_field(register_list,i,i) == 1:
							Memory = set_memory(Memory,address,register[i],4)
							address = address+4
						assert end_address == address-4
			return Memory, register
def do_LS(address,Memory,register,inst,word):
			#LDR, LDRB, LDRBT,LDRH,LDRSB,LDRSH,LDRT,STR,STRB,STRBT,STRH,STRT= 33,34,35,36,37,38,39,40,41,42,43,44
			adr_1_0 = extract_field(address,1,0)
			Rd = extract_field(word,15,12)
			adr_0 = extract_field(address,0,0)
			cond = extract_field(word,31,28)
			UNDPREDICTABLE=0
			if inst == 33:
				# LDr
				if adr_1_0 == 0:
					value = fetch_inst(Memory,address,4)
				elif adr_1_0 == 1:
					value = fetch_inst(Memory,address,4) >> 8
				elif adr_1_0 == 2:
					value = fetch_inst(Memory,address,4) >> 16
				elif adr_1_0 == 3:
					value = fetch_inst(Memory,address,4) >> 24
				if Rd == PC:
					if version >= 5:
						register[PC] = value & 0xffffffff
						#T_Bit = extract_field(value,0,0)
					else:
						register[PC] = value & oxfffffffc
				else:
					register[Rd] = int(value)
			elif inst == 34:
				# LDRB
				if condition_passed(cond,register):
					register[Rd] = int(fetch_inst(Memory,addres,1))
			elif inst == 35:
				# LDRBT
				if condition_passed(cond,register):
					register[Rd] = int(fetch_inst(Memory,addres,1))
			elif inst == 36:
				# LDRH
					if condition_passed(cond,register):
						if adr_0 == 0:
							data = fetch_inst(Memory,address,2)
						else:
							data = UNDPREDICTABLE
						register[Rd] = int(data)
			elif inst == 37:
				# LDRSB				
				if condition_passed(cond,register):
					register[Rd] = int(signExtend(data,7,8))
			elif inst == 38:
				# LDRSH
				if condition_passed(cond,register):
					if adr_0 == 0:
						data = fetch_inst(Memory,addres,2)
					else:
						data = UNDPREDICTABLE
					register[Rd] = int(signExtend(data,15,16))
			elif inst == 39:
				# LDRT
				if adr_1_0 == 0:
					register[Rd] = int(fetch_inst(Memory,address,4))
				elif adr_1_0 == 1:
					register[Rd] = int(fetch_inst(Memory,address,4) >> 8)
				elif adr_1_0 == 2:
					register[Rd] = int(fetch_inst(Memory,address,4) >> 16)
				elif adr_1_0 == 3:
					register[Rd] = int(fetch_inst(Memory,address,4) >> 24)
			elif inst == 40:
				# str
				if condition_passed(cond,register):
						Memory = set_memory(Memory,address,register[Rd],4)
			elif inst == 41:
				# STRB
				if condition_passed(cond,register):
					Memory = set_memory(Memory,address,extract_field(register[Rd],7,0),1)
			elif inst == 42:
				# STRBT
				if condition_passed(cond,register):
					Memory = set_memory(Memory,address,extract_field(register[Rd],7,0),1)
			elif inst == 43:
				# strh
				if condition_passed(cond,register):
					if adr_0 == 0:
						data = extract_field(register[Rd],15,0)
					else:
						data = UNPREDICTABLE
					Memory = set_memory(Memory,address,data,2)
			elif inst == 44:
				# strt
				if condition_passed(cond,register):
						Memory = set_memory(Memory,address,register[Rd],4)
			return register, Memory
def do_dp(shifter_operand,shifter_carry_out,register,inst,word):
			cond = extract_field(word,31,28)
			three_bits = extract_field(word,27,25)
			I = extract_field(word,25,25)
			P = extract_field(word, 24,24)
			U = extract_field(word,23,23)
			B = extract_field(word,22,22)
			W = extract_field(word,21,21)
			S = extract_field(word,20,20)
			Rn = extract_field(word,19, 16)
			Rd = extract_field(word,15,12)
			N = extract_field(register[CPSR],31,31)
			Z = extract_field(register[CPSR],30,30)
			C = extract_field(register[CPSR],29,29)
			V = extract_field(register[CPSR],28,28)
			if inst == 1:
				# ADC
				if condition_passed(cond,register):
					register[Rd] = int((register[Rn] + shifter_operand + C)&0xffffffff)
					if S == 1 and Rd == PC:
						register[CPSR] = register[SPSR]
					elif S == 1:
						# Negative Flag
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[Rd],31,31))
						# Z carry (unsigned overflow)
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
						# C (signed overflow)
						register[CPSR] = set_bit(register[CPSR],29,(carry_from(register[Rn] + shifter_operand + C)))
						# V most signif 32bits are all 0....
						register[CPSR] = set_bit(register[CPSR],28,overflow_from(register[Rn] + shifter_operand+C))			
			elif inst == 2:
				# ADD
				if condition_passed(cond,register):
					register[Rd] = int((register[Rn] + shifter_operand)&0xffffffff)
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					else:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[Rd],31,31))
						# Z carry (unsigned overflow)
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
						# C (signed overflow)
						register[CPSR] = set_bit(register[CPSR],29,(carry_from(register[Rn]+ shifter_operand)))
						# V most signif 32bits are all 0....
						register[CPSR] = set_bit(register[CPSR],28,overflow_from(register[Rn]+ shifter_operand,register[Rn]))
			elif inst == 3:
				if condition_passed(cond,register):
					register[Rd] = register[Rn] & shifter_operand
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					else:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[Rd],31,31))
						# Z carry (unsigned overflow)
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
						# C (signed overflow)
						register[CPSR] = set_bit(register[CPSR],29,(shifter_carry_out))
						# V most signif 32bits are all 0....
						#unnaffectedd
			elif inst == 4:
				# bic
				if condition_passed(cond,register):
					register[Rd] = register[Rn] & ~(shifter_operand)
					if S == 1 and Rd == PC:
						register[CPSR] = register[SPSR]
					else:
						# N flag
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[Rd],31,31))
						# Z carry (unsigned overflow)
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
						# C (signed overflow)
						register[CPSR] = set_bit(register[CPSR],29,(shifter_carry_out))
						# V most signif 32bits are all 0....
						#unnaffectedd
			elif inst == 5:
				# CMN
				if condition_passed(cond,register):
					alu_out = (register[Rn] + shifter_operand)&0xffffffff
					# N flag
					register[CPSR] = set_bit(register[CPSR],31,extract_field(alu_out,31,31))
					# Z carry (unsigned overflow)
					if alu_out == 0:
						register[CPSR] = set_bit(register[CPSR],30,1)
					else:
						register[CPSR] = set_bit(register[CPSR],30,0)
					# C (signed overflow)
					register[CPSR] = set_bit(register[CPSR],29,carry_from(register[Rn] + shifter_operand))
						# V most signif 32bits are all 0....
						#unnaffectedd
					register[CPSR] = set_bit(register[CPSR],28,overflow_from(register[Rn] + shifter_operand))
			elif inst == 6:
				# cmp
				if condition_passed(cond,register):
					alu_out = register[Rn] - shifter_operand
					#n
					register[CPSR] = set_bit(register[CPSR],31,extract_field(alu_out,31,31))
					# Z carry (unsigned overflow)
					if alu_out == 0:
						register[CPSR] = set_bit(register[CPSR],30,1)
					else:
						register[CPSR] = set_bit(register[CPSR],30,0)
					# C (signed overflow)
					# NOT BORROW FROM, IS'nt CARRY_FROM.  Figure this shit ou.\t
					register[CPSR] = set_bit(register[CPSR],29,~(carry_from(register[Rn] + shifter_operand)))
						# V most signif 32bits are all 0....
						#unnaffectedd
					register[CPSR] = set_bit(register[CPSR],28,overflow_from(register[Rn] + shifter_operand))
			elif inst == 7:
				# EOR
				if condition_passed(cond,register):
					register[Rd] = register[Rn] ^ shifter_operand
					if S == 1 and Rd== PC:
						register[CPSR] = register[SPSR]
					else:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
						register[CPSR] = set_bit(register[CPSR],29,shifter_carry_out)
						# v flag is left the fuck alone
			elif inst == 8:
				# MOV
				if condition_passed(cond,register):
					
					register[Rd] = int(shifter_operand)
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					elif S == 1:
						register[CPSR] = set_bit(register[CPSR], 31, extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR], 30, 1)
						else:
							register[CPSR] = set_bit(register[CPSR], 30, 0)
						register[CPSR] = set_bit(register[CPSR],29, shifter_carry_out)
						# v is un affected
			elif inst == 9:
				# MVN
				if condition_passed(cond,register):
					register[Rd] = ~(shifter_operand)
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					elif S ==1:
						register[CPSR] = set_bit(register[CPSR], 31, extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR], 30, 1)
						else:
							register[CPSR] = set_bit(register[CPSR], 30, 0)
						register[CPSR] = set_bit(register[CPSR],29, shifter_carry_out)
						# v is un affected
			elif inst == 10:
				# ORR:
				if condition_passed(cond,register):
					register[Rd] = register[Rn] | shifter_operand
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					elif S == 1:
						register[CPSR] = set_bit(register[CPSR], 31, extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR], 30, 1)
						else:
							register[CPSR] = set_bit(register[CPSR], 30, 0)
						register[CPSR] = set_bit(register[CPSR],29, shifter_carry_out)
						# v is un affected
			elif inst == 11:
				# RSB
				if condition_passed(cond,register):
					register[Rd] = int(shifter_operand-register[Rn]) 
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					elif S == 1:
						register[CPSR] = set_bit(register[CPSR], 31, extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR], 30, 1)
						else:
							register[CPSR] = set_bit(register[CPSR], 30, 0)
						register[CPSR] = set_bit(register[CPSR],29, ~(carry_from(shifter_operand-register[Rn])))
						register[CPSR] = set_bit(register,[CPSR],28,overflow_from(shifter_operand,register[Rn]))
						
			elif inst == 12:
				# RSC
				if condition_passed(cond,register):
					register[Rd] = int(shifter_operand-register[Rn] -(~(C)))
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					elif S == 1:
						register[CPSR] = set_bit(register[CPSR], 31, extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR], 30, 1)
						else:
							register[CPSR] = set_bit(register[CPSR], 30, 0)
						register[CPSR] = set_bit(register[CPSR],29, ~(carry_from(shifter_operand-register[Rn] - (~(C)))))
						register[CPSR] = set_bit(register[CPSR],28,overflow_from(shifter_operand-register[Rn] -(~(C))))
			elif inst == 13:
						# SBC
				if condition_passed(cond,register):
					register[Rd] = int(register[Rn]-shifter_operand-(~(C)))
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					elif S == 1:
						register[CPSR] = set_bit(register[CPSR], 31, extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR], 30, 1)
						else:
							register[CPSR] = set_bit(register[CPSR], 30, 0)
						register[CPSR] = set_bit(register[CPSR],29, ~(carry_from(register[Rn]-shifter_operand-(~C))))
						register[CPSR] = set_bit(register,[CPSR],28,overflow_from(register[Rn]-shifter_operand-(~C)))
			elif inst == 14:
					# SUB
				if condition_passed(cond,register):
					register[Rd] = int(register[Rn] - shifter_operand)
					if S == 1 and register[Rd] == PC:
						register[CPSR] = register[SPSR]
					elif S == 1:
						register[CPSR] = set_bit(register[CPSR], 31, extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR], 30, 1)
						else:
							register[CPSR] = set_bit(register[CPSR], 30, 0)
							register[CPSR] = set_bit(register[CPSR],29, ~(carry_from(register[Rn]-shifter_operand)))
							register[CPSR] = set_bit(register,[CPSR],28,overflow_from(register[Rn]-shifter_operand))
				
	#	register[Rd] = result
			elif inst == 15:
					#TEQ
				if condition_passed(cond,register):
					alu_out = register[Rn] ^ shifter_operand
					register[CPSR] = set_bit(register[CPSR],31,extract_field(allue_out,31,31))
					if alu_out == 0:
						register[CPSR] = set_bit(register[CPSR],30,1)
					else:
						register[CPSR] = set_bit(register[CPSR],30,0)
						register[CPSR] = set_bit(register[CPSR],29,shifter_caryy_out)
						# v is unaffected
			elif inst == 16:
				alu_out = register[Rn] & shifter_operand
				register[CPSR] = set_bit(register[CPSR],31,extract_field(allue_out,31,31))
				if alu_out == 0:
					register[CPSR] = set_bit(register[CPSR],30,1)
				else:
					register[CPSR] = set_bit(register[CPSR],30,0)
				register[CPSR] = set_bit(register[CPSR],29,shifter_caryy_out)

	
					
			return register
		
def do_multiplies(Memory,register,word,inst,addMode):
			Rd = extract_field(word,19,16)
			Rn = extract_field(word,15,12)
			Rm = extract_field(word,3,0)
			Rs = extract_field(word,11,8)			
			RdHi = extract_field(word,19,16)
			RdLo = extract_field(word,15,12)
			if inst == 23:
				#MLA
				
				if condition_passed(cond,register):
					register[Rd] = int(extract_field((register[Rm]*register[Rs]+register[Rn]),31,0))
					if S == 1:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
			elif inst == 24:
				if condition_passed(cond,register):
					register[Rd] = int(extract_field((register[Rm]*register[Rs]),31,0))
					if S == 1:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[Rd],31,31))
						if register[Rd] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
			elif inst == 25:
				#SMLAL # Signed, need to fix.  FUCK
				if condition_passed(cond,register):
					register[RdLo] = (extract_field(register[Rm]*register[Rs],31,0)+register[RdLo])&0xffffffff
					register[RdHi] = (extract_field(register[Rm]*register[Rs],63,32)+register[RdHi]+extract_field(carry_from(register[Rm]*register[Rs]+register[RdLo]),31,0))&0xffffffff		
				
					if S == 1:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[RdHI],31,31))
						if register[RdHi] == 0 and register[RdLo] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
			elif inst == 26:
				#SMULL # signed need to fix...
				if condition_passed(cond,register):
					register[RdLo] = extract_field(register[Rm]*register[Rs],31,0)
					register[RdHi] = extract_field(register[Rm]*register[Rs],63,32)
				
					if S == 1:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[RdHI],31,31))
						if register[RdHi] == 0 and register[RdLo] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
			elif inst == 27:
				# umlal
				if condition_passed(cond,register):
					register[RdLo] = (extract_field(register[Rm]*register[Rs],31,0)+register[RdLo])&0xffffffff
					register[RdHi] = (extract_field(register[Rm]*register[Rs],63,32)+register[RdHi]+extract_field(carry_from(register[Rm]*register[Rs]+register[RdLo]),31,0))&0xffffffff		
				
					if S == 1:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[RdHI],31,31))
						if register[RdHi] == 0 and register[RdLo] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
			elif inst == 28:
				if condition_passed(cond,register):
					register[RdLo] = extract_field(register[Rm]*register[Rs],31,0)
					register[RdHi] = extract_field(register[Rm]*register[Rs],63,32)
				
					if S == 1:
						register[CPSR] = set_bit(register[CPSR],31,extract_field(register[RdHI],31,31))
						if register[RdHi] == 0 and register[RdLo] == 0:
							register[CPSR] = set_bit(register[CPSR],30,1)
						else:
							register[CPSR] = set_bit(register[CPSR],30,0)
			#MLA,MUL,SMLAL,SMULL,UMLAL,UMULL = 23,24,25,26,27,28
			return register
def extract_field(word, hbit,lbit): 
			word = word >> lbit
			mask = (2**(hbit-lbit+1))-1
			
	#print(word & mask)	
			return word & mask	
		# returns an instruction codez
def parseInstruction(word):
			
			usr = 0
			sys = 1
			svc = 2
			abt = 3
			und = 4
			irq = 5
			fiq = 6
			mode = usr
			LR = 14
			PC = 15     
			
			SPSR = 17	
			# Data Proc
			ADC, ADD, AND, BIC, CMN, CMP, EOR, MOV, MVN,ORR, RSB, RSC, SBC, SUB, TEQ, TST = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
			# Misc Insts, Branching.

			MRS, MSR , BX, CLZ, BLX2, BLX1, BBL = 17,18,19,20,21,22,48
			# Multiplies:

			MLA,MUL,SMLAL,SMULL,UMLAL,UMULL = 23,24,25,26,27,28
			## load/store mults:
	
			LDM1, LDM2, LDM3, STM1, STM2 = 29,30,31,32,33
			# extra load/store instructions:
	
			LDR, LDRB, LDRBT,LDRH,LDRSB,LDRSH,LDRT,STR,STRB,STRBT,STRH,STRT= 34,35,36,37,38,39,40,41,42,43,44,45
			# branching instructions

			UND = 96
			UNPRED = 99
			BKPT = 98
			SWI = 97
			inst = UND
			## these fields represent various aspects of the word.
			cond = extract_field(word,31,28)
			three_bits = extract_field(word,27,25)
			oppcode = extract_field(word,24,21)
			S = extract_field(word,20,20)
			# two bits are bits 24 and 23... 
			two_bits = extract_field(word, 24,23)
			twenty_one =extract_field(word,21,21)
			twenty_two = extract_field(word,22,22)
			seven = extract_field(word,7,7)
			four = extract_field(word,4,4)
			seven_four = extract_field(word,7,4)
			fifteen = extract_field(word,15,15)
			twenty_four = extract_field(word,24,24)
			# this checks the shits out.
			if (three_bits == 0):
				
				if two_bits == 2 and S == 0:
					## misc instructions
					if seven_four == 0:
						if twenty_one == 0:
							inst = MRS
						elif twenty_one == 1:
							inst = MSR	
					elif seven_four  == 1:
						if oppcode == 9:
							inst = BX
						elif oppcode == 11:
							inst = CLZ
					elif seven_four == 3:
						if oppcode == 9:
							inst = BLX2
					elif seven_four == 5:
						## DSP Instruction.  Not Implemented. see page 3-4 of manual, refrences ch 10 ENCHANCED DSP INST
						pass
					elif seven_four == 7:
						if cond!= 14:
							inst = UNPRED
						else:
							inst = BKPT
					elif seven_four >= 8:
						# DSP instruction.  NOT IMPLEMENTED.  See page 3-4 of manual, refrences ch 10 ENHANCED DSP INST
						pass

				elif seven == 1 and four == 1:
					## multiplies and load stores
					if seven_four == 9:
						if oppcode == 1:
							inst = MLA
						elif oppcode == 0:
							inst = MUL
						elif oppcode == 7:
							inst = SMLAL
						elif oppcode == 6:
							inst = SMULL
						elif oppcode == 5:
							inst = UMLAL
						elif oppcode == 4:
							inst = UMULL
					elif seven_four == 11:
						if S ==1:
							
								inst = LDRH
							
						if S == 0:
						
								inst = STRH
				
					elif seven_four == 13:
						if S == 1:
							inst = LDRSB
					elif seven_four ==  15 and S ==1:
						inst = LDRSH
				else:
					# Data Processing Instructions
					if oppcode == 5:
						inst = ADC
					elif oppcode== 4:
						inst = ADD
					elif oppcode == 0:
						inst = AND
					elif oppcode == 14:
						inst = BIC
					elif oppcode == 11 and S == 1:
						inst = CMN
					elif oppcode == 10 and S == 1:
						inst = CMP
					elif oppcode == 1:
						inst = EOR
					elif oppcode == 13:
						inst = MOV
					elif oppcode == 15:
						inst = MVN
					elif oppcode == 12:
						inst = ORR
					elif oppcode == 3:
						inst = RSB
					elif oppcode == 7:
						inst = RSC
					elif oppcode == 6:
						inst = SBC
					elif oppcode == 2:
						inst = SUB
					elif oppcode == 9:
						inst = TEQ
					elif oppcode == 8:
						inst == TST
			elif three_bits == 1:
				if two_bits == 2 and twenty_one == 0 and S == 0:
					inst = UND
				elif two_bits ==2 and twenty_one == 1 and S == 0:
					inst = MOV
				else:
					# Data Processing Instructions
					if oppcode == 5:
						inst = ADC
					elif oppcode== 4:
						inst = ADD
					elif oppcode == 0:
						inst = AND
					elif oppcode == 14:
						inst = BIC
					elif oppcode == 11 and S == 1:
						inst = CMN
					elif oppcode == 10 and S == 1:
						inst = CMP
					elif oppcode == 1:
						inst = EOR
					elif oppcode == 13:
						inst = MOV
					elif oppcode == 15:
						inst = MVN
					elif oppcode == 12:
						inst = ORR
					elif oppcode == 3:
						inst = RSB
					elif oppcode == 7:
						inst = RSC
					elif oppcode == 6:
						inst = SBC
					elif oppcode == 2:
						inst = SUB
					elif oppcode == 9:
						inst = TEQ
					elif oppcode == 8:
						inst == TST
			elif three_bits == 2:
				if twenty_four == 0 and twenty_two == 1 and twenty_one == 1 and S == 1:
					inst = LDRBT
				elif twenty_four == 0 and twenty_two == 0 and twenty_one == 1 and S == 1:
					inst = LDRT
				elif twenty_four == 0 and twenty_two == 1 and twenty_one == 1 and S == 0:
					inst = STRBT
				elif twenty_four == 0 and twenty_two == 0 and twenty_one == 1 and S == 0:
					inst = STRT
				elif twenty_two == 0 and S == 1:
					inst = LDR
				elif twenty_two == 1 and S == 1:
					inst = LDRB
				elif twenty_two == 0 and S == 0:
					inst = STR
				elif twenty_two == 1 and S == 0:
					inst = STRB
			elif three_bits == 3:
				if four == 0:
					if twenty_four == 0 and twenty_two == 1 and twenty_one == 1 and S == 1:
						inst = LDRBT
					elif twenty_four == 0 and twenty_two == 0 and twenty_one == 1 and S == 1:
						inst = LDRT
					elif twenty_four == 0 and twenty_two == 1 and twenty_one == 1 and S == 0:
						inst = STRBT
					elif twenty_four == 0 and twenty_two == 0 and twenty_one == 1 and S == 0:
						inst = STRT
					elif twenty_two == 0 and S == 1:
						inst = LDR
					elif twenty_two == 1 and S == 1:
						inst = LDRB
					elif twenty_two == 0 and S == 0:
						inst = STR
					elif twenty_two == 1 and S == 0:
						inst = STRB
				else:
					inst = UND
			elif three_bits == 4 and cond != 15:
				if S == 1 and twenty_two == 0:
					inst = LDM1
				elif twenty_two == 0 and twenty_one == 0 and S == 1 and fifteen == 0:
					inst = LDM2
				elif twenty_two==1 and S == 1 and fifteen == 1:
					inst = LDM3
				elif twenty_two == 0 and S == 0:
					inst = STM1
				elif twenty_two == 1 and twenty_one == 0 and S == 0:
					inst = STM2
				else:
					inst = UND
			elif three_bits == 4 and cond == 15:
				inst = UND

			elif three_bits == 5 and cond != 15:
				inst = BBL
			elif three_bits == 5 and cond ==15:
				inst = BLX1
			elif three_bits == 7 and twenty_four == 1:
				inst = SWI
			else:
				inst = UND	
			return inst
