import numpy as np
import pandas as pd

""" df = pd.read_csv('cars.csv')
df.head()

print(df.isnull().sum())

to_drop = ['vs', 'am', 'mpg'] #dropping unwanted columns
df.drop(to_drop, inplace = True, axis = 1)

df['Name'].is_unique #checking if Name column is unique
df = df.set_index('Name')

df.dropna(thresh = 8) #dropping rows with less 8 or less


df.dropna(inplace = True) #drop rows with missing values
print(df.shape) #summarize the number of rows and columns in the dataset

print(df) """

def cleanData(theData):
    #theData.dropna(thresh = 8) #dropping rows with 8 or less
    #theData = theData.loc[:, theData.isnull().sum() < 0.8*theData.shape[0]]
    #theData.dropna(inplace = True) #drop rows with missing values
    print('Received data for cleaning: \n'+str(theData))

    return theData