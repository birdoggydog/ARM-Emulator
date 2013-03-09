#class BarrellShifter():
		
def condition_passed(cond,register):
	PC = 15
	if cond == extract_field(register[PC],31,28):
		return True
	else:
		return False
def count_set_bits(num,length):
		counter = 0
		for i in range(length):
			if extract_field(num,i,i) == 1: 
				counter = counter + 1
		return counter

def extract_field(word, hbit,lbit): 
		word = word >> lbit
		mask = (2**(hbit-lbit+1))-1
			
	#print(word & mask)	
		return word & mask	
def setBit(num, shift, bit):
	
		mask = num&(~(1<<shift))
		returnVal = (bit<<shift) | num
	
		return returnVal&0xffffffff
def arithmetic_shift_right(num,shift):
		bit = 0
		for i in range(shift):
			if num & 0x80000000 != 0:
				num = num >> 1
				num = num | 0x80000000
			else: num = num >> 1

		return num
def rotate_right(num,shift):

		for i in range(shift):
			if num & 1 != 0:
				num = num >> 1
				num = num | 0x80000000
			else: num = num >> 1
		return num

def arithmetic_shift_left(num,shift):
		bit = 0
		for i in range(shift):
				num = num << 1

		return num
def rotate_left(num,shift):
		for i in range(shift):
			if num & 0x80000000 != 0:
				
				num = num << 1
				num = num | 0x80000000
			else:
				num = num << 1

def do_data_proc(word,addMode,inst, register):
		DP32BitImmediate = 0
		DPImmediateShift= 1 
		DPRegShift = 2
		MLSImmOffIndex = 3
		MLSRegOffIndex = 4
		LSImmOffIndex = 5
		LSRegOffIndex = 6
		LSScaleRegOffIndex = 7		
		LSMultiple = 8
		seven = extract_field(word,7,7)
		six = extract_field(word,6,6)
		five = extract_field(word,5,5)
		four = extract_field(word,4,4)
		seven_four = extract_field(word,7,4)
		shift_imm = extract_field(word,11,7)
		Rm = extract_field(word,3,0)
		eleven_four = extract_field(word,11,4)
		C = extract_field(word,30,30)
		immed_8 = extract_field(word,7,0)
		rotate_imm = extract_field(word,11,8)
		Rs = extract_field(word,11,8)
		rm31 =extract_field(register[Rm],31,31) 
		regRs70 = extract_field(register[Rs],7,0)
		regRs40 = extract_field(register[Rs],4,0)
		if addMode == DP32BitImmediate:
			# 32 bit immediate
			print('immed')
			shifter_operand = rotate_right(immed_8 ,(rotate_imm *2))
			if rotate_imm == 	0:
				shifter_carry_out = C
			else:
				shifter_carry_out = extract_field(shifter_operand,31,31)
		elif addMode == DPImmediateShift:
			print('immedShift')
			if five == 1 and six == 0:
				# lsr by imm
				if shift_imm == 0:
					
					shifter_operand = 0
					shifter_carry_out = extract_field(register[Rm],31,31)
				else:
					shifter_operand = register[Rm] >> shift_imm
					shifter_carry_out = extract_field(register[Rm],shift_imm-1,shift_imm-1)
			elif eleven_four == 0:
				# Data Proc operands register
				shifter_operand = register[Rm]
				shifter_carry_out = C
			elif six == 0 and five == 0 and four == 0:
				# data proc lsl by imm
				if shift_imm ==0:
					shifter_operand = register[Rm]
					shifter_carry_out = C
				else:
					shifter_operand = register[Rm] << shift_imm
					shifter_carry_out = extract_field(Rm,32-shift_imm,32-shift_imm)
			elif six == 1 and five == 0 and four == 0:
				# Arithmetic Shift..RIGHT by IMMEDIATE  
				
				if shift_imm == 0:
					if rm31 == 0:
						shifter_operand = 0
						shifter_carry_out = rm31
					else:
						shifter_operand = 0xffffffff
						shifter_caryy_out = rm31
				else:
					# 
					shifter_operand = arithmetic_shift_right(register[Rm],shift_imm)
					shifter_carry_out = extract_field(register[Rm],shift_imm-1,shift_imm-1)
			elif six == 1 and five ==1 and four == 0:
				# Rotate Right by Immediate
				if shift_imm == 0:
					# rotating with sign extend * HACK *
					shifter_operand = (C << 31) | (register[Rm] >> 1)
					shifter_carry_out = extract_field(register[Rm],0,0)
				else: 
					# actually rotate
					shifter_operand = rotate_right(register[Rm],shift_imm)
					shifter_carry_out = extract_field(register[Rm],shift_imm-1,shift_imm-1)

		elif addMode == DPRegShift:
			print('regShift')
			if seven_four == 1:
				print('lsl')
				# lsl by register
				if regRs70 == 0:
					shifter_operand = register[Rm]
					shifter_carry_out = C
				elif  regRs70 < 32:
					shifter_operand = register[Rm] << regRs70
					shifter_carry_out = register[Rm] - regRs70
				elif regRs70 == 32:
					shifter_operand = 0
					shifter_carry_out = extract_field(register[Rm],0,0)
				else:
					shifter_operand = 0
					shifter_carry_out = 0
			elif seven_four == 3:
				# LSR by Reg
				print('lsr')
				if regRs70 == 0:
					shifter_operand = register[Rm]
					shifter_carry_out = C
				elif  regRs70 < 32:
					shifter_operand = register[Rm] >> regRs70
					shifter_carry_out = extract_field(register[Rm],regRs70-1,regRs70-1)
				elif regRs70 == 32:
					shifter_operand = 0
					shifter_carry_out = extract_field(register[Rm],31,31)
				else:
					shifter_operand = 0
					shifter_carry_out = 0
			elif seven_four == 5:
				print('asr')
				# arithmetic shift right by register
				if regRs70 == 0:
					print('1')
					shifter_operand = register[Rm]
					shifter_carry_out = C
				elif  regRs70 < 32:
					print('2')
					shifter_operand = arithmetic_shift_right(register[Rm],regRs70)
					shifter_carry_out = extract_field(register[Rm],regRs70-1,regRs70-1)
				else:
					if rm31== 0:
						print('3')
						shifter_operand = 0 
						shifter_carry_out = rm31
					else:
						print('4')
						shifter_operand = 0xffffffff
						shifter_carry_out = rm31
			elif seven_four == 7:
				print('other...')
				if regRs70 == 0:
					shifter_operand = register[Rm]
					shifter_carry_out = C
				elif regRs40 == 0:
					shifter_operand= register[Rm]
					shifter_carry_out = rm31
				else:
					shifter_operand = rotate_right(register[Rm],regRs40)
					shifter_carry_out = extract_field(register[Rm],regRs40-1,regRs40-1)
			else:
					print('wtf?')
		return shifter_operand,shifter_carry_out,register

