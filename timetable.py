#Importing packages
import random
from copy import deepcopy
from tkinter import W
from modules.departments import *
from modules.teachers import *
from modules.subjects import *
	
#Reading a file
def readFile():
	inp=open('input.txt','r')
	departments=[]
	teachers=[]
	index=0
	flag=0
	noOfClassesAllSem={}
	ind=0
	for i in inp.readlines():
		data=i.split(' ')

		if(len(data)==1):
			flag=1
			continue
		if flag==0:
			subjects=[]
			noOfClassesEachSem={}
			for sub in range(1,len(data),3):
				noOfClassesEachSem[data[sub+1]]=int(data[sub+2])
				subjects.append(Subjects(data[sub],data[sub+1],data[sub+2]))
			noOfClassesAllSem[ind]=noOfClassesEachSem
			departments.append(Department(data[0],(len(data)-1)//3,subjects))
			index+=1
		else:
			teachers.append(Teacher(data[0],data[1]))
			# print(data[0]+" "+data[1])
		ind+=1
	

	inp.close()
	# print(d)
	return (departments,teachers,noOfClassesAllSem)
def fitness(departments,noOfClassesAllSem):
	count=0
	for i in range(4):
		for j in range(5):
			for k in range(6):
				if(departments[i][j][k]!="None"):
					if(noOfClassesAllSem[i][departments[i][j][k]]<=0):
						count+=1
					noOfClassesAllSem[i][departments[i][j][k]]-=1
	for i in range(5):
		for j in range(6):
			noOfClassesAllSem={}
			for k in range(4):
				if(departments[k][i][j]!="None"):
					if departments[k][i][j] in noOfClassesAllSem.keys():
						noOfClassesAllSem[departments[k][i][j]]+=1
						count+=1
					else:
						noOfClassesAllSem[departments[k][i][j]]=1
	return count
def crossover(parent1,parent2):
	dept_s=random.choice([i for i in range(4)])
	dept_f=random.choice([i for i in range(dept_s,4)])
	row_s=random.choice([i for i in range(5)])
	row_f=random.choice([i for i in range(row_s,5)])
	col_s=random.choice([i for i in range(6)])
	col_f=random.choice([i for i in range(col_s,6)])
	for i in range(dept_s,dept_f+1):
		for j in range(row_s,row_f+1):
			for k in range(col_s,col_f+1):
				parent1[i][j][k],parent2[i][j][k]=parent2[i][j][k],parent1[i][j][k]
	# print(parent1)
	return (parent1,parent2)
def mutation(parent1,parent2):
	child_chromosome=[]
	for i in range(4):
		a=[]
		for j in range(5):
			b=[]
			for k in range(6):
				prob=random.random()
				if(prob<0.45):
					b.append(parent1[i][j][k])
				else:
					b.append(parent2[i][j][k])
			a.append(b)
		child_chromosome.append(a)
	return child_chromosome
def removeClashes(ans):
	arr=[[] for i in range(4)]
	for i in range(5):
		for j in range(6):
			teachers=[]
			for k in range(4):
				if(ans[k][i][j]!="None"):
					if ans[k][i][j] in teachers:
						arr[k].append(ans[k][i][j])
						ans[k][i][j]="None"
					else:
						teachers.append(ans[k][i][j]);
	for k in  range(1,4):
		for l in arr[k]:
			flag=0;
			for i in range(5):
				for j in range(6):
					teachers=[]
					for kk in range(4):
						teachers.append(ans[kk][i][j])
						if l in teachers:
							break;
					if l not in teachers:
						ans[k][i][j]=l
						flag=1
						break
				if flag==1:
					break
	# print(arr)
	return ans

def stableNoOfSubs(ans,noOfClassesAllSem):
	for i in range(4):
		for j in range(5):
			for k in range(6):
				if(ans[i][j][k]!="None"):
					noOfClassesAllSem[i][ans[i][j][k]]-=1
					if(noOfClassesAllSem[i][ans[i][j][k]]<0):
						ans[i][j][k]="None"
		# print(i," ",noOfClassesAllSem[i])		
	for i in range(4):
		for key,val in noOfClassesAllSem[i].items():
			for j in range(val):
				for k in range(5):
					for l in range(6):
						if(ans[i][k][l]=="None"):
							ans[i][k][l]=key
	return ans
def createPopulation(departments,dic):
	dic2=deepcopy(dic)
	population=[[[["" for k in range(6)] for j in range(5)] for i in range(len(departments))] for ii in range(10)]
	# print(population)
	teachearArr=[]
	for i in departments:
		listOfSubs=i.getSubs()
		# print(len(listOfSubs))
		cnt=0
		temp=[]
		for j in range(len(listOfSubs)):
			for k in range(int(listOfSubs[j].getNoOfClasses())):
				temp.append(listOfSubs[j].getSubTeacherName())
				cnt+=1
		for i in range(30-cnt):
			temp.append("None")
		teachearArr.append(temp)
	ii=[0,1,2,3,4]
	jj=[0,1,2,3,4,5]
	for i in range(10):
		for j in range(4):
			
			index=0
			while(index<30):
				x=random.choice(ii)
				y=random.choice(jj)
				if(len(population[i][j][x][y])==0):
					population[i][j][x][y]=teachearArr[j][index]
					index+=1
	population_size=10
	err=10000
	ans=[]
	while True:
		fit=[]
		for i in range(len(population)):
			fit.append((i,fitness(population[i],dic)))
		fit=sorted(fit,key=lambda x:x[1])
		a1,b1=fit[0]
		a2,b2=fit[1]
		# print(a1," ",b1)
		if(err>b1):
			err=b1
			ans=population[a1]
		if(b1==0 or len(population) <= 2):
			# print(population[a1])
			break
		(population[a1],population[a2])=crossover(population[a1],population[a2])
		size=len(population)//2
		new_population=[]
		for i in range(size):
			new_population.append(population[i])
		new_population.append(mutation(population[a1],population[a2]))
		population=new_population
	# print(ans)
	# print(dic2)
	ans=stableNoOfSubs(ans,dic2)
	# print(err)
	# print(ans)
	ans=removeClashes(ans)
	print(ans)
	storeOutput(ans)



def storeOutput(generatedRoster) :
	f = open('schedule.txt','w')
	f.write(str(generatedRoster))
def main():
	(department,teachers,dic)=readFile()
	createPopulation(department,dic)
	# print(teachers[0].getTeacherName())
		
if __name__=='__main__':
	main()