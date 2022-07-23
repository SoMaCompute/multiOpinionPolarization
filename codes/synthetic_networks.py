##Importing Required Libraries
import networkx as nx
import community
import numpy as np
import pickle
from prettytable import PrettyTable
from polarization_metric import *



G=nx.read_gexf('../data/Political_Retweet_network_CC.gexf')
G=nx.relabel.convert_node_labels_to_integers(G,label_attribute='st2int')
dom_ratios=[0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
num_opinions_lt=[2,3,4,5,6,7,8,9,10]
x = PrettyTable()
x.field_names = [ "numOpinions/domRatio"]+[str(dom_ratio) for dom_ratio in dom_ratios]

nodes=list(G.nodes())
edges=list(G.edges())

num_executions=100

print('Finding Communities')
community_structures=[]
for j in range(num_executions):
    community_structures.append(community.best_partition(G))
    

for num_opinions in num_opinions_lt:
    pol_scores=[]
    for dom_ratio in dom_ratios:
        print('Computing Polarization Score for network with numOpinions=',num_opinions,' and domRatio=',dom_ratio)
        Gt=G.copy()
        with open('../data/synthetic_labels/labels_dict_'+str(num_opinions)+'_'+str(dom_ratio)+'.pkl', 'rb') as f:
            labels_dict=pickle.load(f)
        nx.set_node_attributes(Gt,labels_dict,'labels')
        pol_scores1=[]
        
        for i in range(10):
            #Finding communities
            community_structure = community_structures[i]
            pol_scores1.append(computeMultiOpinionPolarization(Gt,community_structure,num_opinions))

        final_pol_score=round(np.average(pol_scores1),2)
        pol_scores.append(str(final_pol_score))
        
    x.add_row([str(num_opinions)]+pol_scores)
print(x)
data = x.get_string()

with open('../data/all_scores_synthetic_networks_implementation.txt', 'w') as f:
    f.write(data)