def do_misc_l_s(word,addMode,inst,register):
		DP32BitImmediate = 0
		DPImmediateShift= 1 
		DPRegShift = 2
		MLSImmOffIndex = 3
		MLSRegOffIndex = 4
		LSImmOffIndex = 5
		LSRegOffIndex = 6
		LSScaleRegOffIndex = 7		
		LSMultiple = 8
		cond = extract_field(word,31,28)
		MLSImmOffIndex = 3
		MLSRegOffIndex = 4
		cond = extract_field(word,31,28)
		P = extract_field(word,24,24)
		U = extract_field(word,23,23)
		twenty_two = extract_field(word,22,22)
		W = extract_field(word,21,21)
		L = extract_field(word,20,20)
		Rn = extract_field(word,19,16)	
		Rm = extract_field(word, 3,0)
		Rd = extract_field(word,15,12)
		immed_H = extract_field(word,11,8)
		seven = extract_field(word,7,7)
		S = extract_field(word,6,6)
		H = extract_field(word,5,5)
		four = extract_field(word,4,4)
		immed_L = extract_field(word,3,0)
		if addMode == MLSImmOffIndex:
			if P == 1:
				if W == 0:
					# L/S Immed Offset
					offset_8 = (immed_H<<4) | immed_L
					if U == 1:
						address = register[Rn] + offset_8
					else:
						address = register[Rn] - offset_8
				if W == 1:
					offset_8 = (immed_H<<4) | immed_L
					if U == 1:
						address = register[Rn] + offset_8
					else:
						address = register[Rn] - offset_8
					if condition_passed(cond,register):
						register[Rn] = address
				elif W ==1 :
					#immediate pre indexed
					offset_8 = (immed_h << 4) | immed_L
					if U == 1:
						address = register[Rn] + offset_8
					else:
						address = register[Rn] - offset_8
					if condition_passed(cond,register):
						register[Rn] = address
			elif P == 0:
				address = register[Rn]
				offset_8 = (immed_H << 4) | immed_L
				if condition_passed(cond,register):
					if U == 1:
						register[Rn] = register[Rn] + offset_8
					else:
						register[Rn] = register[Rn] - offset_8
		elif addMode == MLSRegOffIndex:
			if P == 1:	 # bit 24	
				if W == 0:
					# register offset
					if U == 1:
						address = register[Rn] + register[Rm]
					else: 
						address = register[Rn] - register[Rm]
				elif W == 1:# bit 21
					# register pre indexed
					if U == 1:
						address = register[Rn] + register[Rm]
					elif U == 0:
						address = register[Rn] - register[Rm]
					if condition_passed(cond,register):
						register[Rn] = address
			else:
				# register psot indexed
				address = register[Rn]
				if condition_passed(cond,register):
						if U == 0:
							register[Rn] = register[Rn] + register[Rm]
						elif U == 1:
							register[Rn] = register[Rn]  - register[Rm]

		return address, register
