import pandas as pd
import csv
import numpy as np

header = ['indice','person','organization','event']

fakeEntity = pd.read_csv('true_entity_gc.csv')
fakeEntity.drop(["representative_name"], axis=1, inplace=True)
fakeEntityMean = fakeEntity.groupby(['indice','entity_type']).mean()
fakeEntityMean = fakeEntityMean.pivot_table(values='entity_salience', index='indice', columns='entity_type', aggfunc='first')
fakeEntityMean.drop(["ADDRESS","CONSUMER_GOOD",'OTHER','PHONE_NUMBER','DATE','NUMBER','PRICE','WORK_OF_ART'],axis=1,inplace=True)
print(fakeEntityMean)

fakeEntityMean.to_csv('true-entity-processed.csv')