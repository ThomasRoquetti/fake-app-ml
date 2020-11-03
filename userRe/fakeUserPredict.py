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

userPredict("318, 286, 0, 8, 31, 0, 115, 7, 14, 3, 0, 0, 8, 4.8, 1391, 27.8, 4.863636363636363, 0, 0.0, 1.7999999523162842, 0.010209628380835056, 0.01110676055153211, 0.01392211583442986, 0.011159727011214603")