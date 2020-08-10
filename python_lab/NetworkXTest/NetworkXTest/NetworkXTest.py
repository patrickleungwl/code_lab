
import networkx as nx

G = nx.DiGraph()
G.add_edge(1,2)
G.add_edge(2,3, weight=0.9)
G.add_edge(2,4, weight=0.8)

print(G[1])
print(G[2])
print(list(G.nodes))

print(list(G.edges))

