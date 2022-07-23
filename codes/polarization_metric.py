##Importing required libraries
import networkx as nx
import numpy as np
import statistics as st

##Defining Cap funtion
def cap(x):
    if x>0.5:
        x=0.5
    return x

#Defining Multi Opinion-Based Polarization Metric
def computeMultiOpinionPolarization(G,community_structure,num_opinions):
    edge_list=list(G.edges())
    labels=nx.get_node_attributes(G,'labels')
    labels_keys=list(labels.keys())
    labels_vals=list(labels.values())
    labels=dict(zip(labels_keys,labels_vals))
    num_nodes=[labels_vals.count(k) for k in range(num_opinions)]
    group_weights=[num_nodes[k]/sum(num_nodes) for k in range(num_opinions)]
    num_mixed_edges_with=np.zeros((num_opinions,num_opinions))
    num_pure_edges_with=np.zeros((num_opinions,num_opinions))
    num_mixed_edges_btw=np.zeros((num_opinions,num_opinions))
    num_pure_edges_btw=np.zeros((num_opinions,num_opinions))
    for edge in edge_list:
        l1=labels[edge[0]]
        l2=labels[edge[1]]
        if l1<l2:
            a=l1
            b=l2
        else:
            a=l2
            b=l1
        if community_structure[edge[0]]==community_structure[edge[1]]:
            if l1!=l2:
                num_mixed_edges_with[a,b]+=G[edge[0]][edge[1]]["weight"]
            else:
                num_pure_edges_with[a,b]+=G[edge[0]][edge[1]]["weight"]
        else:
            if l1!=l2:
                num_mixed_edges_btw[a,b]+=G[edge[0]][edge[1]]["weight"]
            else:
                num_pure_edges_btw[a,b]+=G[edge[0]][edge[1]]["weight"]

    total_num_pure_edges_with=0
    total_num_pure_edges_btw=0
    total_num_mixed_edges_with=0
    total_num_mixed_edges_btw=0

    for i in range(num_opinions):
        for j in range(num_opinions):
            if i<=j:
                
                
                num_pure_edges_with[i,j]*=(group_weights[i]+group_weights[j])/2
                total_num_pure_edges_with+=num_pure_edges_with[i,j]

                
                num_pure_edges_btw[i,j]*=(group_weights[i]+group_weights[j])/2
                total_num_pure_edges_btw+=num_pure_edges_btw[i,j]

               
                num_mixed_edges_with[i,j]*=(group_weights[i]+group_weights[j])/2
                total_num_mixed_edges_with+=num_mixed_edges_with[i,j]

                num_mixed_edges_btw[i,j]*=(group_weights[i]+group_weights[j])/2
                total_num_mixed_edges_btw+=num_mixed_edges_btw[i,j]
                
                
    total_num_edges_with=total_num_pure_edges_with+total_num_mixed_edges_with
    total_num_edges_btw=total_num_pure_edges_btw+total_num_mixed_edges_btw
    pol_with=round(1-2*cap((total_num_mixed_edges_with/total_num_edges_with)),2)
    pol_btw=round(1-2*cap((total_num_mixed_edges_btw/total_num_edges_btw)),2)
    pol_score=round((1/(total_num_edges_with+total_num_edges_btw))*((total_num_edges_with*pol_with)+(total_num_edges_btw*pol_btw)),2)
    return pol_score