def do_mult():
		DP32BitImmediate = 0
		DPImmediateShift= 1 
		DPRegShift = 2
		MLSImmOffIndex = 3
		MLSRegOffIndex = 4
		LSImmOffIndex = 5
		LSRegOffIndex = 6
		LSScaleRegOffIndex = 7		
		LSMultiple = 8
		pass
def do_l_s_mult(word,addMode,inst,register):
		DP32BitImmediate = 0
		DPImmediateShift= 1 
		DPRegShift = 2
		MLSImmOffIndex = 3
		MLSRegOffIndex = 4
		LSImmOffIndex = 5
		LSRegOffIndex = 6
		LSScaleRegOffIndex = 7		
		LSMultiple = 8
		P = extract_field(word,24,24)
		U = extract_field(word,23,23)
		S= extract_field(word,22,22)
		W = extract_field(word,21,21)
		L = extract_field(word,20,20)
		Rn = extract_field(word,19,16)
		register_list=extract_field(word,15,0)
		cond = extract_field(word,31,28)
		if P == 0:
			if U == 0:
				# load store mult, decremeent after
				start_address = register[Rn] - (count_set_bits(register_list,16)*4) + 4# FUCKING TEST
				end_address = register[Rn]
				if condition_passed(cond,register) and W == 1:
					register[Rn] = register[Rn] - (count_set_bits(register_list,16)*4)
			elif U == 1:
				# load store mult, increment after
				start_address = register[Rn]
				end_address = register[Rn] + (count_set_bits(register_list,16)*4) -4
				if condition_passed(cond,register) and W == 1:
					register[Rn] = register[Rn] + (count_set_bits(register_list,16)*4)
		else:
			if U == 1:
				# increment before
				start_address = register[Rn] + 4
				end_address = register[Rn] + (count_set_bits(register_list,16)*4)
				if condition_passed(cond,register) and W == 1:
					register[Rn] = register[Rn] + (count_set_bits(register_list,16)*4)
				
			else:
				# decrement before
				start_address = register[Rn] - (count_set_bits(register_list,16)*4) -4# FUCKING TEST
				end_address = register[Rn] -4
				if condition_passed(cond,register) and W == 1:
					register[Rn] = register[Rn] - (count_set_bits(register_list,16)*4)
		return start_address,end_address,register
