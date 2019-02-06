import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
import csv




lines = [] 

with open("sf_uber_movement.prn") as file:
	for line in file:
		lines.append(line)

uber = nx.parse_edgelist(lines, nodetype = int, create_using=nx.DiGraph(), data=(('weight',float),))

in_degree = nx.in_degree_centrality(uber)
out_degree = nx.out_degree_centrality(uber)
pagerank8 = nx.pagerank(uber, alpha=0.8)
pagerank95 = nx.pagerank(uber, alpha=0.95) #paper found this best
betweeness_centrality = nx.betweenness_centrality(uber, weight='weight')
sccs = nx.strongly_connected_components(uber)


def in_scc(sccs, node):
	for scc in sccs:
		if node in scc:
			return 1
	return 0

def diameter(graph, node):
	copy = graph.copy()
	copy.remove_node(node)
	return nx.diameter(copy)


with open('sf_uber_stats.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Node', 'In Degree', 'Out Degree', 'Page Rank 0.8', 'Page Rank 0.95', 'Betweeness Centrality', 'Part of SCC', 'Diameter when Removed'])
    for node, in_deg in in_degree.items():
    	row = []
    	row.append(node)
    	row.append(in_deg)
    	row.append(out_degree[node])
    	row.append(pagerank8[node])
    	row.append(pagerank95[node])
    	row.append(betweeness_centrality[node])
    	row.append(in_scc(sccs, node))
    	#row.append(diameter(uber, node))
    	filewriter.writerow(row)


# nx.draw(uber)
# plt.draw()
# plt.show()


def time_diff(start, end):
	FMT = '%H:%M:%S'
	if start[:2] == "24":
		start = "00" + start[2:]
	if end[:2] == "24":
		end = "00" + end[2:]
	if start[:2] == "25":
		start = "01" + start[2:]
	if end[:2] == "25":
		end = "01" + end[2:]
	return datetime.strptime(start, FMT) - datetime.strptime(end, FMT)


bart = nx.DiGraph()

with open("stops.txt") as bart_stops:
	bart_stops.readline()
	for line in bart_stops:
		bart.add_node(line.split(",")[0])


edges_times = defaultdict(int)
edges_counts = defaultdict(int)

with open("stop_times.txt") as stop_times:
	stop_times.readline()
	line = stop_times.readline()
	line = line.split(",")
	prev_time = line[1]
	prev_stop = line[3]
	prev_stop_idx = int(line[4])

	for line in stop_times:
		line = line.split(",")
		time = line[1]
		stop = line[3]
		stop_idx = int(line[4])

		if stop_idx > prev_stop_idx:
			edges_times[(prev_stop, stop)] += time_diff(time, prev_time).total_seconds()
			edges_counts[(prev_stop, stop)] += 1

		prev_time = time
		prev_stop = stop
		prev_stop_idx = stop_idx

for edge, total in edges_times.items():
	bart.add_edge(edge[0], edge[1], weight=float(total)/edges_counts[edge])



in_degree = nx.in_degree_centrality(bart)
out_degree = nx.out_degree_centrality(bart)
pagerank8 = nx.pagerank(bart, alpha=0.8)
pagerank95 = nx.pagerank(bart, alpha=0.95) #paper found this best
betweeness_centrality = nx.betweenness_centrality(bart, weight='weight')
sccs = nx.strongly_connected_components(bart)

with open('sf_bart_stats.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Node', 'In Degree', 'Out Degree', 'Page Rank 0.8', 'Page Rank 0.95', 'Betweeness Centrality', 'Part of SCC', 'Diameter when Removed'])
    for node, in_deg in in_degree.items():
    	row = []
    	row.append(node)
    	row.append(in_deg)
    	row.append(out_degree[node])
    	row.append(pagerank8[node])
    	row.append(pagerank95[node])
    	row.append(betweeness_centrality[node])
    	row.append(in_scc(sccs, node))
    	#row.append(diameter(bart, node))
    	filewriter.writerow(row)


# nx.draw(bart)
# plt.draw()
# plt.show()