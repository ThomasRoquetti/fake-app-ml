from google.cloud import language_v1
from google.cloud.language_v1 import enums
import os
import csv

os.environ['GOOGLE_APPLICATION_CREDENTIALS']="credentials/google.json"

client = language_v1.LanguageServiceClient()

type_ = enums.Document.Type.PLAIN_TEXT

language = "pt"


encoding_type = enums.EncodingType.UTF8


fake_or_true = 'fake'

header = ["indice", "mention_content", "mention_type"]

with open('fake_mention_gc.csv', 'w', newline='', encoding="utf8") as f_output:
    csv_output = csv.writer(f_output)
    csv_output.writerow(header)
        

    for x in range(1,3603):
        try:
            filepath = os.path.normpath(r"C:\\Users\\thobo\\Documents\\TCC\\fake-app-ml\\fake-corpus-br\\full_texts\\{}\\{}.txt".format(fake_or_true, x))
            
            with open(filepath, 'r', encoding="utf8") as f_text:
                list_text = f_text.readlines()
                string = ""
                for item in list_text:
                    string += item

                document = {"content": string, "type": type_, "language": language}

                response = client.analyze_entities(document, encoding_type=encoding_type)

                for mention in entity.mentions:
                    mention_content = mention.text.content
                    mention_type = enums.EntityMention.Type(mention.type).name
                    csv_list = [x, mention_content, mention_type]
                    csv_output.writerow(csv_list)
        except:
            print("fail {}".format(x))