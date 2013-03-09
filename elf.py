import math

ELFHeader=[['id',16],['type',2],['machine',2],['version',4],['entry',4],['phoff',4],['shoff',4],['flags',4],['ehsize',2],['phentsize',2],['phnum',2],['shentsize',2],['shnum',2],['shstrndx',2]]
SectionHeader=[['name',4],['type',4],['flags',4],['addr',4],['offset',4],['size',4],['link',4],['info',4],['addalign',4],['entsize',4]]

ELF64Header=[['id',16],['type',2],['machine',2],['version',4],['entry',8],['phoff',8],['shoff',8],['flags',4],['ehsize',2],['phentsize',2],['phnum',2],['shentsize',2],['shnum',2],['shstrndx',2]]
Section64Header=[['name',4],['type',4],['flags',4],['addr',8],['offset',8],['size',4],['link',4],['info',4],['addalign',4],['entsize',4]]

def extractfield(filespace, hparse, field, offset):
	#find field
	off=0
	for f in hparse:
		if f[0]==field:
			break
		off=off+f[1]
	#extract field
	field=filespace[off+offset:off+offset+f[1]]

	n=0
	for i in range(len(field)):
		n=n+ord(field[i])*int(math.pow(256,i))
	return n

def loadfile(filename):
	memory={}

	#get file	
	f = file(filename,"r")
	filespace=f.read()
	
	#extract main ELF header
	entry=extractfield(filespace,ELFHeader,'entry',0)
	print hex(entry)

	#extract number of sections
	secnum=extractfield(filespace,ELFHeader,'shnum',0)
	print 	secnum

	shentsize=extractfield(filespace,ELFHeader,'shentsize',0)
	shoff=extractfield(filespace,ELFHeader,'shoff',0)
	place=shoff

	for sec in range(secnum):
		addr=extractfield(filespace,SectionHeader,'addr',place)
		size=extractfield(filespace,SectionHeader,'size',place)
		offset=extractfield(filespace,SectionHeader,'offset',place)
		if (addr!=0 and size!=0):
			print "Found a segment at offset",hex(place)
			print "Segment is",hex(size),"big and is located at",hex(offset)
			print "Segment should be placed at",hex(addr)

			for b in range(offset,size+offset):
				print hex(ord(filespace[b])),
				memory[hex(addr+b-offset)]=ord(filespace[b])
			print
		place=place+shentsize
		
	return memory,entry,

def main(filename):
	memory,entry=loadfile(filename)

	IP=entry
	
	while(True):
		if memory[IP]==0x90:
			print "NOP"

		IP=IP+1
