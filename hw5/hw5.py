import sys 
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

def read(filename):
	x = []
	y = []
	with open(filename) as file:
		csvreader = csv.reader(file)
		next(csvreader) # skip the header
		for r in csvreader:
			x.append([1, int(r[0])])
			y.append(int(r[1]))

	return np.array(x), np.array(y)

def Q5(beta):
	if (beta[1] > 0):
		return ">"
	elif (beta[1] < 0):
		return "<"
	else:
		return "="

# commands to execute
X, Y = read(sys.argv[1])
#Q3
print("Q3a:")
print(X)
print("Q3b:")
print(Y)
Z = np.dot(np.transpose(X), X)
print("Q3c:")
print(Z)
I = np.linalg.inv(Z)
print("Q3d:")
print(I)
PI = np.dot(I, np.transpose(X)) # pseudo-inverse
print("Q3e:")
print(PI)
hat_beta = np.dot(PI, Y)
print("Q3f:")
print(hat_beta)
#Q4
y_test = hat_beta[0] + (hat_beta[1] * 2021) # 2021 is the test value
print("Q4: " + str(y_test))
#Q5
print("Q5a: " + Q5(hat_beta))
print("Q5b: The calculated sign for beta is negative, so the general trend is negative or",
	"decreasing. This means that the amount of Mendota ice days, and perhaps the amount", 
	"of total ice on Mendota, is on average decreasing from year to year.")
#Q6
x_star = (0-hat_beta[0]) / hat_beta[1]
print("Q6a: " + str(x_star))
print("Q6b: I think the prediction is likely compelling. While looking generally at the", 
	"dataset, I observed how the number of years where the number of ice days exceeds 100", 
	"has generally decreased from decade to decade. From the 1850s until the recent 20 years,",
	"there has been mostly years over 100 ice days. In recent years however,", 
	"it has mostly been below 100 ice days yearly. At the beginning of the data,",
	"the ice days averaged around 120 and now in the past decade, it has become",
	"an average of about 80 ice days. Therefore, it took around 170 years to decrease",
	"the average number of ice days by 40 days. Thus it will take about",
	"another 400 years to decrease the ice days to 0, which aligns with the time",
	"predicted by the model.") 

#Plot
plt.plot(X[:,1], Y, color ="purple")
plt.xlabel("Year")
plt.ylabel("Number of frozen days")
plt.savefig("plot.jpg")


