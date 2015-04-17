import os, pickle
def main():
	print 'aha'


def prepareData():
	root = '20news-18828'
	folders = os.listdir(root)
	data = {}
	for folder in folders:
		if folder == '.DS_Store':
			continue
		print folder
		cat = folder.split('.')[0]
		files = os.listdir(root+'/'+folder)
		for fle in files:
			# print fle
			f = open(root+'/'+folder+'/'+fle)
			tmp = {}
			text = ''
			f.readline()
			for l in f:
				text+=l.replace('>', '').strip()
			tmp['text'] = text
			tmp['cat'] = cat
			data[fle] = tmp
			f.close()
	pickle.dump(data, open('data.p', 'wb'))


if __name__ == '__main__':
	main()