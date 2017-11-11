# Created by Ian Annase on 11/11/2017

from xlwt import Workbook
import json
import requests

# key and base url
key="YOUR_KEY"
baseURL="https://api.mailgun.net/v3/YOUR_DOMAIN/"

# excel workbooks
bouncesWorkbook = Workbook()
complaintsWorkbook = Workbook()
unsubscribesWorkbook = Workbook()

# sheets
bouncesSheet = bouncesWorkbook.add_sheet('Bounces')
complaintsSheet = complaintsWorkbook.add_sheet('Complaints')
unsubscribesSheet = unsubscribesWorkbook.add_sheet('Unsubscribes')

# api call for bounces
page = baseURL + "bounces"
z=0
for i in range(5): # each number in this range gets 10,000 list items
	request = requests.get(page, auth=("api", key), params={"limit": 10000})
	data = request.json()
	for j in range(len(data['items'])):
		page = data['paging']['next']
		emailAddress=data['items'][j]['address']
		bouncesSheet.write(z,0,emailAddress)
		print(emailAddress)
		z+=1

# api call for complaints
page = baseURL + "complaints"
z=0
for i in range(5): # each number in this range gets 10,000 list items
	request = requests.get(page, auth=("api", key), params={"limit": 10000})
	data = request.json()
	for j in range(len(data['items'])):
		page = data['paging']['next']
		emailAddress=data['items'][j]['address']
		complaintsSheet.write(z,0,emailAddress)
		print(emailAddress)
		z+=1

# api call for bounces
page = baseURL + "unsubscribes"
z=0
for i in range(5): # each number in this range gets 10,000 list items
	request = requests.get(page, auth=("api", key), params={"limit": 10000})
	data = request.json()
	for j in range(len(data['items'])):
		page = data['paging']['next']
		emailAddress=data['items'][j]['address']
		unsubscribesSheet.write(z,0,emailAddress)
		print(emailAddress)
		z+=1

# save workbooks
bouncesWorkbook.save('bounces.xls')
complaintsWorkbook.save('complaints.xls')
unsubscribesWorkbook.save('unsubscribes.xls')