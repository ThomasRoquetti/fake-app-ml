import pandas as pd
import numpy as np
import boto3
import sagemaker
import os, sys

def userPredict(parameters):
    region = boto3.Session().region_name

    sm = boto3.Session().client(service_name='sagemaker',region_name=region)
    sm_rt = boto3.Session().client('runtime.sagemaker', region_name=region)

    ep_name = "automl-dm-ep-30-03-36-26"
                    
    response = sm_rt.invoke_endpoint(EndpointName=ep_name, ContentType='text/csv', Accept='text/csv', Body=parameters)
    #print(response)
    print(response['Body'].read().decode("utf-8"))

    sm.get_waiter('endpoint_in_service').wait(EndpointName=ep_name)

    resp = sm.describe_endpoint(EndpointName=ep_name)
    status = resp['EndpointStatus']

userPredict("186,166,112,4,27,2,52,4,5,2,0,0,5,2.5,832,20.75,5.01205,0.0,0.0,1.2999999523162842,0.0126278103950123,,0.020194279650847118,0.023404215104304828")