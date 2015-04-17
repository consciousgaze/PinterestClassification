import numpy as np
import math
import random

class cluster:
    '''
        represent a cluster of a data set
        the data reside in a two dimontinal space
    '''
    mu = np.array([0, 0])
    sigma = np.array([[1, 0], [0, 1]])
    def __init__(self, m, s):
        self.mu = m
        self.sigma = s

    def prob(self, x, y):
        '''
            returns the probability for a point to
            be in this cluster
        '''
        p = np.array([x, y])
        tmp = np.dot((p-self.mu).T, np.linalg.inv(self.sigma))
        tmp = np.dot(tmp, p-self.mu)
        left = math.exp(-0.5*tmp)
        tmp = 2*math.pi
        tmp = math.pow(tmp, 2)
        tmp = tmp*np.det(self.sigma)
        tmp = 1.0/math.sqrt(tmp)
        return tmp*left

    def generate_samples(sample_num):
        '''
            generate a set of points according to mu and sigma
        '''
        samples = []
        for i in range(sample_num)
            x = random.gauss(mu[0], sigma[0][0])
            y = random.guass(mu[1], sigma[1][1])
            while((x, y) in samples):
                x = random.gauss(mu[0], sigma[0][0])
                y = random.guass(mu[1], sigma[1][1])

            samples.append((x, y))
        return samples

class data_set:
    '''
        defines a data set
        it consists a set of clusters and a set of data points
        each cluster has a probability to show up
        each data point in the data set belongs to a cluster
    '''
    clusters = []
    points = {}
    total_weight = 0.0
    def add_cluster(self, mu, sigma, weight):
        '''
            add in a cluster, the total weight of prvious clusters
            are always 1
        '''
        self.clusters.append((cluster(mu, sigma), weight))
        self.total_weight += weight

    def sample(self, sample_num):
        '''
            store and retuns a set of samples
            they are samples according to cluster weight and cluster 
            distribution
        '''
        self.points = {}
        for i in range(sample_num):
            r = random.random()
            cur_w = 0.0
            for ii in range(len(self.clusters)):
                cur_w += sefl.clusters[ii][1]
                if r < float(cur_w)/self.total_weight:
                    tmp = self.clusters[ii].generate_samples(1)[0]
                    while(tmp in self.points):
                        tmp = self.clusters[ii].generate_samples(1)[0]
                    self.points[tmp] = ii
                    break
class domain:
    '''
        defines a domain which groups certain clusters in a data
        set as a category
    '''
    observed_data = []
    
