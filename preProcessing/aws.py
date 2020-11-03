import boto3
import json
import os
import csv

header = ["indice", "sentiment", "positive_chance", "negative_chance", "Neutrale_chance", "Mixed"]

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

fake_or_true = 'true'
                

with open('true_sentiment_aws.csv', 'w', newline='', encoding="utf8") as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(header)
        

    for x in range(1,3603):
        # try:
            filepath = os.path.normpath(r"C:\\Users\\thobo\\Documents\\TCC\\fake-app-ml\\fake-corpus-br\\full_texts\\{}\\{}.txt".format(fake_or_true, x))
            
            with open(filepath, 'r', encoding="utf8") as f_text:
                list_text = f_text.readlines()
                string = ""
                for item in list_text:
                    string += item
                
                comprehend_dict = comprehend.detect_sentiment(Text=string, LanguageCode='pt')
                dict_sentScore = comprehend_dict['SentimentScore']

                csv_list = [x, comprehend_dict['Sentiment'], dict_sentScore['Positive'], dict_sentScore['Negative'], dict_sentScore['Neutral'], dict_sentScore['Mixed']]
                csv_output.writerow(csv_list)

                
        # except:
            print("fail {}".format(x))