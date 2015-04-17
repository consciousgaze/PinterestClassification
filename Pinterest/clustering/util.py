from pymongo import MongoClient
import sys

client = MongoClient("52.11.27.173", 27017)
db = client['pinterest']
boards = db.boards
pins = db.pins

# prepare graph
def import_graph():
	'''
		build a graph according to related pins and pins in same board
		the graph contains all pins in pinterest.pins collection
		each pin is structured like 
			pin_id:{'b':[pins in same board], 'r':[related pins]}
	'''
	graph = {}
	cnt = 0
	for pin in pins.find().batch_size(100):
		# append all related pins to a list
		tmp = pin['related_pins'][0]
		related_pins = []
		for t in tmp:
			related_pins.append(t['src'][0].split('/pin/')[1].replace('/', ''))

		# collect all the pins that has the same board
		board_pins=[]
		tmp = pin['board'][0]
		for t in tmp:
			try:
				boardID = t['src'][0].split('/')[4]
			except:
				print str(t['src']).replace('\n', '\\n'), 'search error'
				continue
			for b in boards.find({'ID':boardID}):
				for p in b['pins'][0]:
					board_pins.append(p['src'][0].split('/')[2])


		graph[pin['ID'][0]] = {'b':set(board_pins), 'r':set(related_pins)}

	return graph

def unify_graph(g):
	'''
		make related pins and pins in same board all neighbor of the pin
	'''
	graph = {}
	for p in g:
		l = g[p]['r'].union(g[p]['b'])
		rl = []
		for rp in l:
			if rp in g:
				rl.append(rp)
		graph[p] = set(rl)
	return graph


def connect_graph(g):
	'''
		the graph may not be fully connected. 
		a neighbor pin, e, of s may not have neighbor s.
	'''
	graph = dict(g)
	for p in graph:
		print graph[p]
		related_pins = graph[p]
		for rp in related_pins:
			graph[rp] = graph[rp].union(set([rp]))
	return graph

def clean_stand_alone(g):
	'''
		some pins in a graph may not be connected to any other pins
		remove them
	'''
	graph = {}
	for p in g:
		if len(g[p])>0:
			graph[p] = set(g[p])
	return graph


# clustering functions
def is_alph_beta(c, g, alph, beta):
	'''
		a cluster is defined as a list of pins
		this function returns whether a cluster is an alph-beta cluster
	'''
	size = len(c)
	samllest_interal = size
	for v in c:
		edge_num = 0
		for neighbor in g[v]:
			if neighbor in c:
				edge_num+=1
		if edge_num <= samllest_interal:
			samllest_interal = edge_num
	if samllest_interal < beta*size:
		return False
	largest_external = 0
	for v in g:
		edge_num = 0
		for neighbor in g[v]:
			if neighbor in c:
				edge_num +=1
		if edge_num >= largest_external:
			largest_external = edge_num
	if largest_external > alph*size:
		return False
	return True

def tau(v, g):
	'''
		returns all vertecies that has a distance less than 3 to v
	'''
	rlt = []
	for neighbor in g[v]:
		rlt.append(neighbor)
		for level_2_v in g[neighbor]:
			rlt.append(level_2_v)
	return set(rlt)

def alph_beta_clustering(alph, beta, s, g):
	'''
		returns all alph-beta cluster as described in 
		Mishra, Nina, et al. "Clustering social networks." 
		Algorithms and Models for the Web-Graph. Springer 
		Berlin Heidelberg, 2007. 56-67.
	'''
	rlt = []
	# total = len(g)
	# i = 0
	for c in g:
		# print i, g
		cluster = set([])
		for v in tau(c, g):
			tmp = g[v].intersection(g[c])
			if len(tmp) >(2*beta - 1)*s:
				cluster = cluster.union(set([v]))
		if is_alph_beta(cluster, g, alph, beta):
			rlt.append(cluster)
		# i+=1
	return rlt

def naive_clustering(g):
	'''
		cluster two pins as long as they can reach each other
		return a list of clusters
	'''
	seen = set()
	clusters = []
	i = 0
	total = len(g)
	for v in g:
		i+=1
		print i, total
		if v in seen:
			continue
		cluster = set([v])
		next_layer = set(g[v])
		round_cnt = 0
		while len(next_layer) > 0:
			print i, round_cnt, len(next_layer)
			round_cnt += 1
			tmp = set()
			for c in next_layer:
				if c not in cluster:
					cluster = cluster.union(set([c]))
					tmp = tmp.union(set(g[c]))
					seen = seen.union(set([c]))

			next_layer = tmp

		clusters.append(cluster)
	return clusters

def assign_clusters(clusters, g):
	'''
		output a hash table that assigns each pin to its cluster idx in clusters
	'''
	rlt = {}
	for i in g:
		for cidx in range(len(clusters)):
			if i in clusters[cidx]:
				rlt[i] = cidx
				break
	return rlt






