import pickle, math
from sklearn import svm
# test accuracy 0.164907651715
# train accuracy: 0.1643454039

def main():
	data = pickle.load(open('../classification/data.p'))
	trainDict = pickle.load(open('cls_train.p'))
	testDict = pickle.load(open('cls_test.p'))

	train = []
	trainY = []
	test = []
	testY = []

	for i in trainDict:
		tmp = []
		for j in trainDict[i]:
			if math.isnan(j) or math.isinf(j):
				j = 0.5
			tmp.append(j)
		train.append(tmp)
		trainY.append(data[i]['class'])

	for i in testDict:
		tmp = []
		for j in testDict[i]:
			if math.isnan(j) or math.isinf(j):
				j = 0.5
			tmp.append(j)
		test.append(tmp)
		testY.append(data[i]['class'])
		
	cls = svm.SVC()
	cls.fit(train, trainY)

	rlt = cls.predict(test)

	cnt = len(rlt)
	cor = 0

	for i in range(cnt):
		if rlt[i] == testY[i]:
			cor+=1
	print 'test error', float(cor)/cnt

	rlt = cls.predict(train)
	cnt = len(rlt)
	cor = 0
	for i in range(cnt):
		if rlt[i] == trainY[i]:
			cor +=1
	print 'train error:', float(cor)/cnt




if __name__ == '__main__':
	main()