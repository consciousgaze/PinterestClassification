from pymongo import MongoClient
import sys
client = MongoClient("52.11.27.173", 27017)
db = client['pinterest']
boards = db.boards
pins = db.pins

# gather all pins and boards from boards and pins
unfamiliar_boards = []
unfamiliar_pins = []
for pin in pins.find().batch_size(100):
    tmpboards = pin['board']
    for bs in tmpboards:
        for b in bs:
            name = b["name"]
            if boards.find_one({"name":name})==None:
                unfamiliar_boards.append(b['src'][0])
    tmppins = pin['related_pins']
    for ps in tmppins:
        for p in ps:
            src = p['src'][0]
            pinId = src.split('pin/')[1]
            if pins.find_one({"ID":pinId})==None:
                unfamiliar_pins.append(src)
f=open('p.txt', 'w')
unfamiliar_pins = set(unfamiliar_pins)
for p in unfamiliar_pins:
    f.write(p+"\n")
f.close()


for board in boards.find().batch_size(100):
    tmpPins = board['pins']
    for ps in tmpPins:
        for p in ps:
            pid = p['src'][0].replace('/pin/', '')
            if pins.find_one({"ID":pid})==None:
                unfamiliar_pins.append("https://www.pinterest.com"+p['src'][0])
f = open('b.txt', 'w')
unfamiliar_boards = set(unfamiliar_boards)
for b in unfamiliar_boards:
    f.write(b+"\n")
f.close()

o = open('second_round.csv', 'w')
f = open('b.txt')
for l in f:
    tmp = '6E+17,RT @avon_valerie: SKIN SO SOFT Original - softens and conditions skin with Jojoba Oil. Experience crisp botanicals and http://t.co/T3DClA4[],"[{""expanded_url"":""'+\
          l.strip() + '""}]",,,,,,,,\n'
    o.write(tmp)
f.close()

f = open('p.txt')
for l in f:
    tmp = '6E+17,RT @avon_valerie: SKIN SO SOFT Original - softens and conditions skin with Jojoba Oil. Experience crisp botanicals and http://t.co/T3DClA4[],"[{""expanded_url"":""'+\
          l.strip() + '""}]",,,,,,,,\n'
    o.write(tmp)
f.close()


o.close()

