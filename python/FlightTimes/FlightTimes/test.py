import urllib2
import json

application_id = 'f11595fd'
application_key = '2e17d6c63ee21ddfda46e64e172a244b'

departure = 'IFP'
arrival = 'DTW'
year = '2014'
month = '2'
day = '1'

url = 'https://api.flightstats.com/flex/connections/rest/v1/json/connecting/from/%s/to/%s/arriving/%s/%s/%s?appId=f11595fd&appKey=2e17d6c63ee21ddfda46e64e172a244b&days=7' % (departure, arrival, year, month, day)

minutes = 0
count = 0

response = urllib2.urlopen(url)
json_response = response.read()
print json_response

response_obj = json.loads(json_response)
all_flights = response_obj['flights']
for flight in all_flights:
    min1 = flight['layoverDurationMinutes']
    min2 = flight['flightDurationMinutes']
    minutes = minutes + min1 + min2
    count = count + 1

print "AVG:" + str(minutes/count) + " TOTAL:" + str(minutes) + " COUNT:" + str(count) 



