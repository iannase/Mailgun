# Created by Ian Annase on 11/11/2017

import xlsxwriter
import json
import requests

# key and base url
key="YOUR_KEY"
baseURL="https://api.mailgun.net/v3/YOUR_DOMAIN/"

# excel workbooks
bouncesWorkbook = xlsxwriter.Workbook('bounces.xlsx')
complaintsWorkbook = xlsxwriter.Workbook('complaints.xlsx')
unsubscribesWorkbook = xlsxwriter.Workbook('unsubscribes.xlsx')

# sheets
bouncesSheet = bouncesWorkbook.add_worksheet()
complaintsSheet = complaintsWorkbook.add_worksheet()
unsubscribesSheet = unsubscribesWorkbook.add_worksheet()

print()
print("Loading...")
print()

# api call for bounces
page = baseURL + "bounces"
z=0
while True: # each number in this range gets 10,000 list items
	# api call
	request = requests.get(page, auth=("api", key), params={"limit": 10000})
	data = request.json()

	# break the loop if there's no data left
	if len(data['items']) == 0:
		break

		# append and print email address
	for j in range(len(data['items'])):
		page = data['paging']['next']
		emailAddress=data['items'][j]['address']
		bouncesSheet.write(z,0,emailAddress)
		print(emailAddress)
		z+=1

	print()
	print(str(z) + " bounces downloaded so far..")
	bouncesDownloaded = z

# api call for complaints
page = baseURL + "complaints"
z=0
while True:
	# api call
	request = requests.get(page, auth=("api", key), params={"limit": 10000})
	data = request.json()

	# break the loop if there's no data left
	if len(data['items']) == 0:
		break

	# append and print email address
	for j in range(len(data['items'])):
		page = data['paging']['next']
		emailAddress=data['items'][j]['address']
		complaintsSheet.write(z,0,emailAddress)
		print(emailAddress)
		z+=1

	print()
	print(str(bouncesDownloaded) + " bounces downloaded.")
	print(str(z) + " complaints downloaded so far..")
	complaintsDownloaded = z

# api call for bounces
page = baseURL + "unsubscribes"
z=0
while True:
	# api call
	request = requests.get(page, auth=("api", key), params={"limit": 10000})
	data = request.json()

	# break the loop if there's no data left
	if len(data['items']) == 0:
		break

	# append and print email address
	for j in range(len(data['items'])):
		page = data['paging']['next']
		emailAddress=data['items'][j]['address']
		unsubscribesSheet.write(z,0,emailAddress)
		print(emailAddress)
		z+=1

	print()
	print(str(bouncesDownloaded) + " bounces downloaded.")
	print(str(complaintsDownloaded) + " complaints downloaded.")
	print(str(z) + " unsubscribes downloaded so far..")
	unsubscribesDownloaded = z

print()
print("Success!")
print()
print(str(bouncesDownloaded) + " bounces downloaded.")
print(str(complaintsDownloaded) + " complaints downloaded.")
print(str(unsubscribesDownloaded) + " complaints downloaded.")

# save workbooks
bouncesWorkbook.close()
complaintsWorkbook.close()
unsubscribesWorkbook.close()
