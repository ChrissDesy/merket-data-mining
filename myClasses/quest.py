import os
import csv
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as eT
from flask import flash, session
# from tabula import wrapper
from random import randrange

def xml2df(xml_data):
    root = eT.XML(xml_data) # element tree
    all_records = []

    for i, child in enumerate(root):
        print(i)
        record = {}

        for subchild in child:
            record[subchild.tag] = subchild.text

        all_records.append(record)

    df = pd.DataFrame(all_records)
    return df

def update_headers(fname, user):
    headers = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'Country', 'CustomerID']
    df = pd.read_csv("tmp/"+user+'/'+fname, names = headers)
    return df

def extractData(filename):
    usern = session['username']
    print(os.getcwd()+" with file name "+filename)
    ext = os.path.splitext(filename)[-1].lower()
    print("extension is "+ext)
    
    try:
        if ext == ".pdf":
            # print('extracting '+ext)
            # fname = "pdfExtract%d"%randrange(1, 100)
            # wrapper.convert_into("tmp/"+usern+'/'+filename, "tmp/"+usern+'/'+fname, output_format='csv')
            # data = update_headers(fname, usern)
            # print("data found")
            # return data
            return []


        elif ext == ".txt":
            # print('extracting '+ext)
            # file_reader = pd.read_csv("tmp/"+usern+'/'+filename,delimiter='\t')
            # print("data found")
            # return file_reader
            return []

        elif ext == ".json":
            # print('extracting '+ext)
            # file_reader = pd.read_json("tmp/"+usern+'/'+filename)
            # print("data found")
            # return file_reader
            return []

        elif ext == ".xlsx":
            print('extracting '+ext)
            file_reader = pd.read_excel("tmp/"+usern+'/'+filename)
            # print("data found")
            return file_reader

        elif ext == ".csv" :
            print('extracting '+ext)
            file_reader = pd.read_csv("tmp/"+usern+'/'+filename)
            # print("data found")
            return file_reader

        else:
            print('Unrecognized file')
            return None

    except Exception as e:
        print("Error: "+ str(e))
        return e
