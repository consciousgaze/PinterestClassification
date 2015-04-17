import pickle, math
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
# test error 0.777044854881
# train error 0.792233327872

def main():
	data = pickle.load(open('../classification/data.p'))
	trainDict = pickle.load(open('detection_train.p'))
	testDict = pickle.load(open('detection_test.p'))
	train = []
	trainY = []
	test = []
	testY = []
	for i in trainDict:
		train.append(trainDict[i])
		trainY.append(data[i]['class'])
	for i in testDict:
		test.append(testDict[i])
		testY.append(data[i]['class'])
	cls = svm.SVC(probability=True)
	cls.fit(train, trainY)
	pickle.dump(cls, open('detection_cls.p', 'wb'))
	testRLT = cls.predict(test)
	cnt = 0
	cor = 0
	for i in range(len(testRLT)):
		cnt+=1
		if testRLT[i] == testY[i]:
			cor+=1
	print 'test error', float(cor)/cnt


	rlt = cls.predict(train)
	cnt = 0
	cor = 0
	for i in range(len(rlt)):
		cnt+=1
		if rlt[i] == trainY[i]:
			cor+=1
	print 'train error', float(cor)/cnt

# test error 0.634564643799
# train error 0.632311977716

def naiveBayes():
	data = pickle.load(open('../classification/data.p'))
	trainDict = pickle.load(open('detection_train.p'))
	testDict = pickle.load(open('detection_test.p'))
	train = []
	trainY = []
	test = []
	testY = []
	for i in trainDict:
		# train.append(trainDict[i])
		tmp = []
		for j in trainDict[i]:
			tmp.append(math.exp(j))
		train.append(tmp)
		trainY.append(data[i]['class'])
	for i in testDict:
		# test.append(testDict[i])
		tmp = []
		for j in testDict[i]:
			tmp.append(math.exp(j))
		test.append(tmp)
		testY.append(data[i]['class'])
	cls = MultinomialNB()
	cls.fit(train, trainY)
	# pickle.dump(cls, open('detection_cls.p', 'wb'))
	testRLT = cls.predict(test)
	cnt = 0
	cor = 0
	for i in range(len(testRLT)):
		cnt+=1
		if testRLT[i] == testY[i]:
			cor+=1
	print 'test error', float(cor)/cnt


	rlt = cls.predict(train)
	cnt = 0
	cor = 0
	for i in range(len(rlt)):
		cnt+=1
		if rlt[i] == trainY[i]:
			cor+=1
	print 'train error', float(cor)/cnt






if __name__ == '__main__':
	main()