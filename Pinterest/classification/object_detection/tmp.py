# /Users/Ted/caffe/python/detect.py --gpu --crop_mode=selective_search --pretrained_model=/Users/Ted/caffe/models/bvlc_reference_rcnn_ilsvrc13/bvlc_reference_rcnn_ilsvrc13.caffemodel --model_def=/Users/Ted/caffe/models/bvlc_reference_rcnn_ilsvrc13/deploy.prototxt --raw_scale=255 train0.txt ../detection_rlts/train10_output.h5
def seg():
	typeName = 'train'
	prefix = '/Users/Ted/image/train/'
	f = open(typeName+'.list')
	for i in range(1000):
		tmpf = open(typeName+str(i)+'.txt', 'w')
		for j in range(10):
			l = f.readline()
			if l == "":
				tmpf.close()
				return
			tmpf.write(prefix+l)
		tmpf.close()

seg()

# for ((i=0;i<=75;i++))
# do
# 	echo $i, `date`
# 	/Users/Ted/caffe/python/detect.py --gpu --crop_mode=selective_search --pretrained_model=/Users/Ted/caffe/models/bvlc_reference_rcnn_ilsvrc13/bvlc_reference_rcnn_ilsvrc13.caffemodel --model_def=/Users/Ted/caffe/models/bvlc_reference_rcnn_ilsvrc13/deploy.prototxt --raw_scale=255 test$i.txt ../detection_rlts/test${i}_output.h5 &> ../logs/"log${i}_`date`.txt"
# done
