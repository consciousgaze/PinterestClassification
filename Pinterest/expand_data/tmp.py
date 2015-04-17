f = open('list.txt')
o = open('b.txt', 'w')
for l in f:
	l = l.split('\t')[0]
	tmp = '6E+17,RT @avon_valerie: SKIN SO SOFT Original - softens and conditions skin with Jojoba Oil. Experience crisp botanicals and http://t.co/T3DClA4[],"[{""expanded_url"":""'+\
		  l.strip() + '""}]",,,,,,,,\n'
	o.write(tmp)
f.close()

# f = open('p.txt')
# for l in f:
# 	tmp = '6E+17,RT @avon_valerie: SKIN SO SOFT Original - softens and conditions skin with Jojoba Oil. Experience crisp botanicals and http://t.co/T3DClA4[],"[{""expanded_url"":""'+\
# 		  l.strip() + '""}]",,,,,,,,\n'
# 	o.write(tmp)
# f.close()


o.close()