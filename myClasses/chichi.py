#imports..
import os
from pathlib import Path
import time
import pandas as pd
from flask import session

#create datasets and integrations...
def integration(theData, type):
	print('Received data for intergrating: \n'+str(theData))

	theDate = time.strftime('%d-%b-%y')
	headers = [
		'country','year','c_new_tsr',
		'tbhiv_fail','tbhiv_died','tbhiv_succ',
		'mdr_fail','mdr_died','mdr_succ',
		'xdr_fail','xdr_died','xdr_succ',
		'c_tbhiv_tsr','c_newinc',
		'conf_xdr_tx','conf_mdr_tx',
		'hivtest_pos','ret_rel'
		]

	#check and load original data...
	try:
		ogPath = Path('data/new_Data.csv')
		# ogPath = os.path.join('data/new_Data.csv')
		ogData = pd.read_csv(str(ogPath))
		isAvailable = True
	except Exception as e:
		print('Original Data not found in ' + str(ogPath) +' with Error: '+ str(e))
		isAvailable = False

	#merge data...
	try:
		if isAvailable:
			oldPath = Path('data/old/old_Data')
			# newData = pd.concat([ogData, theData], sort=False).drop_duplicates().reset_index(drop=False)
			newData = pd.concat([ogData, theData], sort=False, ignore_index=True).drop_duplicates()
			ogData.to_csv(str(oldPath)+str(theDate)+'.csv')
		else:
			newData = theData

		newData.to_csv('data/new_data.csv', columns = headers, index=False)
		return True

	except Exception as e:
		print(e)
		return False

#merge dataframes...
def merge(data1, data2):
	try:
		finalData = pd.concat([data1, data2]).drop_duplicates().reset_index(drop=True)
		finalData.to_csv('tmp/tb_merged_data.csv')
		return True

	except Exception as ex:
		print("Error when saving to file. Error: "+str(ex))
		return False
