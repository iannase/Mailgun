# Created by Ian Annase on 11/11/2017

from prettytable import PrettyTable
import requests
import json
import math
import datetime

# key and base URL
key="YOUR_KEY"
baseURL="https://api.mailgun.net/v3/YOUR_DOMAIN/"

# menu loop
for z in range(10):
	# tags
	print()
	tag = input("Enter a tag: ")
	tagA = tag + "a"
	tagB = tag + "b"
	tagC = tag + "c"

	# create file
	filename = "./results/"+tag+" statistics.txt"
	f = open(filename,"w")

	# array of tags
	tags = [tag,tagA,tagB,tagC]

	#sums
	acceptedSum=0
	deliveredSum=0
	opensSum=0
	uniqueOpensSum=0
	clicksSum=0
	uniqueClicksSum=0
	failuresSum=0
	unsubscribesSum=0
	complaintsSum=0
	bouncesSum=0
	originalBouncesSum=0
	originalComplainsSum=0
	mobileOpenSum=0
	mobileClickSum=0
	desktopOpenSum=0
	desktopClickSum=0
	tabletOpenSum=0
	tabletClickSum=0

	print()
	print()

	# get logs for a,b,c
	for i in tags:
		# api request
		request = requests.get(baseURL + "tags/" + i + "/stats",
		        auth=("api", key),
		        params={"event": ["accepted", "delivered", "opened", "clicked", "failed", "unsubscribed", "complained", "stored"],"duration": "1m"})

		# json response object
		data = request.json()

		t = PrettyTable(['Event', '#'])

		# reset variables
		accepted = 0
		delivered = 0
		opened = 0
		uniqueOpened = 0
		clicked = 0
		uniqueClicked = 0
		failed = 0
		unsubscribed = 0
		complained = 0
		bounced = 0
		originalBounced = 0
		originalComplained = 0

		# get response objects
		try:
			accepted = data['stats'][0]['accepted']['total']
		except KeyError:
			pass
		try:
			delivered = data['stats'][0]['delivered']['total']
		except KeyError:
			pass
		try:
			opened = data['stats'][0]['opened']['total']
		except KeyError:
			pass
		try:
			uniqueOpened = data['stats'][0]['opened']['unique']
		except KeyError:
			pass
		try:
			clicked = data['stats'][0]['clicked']['total']
		except KeyError:
			pass
		try:
			uniqueClicked = data['stats'][0]['clicked']['unique']
		except KeyError:
			pass
		try:
			failed = data['stats'][0]['failed']['permanent']['total']
		except KeyError:
			pass
		try:
			unsubscribed = data['stats'][0]['failed']['permanent']['suppress-unsubscribe']
		except KeyError:
			pass
		try:
			complained = data['stats'][0]['failed']['permanent']['suppress-complaint']
		except KeyError:
			pass
		try:
			bounced = data['stats'][0]['failed']['permanent']['suppress-bounce']
		except KeyError:
			pass
		try:
			originalBounced = data['stats'][0]['failed']['permanent']['bounce']
		except KeyError:
			pass
		try:
			originalComplained = data['stats'][0]['complained']['total']
		except KeyError:
			pass

		# add each tag to the sum
		acceptedSum+=accepted
		deliveredSum+=delivered
		opensSum+=opened
		uniqueOpensSum+=uniqueOpened
		clicksSum+=clicked
		uniqueClicksSum+=uniqueClicked
		failuresSum+=failed
		unsubscribesSum+=unsubscribed
		complaintsSum+=complained
		bouncesSum+=bounced
		originalBouncesSum+=originalBounced
		originalComplainsSum+=originalComplained

		# print data
		print(i)
		t.add_row(['Accepted',accepted])
		t.add_row(['Delivered',delivered])
		t.add_row(['Opens',opened])
		t.add_row(['Unique Opens',uniqueOpened])
		t.add_row(['Unique Clicks',uniqueClicked])
		print(t)
		print()

		f.write(i+"\n")
		f.write(str(t)+"\n\n")

	# get mobile / desktop data
	for i in tags:

		# api request
		request = requests.get(baseURL + "tags/" + i + "/stats/aggregates/devices",
		        auth=("api", key))

		# json object
		data = request.json()

		# reset variables
		mobileOpens = 0
		mobileClicks = 0
		desktopOpens = 0
		desktopClicks = 0
		tabletOpens = 0
		tabletClicks = 0

		# parsing json
		try:
			mobileOpens = data['devices']['mobile']['unique_opened']
		except KeyError:
			pass
		try:
			mobileClicks = data['devices']['mobile']['unique_clicked']
		except KeyError:
			pass
		try:
			desktopOpens = data['devices']['desktop']['unique_opened']
		except KeyError:
			pass
		try:
			desktopClicks = data['devices']['desktop']['unique_clicked']
		except KeyError:
			pass
		try:
			tabletOpens = data['devices']['tablet']['unique_opened']
		except KeyError:
			pass
		try:
			tabletClicks = data['devices']['tablet']['unique_clicked']
		except KeyError:
			pass

		# add to sum
		mobileOpenSum+=mobileOpens
		mobileClickSum+=mobileClicks
		desktopOpenSum+=desktopOpens
		desktopClickSum+=desktopClicks
		tabletOpenSum+=tabletOpens
		tabletClickSum+=tabletClicks

	# rates
	openRate = round(opensSum/deliveredSum*100,2)
	uniqueOpenRate = round(uniqueOpensSum/deliveredSum*100,2)
	clickThroughRate = round(clicksSum/opensSum*100,2)
	uniqueClickThroughRate = round(uniqueClicksSum/uniqueOpensSum*100,2)
	bounceRate = round((bouncesSum+originalBouncesSum)/deliveredSum*100,2)
	desktopTabletMobileTotal = desktopOpenSum+tabletOpenSum+mobileOpenSum
	desktopRate = round(desktopOpenSum/desktopTabletMobileTotal*100,2)
	mobileRate = round(mobileOpenSum/desktopTabletMobileTotal*100,2)
	tabletRate = round(tabletOpenSum/desktopTabletMobileTotal*100,2)
	desktopCTR = round(desktopClickSum/desktopOpenSum*100,2)
	mobileCTR = round(mobileClickSum/mobileOpenSum*100,2)
	tabletCTR = round(tabletClickSum/tabletOpenSum*100,2)

	# get from name and subject
	request = requests.get(baseURL + "events",
        auth=("api", key),
		params={"limit": 1, "tags":tag, "event":"accepted"})
	data = request.json()

	# parse data
	fromName = data['items'][0]['message']['headers']['from']
	subject = data['items'][0]['message']['headers']['subject']
	time = data['items'][0]['timestamp']

	# convert timestamp to time
	formattedTime = datetime.datetime.fromtimestamp(time).strftime('%m/%d/%Y %H:%M')

	# print results
	print("Rates")
	t = PrettyTable(['Rate', '%'])
	openRateString = str(openRate) + "%"
	uniqueOpenRateString = str(uniqueOpenRate) + "%"
	clickThroughRateString = str(clickThroughRate) + "%"
	uniqueClickThroughRateString = str(uniqueClickThroughRate) + "%"
	t.add_row(['Open Rate',openRateString])
	t.add_row(['Unique Open Rate',uniqueOpenRateString])
	t.add_row(['Click Through Rate',clickThroughRateString])
	t.add_row(['Unique CTR',uniqueClickThroughRateString])
	print(t)
	print()

	f.write("Rates\n")
	f.write(str(t)+"\n\n")

	print("Devices")
	t = PrettyTable(['Device', '% of deliveries', 'CTR'])
	desktopRateString = str(desktopRate) + "%"
	mobileRateString = str(mobileRate) + "%"
	tabletRateString = str(tabletRate) + "%"
	desktopCTRString = str(desktopCTR) + "%"
	mobileCTRString = str(mobileCTR) + "%"
	tabletCTRString = str(tabletCTR) + "%"
	t.add_row(['Desktop',desktopRateString,desktopCTRString])
	t.add_row(['Mobile',mobileRateString,mobileCTRString])
	t.add_row(['Tablet',tabletRateString,tabletCTRString])
	print(t)
	print()

	f.write("Devices\n")
	f.write(str(t)+"\n\n")

	print('Failures / Bounces')
	t = PrettyTable(['Event', '#'])
	t.add_row(['Failures',failuresSum])
	t.add_row(['Unsubscribes',unsubscribesSum])
	t.add_row(['Permanent Bounces',bouncesSum])
	t.add_row(['Temp Bounces',originalBouncesSum])
	t.add_row(['Permanent Complaints',complaintsSum])
	t.add_row(['Temp Complaints',originalComplainsSum])
	print(t)
	print()

	f.write("Totals\n")
	f.write(str(t)+"\n\n")

	print("Totals")
	t = PrettyTable(['Event', '#'])
	t.add_row(['Accepts',acceptedSum])
	t.add_row(['Deliveries',deliveredSum])
	t.add_row(['Opens',opensSum])
	t.add_row(['Unique Opens',uniqueOpensSum])
	t.add_row(['Clicks',clicksSum])
	t.add_row(['Unique Clicks',uniqueClicksSum])
	print(t)
	print()

	f.write("Totals\n")
	f.write(str(t)+"\n\n")

	output1="========== " + "Message Info / Summary" + " =========="
	output2="From: " + fromName
	output3="Subject: " + subject
	output4="Date: " + formattedTime
	output5="From the messages tagged with " + tag + " we successfully delivered " + str(deliveredSum) + " emails."
	output6="This mailgun message had an open rate of " + str(uniqueOpenRate) + "% and a CTR of " + str(uniqueClickThroughRate) + "%."
	output7="There was a bounce rate of " + str(bounceRate) + "%."

	print(output1)
	print(output2)
	print(output3)
	print(output4)
	print()
	print(output5) 
	print(output6)
	print(output7) 

	f.write(output1+"\n")
	f.write(output2+"\n")
	f.write(output3+"\n")
	f.write(output4+"\n\n")
	f.write(output5+"\n")
	f.write(output6+"\n")
	f.write(output7+"\n")


	# close file
	f.close()

	# restart?
	again = input("Again? (y/n): ")

	if again == "n":
		break

	print()
print()
print("Goodbye!")
print()


# use this code to dump JSON data to console
# print(json.dumps(data, indent=2))
