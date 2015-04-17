from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix

import pickle

# test accuracy: 0.800791556728
# train accuracy: 0.901032279207


def main():
	data = pickle.load(open('../classification/data.p'))
	trainDict = pickle.load(open('text_train.p'))
	testDict = pickle.load(open('text_test.p'))

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


	clf = Pipeline([('vect', CountVectorizer()),
					('tfidf', TfidfTransformer()),
					('clf', MultinomialNB())])

	clf.fit(train, trainY)

	pickle.dump(clf, open('text_cls.p', 'wb'))

	rlt = clf.predict(test)
	cnt = len(rlt)
	cor = 0
	for i in range(cnt):
		if rlt[i] == testY[i]:
			cor+=1
	print 'test error:', float(cor)/cnt, cnt

	rlt = clf.predict(train)
	cnt = len(rlt)
	cor = 0
	for i in range(cnt):
		if rlt[i] == trainY[i]:
			cor+=1
	print 'train error:', float(cor)/cnt, cnt





if __name__ == '__main__':
	main()