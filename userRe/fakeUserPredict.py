import pandas as pd
import numpy as np
import boto3
import sagemaker
import os, sys


sess   = sagemaker.Session()
bucket = sess.default_bucket()                     
prefix = 'sagemaker/automl-dm'
region = boto3.Session().region_name

# Role when working on a notebook instance
role = "arn:aws:iam::388295382521:role/service-role/AmazonSageMaker-ExecutionRole-20201029T114207"

sm = boto3.Session().client(service_name='sagemaker',region_name=region)
sm_rt = boto3.Session().client('runtime.sagemaker', region_name=region)

ep_name = "automl-dm-ep-29-19-27-44"

l = "sociedade_cotidiano,166,146,110,1,28,0,47,8,6,5,0,0,6,2.85714,740,20.8571,5.06849,0.0,0.0,1.2000000476837158,0.017082443693652753,,0.011033521344264349,0.01707558892667294"
                
response = sm_rt.invoke_endpoint(EndpointName=ep_name, ContentType='text/csv', Accept='text/csv', Body=l)
response = response['Body'].read().decode("utf-8")
print(response)

sm.get_waiter('endpoint_in_service').wait(EndpointName=ep_name)

resp = sm.describe_endpoint(EndpointName=ep_name)
status = resp['EndpointStatus']

print("Endpoint ARN   : " + resp['EndpointArn'])
print("Endpoint status: " + status)