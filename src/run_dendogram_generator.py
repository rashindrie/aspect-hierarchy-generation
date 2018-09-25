from model_loader import load_model_vectors
from plot_dendrogram import plot_dendogram,plot_labeled_dendogram

from scipy.cluster.hierarchy import linkage


model_name = raw_input("Enter model name:")

model_vectors, aspects = load_model_vectors(model_name)             #load vectors for existing aspects

linkage_matrix = linkage(model_vectors, method='complete', metric="cosine")              #get the linkage matrix


plot_dendogram('Hierarchical Clustering Dendrogram', 'Distance', 'Word', linkage_matrix, aspects, model_name)

# plot_labeled_dendogram('Hierarchical Clustering Dendrogram', 'Distance', 'Word', linkage_matrix, aspects, model_name)
#plot_dendogram(' ', 'Distance', 'Word', linkage_matrix, aspects, model_name+"ward")
#plot_labeled_dendogram('Hierarchical Clustering Dendrogram', 'Distance', 'Word', linkage_matrix, aspects, model_name)






