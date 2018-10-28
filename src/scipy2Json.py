#!/usr/bin/python
from cmath import polar

import scipy.spatial
import scipy.cluster
import json
import matplotlib.pyplot as plt
from model_loader import get_centroid

import gensim

def get_Json(model_names, linkage, aspects,model_vectors):
    T = scipy.cluster.hierarchy.to_tree(linkage, rd=False)

    # Create dictionary for labeling nodes by their IDs
    labels = list(aspects)
    id2name = dict(zip(range(len(labels)), labels))

    # Draw dendrogram using matplotlib to scipy-dendrogram.pdf
    scipy.cluster.hierarchy.dendrogram(linkage, labels=aspects, orientation='right')
    plt.savefig("../output/dendrogram.png")

    # Create a nested dictionary from the ClusterNode's returned by SciPy
    def add_node(node, parent):
        # First create the new node and append it to its parent's children
        newNode = dict(node_id=node.id, children=[])
        parent["children"].append(newNode)

        # Recursively add the current node's children
        if node.left: add_node(node.left, newNode)
        if node.right: add_node(node.right, newNode)

    # Initialize nested dictionary for d3, then recursively iterate through tree
    d3Dendro = dict(children=[], name="Root")
    add_node(T, d3Dendro)

    # Label each node with the names of each leaf in its subtree
    def label_tree(n):
        # If the node is a leaf, then we have its name
        if len(n["children"]) == 0:
            leafNames = [id2name[n["node_id"]]]

        # If not, flatten all the leaves in the node's subtree
        else:
            leafNames = reduce(lambda ls, c: ls + label_tree(c), n["children"], [])

        # Delete the node id since we don't need it anymore and
        # it makes for cleaner JSON
        del n["node_id"]

        # Labeling convention: "-"-separated leaf names
        name = "-".join(sorted(map(str, leafNames)))
        n["title"] = get_centroid(model_names, name)
        n["subtitle"] = get_reviews(n["title"])
        n["polarity"] = get_polarity(n["title"])

        # n["name"] = name = sorted(map(str, leafNames))[0]

        return leafNames

    label_tree(d3Dendro["children"][0])
    # Output to JSON
    json.dump(d3Dendro["children"][0], open("../output/dendrogram.json", "w"), sort_keys=True, indent=4)


# aspect_dict = {}
# with open('../data/aspect_list_with_count.txt') as f:
#     for line in f:
#         (key, val) = line.split()
#         aspect_dict[val] = int(key)

from extract_reviews import dictionary
def get_reviews(name):
    data = []
    if name in dictionary:
        i = 2 if len(dictionary[name]['text']) > 1 else len(dictionary[name]['text'])
        for x in range(0,i):
            data.append(dictionary[name]['text'][x])
    return data

def get_polarity(name):
    data = {}
    negCount = 1
    posCount = 1
    neuCount = 1
    if name in dictionary:
        temp = dictionary[name]['polarity']

        for t in temp:
            if t == -1:
                negCount +=1
            else:
                if t == 1:
                    posCount += 1
                else:
                    neuCount += 1
    sum = posCount + negCount + neuCount

    data['positive'] = round((posCount/float(sum))*100,2)
    data['negative'] = round((negCount/float(sum))*100,2)
    data['neutral'] = round((neuCount/float(sum))*100,2)
    return data
