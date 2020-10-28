header1 = ["author", "link", "category", "date of publication", "number of tokens", "number of words without punctuation", 
"number of types", "number of links inside the news", "number of words in upper case", 
"number of verbs", "number of subjuntive and imperative verbs" , "number of nouns", "number of adjectives",
"number of adverbs", "number of modal verbs", "number of singular first and second personal pronouns", 
"number of plural first personal pronouns", "number of pronouns", "pausality", "number of chracteres", "average sentence length", "average word length", 
"percentage of news with speeling errors", "emotiveness", "diversity"]

header2 = ["indice","document_score","document_magnitude"]

header3 = ["indice","representative_name","entity_type","entity_salience"]

rmHeader = ["author", "link", "date of publication", "number of links inside the news", "emotiveness", "diversity"]

import csv
import os
import pandas as pd


# Merge toguether csv for fake

fakeMeta = pd.read_csv("fake-meta-corpus.csv") 
fakeMeta.drop(["author", "link", "date of publication", "number of links inside the news", "emotiveness", "diversity"], axis=1, inplace=True)
fakeMeta.set_index('indice', inplace=True)
print(fakeMeta)

fakeEntity = pd.read_csv("fake_entity_gc.csv")
fakeEntity.set_index("indice", inplace=True)
print(fakeEntity)

fakeSentiment = pd.read_csv("fake_sentiment_gc.csv")
fakeSentiment.set_index("indice", inplace=True)
print(fakeSentiment)

fakeMerged = fakeMeta.merge(fakeSentiment, left_index=True, right_index=True)
print(fakeMerged)
