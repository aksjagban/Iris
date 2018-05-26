import re, cmath, os, sys
from math import sqrt

print("\n***** This script classifies the species of iris on the basis of sepal length, sepal width, petal length and petal width. *****\n")


#	Reading 'iris.txt' file.

f = open('iris.txt')
lines = f.readlines()
f.close()


#	Creating lists of sepal length, sepal width, petal length, petal width and list of these parametres.

sepal_length = []
for line in lines:
	sl_regex = re.search(r'.*?(?=(,\d\.\d){3})', line)
	if sl_regex:
		sepal_length.append(sl_regex.group())

sepal_width = []
for line in lines:
	sw_regex = re.search(r'(?<=\d\.\d,).*?(?=(,\d\.\d){2})', line)
	if sw_regex:
		sepal_width.append(sw_regex.group())

petal_length = []
for line in lines:
	pl_regex = re.search(r'(?<=(\d\.\d,){2}).*?(?=,\d\.\d)', line)
	if pl_regex:
		petal_length.append(pl_regex.group())

petal_width = []
for line in lines:
	pw_regex = re.search(r'(?<=(\d\.\d,){3}).*(?=,\D*)', line)
	if pw_regex:
		petal_width.append(pw_regex.group())

parametres = [sepal_length, sepal_width, petal_length, petal_width]


#	Calculating statistical values to use 3-sigma test for classifying the species of iris.
#	Set of values are calculated for each 4 parameter and each 3 species.

sums = []
avg = []
devsq = []
var = []
sigma3 = []
min_sigma3 = []
max_sigma3 = []
listoflist = [sums, avg, devsq, var, sigma3, min_sigma3, max_sigma3]

def zeros ():
	for g in range(0, len(listoflist)):
		for h in range(0, 3):
			listoflist[g].append([])
			listoflist[g][h] = [0,0,0,0]
	return
zeros ()

def values ():
	mini = 0
	maxi = 50
	for h in range(0, 3):
		for i in range(0, len(parametres)):
			for j in range(mini, maxi):
				sums[h][i] = float(sums[h][i]) + float(parametres[i][j])		#Sum of values.
			avg[h][i] = sums[h][i] / 50		#Mean of sum.
			for j in range(mini, maxi):
				devsq[h][i] = float(devsq[h][i]) + (float(parametres[i][j]) - float(avg[h][i])) * (float(parametres[i][j]) - float(avg[h][i]))		#Sum of the squared deviations from the mean.
				var[h][i] = devsq[h][i] / 50		#Variance.
				sigma3[h][i] = 3 * sqrt(var[h][i])		#3-sigma value.
				min_sigma3[h][i] = abs(avg[h][i] - 3 * sqrt(var[h][i]))		#Minimal 3-sigma limit.
				max_sigma3[h][i] = abs(avg[h][i] + 3 * sqrt(var[h][i]))		#Maximal 3-sigma limit.
		mini = mini + 50
		maxi = maxi + 50
	return
values ()


#	Inputting values of your parametres.

your_sepal_length = 0
your_sepal_width = 0
your_petal_length = 0
your_petal_width = 0

while True:
	try:
		your_sepal_length = float(input("Please give the sepal length: "))
		break
	except:
		print("Sepal length must be a number!")

while True:
	try:
		your_sepal_width = float(input("Please give the sepal width: "))
		break
	except:
		print("Sepal width must be a number!")

while True:
	try:
		your_petal_length = float(input("Please give the petal length: "))
		break
	except:
		print("Petal length must be a number!")

while True:
	try:
		your_petal_width = float(input("Please give the petal width: "))
		break
	except:
		print("Petal width must be a number!")


#	Returning species of iris on the basis of 3-sigma test conditions.

result = ""

def check (your_sepal_length, your_sepal_width, your_petal_length, your_petal_width):

	if ((your_sepal_length >= min_sigma3[0][0]) and (your_sepal_length <= max_sigma3[0][0]) and (your_sepal_width >= min_sigma3[0][1]) and (your_sepal_width <= max_sigma3[0][1]) and (your_petal_length >= min_sigma3[0][2]) and (your_petal_length <= max_sigma3[0][2]) and (your_petal_width >= min_sigma3[0][3]) and (your_petal_width <= max_sigma3[0][3])):
		result = "setosa"
		return result

	elif ((your_sepal_length >= min_sigma3[1][0]) and (your_sepal_length <= max_sigma3[1][0]) and (your_sepal_width >= min_sigma3[1][1]) and (your_sepal_width <= max_sigma3[1][1]) and (your_petal_length >= min_sigma3[1][2]) and (your_petal_length <= max_sigma3[1][2]) and (your_petal_width >= min_sigma3[1][3]) and (your_petal_width <= max_sigma3[1][3])):
		result = "versicolor"
		return result

	elif ((your_sepal_length >= min_sigma3[2][0]) and (your_sepal_length <= max_sigma3[2][0]) and (your_sepal_width >= min_sigma3[2][1]) and (your_sepal_width <= max_sigma3[2][1]) and (your_petal_length >= min_sigma3[2][2]) and (your_petal_length <= max_sigma3[2][2]) and (your_petal_width >= min_sigma3[2][3]) and (your_petal_width <= max_sigma3[2][3])):
		result = "virginica"
		return result

	else:
		result = "unknown species"
		return result

print ("\nThis is "+check (your_sepal_length, your_sepal_width, your_petal_length, your_petal_width)+".\n")


#	Checking if all values from 'iris.txt' are consistent with theoretical ones calculated by 3-sigma test, by comparing 'iris.txt' with generated 'report.txt'.

report = open('report.txt','w')
report.write("sepal_length,sepal_width,petal_length,petal_width,species\n")

for i in range(0, 150):
	your_sepal_length = sepal_length[i]
	your_sepal_width = sepal_width[i]
	your_petal_length = petal_length[i]
	your_petal_width = petal_width[i]

	result = str(check (float(your_sepal_length), float(your_sepal_width), float(your_petal_length), float(your_petal_width)))
	check (float(your_sepal_length), float(your_sepal_width), float(your_petal_length), float(your_petal_width))
	report.write((str(your_sepal_length)+","+str(your_sepal_width)+","+str(your_petal_length)+","+str(your_petal_width)+","+result))
	report.write("\n")

report.write("\n")
report.close()


#	Comparing lines from 'iris.txt' with lines 'report.txt' and generating 'lines.txt' including different lines.

file1 = open('iris.txt', 'r').readlines()
file2 = open('report.txt', 'r').readlines()
out = []
count = 1

report = open('lines.txt', 'w')
report.write("Here are the numbers of lines that distinguish file 'iris.txt' from file 'report.txt':\n\n")

for i in file1:
	logic = False
	for j in file2:
		if (i == j):
			logic = True
	if not logic:
		out.append(count)
	count = count + 1
for o in out:
	report.write(str(o)+"\n")

report.write("\nIn these lines species from 'iris.txt' are not consistent with theoretical species from 'report.txt', calculated on the basis of statistical 3-sigma test.\nSome values from these lines lay outside the 3-sigma ranges.\nThat is why 16 virginica irises have been classified as versicolor and 1 setosa iris has been classified as unknown.\n")
report.close()


