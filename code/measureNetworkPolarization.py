import networkx as nx
import community as louvain
from TRIADMethodology import *

#selecting the network type as retweet, mention or followers
network_type='retweet'

#getting edge list
file = open('../data/'+network_type+'_network/edges.txt')
lines = file.readlines()
edge_list=[(int(line.split(',')[0]),int(line.split(',')[1][:-1])) for line in lines]
file.close()


####getting the opinion of nodes
file = open('../data/'+network_type+'_network/node_labels.txt')
lines = file.readlines()
labels=dict(zip([int(line.split(',')[0]) for line in lines],[int(line.split(',')[1][:-1]) for line in lines]))
file.close()

#constructing graph using edges
G=nx.Graph()
G.add_edges_from(edge_list)

G.remove_edges_from(nx.selfloop_edges(G))
G.remove_nodes_from(list(nx.isolates(G)))
nx.set_node_attributes(G,labels,'labels')
pol_scores=[]
print('******Computing polarization score******')
for i in range(100):
    
    #Finding communities
    partition = louvain.best_partition(G)

    #Finding three different scores
    num_edges_with,pol_with=withinCommunityScore(G,partition)
    num_edges_btw,pol_btw=betweenCommunityScore(G,partition)
    num_edges,pol_no=noCommunityScore(G)

    pol_scores.append(round((1/(num_edges_with+num_edges_btw+num_edges))*((num_edges_with*pol_with)+(num_edges_btw*pol_btw)+(num_edges*pol_no)),2))

pol_score=round(np.average(pol_scores),2)
print('final_polarization_score=',pol_score)

