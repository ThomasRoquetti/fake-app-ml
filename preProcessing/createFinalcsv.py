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
fakeMeta.drop(["author", "link", "date of publication", "number of links inside the news", "emotiveness", "diversity",'category','percentage of news with speeling errors', 'number of types','number of words without punctuation'], axis=1, inplace=True)
fakeMeta.set_index('indice', inplace=True)

fakeEntity = pd.read_csv("fake-entity-processed.csv")
fakeEntity.set_index("indice", inplace=True)

fakeSentiment = pd.read_csv("fake_sentiment_gc.csv")
fakeSentiment.set_index("indice", inplace=True)

fakeMerged = fakeMeta.merge(fakeSentiment, left_index=True, right_index=True)
fakeMerged = fakeMerged.merge(fakeEntity, left_index=True, right_index=True)

fakeMerged = fakeMerged.drop(fakeMerged.index[[0,3,16,20,23,37,39,90]])
fakeMerged['classification'] = 'FAKE'

# i=1
# for index, row in fakeMerged.iterrows():
#     if int(index) != int(i):
#         print(i)
#         i+=1
#     i+=1
# print("End fake\n")
# fakeMerged.reset_index(drop=True, inplace=True)
#print(fakeMerged)

# Merge toguether csv for true 
trueMeta = pd.read_csv("true-meta-corpus.csv") 
trueMeta.drop(["author", "link", "date of publication", "number of links inside the news", "emotiveness", "diversity",'category','percentage of news with speeling errors', 'number of types','number of words without punctuation'], axis=1, inplace=True)
trueMeta.set_index('indice', inplace=True)

trueEntity = pd.read_csv("true-entity-processed.csv")
trueEntity.set_index("indice", inplace=True)

trueSentiment = pd.read_csv("true_sentiment_gc.csv")
trueSentiment.set_index("indice", inplace=True)

trueMerged = trueMeta.merge(trueSentiment, left_index=True, right_index=True)
trueMerged = trueMerged.merge(trueEntity, left_index=True, right_index=True)
trueMerged['classification'] = 'TRUE'

# i=1
# for index, row in trueMerged.iterrows():
#     if int(index) != int(i):
#         print(i)
#         i+=1
#     i+=1

trueMerged.reset_index(drop=True, inplace=True)
#print(trueMerged)

merged = pd.concat([fakeMerged, trueMerged])
merged.to_csv("finalCSVforTraining3.csv")

