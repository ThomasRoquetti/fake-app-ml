import pandas as pd
import numpy as np
import boto3
import sagemaker
import os, sys

print (sagemaker.__version__)

sess   = sagemaker.Session()
bucket = sess.default_bucket()                     
prefix = 'sagemaker/automl-dm'
region = boto3.Session().region_name

# Role when working on a notebook instance
role = "arn:aws:iam::388295382521:role/service-role/AmazonSageMaker-ExecutionRole-20201029T114207"

data = pd.read_csv('finalCSVforTraining.csv', sep=',')
data.set_index('indice', inplace=True)
pd.set_option('display.max_columns', 500)     # Make sure we can see all of the columns
pd.set_option('display.max_rows', 50)         # Keep the output on one page
print(data[:10]) # Show the first 10 lines


print(data.shape) # (number of lines, number of columns)

train_data, test_data, _ = np.split(data.sample(frac=1, random_state=123), 
                                                  [int(0.85 * len(data)), int(len(data))])  

# Save to CSV files
train_data.to_csv('automl-train.csv', index=False, header=True, sep=',') # Need to keep column names
test_data.to_csv('automl-test.csv', index=False, header=True, sep=',')