from myClasses.quest import extractData
from myClasses.brt import cleanData
from myClasses.chichi import integration
import os

def processData(filename):
    print("received file "+filename)
    status = False
          
    #extract the data from file
    extractedData = extractData(filename)

    if extractedData is not False:
        #clean the data
        cleanedData = cleanData(extractedData)

        #store file
        status = integration(cleanedData, 'type')

    return status