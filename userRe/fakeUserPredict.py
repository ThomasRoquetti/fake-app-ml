import pandas as pd
import numpy as np
import boto3
import sagemaker
import os, sys


class UserPredict():

    def predict(self, parameters):
        print('Starting Prediction')
        region = boto3.Session().region_name
        
        sm = boto3.Session().client(service_name='sagemaker',region_name=region)
        sm_rt = boto3.Session().client('runtime.sagemaker', region_name=region)

        ep_name = "automl-dm-ep-03-03-31-06"
                        
        string_parameters = [str(i) for i in parameters] 
        parameters = ','.join(string_parameters)

        response = sm_rt.invoke_endpoint(EndpointName=ep_name, ContentType='text/csv', Accept='text/csv', Body=parameters)
        #print(response)
        userResponse = response['Body'].read().decode("utf-8")

        characters = ["'",'"'," ","[","]"]
        for character in characters:
            userResponse = userResponse.replace(character, "")

        userResponse = userResponse.rstrip("\n")
        userResponse = userResponse.split(',')
        print(userResponse)

        sm.get_waiter('endpoint_in_service').wait(EndpointName=ep_name)

        resp = sm.describe_endpoint(EndpointName=ep_name)
        status = resp['EndpointStatus']
        print(status)

        return userResponse