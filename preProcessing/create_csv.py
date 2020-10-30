import csv
import os
import pandas as pd

header = ["author", "link", "category", "date of publication", "number of tokens", "number of words without punctuation", 
"number of types", "number of links inside the news", "number of words in upper case", 
"number of verbs", "number of subjuntive and imperative verbs" , "number of nouns", "number of adjectives",
"number of adverbs", "number of modal verbs", "number of singular first and second personal pronouns", 
"number of plural first personal pronouns", "number of pronouns", "pausality", "number of chracteres", "average sentence length", "average word length", 
"percentage of news with speeling errors", "emotiveness", "diversity","indice"]

with open('true-meta-corpus.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(header)

    for x in range(1, 3603):
        try:
            filepath = os.path.normpath(r"/home/thoborges/fake-app-ml/fake-corpus-br/full_texts/{}-meta-information/{}-meta.txt".format('true', x))

            with open(filepath, 'r', newline='') as f_text:
                with open(filepath, 'a') as f_text_indice:
                    f_text_indice.write("\n"+str(x))
                csv_text = csv.reader(f_text, delimiter='\n', skipinitialspace=True)
                csv_output.writerow(row[0] for row in csv_text)
        except:
            pass