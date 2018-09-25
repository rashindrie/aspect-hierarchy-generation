import os
import json
import re

from nltk.stem import WordNetLemmatizer

stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
              "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can",
              "can't", "cannot", "could", "could've", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing",
              "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
              "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself",
              "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is",
              "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no",
              "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "	ourselves",
              "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
              "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
              "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to",
              "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
              "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's",
              "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're",
              "you've", "your", "yours", "yourself", "yourselves"]


wordnet_lemmatizer = WordNetLemmatizer()

with open(os.path.join(os.path.dirname(__file__), '../data/reviews.json')) as data:
    data = json.load(data)

reviewData = []
onlySentences = []
reviews = data['Reviews']

for review in reviews['Review']:
    sentences = review['sentences']
    for sentence in sentences['sentence']:
        sentenceData = []
        if 'Opinions' in sentence:
            opinions = sentence['Opinions']  # some sentences dont have opinions
            opinionList = opinions['Opinion']
            if not isinstance(opinionList, list):
                opinionList = []
                opinionList.append(opinions['Opinion'])
            for opinion in opinionList:
                opinionsData = []
                aspect = wordnet_lemmatizer.lemmatize(opinion['-target']).lower()
                category = opinion['-category']
                if aspect != "NULL":  # an empty list will be there for opinions with Null aspect
                    temp = re.findall(r"[\w']+",
                                      aspect.lower())  # we are removing punctuation as well as stop words from aspects (like changing wine by the glass to wine glass)
                    aspect = ' '.join([wordnet_lemmatizer.lemmatize(w) for w in temp if not w in stop_words])
                    opinionsData.append([aspect, category])

                sentenceData.append(opinionsData)

            reviewData.append(sentenceData)

aspects = []
for i in reviewData:
    for j in i:
        if j:
            aspects.append(j[0])

classes = []
for i in range(len(aspects)):
    groups = aspects[i][1].split('#')
    classes.append([aspects[i][0]] + groups)

# restaurant = ['RESTAURANT']
# ambience = ['AMBIENCE']
# food = ['FOOD']
# drinks = ['DRINKS']
# service = ['SERVICE']
# location = ['LOCATION']

restaurant = []
ambience = []
food = []
drinks = []
service = []
location = []


# for i in classes:
#     if i[1] == 'RESTAURANT':
#         restaurant.append([i[0], i[2]])
#     elif i[1] == 'FOOD':
#         food.append([i[0], i[2]])
#     elif i[1] == 'AMBIENCE':
#         ambience.append([i[0], i[2]])
#     elif i[1] == 'SERVICE':
#         service.append([i[0], i[2]])
#     elif i[1] == 'DRINKS':
#         drinks.append([i[0], i[2]])
#     elif i[1] == 'LOCATION':
#         location.append([i[0], i[2]])


for i in classes:
    i[0]=i[0].replace("'","")
    if i[0] !='null':
        if i[1] == 'RESTAURANT':
            restaurant.append(i[0])
        elif i[1] == 'FOOD':
            food.append(i[0])
        elif i[1] == 'AMBIENCE':
            ambience.append(i[0])
        elif i[1] == 'SERVICE':
            service.append(i[0])
        elif i[1] == 'DRINKS':
            drinks.append(i[0])
        elif i[1] == 'LOCATION':
            location.append(i[0])


#for i in set(restaurant):
 #   print i+",",
#print ''
#for i in set(food):
#    print i+",",
#print ''
#for i in set(ambience):
#    print i+",",
#print ''
#for i in set(service):
#    print i+",",
#print ''
#for i in set(drinks):
#    print i+",",
#print ''
#for i in set(location):
#    print i+",",

# print set(food)
# print set(ambience)
# print set(service)
# print set(drinks)
# print set(location)

r = [u'GENERAL', u'MISCELLANEOUS', u'PRICES']
f = [u'QUALITY', u'STYLE_OPTIONS', u'PRICES']
d = [u'STYLE_OPTIONS', u'PRICES', u'QUALITY']
a = [u'GENERAL']
s = [u'GENERAL']
l = [u'GENERAL']

aspectClasses = []
r0 = [r[0]]
r1 = [r[1]]
r2 = [r[2]]
for i in restaurant[1:]:

    if i[1] == r[0] and [i[0], 0] not in r0:
        r0.append([i[0], 0])
    elif i[1] == r[1] and [i[0], 1] not in r1:
        r1.append([i[0], 0])
    elif i[1] == r[2] and [i[0], 2] not in r2:
        r2.append([i[0], 0])

restaurant = ['RESTAURANT', r0, r1, r2]
# print restaurant

