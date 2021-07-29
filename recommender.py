import numpy as np
from sklearn.metrics.pairwise import linear_kernel
import random
from numpy.core.fromnumeric import size
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pickle
from random import randint, randrange

df = pd.read_csv('gen_books.csv')

def combine_features(data):
    features = []
    for i in range(0, data.shape[0]):
        features.append(str(data['original_title'].iloc[i])+' '+str(data['authors'].iloc[i]))
    return features

df['combined_feature'] = combine_features(df)
cm = CountVectorizer().fit_transform(df['combined_feature'])
cs = cosine_similarity(cm)

def recommend(Title):
    titles=df.original_title.tolist()
    count=titles.count(Title)
    if (count>0):
        book_id = df[df.original_title== Title]['book_index'].values[0]
        scores = list(enumerate(cs[book_id]))
        sorted_scores = sorted(scores,key= lambda x:x[1], reverse = True)
        sorted_scores = sorted_scores[1:]
        j = 0
        book_title = []
        for item in sorted_scores:
            book_title.append(df[df.book_index == item[0]]['original_title'].values[0])
            j = j +1
            if j>=20:
                break 
        books = []
        x = randint(1,5)
        for i in range(x,x+5):
            books.append(book_title[i])
        return books
    else:
        return 0
