from nltk.stem import WordNetLemmatizer
import re
import json

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

dictionary = {}

#extract the reviews and put into a seperate file
wordnet_lemmatizer = WordNetLemmatizer()

reviewData = []
# file = open('../data/extracted_reviews.txt', 'a')

with open('../data/reviews.json') as data_file:
    data = json.loads(data_file.read())

reviews = data['Reviews']

for review in reviews['Review']:
    sentences = review['sentences']
    temp = []
    for sentence in sentences['sentence']:
        sentenceData = []
        text = sentence['text']
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
                polarity = 1 if (opinion['-polarity'] == "positive") else -1 if (opinion['-polarity'] == "negative") else  0
                if aspect != "NULL":  # an empty list will be there for opinions with Null aspect
                    temp = re.findall(r"[\w']+",
                                      aspect.lower())  # we are removing punctuation as well as stop words from aspects (like changing wine by the glass to wine glass)
                    aspect = ' '.join([wordnet_lemmatizer.lemmatize(w) for w in temp if not w in stop_words])
                    reviewData.append([aspect, category, polarity,text])

                    if aspect in dictionary:
                        data = dictionary[aspect]
                        data['polarity'].append(polarity)
                        if text not in data['text']:
                            data['text'].append(text)
                    else:
                        data = {'category': [category], 'polarity':[polarity], 'text': [text]}
                        dictionary[aspect] = data
                # sentenceData.append(opinionsData)

            # reviewData.append(sentenceData)
# print(reviewData)
# print(dictionary)
# print(type(dictionary))
