import json


with open('../output/labelled_dendrogram.json') as data_file:
    data = json.loads(data_file.read())


def internal_nodes(x):
    res = []
    if x:
        print(x['name'])
        if len(x["children"]) > 0:
            res = internal_nodes(x["children"][0])
        if len(x["children"]) > 1:
            res = res + internal_nodes(x["children"][1])
        # print(x['name'])
    return res

response ={}
def traverse(x):

    y = x

    if y:
        response['title'] = y['name']
        response['subtitle'] = y['review'] if 'review' in response.keys() else []
        child_1 = []
        child_2 = []
        print('y', y)
        if len(y["children"]) > 0:
            child_1 = traverse(y["children"][0])
        if len(y["children"]) > 1:
            child_2 = traverse(y["children"][1])
        print(child_1)
        print(child_2)
        response['children'] = [].append(child_1)


# s = internal_nodes(data)

d = traverse(data)
print(response)