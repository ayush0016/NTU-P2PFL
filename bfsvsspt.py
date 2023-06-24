import random
import networkx as nx
import time

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.knowledge = None
    
    def receive_knowledge(self, knowledge):
        self.knowledge = knowledge
    
def disseminate_knowledge_bfs(network, source_node_id, knowledge):
    source_node = network[source_node_id]
    source_node.receive_knowledge(knowledge)
    
    queue = [source_node_id]
    visited = set(queue)
    
    while queue:
        node_id = queue.pop(0)
        node = network[node_id]
        
        # Broadcast the knowledge to neighbors
        for neighbor_id in node.neighbors:
            if neighbor_id not in visited:
                neighbor = network[neighbor_id]
                neighbor.receive_knowledge(node.knowledge)
                queue.append(neighbor_id)
                visited.add(neighbor_id)

def disseminate_knowledge_mst(network, source_node_id, knowledge):
    source_node = network[source_node_id]
    source_node.receive_knowledge(knowledge)
    
    # Convert graph to adjacency list representation
    adjacency_list = {node_id: list(graph.neighbors(node_id)) for node_id in graph.nodes}
    
    # Build the minimum spanning tree using Kruskal's algorithm
    mst_edges = nx.minimum_spanning_edges(graph, weight='weight', data=False)
    mst = nx.Graph()
    mst.add_edges_from(mst_edges)
    
    stack = [source_node_id]
    visited = set(stack)

    while stack:
        node_id = stack.pop()
        node = network[node_id]

        # Broadcast the knowledge to neighbors
        for neighbor_id in adjacency_list[node_id]:
            if neighbor_id not in visited:
                neighbor = network[neighbor_id]
                neighbor.receive_knowledge(node.knowledge)
                stack.append(neighbor_id)
                visited.add(neighbor_id)

# Sample usage
num_nodes = 1000
p = 0.02# Probability of an edge between two nodes

# Create a random graph
graph = nx.fast_gnp_random_graph(num_nodes, p)

# Assign random weights to edges
for u, v in graph.edges:
    graph.edges[u, v]['weight'] = random.randint(1, 10)

# Create nodes and set up the network topology
network = {}
for node_id in graph.nodes:
    node = Node(node_id)
    network[node_id] = node

# Set neighbors for each node based on the graph topology
for node_id in graph.nodes:
    node = network[node_id]
    node.neighbors = list(graph.neighbors(node_id))

# Choose a random node to be the source of knowledge dissemination
source_node_id = random.choice(list(network.keys()))

# Knowledge to be disseminated
knowledge = "Sample knowledge"

# Measure time taken by BFS algorithm
start_time_bfs = time.time()
disseminate_knowledge_bfs(network, source_node_id, knowledge)
end_time_bfs = time.time()
time_taken_bfs = end_time_bfs - start_time_bfs

# Measure time taken by MST algorithm
start_time_mst = time.time()
disseminate_knowledge_mst(network, source_node_id, knowledge)
end_time_mst = time.time()
time_taken_mst = end_time_mst - start_time_mst

# Print the final knowledge of each node
print("Final Node Knowledge (BFS Algorithm):")
#for node_id, node in network.items():
 #   print(f"Node {node_id}: {node.knowledge}")

print("\nFinal Node Knowledge (MST Algorithm):")
#for node_id, node in network.items():
 #   print(f"Node {node_id}: {node.knowledge}")

# Print the time taken by each algorithm
print("\nTime taken by BFS Algorithm: {:.6f} seconds".format(time_taken_bfs))
print("Time taken by MST Algorithm: {:.6f} seconds".format(time_taken_mst))
