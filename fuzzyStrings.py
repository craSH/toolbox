
#  foo://username:password@example.com:8042/over/there/index.dtb;type=animal?name=ferret#nose
#  \ /   \________________/\_________/ \__/\_________/ \___/ \_/ \_________/ \_________/ \__/
#   |           |               |        |     |         |     |       |            |     |
# scheme     userinfo         hostname  port  path  filename extension parameter(s) query fragment
#        \_______________________________/
#                   authority


import random
import time
import binascii

#ASCII_CNTRL = range(32,47) + range(58,64) + range(91,96) + range(123,126)
#ASCII_ALPHA = range(48,57) + range(65,90) + range(97,122)
#ASCII = ASCII_CNTRL + ASCII_ALPHA
#MAXLEN = 1030


class fuzzyStrings:

	def __init__(self, itterations=0):
		random.seed(self.seed())
		self.Dictionaries = self.create_ascii_dictionaries()
                self.count = 0
                self.itterations = itterations 

	def create_ascii_dictionaries(self):
		dictionaries = {}

		# ascii control characters        
		cntrl_nums = range(32,47) + range(58,64) + range(91,96) + range(123,126)
		cntrl_list = []
		for i in cntrl_nums:
			h = hex(i)[2:4]
			cntrl_list.append(binascii.unhexlify(h))
		dictionaries['ascii_cntrl'] = cntrl_list

		# ascii alpha numeric characters
		alpha_nums = range(48,57) + range(65,90) + range(97,122)
		alpha_list = []
		for i in alpha_nums:
			h = hex(i)[2:4]
			alpha_list.append(binascii.unhexlify(h))	
		dictionaries['ascii_alpha'] = alpha_list

		# ascii complete
		dictionaries['ascii'] = alpha_list + cntrl_list
                
                # singleton 'A'
                dictionaries['A'] = ['A']

		return dictionaries
	
        
        def seed(self):
		""" Generate a somewhat random number to seed the PRNG"""
		r = time.time()
		a = str(r-int(r))
		n = a[2:len(a)]
		d = random.randint(0, int(n))
		return d

            
        # ==== required to be itterable =====

        def next(self):
            if self.count >= self.itterations):
                self.count = 0
                raise StopIteration
            else:
                self.count = self.count +1
                return randString()
 
        def __getitem__(self, item):
            return None

        def __iter__(self):
            return self

        # ==== end itterable requirements ====            

	def randString(self, minLen=0, maxLen=1032, dictionary='ascii'):
		"""
		Create a string of random characters from dictionary containing at least minLen chars and no more than maxLen.
		Tis but a scratch! A scratch, your arm's off. No it isn't.
		"""
		d = self.Dictionaries[dictionary]
		s = ""
		for x in range(0, random.randint(minLen, maxLen)):
			s += d[random.randint(0, len(d)-1)]
		return s
			
	def insertRandChars(self, string, dictionary='ascii_cntrl', minChars=0, maxChars=16):
		"""
		Insert elements from dictionary into string in random locations. This extends the overall length of the string.
		I dont wanna talk to you anymore. You empty headed animal food trough wiper! I fart in your general direction. Your mother was a hampster and father smelt of elderberreis.
		"""
		d = self.Dictionaries[dictionary]
		count = random.randint(minChars, maxChars)
		x = self.stringToList(string)
		for i in range(0, count):
			index = random.randint(0, len(string)-1)
			x.insert(index, self.randString(1,1, dictionary))
		return "".join(x)

        def insertRandString(self, text, dictionary='ascii', minLen=0, maxLen=10042):
            index = self.randint(0, len(text))
            rstring = self.randString(minLen, maxLen, dictionary)
            return text[0:index] + rstring + text[index:len(text)]

        def insertString(self, insertion, target, index):
            return target[0:index] + insertion + target[index:len(target)]



	def stringToList(self, string):
		"""What? A swallow carrying a coconut?"""
		lst = []
		for c in string:
			lst.append(c)
		return lst


	def loadDictionary(self, path, name):
		"""Load a dictionary from a file under name"""
		f = open(path)
		lines = f.readlines()
		f.close()
		
		# strip \r\n and add to Dictionaries
		stripped = []
		for x in lines:
			stripped.append(x.strip('\r').strip('\n'))
		self.Dictionaries[name] = stripped

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
		

