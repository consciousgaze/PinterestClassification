from pymongo import MongoClient
import urllib, cStringIO
import sys, pickle
from PIL import Image

client = MongoClient("52.11.27.173", 27017)
db = client['pinterest']
boards = db.boards
pins = db.fast_pins
# all_records = pickle.load(open('use_boards.p'))


def get_info(pin):
	tmp = pins.find({"ID":pin}).next()
	URL = tmp['image'][0]
	text = 'dummy '
	for comment in tmp['comments'][0]:
		text += comment['content'][0]

	text += tmp['name'][0]
	return (URL, text)

def get_image(pin):
	tmp = pins.find({"ID":pin}).next()
	URL = tmp['image'][0]
	file = cStringIO.StringIO(urllib.urlopen(URL).read())
	img = Image.open(file)
	return img


def get_texts(pin):
	tmp = pins.find({"ID":pin}).next()
	text = 'dummy '
	for comment in tmp['comments'][0]:
		text += comment['content'][0]

	text += tmp['name'][0]
	return text

# def get_board(pin):
# 	for i in all_records:
# 		if 'https://www.pinterest.com/pin/'+pin+'/' in all_records[i]:
# 			return i.split('/')[4]
# 	raise Exception(pin)