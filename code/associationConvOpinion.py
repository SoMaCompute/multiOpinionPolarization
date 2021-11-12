import networkx as nx
import community as louvain
import numpy as np
import math
from TRIADMethodology import *


#getting edge list of followers network
file = open('../data/followers_network/edges.txt')
lines = file.readlines()
edge_list_fol=[(int(line.split(',')[0]),int(line.split(',')[1][:-1])) for line in lines]
file.close()


####getting the opinion of nodes of followers network
file = open('../data/followers_network/node_labels.txt')
lines = file.readlines()
labels=dict(zip([int(line.split(',')[0]) for line in lines],[int(line.split(',')[1][:-1]) for line in lines]))
file.close()

#constructing followers graph using edges
G1=nx.Graph()
G1.add_edges_from(edge_list_fol)
nodes_fol=list(G1.nodes())




#selecting the conversation network type as retweet or mention
network_type='mention'

#getting edge list of conversation network
file = open('../data/'+network_type+'_network/edges.txt')
lines = file.readlines()
edge_list_conv=[(int(line.split(',')[0]),int(line.split(',')[1][:-1])) for line in lines]
file.close()


####getting the opinion of nodes of conversation network
file = open('../data/'+network_type+'_network/node_labels.txt')
lines = file.readlines()
labels=dict(zip([int(line.split(',')[0]) for line in lines],[int(line.split(',')[1][:-1]) for line in lines]))
file.close()

#constructing conversation graph using edges
G2=nx.Graph()
G2.add_edges_from(edge_list_conv)
nodes_conv=list(G2.nodes)
#labels=nx.get_node_attributes(G2,'labels')

#finding nodes of the overlapped network
nodes=list(set(nodes_fol).intersection(nodes_conv))

#finding edges of the overlapped network
nodes_prime=list(set(nodes_conv).difference(nodes_fol))
edge_list=[]
for edge in edge_list_conv:
    if edge[0] not in nodes_prime and edge[1] not in nodes_prime:
        edge_list.append(edge)

#constructing overlapped network
G=nx.Graph()
G.add_edges_from(edge_list)
nx.set_node_attributes(G,labels,'labels')
nodes=list(G.nodes)
with_list=[]
btw_list=[]
print('******Computing polarization scores******')
for i in range(100):

    #finding communities of followers network
    partition_fol = louvain.best_partition(G1)
    
    #finding modified partition for overlapped network
    partition = dict([(key, val) for key, val in partition_fol.items() if key in nodes])

    #computing within-community score
    _,pol_with=withinCommunityScore(G,partition)


    #computing between-community score
    _,pol_btw=betweenCommunityScore(G,partition)
    with_list.append(pol_with)
    btw_list.append(pol_btw)

pol_with=round(np.average(with_list),2)
pol_btw=round(np.average(btw_list),2)

print(pol_with,pol_btw)
