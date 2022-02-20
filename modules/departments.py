class Department:
	name=""
	no_of_subs=0
	subs=[]
	def __init__(self,name,no_of_subs,subs):
		self.name=name
		self.no_of_subs=no_of_subs
		self.subs=subs
	def getDepartmentName(self):
		return self.name
	def getNoOfSubs(self):
		return self.no_of_subs
	def getSubs(self):
		return self.subs