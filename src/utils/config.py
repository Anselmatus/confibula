# -*- coding: utf-8 -*-

__author__ = "Chou & Antoine"
__date__ = "$26 nov. 2011 19:31:10$"

import logger

class Config:
	"""class Config:

Loads a text file and reads values from it.
Values are stored in a dictionnary and can be accessed by their key.

- The text file is evaluated line by line and should apply to this pattern:

  key = value
	
  age = 18
  pi = 3.14
  message = "a string is delimited by guillemets"
  ; This line is a comment and will not be evaluated.
  ; Basically, anything after ';' is considerated as a comment.
  isSteveJobsDead = True ; Any case of the words "true" and "false" are accepted.
  ; Spaces between keys, equality sign and values do not matter.
       country   =         "France"
  myList = (2, 37.98, "hello", false)
  
- Loading a config file :

  myConfig = Config(fileName)
  myConfig.load()
  ; Example :
  myConfig = Config('myConfigFile.txt')
  myConfig.load()
  The file extension doesn't matter yet the content of the file has to be plain text.

- Accessing values :

  Accessing single value :

  var = myConfig.getValue(key)
  ; Example :
  var = myConfig.getValue('pi')
  print var * 3
  ; Result : 9.42
  
  Accessing a list value :
  
  list = myConfig.getValue(listName)
  ; Example :
  list = myConfig.getValue('myList')
  for item in list:
  	print item

  Accessing the whole set of values :

  dictionnary = myConfig.getAll()
  ;Example :
  myDic = myConfig.getAll()
  for key in myDic:
  	print myDic[key]
	"""
	def __init__(self, fileName):
		self.params = {}
		self.fileName = fileName
	
	def readFile(self):
		"""
	Open the file specified at the instanciation of the Config object, reads it and return the content as a list of lines.
		"""
		try:
			fichier = open(self.fileName,'r')
			lines = fichier.readlines()
			return lines
		except IOError:
			print "Can not open file", self.fileName, "."
			exit()
	
	def load(self):
		"""
	Loads every value in the config file and stores it in a dictionnary.
		"""
		lines = self.readFile()
		i = 1
		for line in lines:
			line = line.split(';')[0] ## stripping comments
			line = line.split('=') ## splitting keys and values
			
			if len(line) == 2 : ## if we have both the key and the value
				self.parseLine(line, i)
			i += 1
	
	def parseLine(self, line, lineNum):
		"""
	Evaluates the config file, line by line, from the result of self.readFile()
		"""
		key = line[0].strip() ## strip() gets rid of spaces at the beginning/end of the line
		value = line[1].strip()
		
		try:
			self.params[key] = self.parseValue(value)
					
		except Exception:
			logger.error("Erreur lors de la lecture de '%s = %s' à la ligne %s de %s" % (key, value, lineNum, self.fileName))
			#exit()
	
	def parseValue(self, value):
		"""
	Evaluates the type of every value and stores it correctly.
		"""
		if value[0] == '"' and value[-1] == '"': ## if it's delimited by " " then we have a string here
			return value[1:-1] ## and we store it whithout the " " (list slicing)
		
		elif value[0] == '(' and value[-1] == ')': ## if we have a value that contains a list
			return self.parseList(value)
		
		else: ## it's a numeric value
			if value.lower() == 'true':
				return True
				
			elif value.lower() == 'false':
				return False
				
			elif '.' in value: ## that's a float
				return  float(value)
				
			else: ## that's an int
				return int(value)
	
	def parseList(self, valueList):
		"""
	Evaluates a value as a symbolic list and stores it as a list in the dictionnary.
		"""
		return [ self.parseValue( value.strip() ) for value in valueList[1:-1].split(',') ]
	
	def getValue(self, key):
		return self.params[key]
	
	def getAll(self):
		return self.params
	
	def getAllValues(self):
		return [ self.params[key] for key in self.params ]
	
	def getAllKeys(self):
		return [ key for key in self.params ]


if __name__ == "__main__":
	maConfig = Config('confibula.cfg')
	maConfig.load()
	
	print 'All : \n'
	dico = maConfig.getAll()
	for key in dico:
		print key, ':', dico[key]
	for item in dico['myList']:
		print item*3