def do_l_s(word,addMode,inst,register):
		DP32BitImmediate = 0
		DPImmediateShift= 1 
		DPRegShift = 2
		MLSImmOffIndex = 3
		MLSRegOffIndex = 4
		LSImmOffIndex = 5
		LSRegOffIndex = 6
		LSScaleRegOffIndex = 7		
		LSMultiple = 8
		cond = extract_field(word,31,28)

		twenty_four = extract_field(word,24,24)	
		U = extract_field(word,23,23)
		B = extract_field(word,22,22)
		twenty_one = extract_field(word,21,21)
		L = extract_field(word,20,20)			
		Rn = extract_field(word,19,16)
		Rd = extract_field(word,15,12)
		shift_imm = extract_field(word,11,7)
		offset_12 = extract_field(word,11,0)
		shift = extract_field(word,6,5)
		Rm = extract_field(word,3,0)
		if addMode == LSImmOffIndex:
				if twenty_four == 1:
					if twenty_one == 0:
						# load and store word or unsigned byte, immediate offset:
						if U == 1:
							address = register[Rn] + offset_12 
						else:
							address = register[Rn] - offset_12
					if twenty_one == 1:
						# load and store wor do runsigned byte, immediate pre-indexed
						if U == 1:
							address = register[Rn] + offset_12
						else:
							address = register[Rn] - offset_12
						if condition_passed(cond,register):
							register[Rn] = address
				elif twenty_four == 0:
					address = register[Rn]
					if condition_passed(cond,register):
						register[Rn] = register[Rn] + offset_12
					else:
						register[Rn] = register[Rn] - offset_12
		elif addMode == LSRegOffIndex:
			if twenty_four == 1:
				if twenty_one == 0:
					# l/s word or unsigned byte, reg ooffset:
					if U == 1:
						address = register[Rn] + register[Rm]
					else:
						address = register[Rn] - register[Rm]
				else:
					# register offset pre-indexed
					if U == 1:
						address = Register[Rn] + register[Rm]
					else:
						address = Register[Rn] - register[Rm]
					if condition_passed(cond,register):
						register[Rn] = address
			else:
				# reg offset post indexed
				address = reigster[Rn]
				if condition_passed(cond,register):
					if U == 1:
						register[Rn] = register[Rn] + register[Rm]
					else:
						register[Rn] = register[Rn] - register[Rm]
		
		elif addMode == LSScaleRegOffIndex:
			
			if twenty_four == 1:
				if twenty_one == 0:
					# scaled register offset
					# has five possible cases,
					if shift == 0:
						# lsl
						index = register[Rm] << shift_imm
					elif shift == 1:
						# lsr
						if shift_imm == 0:
							index = 0
						else:
							index = register[Rm] >> shift_imm
					elif shift == 2:
						# ASR
						if shift_imm == 0:
							index = 0xFFFFFFFF
						else:
							index = 0
					elif shift == 3:
						# ROR or RRX (ror with extend)
						if shift_imm == 0: # RRX
							index = (C << 31)| register[Rm] >> 1
						else:
							# ROR
							index = rotate_right(regster[Rm],shift_imm)  
					if U == 1:
						address = register[Rn] + index
					else:
						address = register[Rn] - index
				else:
					# scaled reg pre index, 
					# as above, five potential uses
					if shift == 0:
						# lsl
						index = register[Rm] << shift_imm
					elif shift == 1:
						# lsr
						if shift_imm == 0:
							index = 0
						else:
							index = register[Rm] >> shift_imm
					elif shift == 2:
						# ASR
						if shift_imm == 0:
							index = 0xFFFFFFFF
						else:
							index = 0
					elif shift == 3:
						# ROR or RRX (ror with extend)
						if shift_imm == 0: # RRX
							index = (C << 31)| register[Rm] >> 1
						else:
							# ROR
							index = rotate_right(regster[Rm],shift_imm)  
					if U == 1:
						address = register[Rn] + index
					else:
						address = register[Rn] + index
					if condition_passed(cond,register):
						register[Rn] = address
					
			else:
				# reg post indexed
				# as above 5 options	
				address = register[Rn]
				if shift == 0:
						# lsl
						index = register[Rm] << shift_imm
				elif shift == 1:
						# lsr
						if shift_imm == 0:
							index = 0
						else:
							index = register[Rm] >> shift_imm
				elif shift == 2:
						# ASR
						if shift_imm == 0:
							index = 0xFFFFFFFF
						else:
							index = 0
				elif shift == 3:
						# ROR or RRX (ror with extend)
						if shift_imm == 0: # RRX
							index = (C << 31)| register[Rm] >> 1
						else:
							# ROR
							index = rotate_right(regster[Rm],shift_imm)  
				if condition_passed(cond,register):
					if U == 1:
						register[Rn] = register[Rn] + index
					else:
						register[Rn] = register[Rn] - index

		return address, register
def determineMode(word):
		
		# three bits represent the 27-25 bits of the word
		# four is bit 4, seven is bit 7, twentyTwo is 22		
		# DP = data processing, LS = load store, MLS = misc load store
	
		three_bits = extract_field(word,27,25)
		twenty_two = extract_field(word,22,22)
		seven = extract_field(word,7,7)
		four = extract_field(word,4,4)
		eleven_four = extract_field(word,11,4)

		DP32BitImmediate = 0
		DPImmediateShift= 1 
		DPRegShift = 2
		MLSImmOffIndex = 3
		MLSRegOffIndex = 4
		LSImmOffIndex = 5
		LSRegOffIndex = 6
		LSScaleRegOffIndex = 7		
		LSMultiple = 8
		IRREL = 10

		if three_bits == 1:
			mode = DP32BitImmediate
		elif three_bits == 0 and four == 0:
			mode = DPImmediateShift
		elif three_bits == 0 and seven == 0 and four == 1:
			mode = DPRegShift
		elif three_bits == 0 and twenty_two == 1 and seven == 1 and four ==1:
			mode = MLSImmOffIndex
		elif three_bits == 0 and twenty_two == 0 and seven == 1 and four ==1:
			mode = MLSRegOffIndex
		elif three_bits == 2:
			mode = LSImmOffIndex
		elif three_bits == 3 and eleven_four == 0:
			mode = LSRegOffIndex
		elif three_bits == 3 and four == 0:
			mode = LSScaleRegOffIndex
		elif three_bits == 4:
			mode = LSMultiple
		else:
			mode = IRREL
		return mode
