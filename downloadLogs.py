from prettytable import PrettyTable
import xlsxwriter
import json
import requests

# key and base url
key="YOUR_KEY"
baseURL="https://api.mailgun.net/v3/YOUR_DOMAIN/"

# some variables
openedSum=0
clickedSum=0
deliveredSum=0
failedSum=0

# tags
tag = raw_input("Please enter a tag: ")
tagA = tag + "a"
tagB = tag + "b"
tagC = tag + "c"
tags = [tag,tagA,tagB,tagC]

# open excel workbooks
logsWorkbook = xlsxwriter.Workbook('Consolidated Logs ' + tag + '.xlsx')

# add a sheet
logsSheet = logsWorkbook.add_worksheet()

# add headers
bold = logsWorkbook.add_format({'bold': True})
logsSheet.write('A1',"Tag",bold)
logsSheet.write('B1',"Event",bold)
logsSheet.write('C1',"Email Address",bold)
logsSheet.write('D1',"City",bold)
logsSheet.write('E1',"State",bold)
logsSheet.write('F1',"Client",bold)
logsSheet.write('G1',"OS",bold)
logsSheet.write('H1',"Device",bold)

z=1 # list incrementor

# increment through tags a-c
for i in tags:
	lastPage = True
	# original URL
	page = baseURL + "events"

	while lastPage: # each number in this range gets 300 list items
		#table format
		t = PrettyTable(['Tag', 'Event', 'Email', 'City', 'OS', 'Device'])

		# api call
		request = requests.get(page, auth=("api", key), params={"limit": 300, "tags":[i]})
		data = request.json()

		# exit loop if it's the page
		if len(data['items']) == 0:
			lastPage = False
			continue

		for j in range(len(data['items'])):
			# reset all the variables
			emailAddress=""
			city=""
			state=""
			tag=""
			event=""
			client=""
			os=""
			device=""

			# next page URL
			page = data['paging']['next']

			# parse data
			try:
				emailAddress=data['items'][j]['recipient']
			except KeyError:
				pass
			try:
				city = data['items'][j]['geolocation']['city']
			except KeyError:
				pass
			try:
				state = data['items'][j]['geolocation']['region']
			except KeyError:
				pass
			try:
				tag = data['items'][j]['tags'][0]
			except KeyError:
				pass
			try:
				event = data['items'][j]['event']
			except KeyError:
				pass
			try:
				client = data['items'][j]['client-info']['client-name']
			except KeyError:
				pass
			try:
				os = data['items'][j]['client-info']['client-os']
			except KeyError:
				pass
			try:
				device = data['items'][j]['client-info']['device-type']
			except KeyError:
				pass

			# sums of totals
			if event == "delivered":
				deliveredSum+=1
			if event == "opened":
				openedSum+=1
			if event == "clicked":
				clickedSum+=1
			if event == "failed":
				failedSum+=1

			# format the city
			cityState = city + ", " + state

			# add a row to the table
			t.add_row([tag,event,emailAddress,cityState,os,device])

			# write to the logs
			logsSheet.write(z,0,tag)
			logsSheet.write(z,1,event)
			logsSheet.write(z,2,emailAddress)
			logsSheet.write(z,3,city)
			logsSheet.write(z,4,state)
			logsSheet.write(z,5,client)
			logsSheet.write(z,6,os)
			logsSheet.write(z,7,device)
			z+=1

		# output during download
		print t
		print
		print(str(z-1) + " logs downloaded.")

# open and click through rates
openRate = round(openedSum/deliveredSum*100,2)
clickThroughRate = round(clickedSum/openedSum*100,2)

# list sums in the excel file
logsSheet.write('J1', 'Delivered',bold)
logsSheet.write('K1', 'Opened',bold)
logsSheet.write('L1', 'Clicked',bold)
logsSheet.write('M1', 'Failed',bold)
logsSheet.write('J2', deliveredSum)
logsSheet.write('K2', openedSum)
logsSheet.write('L2', clickedSum)
logsSheet.write('M2', failedSum)
logsSheet.write('J4', "Open Rate",bold)
logsSheet.write('M4', "Click Through Rate",bold)
logsSheet.write('J5', str(openRate)+"%")
logsSheet.write('M5', str(clickThroughRate)+"%")

# close the workbook
logsWorkbook.close()