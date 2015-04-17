import pickle, math
from numpy import multiply as mp
from numpy import argmax
from scipy.sparse import coo_matrix, hstack, bmat
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.pipeline import Pipeline
from sklearn import svm

def main():
	trainDict1 = pickle.load(open('../sepa_detection/detection_train.p'))
	testDict1 = pickle.load(open('../sepa_detection/detection_test.p'))
	trainDict2 = pickle.load(open('../sepa_text/text_train.p'))
	testDict2 = pickle.load(open('../sepa_text/text_test.p'))
	data = pickle.load(open('../classification/data.p'))
	# print 'guassnb'
	# for alpha in [0.1, 0.2, 0.5, 1, 5, 10, 100]:
	# 	featueCombine(alpha, trainDict1, testDict1, trainDict2, testDict2, data, mode = 'guassnb')
	print 'mutlinb'
	for alpha in range(10, 100):
		featueCombine(alpha, trainDict1, testDict1, trainDict2, testDict2, data, mode = 'multinb')

# alpha = 0.21, test accuracy = 87.46%, train accuracy = 94.33%, val accuracy = 89.05%
def clfCombine():
	clf_1 = pickle.load(open('../sepa_detection/detection_cls.p'))
	clf_2 = pickle.load(open('../sepa_text/text_cls.p'))
	print clf_2.steps[-1][1].classes_
	print clf_1.classes_
	print '-------------------'
	print 'Loading data...'
	train1 = []
	train2 = []
	trainY = []
	test1 = []
	test2 = []
	testY = []
	val1 = []
	val2 = []
	valY = []
	trainErrL = []
	testErrL = []
	valErrL = []

	data = pickle.load(open('../classification/data.p'))


	trainDict1 = pickle.load(open('../sepa_detection/detection_train.p'))
	testDict1 = pickle.load(open('../sepa_detection/detection_test.p'))
	valDic1 = pickle.load(open('../sepa_detection/detection_val.p'))
	trainDict2 = pickle.load(open('../sepa_text/text_train.p'))
	testDict2 = pickle.load(open('../sepa_text/text_test.p'))
	valDic2 = pickle.load(open('../sepa_text/text_val.p'))
	for i in trainDict1:
		train1.append(trainDict1[i])
		train2.append(trainDict2[i])
		trainY.append(data[i]['class'])
	for i in testDict1:
		test1.append(testDict1[i])
		test2.append(testDict2[i])
		testY.append(data[i]['class'])
	for i in valDic1:
		val1.append(valDic1[i])
		val2.append(valDic2[i])
		valY.append(data[i]['class'])



	print '-------------------'
	for i in range(1, 100):
		alpha = i/100.0
		print alpha
		c = clf(clf_1, clf_2, alpha)

		prob = c(train1, train2)
		rlt = argmax(prob, axis=1)
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == trainY[i]:
				cor +=1
		trainErr = float(cor)/cnt
		trainErrL.append(trainErr)

		prob = c(val1, val2)
		rlt = argmax(prob, axis=1)
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == valY[i]:
				cor +=1
		valErr = float(cor)/cnt
		valErrL.append(valErr)

		prob = c(test1, test2)
		rlt = argmax(prob, axis=1)
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == testY[i]:
				cor +=1
		testErr = float(cor)/cnt
		testErrL.append(testErr)
	print
	print '-------------------'
	# print trainErrL
	# print valErrL
	# print testErrL

	pickle.dump(trainErrL, open('trainError.p', 'wb'))
	pickle.dump(testErrL, open('testError.p', 'wb'))
	pickle.dump(valErrL, open('valError.p', 'wb'))
	plt.plot(range(1, 100), trainErrL, range(1, 100), valErrL, range(1, 100), testErrL)
	plt.show()

def clf(clf_1, clf_2, alpha):
	def cls(X1, X2):
		prob2 = clf_2.predict_log_proba(X2)
		prob1 = clf_1.predict_log_proba(X1)
		prob = mp(alpha, prob1)+mp(1-alpha, prob2)
		return prob
	return cls



