#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 16:34:22 2017

@author: congdonguyen
"""

import json
import nltk
from collections import Counter as cnt
from nltk.corpus import stopwords
from nltk.corpus import words as wCorpus

import csv

stars1 = cnt()
stars2 = cnt()
stars3 = cnt()
stars4 = cnt()
stars5 = cnt()
col1 = []
col2 = []

#Open json file
with open('yelp_academic_dataset_review_small.json') as jsonData:
    jsonObject = json.load(jsonData)
#dump JSON
json_string = json.dumps(jsonObject)
_object = json.loads(json_string)
#Initialize stemmer
wnl = nltk.WordNetLemmatizer()
#Initialize corpuses
wCorpus = set(wCorpus.words("en"))
stopwords = set(stopwords.words("english"))

#Iterate through the object to extract the text and stars, put each text (review) in to corresponding stars
for sub_json in _object:
    text = sub_json.get('text')
    Stars = sub_json.get('stars')
    words = nltk.word_tokenize(text)
    words = [w.lower() for w in words]
    words = [wnl.lemmatize(w) for w in words if w not in stopwords and w.isalnum()]
    if(Stars==1):
        stars1 += cnt(words)
    elif(Stars==2):
        stars2 += cnt(words)
    elif(Stars==3):
        stars3 += cnt(words)
    elif(Stars==4):
        stars4 += cnt(words)
    else:
        stars5 += cnt(words)

#Create a superset to get the sum of all keys in Counter object
superSet = stars1 + stars2 + stars3 + stars4 + stars5

#Discard lemmas that is used fewer than 10
for i in list(superSet):
    if(i not in wCorpus or superSet[i] < 10):
        del superSet[i]
        if(i in set(stars1)):
            del stars1[i]
        if(i in set(stars2)):
            del stars2[i]
        if(i in set(stars3)):
            del stars3[i]
        if(i in set(stars4)):
            del stars4[i]
        if(i in set(stars5)):
            del stars5[i]


#Average = sum/total => mutiply coresponding stars to the number of the element counted in stars counter object
#get the sum for all the stars and divide by the total element occured in the superset
for i in stars2:
    stars2[i] = stars2.get(i)* 2
for i in stars3:
    stars3[i] = stars3.get(i)* 3
for i in stars4:
    stars4[i] = stars4.get(i)* 4
for i in stars5:
    stars5[i] = stars5.get(i)* 5

denom = stars1 + stars2 + stars3 + stars4 + stars5

#Calculate
for i in superSet:
    superSet[i] = float(denom[i] / superSet[i])

#Pick out most and least common
col1 += superSet.most_common()[:-499-1:-1]
col2 += superSet.most_common()[:499]
#ZIP!
rows = zip(col1, col2)
#Write CSV file
with open("data.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    write = writer.writerow(['Most negative lemmas','Most positive lemmas'])
    writer = writer.writerows(rows)

        


                    


