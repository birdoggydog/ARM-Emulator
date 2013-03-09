import sys
def main():
	filePaths = {}
	inp = sys.stdin.readlines()
	for word in inp:
		word = word.strip("\n")
		theFile = "Source/code/instTests/{0}/{1}.elf".format(word,word)
		
main()
