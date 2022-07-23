#************************Binary Benchmark Networks***********************************************

##Importing Required Libraries
import networkx as nx
import community
import numpy as np
from polarization_metric import *

##For Karate, fname='../data/karate_club_CC.gexf'
##For Blogs, fname='../data/Blogs_network_CC.gexf'
##For Retweet, fname='../data/Political_Retweet_network_CC.gexf'
fname='../data/Blogs_network_CC.gexf'
G=nx.read_gexf(fname)
labels=nx.get_node_attributes(G,'labels')
num_opinions=len(set(labels.values()))
pol_scores=[]
print('\n******Computing polarization score******')

num_executions=100
for i in range(num_executions):
    #Finding communities
    community_structure = community.best_partition(G)
    pol_scores.append(computeMultiOpinionPolarization(G,community_structure,num_opinions))

final_pol_score=round(np.average(pol_scores),2)
print('polarization score=',final_pol_score)