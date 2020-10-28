header1 = ["author", "link", "category", "date of publication", "number of tokens", "number of words without punctuation", 
"number of types", "number of links inside the news", "number of words in upper case", 
"number of verbs", "number of subjuntive and imperative verbs" , "number of nouns", "number of adjectives",
"number of adverbs", "number of modal verbs", "number of singular first and second personal pronouns", 
"number of plural first personal pronouns", "number of pronouns", "pausality", "number of chracteres", "average sentence length", "average word length", 
"percentage of news with speeling errors", "emotiveness", "diversity"]

header2 = ["indice","document_score","document_magnitude"]

header3 = ["indice","representative_name","entity_type","entity_salience"]

rmHeader = ["author", "link", "date of publication", "number of links inside the news", "emotiveness", "diversity", "indice"]

import csv
import os
import pandas as pd

# with open('finalCSV.csv', 'w', newline='') as f_output:
#     csv_output = csv.writer(f_output)
#     csv_output.writerow(header)

#     for x in range(1, 3603):
#         try:
#             filepath = os.path.normpath(r"C:\\Users\\thobo\\Documents\\TCC\\fake-app-ml\\fake-corpus-br\\full_texts\\{}\\{}.txt".format('fake', x))

#             with open(filepath, 'r', newline='') as f_text:
#                 csv_text = csv.reader(f_text, delimiter='\n', skipinitialspace=True)
#                 csv_output.writerow(row[0] for row in csv_text)
#         except:
#             pass

fakeMeta = pd.read_csv("fake-meta-corpus.csv") 
print(fakeMeta)
print(type(fakeMeta))
fakeMeta.drop(["author", "link", "date of publication", "number of links inside the news", "emotiveness", "diversity"], axis=1, inplace=True)
print(fakeMeta)