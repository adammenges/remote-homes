###############################################################################
# Every time I travel, I do the same thing. Hunt around on a few sites for
# a reasonably priced place with good reviews, specifically looking at the
# reviewers thoughts on the wifi, because there's no way for me to work
# remotely without solid Internet. It's quite the task for me to find a
# place factoring in all these variables. Well, no longer.
###
# This script many sources, more then I could ever check, and ranks them based
# on the variables above. Uses Sentiment Analysis for determining the reviewers
# feeling on the wifi.
###
# Sources: 
# * airbnb
# * alwaysonvacation
# * apartmentsapart
# * bedycasa
# * bookingpal
# * citiesreference
# * edomizil
# * geronimo
# * gloveler
# * holidayvelvet
# * homeaway
# * homestay
# * hostelworld
# * housetrip
# * interhome
# * nflats
# * roomorama
# * stopsleepgo
# * theotherhome
# * travelmob
# * vacationrentalpeople
# * vaycayhero
# * waytostay
# * webchalet
# * zaranga
###############################################################################



# I could make these proper args, but meh...

latitude = "1.332929"
longitude = "103.873614"
maxdistance = 20
start_date = "13MAR2016"
end_date = "17MAR2016"




import unirest
import datetime
import calendar
from textblob import TextBlob
from scipy.stats import logistic

date = datetime.datetime.strptime(start_date, "%d%b%Y")
start_date_timestamp = calendar.timegm(date.utctimetuple())

date = datetime.datetime.strptime(end_date, "%d%b%Y")
end_date_timestamp = calendar.timegm(date.utctimetuple())

keys = {
	"latitude": "1.332929",
	"longitude": "103.873614",
	"maxdistance": 20,
	'page': 1,
}

homes = []

# FWIW, kind of interesting airbnb sticks this is every one of their responses
# 'x-hi-human': 'The Production Infrastructure team added this header. Come work with us! Email kevin.rice+hiring@airbnb.com'

for page in range(1,4):
	keys['page'] = page
	response = unirest.get("https://zilyo.p.mashape.com/search?latitude={latitude}&longitude={longitude}&maxdistance={maxdistance}&resultsperpage=50&sort=low2high&page={page}".format(**keys),
		headers={
			"X-Mashape-Key": "WjWvyNVU62msh1LAzIexCUbTjib2p1EjstQjsndxXNO7CqCKqH",
			"Accept": "application/json"
		}
	)

	homes += response.body['result']



# Find only the available

### For reference 
# response.body['result'][2]['availability']
# [{u'end': 1426204800, u'start': 1425859200},
#  {u'end': 1427241600, u'start': 1426723200},
#  {u'end': 1427846400, u'start': 1427500800},
#  {u'end': 1428451200, u'start': 1428192000},
#  {u'end': 1430179200, u'start': 1429315200},
#  {u'end': 1431302400, u'start': 1430524800},
#  {u'end': 1434931200, u'start': 1431648000},
#  {u'end': 1437004800, u'start': 1436918400},
#  {u'end': 1437609600, u'start': 1437350400},
#  {u'end': 1440201600, u'start': 1438041600},
#  {u'end': 1442620800, u'start': 1440633600},
#  {u'end': 1451433600, u'start': 1442880000},
#  {u'end': 1489795200, u'start': 1451779200}]


print "AVALI"
available = []
for home in homes:
	for d in home['availability']:
		if d['end'] > end_date_timestamp and d['start'] < start_date_timestamp:
			print 'adding {}'.format(home['attr']['heading'].encode('ascii', 'ignore'))
			available.append(home)
			break

homes = available

# Now time for only those with Wifi
print "WIFI"
wifi_homes = []
for home in homes:
	amenities = ",".join([x['text'] for x in home['amenities']]).split(",")
	amenities = [x.lower().strip() for x in amenities]
	for a in amenities:
		for i in ['internet', 'wifi', 'network', 'cellular', 'wireless']:
			if i in a:
				print 'adding {}'.format(home['attr']['heading'].encode('ascii', 'ignore'))
				wifi_homes.append(home)
				break
		else:
			 continue
		break

homes = wifi_homes

print 'REVIEWS'
# Now only those with reviews
with_reviews = []
for home in homes:
	if home['reviews']['count'] > 0:
		with_reviews.append(home)

homes = with_reviews

### For reference 
# In [27]: real.history
# Out[27]: [<Response [301]>]
# In [28]: not_real.history
# Out[28]: [<Response [301]>, <Response [301]>]

# Some listings no longer exist via this api, check for that
# Maybe I should just scrap myself, but this is so handy
import requests
real_listings = []

print 'requesting all listings...'

for home in homes:
	r = requests.get(home['provider']['url'])
	# TODO: Figure better way to do this...
	if r.status_code == 200 and len(r.history) < 2:
		real_listings.append(home)


homes = real_listings

def rank(list_of_homes):
	return list_of_homes

for home in rank(homes):
	print '*' * 80
	print "Title: {}".format(home['attr']['heading'].encode('ascii', 'ignore'))
	# print "Description: {}".format(home['attr']['description'].encode('ascii', 'ignore'))
	print "Price: {}".format(home['price']['nightly'])
	print "Reviews: {}".format(home['reviews']['count'])
	print "Rating: {}".format(home['reviews']['rating'])

	count = 0
	sentiment = 0
	# homes[0]['reviews']['entries'][0]['text']
	for review in home['reviews']['entries']:
		text = review['text'].lower()
		for i in ['internet', 'wifi', 'network', 'cellular', 'wireless']:
			if i in text:
				blob = TextBlob(text)
				count += 1
				sentiment += logistic.cdf(blob.sentiment.polarity * 5)
				break

	if count > 0:
		print "Sentiment: {}:".format(sentiment / count)

	print "URL: {}".format(home['provider']['url'])
	### For reference
	# [{u'id': 0, u'text': u'Air Conditioning, Heating'},
	# {u'id': 21, u'text': u'Cable Tv, TV'},
	# {u'id': 11, u'text': u'Elevator In Building'},
	# {u'id': 16, u'text': u'Free Parking On Premises'},
	# {u'id': 22, u'text': u'Internet, Wireless Internet'},
	# {u'id': 15, u'text': u'Kitchen'}]
	amenities = ", ".join([x['text'] for x in home['amenities']])
	amenities = [x.strip() for x in amenities.split(",")]
	amenities = '\n'.join(["   * {}".format(x) for x in amenities])
	print "Amenities: \n{}".format(amenities)
	print '*' * 80
