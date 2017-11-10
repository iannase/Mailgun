import requests
import json
import math

# key and base URL
key="YOUR_KEY"
baseURL="https://api.mailgun.net/v3/YOUR_DOMAIN"

# menu loop
for z in range(10):
	# tags
	tag = input("Enter a tag: ")
	tagA = tag + "a"
	tagB = tag + "b"
	tagC = tag + "c"

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
		        params={"event": ["accepted", "delivered", "opened", "clicked", "failed", "unsubscribed", "complained", "stored"],
		                "duration": "1m"})

		# json response object
		data = request.json()

		# get response objects
		accepted = data['stats'][0]['accepted']['total']
		delivered = data['stats'][0]['delivered']['total']
		opened = data['stats'][0]['opened']['total']
		uniqueOpened = data['stats'][0]['opened']['unique']
		clicked = data['stats'][0]['clicked']['total']
		uniqueClicked = data['stats'][0]['clicked']['unique']
		failed = data['stats'][0]['failed']['permanent']['total']
		unsubscribed = data['stats'][0]['failed']['permanent']['suppress-unsubscribe']
		complained = data['stats'][0]['failed']['permanent']['suppress-complaint']
		bounced = data['stats'][0]['failed']['permanent']['suppress-bounce']
		originalBounced = data['stats'][0]['failed']['permanent']['bounce']
		originalComplained = data['stats'][0]['complained']['total']

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
		print("====== " + i + " ======")
		print('Accepted:\t' + str(accepted))
		print('Delivered:\t' + str(delivered))
		print('Opens:\t\t' + str(opened))
		print('Unique Opens:\t' + str(uniqueOpened))
		print('Clicks:\t\t' + str(clicked))
		print('Unique Clicks:\t' + str(uniqueClicked))
		print()

	# get mobile / desktop data
	for i in tags:

		# api request
		request = requests.get(baseURL + "tags/" + i + "/stats/aggregates/devices",
		        auth=("api", key))

		# json object
		data = request.json()

		# parsing json
		mobileOpens = data['devices']['mobile']['unique_opened']
		mobileClicks = data['devices']['mobile']['unique_clicked']
		desktopOpens = data['devices']['desktop']['unique_opened']
		desktopClicks = data['devices']['desktop']['unique_clicked']
		tabletOpens = data['devices']['tablet']['unique_opened']
		tabletClicks = data['devices']['tablet']['unique_clicked']

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

	# print results
	print()
	print("=== Open and Click Rates ===")
	print("Open Rate:\t\t" + str(openRate) + "%")
	print("Unique Open Rate:\t" + str(uniqueOpenRate) + "%")
	print("Click Through Rate:\t" + str(clickThroughRate) + "%")
	print("Unique CTR:\t\t" + str(uniqueClickThroughRate) + "%")
	print()

	print("=== Desktop/Tablet/Mobile ===")
	print("Desktop:\t\t" + str(desktopRate) + "%")
	print("Mobile:\t\t\t" + str(mobileRate) + "%")
	print("Tablet:\t\t\t" + str(tabletRate) + "%")
	print("Desktop CTR:\t\t" + str(desktopCTR) + "%")
	print("Mobile CTR:\t\t" + str(mobileCTR) + "%")
	print("Tablet CTR:\t\t" + str(tabletCTR) + "%")
	print()

	print('===== Failures / Bounces =====')
	print('Failures:\t\t' + str(failuresSum))
	print('Unsubscribes:\t\t' + str(unsubscribesSum))
	print('Hard Bounces:\t\t' + str(bouncesSum))
	print('Soft Bounces:\t\t' + str(originalBouncesSum))
	print('Hard Complaints:\t' + str(complaintsSum))
	print('Soft Complaints:\t\t' + str(originalComplainsSum))
	print()

	print("========== " + "Totals" + " ==========")
	print('Accepted:\t\t' + str(acceptedSum))
	print('Delivered:\t\t' + str(deliveredSum))
	print('Opens:\t\t\t' + str(opensSum))
	print('Unique Opens:\t\t' + str(uniqueOpensSum))
	print('Clicks:\t\t\t' + str(clicksSum))
	print('Unique Clicks:\t\t' + str(uniqueClicksSum))
	print()

	print("From the messages tagged with " + tag + " we successfully delivered " + str(deliveredSum) + " emails.") 
	print("This mailgun message had an open rate of " + str(uniqueOpenRate) + "% and a CTR of " + str(uniqueClickThroughRate) + "%.") 
	print("There was a bounce rate of " + str(bounceRate) + "%.")
	print()

	again = input("Again? (y/n): ")

	if again == "n":
		break

	print()

print()
print("Goodbye!")
print()


# use this code to get JSON data
# print(json.dumps(data, indent=2))


