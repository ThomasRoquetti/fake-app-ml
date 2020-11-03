from google.cloud import language_v1
from google.cloud.language_v1 import enums
import sagemaker
import boto3
import json
import os, sys
import csv

class ApiCall():

    def googleApi(self, text_content):

        os.environ['GOOGLE_APPLICATION_CREDENTIALS']="credentials/google.json"

        client = language_v1.LanguageServiceClient()

        # Available types: PLAIN_TEXT, HTML
        type_ = enums.Document.Type.PLAIN_TEXT

        language = "pt"
        document = {"content": text_content, "type": type_, "language": language}

        encoding_type = enums.EncodingType.UTF8

        return {'client':client, 'document':document, 'encoding_type':encoding_type}
