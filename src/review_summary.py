
aspect_dict={}
with open('../data/aspect_list_with_count.txt') as f:
    for line in f:
        (key, val) = line.split()
        aspect_dict[val] = int(key)