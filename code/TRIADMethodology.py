import networkx as nx
import numpy as np
import math


def withinCommunityScore(G,partition):
    num_comm=len(set(partition.values()))
    labels=nx.get_node_attributes(G,'labels')
    nodes=list(G.nodes())
    pol_score=[]
    comm_size=[]
    num_edges_with=0
    #ctt=0
    for i in range(num_comm):
        num_mixed_edges=0
        num_edges=0
        comm_nodes=[node for node,comm in partition.items() if comm == i]
        if len(comm_nodes)>0:
            comm_size.append(len(comm_nodes))
            comm_edge_list=[]
            for j in range(len(comm_nodes)):
                comm_edge_list.extend(list(G.edges(comm_nodes[j])))
            comm_edge_list=list({tuple(item) for item in map(sorted, comm_edge_list)})
            for edge in comm_edge_list:
                if partition[edge[0]]==partition[edge[1]]:
                    num_edges+=1
                    if labels[edge[0]]!=labels[edge[1]]:
                        num_mixed_edges+=1
            if num_edges==0:
                #ctt+=1
                comm_node_labels=[labels[node] for node in comm_nodes]
                lb0_count=comm_node_labels.count(0)
                lb1_count=comm_node_labels.count(1)
                pol_score.append(1-math.sqrt(1-(math.pow((lb0_count/len(comm_nodes)),2)+math.pow((lb1_count/len(comm_nodes)),2)))/math.sqrt(0.5))
            else:
                pol_score.append(abs(1-2*(num_mixed_edges/num_edges)))
    pol_with=round(np.sum(np.array(comm_size)*np.array(pol_score))/len(nodes),2)
    num_edges_with+=num_edges
    return num_edges_with,pol_with


def betweenCommunityScore(G,partition):
    edge_list=list(G.edges())
    labels=nx.get_node_attributes(G,'labels')
    num_mixed_edges_btw=0
    num_edges_btw=0
    for edge in edge_list:
        if partition[edge[0]]!=partition[edge[1]]:
            num_edges_btw+=1
            if labels[edge[0]]!=labels[edge[1]]:
                num_mixed_edges_btw+=1
    pol_btw=round(abs(1-2*(num_mixed_edges_btw/num_edges_btw)),2)
    return num_edges_btw,pol_btw

def noCommunityScore(G):
    edge_list=list(G.edges())
    labels=nx.get_node_attributes(G,'labels')
    num_edges=len(edge_list)
    num_mixed_edges=0
    for edge in edge_list:
        if labels[edge[0]]!=labels[edge[1]]:
            num_mixed_edges+=1
    pol_no=round(abs(1-2*(num_mixed_edges/num_edges)),2)
    return num_edges,pol_no
