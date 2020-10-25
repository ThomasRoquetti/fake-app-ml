import csv
import os

header = ["author", "link", "category", "date of publication", "number of tokens", "number of words without punctuation", 
"number of types", "number of links inside the news", "number of words in upper case", 
"number of verbs", "number of subjuntive and imperative verbs" , "number of nouns", "number of adjectives",
"number of adverbs", "number of modal verbs", "number of singular first and second personal pronouns", 
"number of plural first personal pronouns", "number of pronouns", "pausality", "number of chracteres", "average sentence length", "average word length", 
"percentage of news with speeling errors", "emotiveness", "diversity"]

with open('emp.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(header)

    for x in range(1, 3603):
        try:
            filepath = os.path.normpath(r"C:\\Users\\thobo\\Documents\\TCC\\fake-app-ml\\fake-corpus-br\\full_texts\\{}\\{}.txt".format('fake', x))

            with open(filepath, 'r', newline='') as f_text:
                csv_text = csv.reader(f_text, delimiter='\n', skipinitialspace=True)
                csv_output.writerow(row[0] for row in csv_text)
        except:
            pass