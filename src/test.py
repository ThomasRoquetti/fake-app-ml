from userRequestProcessor import UserProcessor
from apiCall import ApiCall
import json
import pandas as pd
import os
import csv

test = pd.read_csv("userRe/automl-test.csv") 
userProcessor = UserProcessor()
apiCall = ApiCall()

header = ["number of tokens","number of words in upper case","number of verbs","number of subjuntive and imperative verbs",
"number of nouns","number of adjectives","number of adverbs","number of modal verbs","number of singular first and second personal pronouns",
"number of plural first personal pronouns","number of pronouns","pausality","number of chracteres","average sentence length",
"average word length","document_score","document_magnitude","EVENT","LOCATION","ORGANIZATION","PERSON","classification"]



with open('userRe/automl-test_processeced.csv', 'w', newline='') as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(header)
    print("writed row and started")
    i=0
    for index, row in test.iterrows():
        number = row['indice']
        label = row['classification']


        try:
            filepath = os.path.normpath(r"/home/thoborges/fake-app-ml/fake-corpus-br/full_texts/{}/{}.txt".format(label.lower(), number))

            with open(filepath, 'r', newline='') as f_text:
                    texto = f_text.read()

            googleApi = apiCall.googleApi(text_content=texto)

            client = googleApi['client']
            document = googleApi['document']
            encoding = googleApi['encoding_type']

            sentiment = userProcessor.sentiment(client,document,encoding)
            entities = userProcessor.entities(client,document,encoding)
            syntax = userProcessor.syntax(client,document,encoding)
            text_lens = userProcessor.text_lens(document)
            pausality = userProcessor.pausality_calc(document)


            userProcessed ={
                'number_of_tokens': text_lens['number_of_tokens'],
                'number_of_words_in_uppercase': text_lens['number_of_words_in_uppercase'],
                'number_of_verbs': syntax['number_of_verbs'],
                'number_of_subj_imp_verbs': syntax['number_of_subj_imp_verbs'],    
                'number_of_nouns': syntax['number_of_nouns'],
                'number_of_adjectives': syntax['number_of_adjectives'],
                'number_of_adverbs': syntax['number_of_adverbs'],
                'number_of_modal_verbs': syntax['number_of_modal_verbs'],    
                'number_of_singular_fs_pron': syntax['number_of_singular_fs_pron'],
                'number_of_plural_f_pron': syntax['number_of_plural_f_pron'],    
                'number_of_pronouns': syntax['number_of_pronouns'],
                'pausality': pausality['pausality'],
                'number_of_chars': text_lens['number_of_chars'],
                'average_sent_len': text_lens['average_sent_len'],
                'average_word_len': text_lens['average_word_len'],
                "document_score": sentiment['document_score'], 
                "document_magnitude": sentiment['document_magnitude'],
                'EVENT': entities['EVENT'],
                'LOCATION': entities['LOCATION'],
                'ORGANIZATION': entities['ORGANIZATION'],
                'PERSON': entities['PERSON'],
                'classification':label
            }

            valuesToClassify = list(userProcessed.values())
            csv_output.writerow(valuesToClassify)
            print('done file: {}'.format(i)
            i+=1
        
        except:
            pass

print("DONE")