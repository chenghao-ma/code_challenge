import json
from collections import defaultdict
import numpy as np
from sklearn.cluster import SpectralClustering
from sklearn import preprocessing
import matplotlib.pyplot as plt

def replace(list,element,new_element):
	rep = [new_element if x == element else x for x in list]
	return rep

def mean(list):
	sum = 0
	count = 0
	for i in list:
		if i != 0:
			sum+=i
			count+=1
	return sum/count

def cluster():
	with open("100_info.json", 'r') as f:
	    file = json.loads(f.read())
	arr = list(file.values())
	# print(arr[0])
	edu_code = []
	attribute = []
	for i in arr:
		if 'education' in i.keys() and i['education'] != []:
			if 'college' in i['education'][0].lower():
				edu_code.append(3)
			elif 'un' in i['education'][0].lower():
				edu_code.append(4)
			elif 'tafe' in i['education'][0].lower():
				edu_code.append(2)
			else:
				edu_code.append(1)
		else:
			edu_code.append(0)
		attribute += i['skill']

	skill_code = []
	diction = {}
	for key in attribute:
		diction[key] = diction.get(key, 0) + 1
	for i in arr:
		score = 0
		try:
			for j in i['skill']:
				score += diction[j]
			skill_code.append(score)
		except:
			skill_code.append(0)
	avg = mean(skill_code)
	skill_code = replace(skill_code, 0, avg)
	X = preprocessing.scale(edu_code)
	Y = preprocessing.scale(skill_code)
	points = []
	for i in range(len(X)):
		points.append([X[i],Y[i]])
	points = np.array(points)
	clustering = SpectralClustering(n_clusters=3,assign_labels="discretize",random_state=0).fit(points)
	mark = ['or', 'ob', 'og']
	return points,mark,clustering


def main():
	points,mark,clustering = cluster()
	for i in range(len(points)):
		plt.plot(points[i,0],points[i,1],mark[clustering.labels_[i]])
	plt.show()
