import os, json
import math
from numpy import array
with open(os.path.join(os.path.dirname(__file__),'constants.json')) as f:
    constants = json.load(f)
import pickle
from gensim import models
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA

from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer=WordNetLemmatizer()

def load_model_vectors(model_names):
    model_vectors = []
    aspects = []

    model_names= model_names.split(",")
    word_vectors_combination=[]
    model_combination=[]

    model_basepath = "."
    for model_name in model_names:
        filename=os.path.join(model_basepath, constants["file_paths"][model_name])

        if model_name == "glove" or model_name == "fasttext":
            model = KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), filename), binary=False)
        elif model_name == "s_sg" or model_name == "general" or model_name == "cwindow" or model_name == "cbow_wang" or model_name=="wang_r" or model_name=="wang_l" or model_name=="con2vec" or model_name=="w2v_general_sub" or model_name=="wang_general_sub" or model_name=="w2v_laptop" or model_name=="wang_laptop":
            model = KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), filename), binary=True)
        else:
            model = models.Word2Vec.load(os.path.join(os.path.dirname(__file__), filename))

        word_vectors = model.wv
        word_vectors_combination.append(word_vectors)
        model_combination.append(model)

    # with open('../data/aspect_list.bin','rb') as fp:
	 #    aspects_list = pickle.load(fp)

    with open('../data/multi_granular_restaurant.txt') as f:
        aspects_list = f.read().splitlines()

    for aspect in aspects_list:
        if aspect not in aspects:
            all_contain = True
            vector=[]
            for i in range (len(model_combination)):
                if wordnet_lemmatizer.lemmatize(aspect) not in word_vectors_combination[i].vocab:
                    if aspect=='hard_drive' or aspect =="battery_life":
                        print "asking for hard drive"
                        if aspect=='hard_drive':
                             vector  =vector+list(model_combination[i][wordnet_lemmatizer.lemmatize('harddrive')])

                        if aspect=='battery_life':
                             vector  =vector+list(model_combination[i][wordnet_lemmatizer.lemmatize('batteries')])
                        all_contain=True

                    else:
		        all_contain = False
                else:
                   # if model_name=='general':
                   #    if aspect=='battery_life':
                   #         vector  =vector+list(model_combination[i][wordnet_lemmatizer.lemmatize(aspect)])

                    vector  =vector+list(model_combination[i][wordnet_lemmatizer.lemmatize(aspect)])
            if all_contain:
                aspects.append(aspect)
                model_vectors.append(vector)
#    pca = PCA(n_components=14)
#    model_vectors = pca.fit_transform(model_vectors)
 #   selected=20
#    print pca.explained_variance_ratio_.cumsum()
#    for idx, x in enumerate( pca.explained_variance_ratio_.cumsum()):
#	if x>=0.8:
#	    selected=idx
#	    break
#    print selected

#    model_vectors = pca.fit_transform(model_vectors)
#    pca = PCA(n_components=selected)

    # # context aware word embeddings with tf-idf weightings
    # model_vectors, aspects = get_context_aware_wordembeddings(data, model_combination, word_vectors_combination)
    # pca = PCA(n_components=2)
    # model_vectors = pca.fit_transform(model_vectors)
    return model_vectors, aspects

def get_centroid(model_names, names, aspects_list, model_vectors):
    vectors = []
    label = names.split('-')

    for a in label:
        index = aspects_list.index(a)
        vectors.append(model_vectors[index])

    model_names = model_names.split(",")
    word_vectors_combination = []
    model_combination = []

    model_basepath = "."
    for model_name in model_names:
        filename = os.path.join(model_basepath, constants["file_paths"][model_name])

        if model_name == "glove" or model_name == "fasttext":
            model = KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), filename), binary=False)
        elif model_name == "s_sg" or model_name == "general" or model_name == "cwindow" or model_name == "cbow_wang" or model_name == "wang_r" or model_name == "wang_l" or model_name == "con2vec" or model_name == "w2v_general_sub" or model_name == "wang_general_sub" or model_name == "w2v_laptop" or model_name == "wang_laptop":
            model = KeyedVectors.load_word2vec_format(os.path.join(os.path.dirname(__file__), filename), binary=True)
        else:
            model = models.Word2Vec.load(os.path.join(os.path.dirname(__file__), filename))

        word_vectors = model.wv
        word_vectors_combination.append(word_vectors)
        model_combination.append(model)

    print('calculating centroid')
    print('labels: ', names)
    calc_centroid = lambda inp: [[math.fsum(m) / float(len(m)) for m in zip(*l)] for l in inp]

    centroid = calc_centroid([vectors])

    # word = model_combination[0].similar_by_vector(array(centroid[0]), topn=10, restrict_vocab=None)
    # print word
    pca = PCA(n_components=14)
    result = pca.fit_transform(model_combination[0])
    word = result.similar_by_vector(array(centroid[0]), topn=1, restrict_vocab=None)
    print(word[0][0])
    return word[0][0]