f0 = [f[0]]
f1 = [f[1]]
f2 = [f[2]]
for i in food[1:]:

    if i[1] == f[0] and [i[0], 1] not in f0:
        f0.append([i[0], 1])
    elif i[1] == f[1] and [i[0], 1] not in f1:
        f1.append([i[0], 1])
    elif i[1] == f[2] and [i[0], 1] not in f2:
        f2.append([i[0], 1])

food = ['FOOD', f0, f1, f2]
# print food


d0 = [d[0]]
d1 = [d[1]]
d2 = [d[2]]
for i in drinks[1:]:

    if i[1] == d[0] and [i[0], 2] not in d0:
        d0.append([i[0], 2])
    elif i[1] == d[1] and [i[0], 2] not in d1:
        d1.append([i[0], 2])
    elif i[1] == d[2] and [i[0], 2] not in d2:
        d2.append([i[0], 2])

drinks = ['DRINKS', d0, d1, d2]
# print drinks


a0 = [a[0]]
for i in ambience[1:]:

    if i[1] == a[0] and [i[0], 3] not in a0:
        a0.append([i[0], 3])

ambience = ['AMBIENCE', a0]
# print ambience


s0 = [s[0]]
for i in service[1:]:

    if i[1] == s[0] and [i[0], 4] not in s0:
        s0.append([i[0], 4])

service = ['SERVICE', s0]

l0 = [l[0]]
for i in location[1:]:

    if i[1] == l[0] and [i[0], 5] not in l0:
        l0.append([i[0], 5])

location = ['LOCATION', l0]
# print service

a = [r0[1:], r1[1:], r2[1:], f0[1:], f1[1:], f2[1:], d0[1:], d1[1:], d2[1:], a0[1:], s0[1:], l0[1:]]

for i in a:
    aspectClasses.extend(i)

from random import shuffle

shuffle(aspectClasses)

# returns a dictionary of aspect cluster label pairs
def getData():
    dict = {}
    for entry in aspectClasses:
        dict[entry[0]] = entry[1]
    return dict


# returns a dictionary of aspect as key and Main category as value
def getLabels():
    temp_labels = dict()
    for i in range(len(aspects)):
        groups = aspects[i][1].split('#')
        temp_labels[aspects[i][0].replace(" ","_")] = groups[0]
    return temp_labels


l = getLabels()

freq_restaurant_aspects_labels={'chicken':4, 'chef':2, 'sandwich':4, 'music':1, 'vibe':1, 'setting':1, 'waitstaff':2, 'salmon':4, 'seafood':4, 'rice':4, 'appetizer':4, 'hostess':2, 'crust':4, 'dinner':3, 'beer':5, 'delivery':2, 'topping':4, 'location': 0, 'sauce':4, 'view':1, 'pasta':4, 'people':1, 'martini':5, 'ingredient':3, 'server':2, 'salad':4, 'manager':2, 'spot':1, 'roll':4, 'portion':3, 'wine':5, 'ambience':1, 'dessert':3, 'fish':4, 'bagel':4, 'drink':5, 'waitress':2, 'menu':3, 'meal':3, 'dish':3, 'decor':1, 'waiter':2, 'sushi':4, 'atmosphere':1, 'pizza':4, 'staff':2, 'restaurant':0, 'place':0, 'service':2, 'food':3}

freq_laptop_aspects_labels={"charge":1,"battery_life":1, "program":3, "fan":2, "cost":0, "design":0, "use":0, "memory":2, "graphic":5, "work":0, "feature":0, "gaming":5, "window_7":3, "keyboard":2, "window":3, "speaker":5, "power_supply":1, "hard_drive":2,"iphoto":5, "quality":5, "size":0, "service":4, "system":0, "ram":2, "performance":0, "price":0, "battery life":1, "operating system":3, "motherboard":2, "screen":2, "key":2, "look":0, "value":0, "mouse":2, "boot":3, "speed":0, "battery":1, "touchpad":2, "game":5, "run":3, "shipping":4, "processor":2, "software":3, "warranty":4, "display":5, "vista":3, "application":3, "extended_warranty":4}
def get_ground_truth_values(model_aspects):
    truth_labels = []
    dict = getLabels()

    for aspect in model_aspects:
        truth_labels.append(dict[aspect])
        aspects.append(aspect)
    return truth_labels

def get_restaurant_labels(model_aspects):
    truth_labels = []
    dict = freq_restaurant_aspects_labels

    for aspect in model_aspects:
        truth_labels.append(dict[aspect])
        aspects.append(aspect)
    return truth_labels

def get_laptop_labels(model_aspects):
    truth_labels = []
    dict = freq_laptop_aspects_labels

    for aspect in model_aspects:
        truth_labels.append(dict[aspect])
        aspects.append(aspect)
    return truth_labels
