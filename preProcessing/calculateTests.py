import pandas as pd
import numpy as np
import boto3
import sagemaker
import os, sys

region = boto3.Session().region_name

sm = boto3.Session().client(service_name='sagemaker',region_name=region)
sm_rt = boto3.Session().client('runtime.sagemaker', region_name=region)

ep_name = "automl-dm-ep-03-03-31-06"

# automl_test = pd.read_csv('preProcessing/automl-test.csv')
# automl_test.drop('indice', axis=1, inplace=True)
# automl_test.to_csv(r'preProcessing/automl-test2.csv', index=False)

"""automl-test2 => Accuracy: 0.9506, Precision: 0.9557, Recall: 0.9831, F1: 0.9692 #"""
"""Accuracy: 0.9479, Precision: 0.9531, Recall: 0.7798, F1: 0.8578"""
tp = tn = fp = fn = count = 0

with open('userRe/automl-test_processeced.csv') as f:
    lines = f.readlines()
    for l in lines[1:]:   # Skip header
        l = l.split(',')  # Split CSV line into features
        label = l[-1]     # Store 'yes'/'no' label
        l = l[:-1]        # Remove label
        l = ','.join(l)   # Rebuild CSV line without label
                
        response = sm_rt.invoke_endpoint(EndpointName=ep_name, ContentType='text/csv', Accept='text/csv', Body=l)

        response = response['Body'].read().decode("utf-8")
        #print ("label %s response %s" %(label,response))

        if 'TRUE' in label:
            # Sample is positive
            if 'TRUE' in response[0:4]:
                # True positive
                tp=tp+1
            else:
                # False negative
                fn=fn+1
        else:
            # Sample is negative
            if 'FAKE' in response[0:4]:
                # True negative
                tn=tn+1
            else:
                # False positive
                fp=fp+1
        count = count+1
        if (count % 100 == 0):   
            sys.stdout.write(str(count)+' ')
            
print ("Done")

print ("%d %d" % (tn, fp))
print ("%d %d" % (fn, tp))

accuracy  = (tp+tn)/(tp+tn+fp+fn)
precision = tp/(tp+fp)
recall    = tn/(tp+fn)
f1        = (2*precision*recall)/(precision+recall)

print ("Accuracy: %.4f, Precision: %.4f, Recall: %.4f, F1: %.4f" % (accuracy, precision, recall, f1))

#Accuracy: 0.9576, Precision: 0.9629, Recall: 0.9901, F1: 0.9763#