# multiNB
# train accuracy: 0.391938390955
# test accuracy: 0.382585751979
# GuassianNB
# train accuracy: 0.79485498935
# test accuracy: 0.142480211082
# svm
# train accuracy: 0.33704735376
# test accuracy: 0.339050131926
def featueCombine(alpha, trainDict1 = pickle.load(open('../sepa_detection/detection_train.p')),
				  testDict1 = pickle.load(open('../sepa_detection/detection_test.p')),
				  trainDict2 = pickle.load(open('../sepa_text/text_train.p')),
				  testDict2 = pickle.load(open('../sepa_text/text_test.p')),
				  data = pickle.load(open('../classification/data.p')),
				  mode = 'svm'):
	
	print alpha
	# valDic1 = pickle.load(open('../sepa_detection/detection_val.p'))
	# valDic2 = pickle.load(open('../sepa_text/text_val.p'))
	
	train1 = []
	train2 = []
	trainY = []
	test1 = []
	test2 = []
	testY = []
	# val1 = []
	# val2 = []
	# valY = []

	if mode == 'svm':
		for i in trainDict1:
			train1.append([x*alpha for x in trainDict1[i]])
			# tmp = []
			# for j in trainDict1[i]:
			# 	tmp.append(math.exp(j))
			# train1.append(tmp)
			train2.append(trainDict2[i])
			trainY.append(data[i]['class'])
		for i in testDict1:
			test1.append([x*alpha for x in testDict1[i]])
			# tmp = []
			# for j in testDict1[i]:
			# 	tmp.append(math.exp(j))
			# test1.append(tmp)
			test2.append(testDict2[i])
			testY.append(data[i]['class'])
		# for i in valDic1:
		# 	val1.append(valDic1[i])
		# 	val2.append(valDic2[i])
		# 	valY.append(data[i]['class'])
		print 'data prepared'
		transfer = Pipeline([('vect', CountVectorizer()),
							('tfidf', TfidfTransformer())])

		train = []
		test = []

		transfer.fit(train2)
		tmpstart = len(transfer.steps[0][1].vocabulary_)
		row = []
		col = []
		testdata = []
		for i in range(len(test1)):
			for j in range(len(test1[i])):
				testdata.append(test1[i][j])
				row.append(i)
				col.append(tmpstart+j)
		tmp = transfer.fit_transform(test2).toarray()
		for i in range(len(tmp)):
			for j in range(len(tmp)):
				if tmp[i][j]!=0:
					testdata.append(tmp[i][j])
					row.append(i)
					col.append(j)
		test = coo_matrix((testdata, (row, col)))
		# print test.shape

		traindata = []
		row = []
		col = []
		for i in range(len(train1)):
			for j in range(len(train1[i])):
				traindata.append(train1[i][j])
				row.append(i)
				col.append(j+tmpstart)
		tmp = transfer.fit_transform(train2).toarray()
		for i in range(len(tmp)):
			for j in range(len(tmp)):
				if tmp[i][j]!=0:
					traindata.append(tmp[i][j])
					row.append(i)
					col.append(j)

		train = coo_matrix((traindata, (row, col)))
		# print train.shape
		print 'feature combined'

		# nb = MultinomialNB()
		# nb = GaussianNB()
		nb = svm.SVC()
		nb.fit(train.toarray(), trainY)

		print 'model fitted'

		rlt = nb.predict(train.toarray())
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == trainY[i]:
				cor+=1
		print 'train accuracy:', float(cor)/cnt

		rlt = nb.predict(test.toarray())
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == testY[i]:
				cor +=1 
		print 'test accuracy:', float(cor)/cnt
		return

	for i in trainDict1:
		tmp = []
		for j in trainDict1[i]:
			tmp.append(math.exp(j)*alpha)
		train1.append(tmp)
		train2.append(trainDict2[i])
		trainY.append(data[i]['class'])
	for i in testDict1:
		tmp = []
		for j in testDict1[i]:
			tmp.append(math.exp(j)*alpha)
		test1.append(tmp)
		test2.append(testDict2[i])
		testY.append(data[i]['class'])
	# for i in valDic1:
	# 	val1.append(valDic1[i])
	# 	val2.append(valDic2[i])
	# 	valY.append(data[i]['class'])
	transfer = Pipeline([('vect', CountVectorizer()),
						('tfidf', TfidfTransformer())])

	train = []
	test = []

	transfer.fit(train2)
	tmpstart = len(transfer.steps[0][1].vocabulary_)
	row = []
	col = []
	testdata = []
	for i in range(len(test1)):
		for j in range(len(test1[i])):
			testdata.append(test1[i][j])
			row.append(i)
			col.append(tmpstart+j)
	tmp = transfer.fit_transform(test2).toarray()
	for i in range(len(tmp)):
		for j in range(len(tmp)):
			if tmp[i][j]!=0:
				testdata.append(tmp[i][j])
				row.append(i)
				col.append(j)
	test = coo_matrix((testdata, (row, col)))
	# print test.shape

	traindata = []
	row = []
	col = []
	for i in range(len(train1)):
		for j in range(len(train1[i])):
			traindata.append(train1[i][j])
			row.append(i)
			col.append(j+tmpstart)
	tmp = transfer.fit_transform(train2).toarray()
	for i in range(len(tmp)):
		for j in range(len(tmp)):
			if tmp[i][j]!=0:
				traindata.append(tmp[i][j])
				row.append(i)
				col.append(j)

	train = coo_matrix((traindata, (row, col)))
	# print train.shape
	print 'feature combined'

	if mode == 'multinb':
		nb = MultinomialNB()
		# nb = GaussianNB()
		# nb = svm.SVC()
		nb.fit(train.toarray(), trainY)

		print 'model fitted'

		rlt = nb.predict(train.toarray())
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == trainY[i]:
				cor+=1
		print 'train accuracy:', float(cor)/cnt

		rlt = nb.predict(test.toarray())
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == testY[i]:
				cor +=1 
		print 'test accuracy:', float(cor)/cnt
		return
	if mode == 'guassnb':
		# nb = MultinomialNB()
		nb = GaussianNB()
		# nb = svm.SVC()
		nb.fit(train.toarray(), trainY)

		print 'model fitted'

		rlt = nb.predict(train.toarray())
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == trainY[i]:
				cor+=1
		print 'train accuracy:', float(cor)/cnt

		rlt = nb.predict(test.toarray())
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == testY[i]:
				cor +=1 
		print 'test accuracy:', float(cor)/cnt
