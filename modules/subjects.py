class Subjects:
	no_of_classes=0
	sub_code=""
	subTeacher=""
	def __init__(self,sub_code,subTeacher,no_of_classes,):
		self.sub_code=sub_code
		self.no_of_classes=no_of_classes
		self.subTeacher=subTeacher
	def getSubCode(self):
		return self.sub_code
	def getSubTeacherName(self):
		return self.subTeacher
	def getNoOfClasses(self):
		return self.no_of_classes
	