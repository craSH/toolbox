
import random
import time
import binascii

class FuzzyAlphabet:

	def __init__(self, itterations=0):
                # seed PRNG
                urand = open("/dev/urandom")
                random.seed(urand.read(4096))
                urand.close()
                # setup standard alphabets
		self.Alphabets = self.create_ascii_alphabets()

	def create_ascii_alphabets(self):
                """initialize standard alphabets"""
		alphabets = {}

		# ascii control characters        
		cntrl_nums = range(32,47) + range(58,64) + range(91,96) + range(123,126)
		cntrl_list = []
		for i in cntrl_nums:
			h = hex(i)[2:4]
			cntrl_list.append(binascii.unhexlify(h))
		alphabets['control'] = cntrl_list

		# ascii alpha numeric characters
		alpha_nums = range(48,57) + range(65,90) + range(97,122)
		alpha_list = []
		for i in alpha_nums:
			h = hex(i)[2:4]
			alpha_list.append(binascii.unhexlify(h))	
		alphabets['alpha'] = alpha_list

		# ascii complete
		alphabets['ascii'] = alpha_list + cntrl_list
                
                # singleton 'A'
                alphabets['A'] = ['A']

                # binary bytes
                bytes = []
                for num in range(0,255):
                    bytes.append(binascii.a2b_hex("%02x" % num))
                alphabets['binary'] = bytes

		return alphabets
	
        
	def randString(self, alphabet='ascii', minLen=0, maxLen=1032):
		"""
		Create a string of random characters from alphabet containing at least minLen chars and no more than maxLen.
		Tis but a scratch! A scratch, your arm's off. No it isn't.
		"""
		chars = self.Alphabets[alphabet]
		string = ""
		for x in range(0, random.randint(minLen, maxLen)):
			string += chars[random.randint(0, len(chars)-1)]
		return string
	
        def randStringList(self, count, alphabet='ascii', minLen=0, maxLen=1032):
            """
            Return a list of count strings from select alphabet between minLen and maxLen chars each
            """
            randStrings = []
            for i in range(0, count):
                randStrings.append(self.randString(alphabet, minLen, maxLen))
            return randStrings


        def insert(self, target, insertions):
            """ insert each string in list at random location of target"""
            for string in insertions:
                index = random.randint(0, len(target)-1)
                target = target[0:index] + string + target[index:]
            return target

        def replace(self, target, insertions):
            """ replace substrings of target with strings in stringList"""
            return None # todo

	def insertRandChars(self, string, alphabet='control', minChars=0, maxChars=16):
		"""
		Insert elements from alphabet into string in random locations. This extends the overall length of the string.
		I dont wanna talk to you anymore. You empty headed animal food trough wiper! I fart in your general direction. Your mother was a hampster and father smelt of elderberreis.
		"""
		d = self.Alphabets[alphabet]
		count = random.randint(minChars, maxChars)
		x = self.stringToList(string)
		for i in range(0, count):
			index = random.randint(0, len(string)-1)
			x.insert(index, self.randString(1,1, alphabet))
		return "".join(x)

        def insertRandString(self, text, alphabet='ascii', minLen=0, maxLen=10042):
            index = self.randint(0, len(text))
            rstring = self.randString(minLen, maxLen, alphabet)
            return text[0:index] + rstring + text[index:len(text)]

        def insertString(self, insertion, target, index):
            return target[0:index] + insertion + target[index:len(target)]



	def stringToList(self, string):
		"""What? A swallow carrying a coconut?"""
		lst = []
		for c in string:
			lst.append(c)
		return lst


	def loadalphabet(self, path, name):
		"""Load a alphabet from a file under name"""
		f = open(path)
		lines = f.readlines()
		f.close()
		
		# strip \r\n and add to alphabets
		stripped = []
		for x in lines:
			stripped.append(x.strip('\r').strip('\n'))
		self.Alphabets[name] = stripped

	def listSplit(self, string, delimeters):
		"""split a string at any character in the delimiter list."""
		substring = ""
		parts = []
		i = 0
		while (i < len(string)):
			# does the string from this point start with a delim?
			match = self.startsWithAny(string[i:len(string)-1], delimeters)
			if match:
				# add substring then delim to the list
				if substring:
					parts.append(substring)
					substring = ''
				parts.append(match)
				i += len(match)
			else:
				substring += string[i]
				i += 1
		if substring:
			parts.append(substring)
		return parts
			
		
	def startsWithAny(self, string, startStrings):
		"""
		Check if string starts with any character sequence in the startStrings list.
		Return an element from startStrings or None if no match was found.
		"""
		for x in startStrings:
			if string.startswith(x):
				return x


	def randint(self, min, max):
		return random.randint(min,max)


	def listFromFile(file):
		"""reads and returns a list from a file"""
		f = open(file)
		lst = f.readlines()
		f.close()
		return lst
		

