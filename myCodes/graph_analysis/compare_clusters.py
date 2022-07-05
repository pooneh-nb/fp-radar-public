from myCodes.AST import utilities

umar_graph_clusters = utilities.read_json("/home/c6/Desktop/OpenWPM/myCodes/graph_analysis/network_characterization/Lovain_clusters.json")
generated_umar_graph = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/umar_ds/Graph/Lovain_clusters.json")
my_graph_2019 = utilities.read_json("/home/c6/Desktop/OpenWPM/jsons/AST/CDX_results/Graphs/2019/Lovain_clusters.json")

umar_graph_clusters_giant = set()
for ap in umar_graph_clusters['4']:
    umar_graph_clusters_giant.add(ap)

generated_umar_graph_giant = set()
for ap in generated_umar_graph['3']:
    generated_umar_graph_giant.add(ap)

my_graph_2019_giant = set()
for ap in my_graph_2019['0']:
    my_graph_2019_giant.add(ap)


ident = umar_graph_clusters_giant.intersection(generated_umar_graph_giant)
print(len(ident))

