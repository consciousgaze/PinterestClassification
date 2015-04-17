import caffe, os, pickle, time
import numpy as np
from PIL import Image
model = '/home/ubuntu/caffe/models/bvlc_reference_caffenet/deploy.prototxt'
train = '/home/ubuntu/caffe/models/bvlc_reference_caffenet/caffenet_train_iter_450000.caffemodel'
folder_prefix = '/home/ubuntu/images/'
image_folders = ['test', 'val', 'train']
image_mean = np.load('/home/ubuntu/caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')
# image_mean = image_mean.reshape(256, 256, 3)
net = caffe.Classifier(model, train,
                       mean=image_mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

for image_folder in image_folders:
	image_files = os.listdir(folder_prefix+image_folder)
	images = []
	predict_result = {}
	length = len(image_files)
	for imageIdx in range(length):
	        print time.ctime(), 'Processing No.', imageIdx+1, 'of', length, 'images,', image_files[imageIdx]
	        prediction = net.predict([caffe.io.load_image(folder_prefix+image_folder+'/'+image_files[imageIdx])])
	        predict_result[image_files[imageIdx]] = prediction[0]

	pickle.dump(predict_result, open('predict_'+image_folder+'_result.p', 'wb'))

# PYTHONPATH=/home/ubuntu/caffe/python:$PYTHONPATH