# train accuracy: 0.923971817139
# test accuracy: 0.82981530343
def svmCombine():
	clf_1 = pickle.load(open('../sepa_detection/detection_cls.p'))
	clf_2 = pickle.load(open('../sepa_text/text_cls.p'))
	print clf_2.steps[-1][1].classes_
	print clf_1.classes_
	print '-------------------'
	print 'Loading data...'
	train1 = []
	train2 = []
	trainY = []
	test1 = []
	test2 = []
	testY = []
	val1 = []
	val2 = []
	valY = []


	data = pickle.load(open('../classification/data.p'))


	trainDict1 = pickle.load(open('../sepa_detection/detection_train.p'))
	testDict1 = pickle.load(open('../sepa_detection/detection_test.p'))
	valDict1 = pickle.load(open('../sepa_detection/detection_val.p'))

	trainDict2 = pickle.load(open('../sepa_text/text_train.p'))
	testDict2 = pickle.load(open('../sepa_text/text_test.p'))
	valDict2 = pickle.load(open('../sepa_text/text_val.p'))

	for i in trainDict1:
		train1.append(trainDict1[i])
		train2.append(trainDict2[i])
		trainY.append(data[i]['class'])
	for i in testDict1:
		test1.append(testDict1[i])
		test2.append(testDict2[i])
		testY.append(data[i]['class'])

	for i in valDict1:
		val1.append(valDict1[i])
		val2.append(valDict2[i])
		valY.append(data[i]['class'])


	prob1 = clf_1.predict(train1)
	prob2 = clf_2.predict(train2)
	
	train = []
	for i in range(len(prob1)):
		train.append([prob1[i], prob2[i]])

	test = []
	prob1 = clf_1.predict(test1)
	prob2 = clf_2.predict(test2)
	for i in range(len(prob1)):
		test.append([prob1[i], prob2[i]])

	val = []
	prob1 = clf_1.predict(val1)
	prob2 = clf_2.predict(val2)
	for i in range(len(prob1)):
		val.append([prob1[i], prob2[i]])

	print '-------------------'
	trainErrL = []
	testErrL = []
	valErrL = []
	for c in range(1, 100):
		print c
		svm_clf = svm.SVC(C=float(c)/100)
		svm_clf.fit(train, trainY)
		rlt = svm_clf.predict(train)
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == trainY[i]:
				cor+=1
		# print 'train accuracy:', float(cor)/cnt
		trainErrL.append(float(cor)/cnt)


		rlt = svm_clf.predict(test)
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == testY[i]:
				cor +=1
		# print 'test accuracy:', float(cor)/cnt
		testErrL.append(float(cor)/cnt)

		rlt = svm_clf.predict(val)
		cnt = len(rlt)
		cor = 0
		for i in range(cnt):
			if rlt[i] == valY[i]:
				cor +=1
		# print 'test accuracy:', float(cor)/cnt
		valErrL.append(float(cor)/cnt)
	x = range(1, 100)
	plt.plot(x, trainErrL, x, valErrL, x, testErrL)
	plt.show()





if __name__ == '__main__':
	main()