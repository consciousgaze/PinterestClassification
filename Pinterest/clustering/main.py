from util import *
import pickle

def main():
	clusters = pickle.load(open('clusters.p', 'rb'))
	clusters.sort(key=lambda x:len(x), reverse=True)
	tmp = clusters[:10]
	pickle.dump(tmp, open('useful_clusters.p', 'wb'))




def prepare_data():
	'''
		Firstly build graph from data base
		Then unify graph by taking related pins and pins in same 
		board all as neighbors
		Then connect the graph by add the pin as the neighbors of
		its neighbors
		Then remove stand alone pins.
	'''
	g = import_graph()
	tmp = unify_graph(g)
	tmp = connect_graph(tmp)
	tmp = clean_stand_alone(tmp)
	return tmp

if __name__ == '__main__':
	main()

