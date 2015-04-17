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

# train accuracy 0.966573816156 
# test accuracy 0.852242744063 
# val accuracy 0.870712401055 

def clf(clf_2, alpha):
	def cls(X1, X2):
		prob1 = X1
		prob2 = clf_2.predict_log_proba(X2)
		prob = mp(alpha, prob1)+mp(1-alpha, prob2)
		return prob
	return cls


clf_2 = pickle.load(open('../sepa_text/text_cls.p'))

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


trainDict1 = pickle.load(open('../sepa_train_class/train_rlt.p'))
testDict1 = pickle.load(open('../sepa_train_class/test_rlt.p'))
valDic1 = pickle.load(open('../sepa_train_class/val_rlt.p'))
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
	c = clf(clf_2, alpha)

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

# print 'train accuracy', trainErrL[41], trainErrL[42]
# print 'test accuracy', testErrL[41], testErrL[42]
# print 'val accuracy', valErrL[41], valErrL[42]

pickle.dump(trainErrL, open('trainError.p', 'wb'))
pickle.dump(testErrL, open('testError.p', 'wb'))
pickle.dump(valErrL, open('valError.p', 'wb'))
plt.plot(range(1, 100), trainErrL, range(1, 100), valErrL, range(1, 100), testErrL)
plt.show()

