import pickle, time, os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from util import *
import shutil
import pandas as pd
# data.p is in the format pin_id:{text, class}
# data_set.p is in the format class:[{id, text, image}]
# sets.p is in the format {train:[], test:[], val:[]}


home = os.path.expanduser('~')
root='~/image'
root = os.path.expanduser(root)
train = root+'/train'
val = root+'/val'
test = root+'/test'

def main():
	tmp = pickle.load(open('detection_train.p', 'rb'))
	for i in tmp:
		if len(tmp[i]) != 200:
			print i, len(tmp[i])


def process_detection(t, n):
	rlts = {}
	for i in range(n+1):
		print i
		tmp = pd.read_hdf('detection_rlts/'+t+str(i)+'_output.h5', 'df')
		indices = set(tmp.index)
		for idx in indices:
			try:
				pred = tmp.prediction[idx].values
				objects = [[] for tmpi in range(200)]
				for window in pred:
					for cls in range(200):
						objects[cls].append(window[cls])
				rlt = []
				for cls in range(200):
					rlt.append(max(objects[cls]))
				rlts[idx] = rlt
			except:
				print idx
	return rlts






	







def prepare_image(data, clss):
	shutil.rmtree(root)
	os.mkdir(root)
	os.mkdir(train)
	os.mkdir(val)
	os.mkdir(test)

	tr = open(home+'/train.txt', 'w')
	te = open(home+'/test.txt', 'w')
	va = open(home+'/val.txt', 'w')

	for cls in data:
		c = clss[cls]
		l = len(data[cls])
		d = int(l/10)
		tst = data[cls][:d]
		vld = data[cls][d:2*d]
		trn = data[cls][2*d:]

		for p in trn:
			tr.write(p['id']+'.jpg '+str(c)+'\n')
			URL = p['image']
			tmpFile = cStringIO.StringIO(urllib.urlopen(URL).read())
			img = Image.open(tmpFile)
			img = img.resize((256, 256), Image.ANTIALIAS)
			if img.mode != 'RGB':
				img = img.convert('RGB')
			img.save(train+'/'+p['id']+'.jpg')

		for p in tst:
			te.write(p['id']+'.jpg '+str(c)+'\n')
			URL = p['image']
			tmpFile = cStringIO.StringIO(urllib.urlopen(URL).read())
			img = Image.open(tmpFile)
			img = img.resize((256, 256), Image.ANTIALIAS)
			if img.mode != 'RGB':
				img = img.convert('RGB')
			img.save(test+'/'+p['id']+'.jpg')

		for p in vld:
			va.write(p['id']+'.jpg '+str(c)+'\n')
			URL = p['image']
			tmpFile = cStringIO.StringIO(urllib.urlopen(URL).read())
			img = Image.open(tmpFile)
			img = img.resize((256, 256), Image.ANTIALIAS)
			if img.mode != 'RGB':
				img = img.convert('RGB')
			img.save(val+'/'+p['id']+'.jpg')

	tr.close()
	te.close()
	va.close()





if __name__=='__main__':
	main()