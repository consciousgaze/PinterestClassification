import pickle, math
from sklearn import svm
from numpy import argmax

def main():
	prepare_result()


# sole image result:
# train error: 0.993609700147
# test error: 0.724274406332
def show_result():
	data = pickle.load(open('../classification/data.p'))
	trainDict = pickle.load(open('predict_train_result.p'))
	testDict = pickle.load(open('predict_test_result.p'))

	cor = 0
	cnt = len(testDict)
	for i in testDict:
		if argmax(testDict[i]) == data[i.split('.')[0]]['class']:
			cor+=1

	print 'test accuracy:', float(cor)/cnt


	cor = 0
	cnt = len(trainDict)
	for i in trainDict:
		if argmax(trainDict[i]) == data[i.split('.')[0]]['class']:
			cor+=1

	print 'train accuracy:', float(cor)/cnt



def prepare_result():
	data = pickle.load(open('../classification/data.p'))
	trainDict = pickle.load(open('predict_train_result.p'))
	testDict = pickle.load(open('predict_test_result.p'))
	valDict = pickle.load(open('predict_test_result.p'))

	for i in ['train', 'test', 'val']:
		d = pickle.load(open('predict_'+i+'_result.p'))
		ready = {}
		for ii in d:
			ID = ii.split('.')[0]
			ready[ID] = d[ii][:10]
		pickle.dump(ready, open(i+'_rlt.p', 'wb'))








if __name__ == '__main__':
	main()