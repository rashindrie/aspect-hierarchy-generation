from src.model_loader import load_model_vectors
from src.plot_dendrogram import plot_dendogram,plot_labeled_dendogram
from src.scipy2Json import get_Json
from scipy.cluster.hierarchy import linkage

def get_hierarchy():
    #set the model names to be used for the demo
    model_name = "wang_r"

    print("Loading model Vectors")
    model_vectors, aspects = load_model_vectors(model_name)             #load vectors for existing aspects

    linkage_matrix = linkage(model_vectors, method='complete', metric="cosine")              #get the linkage matrix

    print("Converting Linkage to Json")
    get_Json(model_name,linkage_matrix,aspects,model_vectors)

    # import json
    #
    # with open('../output/dendrogram.json') as f:
    #     data = json.load(f)
    #
    # return json.dumps(data)

get_hierarchy()