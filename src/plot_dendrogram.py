import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, to_tree
import numpy as np

#from groundTruthGenerator import *

matplotlib.rcParams['lines.linewidth'] = 5
matplotlib.rcParams['axes.linewidth'] = 5


def plot_dendogram(title, y_label, x_label, model, aspect_list, name):
    # calculate full dendrogram
    plt.figure(figsize=(60, 24))
    plt.title(title, fontsize=40)
    plt.ylabel(y_label, fontsize=20)
    plt.xlabel(x_label, fontsize=20)

    # Plot the corresponding dendrogram
    dendrogram(
        model,
        leaf_font_size=40,  # font size for the x axis labels
        labels=aspect_list,
        get_leaves=True,
    )

    figure = plt.gcf()
    plt.xticks(rotation=90)
    plt.draw()
    figure.savefig('../output/aspect_dendogram')

def plot_labeled_dendogram(title, y_label, x_label, model, aspects, name):
    plt.figure(figsize=(60, 24))
    plt.title(title, fontsize=40)
    plt.ylabel(y_label, fontsize=20)
    plt.xlabel(x_label, fontsize=20)

    dend = dendrogram(model,
                      leaf_font_size=16.,
                      labels=aspects)
    def flatten(l):
        return [item for sublist in l for item in sublist]

    X = flatten(dend['icoord'])
    Y = flatten(dend['dcoord'])

    leave_coords = [(x, y) for x, y in zip(X, Y) if y == 0]

    # in the dendogram data structure,
    # leave ids are listed in ascending order according to their x-coordinate
    order = np.argsort([x for x, y in leave_coords])
    id_to_coord = dict(zip(dend['leaves'], [leave_coords[idx] for idx in order]))  # <- main data structure

    # map endpoint of each link to coordinates of parent node
    aspect_labels = getLabels()
    aspect_labels["prices"] = "RESTAURANT"
    aspect_labels["price"] = "RESTAURANT"
    aspect_labels["dishes"] = "FOOD"
    aspect_labels["portions"] = "FOOD"
    aspect_labels["drinks"] = "DRINKS"
    aspect_labels["wines"] = "DRINKS"
    label_to_index = {'RESTAURANT': 0, "FOOD": 1, "AMBIENCE": 2, "SERVICE": 3, "DRINKS": 4, "LOCATION": 5}
    children_to_parent_coords = dict()
    for i, d in zip(dend['icoord'], dend['dcoord']):
        x = (i[1] + i[2]) / 2
        y = d[1]  # or d[2]
        parent_coord = (x, y)
        left_coord = (i[0], d[0])
        right_coord = (i[-1], d[-1])
        children_to_parent_coords[(left_coord, right_coord)] = parent_coord

    # traverse tree from leaves upwards and populate mapping ID -> (x,y)
    root_node, node_list = to_tree(model, rd=True)

    ids_left = range(len(dend['leaves']), len(node_list))

    while len(ids_left) > 0:

        for ii, node_id in enumerate(ids_left):
            node = node_list[node_id]
            if (node.left.id in id_to_coord) and (node.right.id in id_to_coord):
                if node_list[node.left.id].is_leaf():
                    left_aspect_name = aspects[node.left.id]
                    category_array = [["R", 0], ["F", 0], ["A", 0], ["S", 0], ["D", 0], ["L", 0]]
                    category_array[label_to_index[aspect_labels[left_aspect_name]]][1] += 1
                    aspects[node.left.id] = category_array
                    left_aspect = category_array
                else:
                    left_aspect = aspects[node.left.id]

                if node_list[node.right.id].is_leaf():
                    right_aspect_name = aspects[node.right.id]
                    category_array = [["R", 0], ["F", 0], ["A", 0], ["S", 0], ["D", 0], ["L", 0]]
                    category_array[label_to_index[aspect_labels[right_aspect_name]]][1] += 1
                    aspects[node.right.id] = category_array
                    right_aspect = category_array
                else:
                    right_aspect = aspects[node.right.id]

                aspects.append([(x[0], x[1] + y[1]) for x, y in zip(left_aspect, right_aspect)])
                left_coord = id_to_coord[node.left.id]
                right_coord = id_to_coord[node.right.id]
                id_to_coord[node_id] = children_to_parent_coords[(left_coord, right_coord)]

        ids_left = [node_id for node_id in range(len(node_list)) if not node_id in id_to_coord]

    ax = plt.gca()

    for node_id, (x, y) in id_to_coord.iteritems():
        if not node_list[node_id].is_leaf():
            ax.plot(x, y, 'ro')
            total = sum([t[1] for t in aspects[node_id]])
            a_percent = [(t[0], round((float(t[1]) / total), 2)) for t in aspects[node_id]]
            ax.annotate(a_percent, (x, y), xytext=(0, -8),
                        textcoords='offset points',
                        va='top', ha='center', size="16")

    figure = plt.gcf()
    plt.draw()
    figure.set_size_inches(40, 20)
    figure.savefig('output/' + name +"_labeled")
