#!/usr/bin/python

import scipy.spatial
import scipy.cluster
import json
import matplotlib.pyplot as plt

def get_Json(linkage,aspects):

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
        # n["name"] = name = "-".join(sorted(map(str, leafNames)))
        n["name"] = name = sorted(map(str, leafNames))[0]

        return leafNames


    label_tree(d3Dendro["children"][0])

    # Output to JSON
    json.dump(d3Dendro, open("../output/dendrogram.json", "w"), sort_keys=True, indent=4)