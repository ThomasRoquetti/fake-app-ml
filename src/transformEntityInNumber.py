import pandas as pd
import csv
import numpy as np

header = ['indice','person','organization','event']

fakeEntity = pd.read_csv('fake_entity_gc.csv')
fakeEntity.drop(["representative_name"], axis=1, inplace=True)
fakeEntityMean = fakeEntity.groupby(['indice','entity_type']).mean()
fakeEntityMean = fakeEntityMean.pivot_table(values='entity_salience', index='indice', columns='entity_type', aggfunc='first')
print(fakeEntityMean)

fakeEntityMean.to_csv('fake-entity-processed.csv')