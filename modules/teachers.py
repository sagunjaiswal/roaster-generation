class Teacher:
	name=""
	subCode=""
	def __init__(self,name,subCode):
		self.name=name
		self.subCode=subCode
	def getTeacherName(self):
		return self.name
	def getSubjectCode(self):
		return self.subCode