from model_loader import load_model_vectors
from plot_dendrogram import plot_dendogram,plot_labeled_dendogram

from scipy.cluster.hierarchy import linkage

#set the model names to be used for the demo
model_name = "wang_r,general"

model_vectors, aspects = load_model_vectors(model_name)             #load vectors for existing aspects

linkage_matrix = linkage(model_vectors, method='complete', metric="cosine")              #get the linkage matrix


plot_dendogram('Hierarchical Clustering Dendrogram', 'Distance', 'Word', linkage_matrix, aspects, model_name)




