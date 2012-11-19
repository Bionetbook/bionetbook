#! /usr/bin/python

__metaclass__ = type # you have to type this statement in so that python2.5-2.7 can work with new style classes.

from datetime import *

class chemReagent:
	def __init__(self, **kvargs):
		# 	self.Name = 'name from chemReagents'
		self.Type = 'Type' # nucleic acid, enzyme, buffer, etc. 
		self.AllowedBuffer = ['ddw']
		self.UserName = []
		self.TempStorage = 'tempStorage'
		self.TempWork = 'tempWork'
		self.TempHandle = 'not specified'
		self.Location = 'Not specified'
		self.CatNumber = 'not specified'
		self.Inputs ={}
		self.Out={}
		self.AllKeys = vars(self).keys()
		self.AllVals = vars(self)
		self.Liv = ''
		for key in kvargs:
			self.Inputs[key] =  kvargs[key]
			#===================================================================
			# if hasattr(self, key):
			#	h = 'self.' + key
			#	self.[key] = kvargs[key]
			#	self.Out[key]= kvargs[key]
			#	func = 'set' + key
			#	eval(func, self.Inputs)
		 # 
		 # self._attributes = kvargs
		 #===================================================================
		
	def set_attributes(self, key, value):
		self._attributes[key]= value
		return
	
	def get_attributes(self, key, value):
		return self._attributes.get(key, None)
		
	def setName(self, name):
		self.Name = name
		
	def getName(self):
		return self.Name		
		
	def getTime(self):
		now = datetime.today()
		self.dateCreated = (now.day, now.month, now.year, now.hour, now.minute)	
		return self.dateCreated
				
	def setType(self, Type):
		self.Type = Type
		return self.Type

	def getType(self):
		return self.Type
	
	def addAllowedBuffer(self, newBuffer):
		self.AllowedBuffer.append(newBuffer)
		return self.AllowedBuffer

	def getAllowedBuffer(self):
		return self.AllowedBuffer
	
	def addUserName(self, newUserName):
		self.UserName.append(newUserName)
		return self.UserName

	def getUserName(self):
		return self.UserName
	
	def setTempWork(self, tempWork):
		self.TempWork = tempWork
		return self.TempWork

	def getTempWork(self):
		return self.TempWork
	
	def setTempStorage(self, tempStorage):
		self.TempStorage = tempStorage
		return self.TempStorage

	def getTempStorage(self):
		return self.TempStorage

	#def AutoFill(self, a):
	#===========================================================================
	# for key in a:	
	#	if hasattr(self, key):
	#		func = 'set' + key
	#		eval(func, a)
	#===========================================================================
			
	
	
def main():
	chem= chemReagent(Name = 'oren', AllowedBuffer = 'acid')
	print chem.AllKeys
	print chem.AllVals
	print chem.Inputs
	print chem.Name
	print chem.getAllowedBuffer()
	chem.addAllowedBuffer('newBuffer')
	print chem.getName()
	print chem.getAllowedBuffer()
	chem.addUserName('Oren')
	print chem.getUserName()
	return chem
	
if __name__ == '__main__': 	main()	
	
	