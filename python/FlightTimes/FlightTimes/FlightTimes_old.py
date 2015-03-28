import urllib2
import json
import os
import datetime
import csv

# input cities csv file
input_cities = os.path.join(os.getcwd(), "data", "airports.csv") #default: /data/airports.csv

# output directory for csv output
output_dir = os.path.join(os.getcwd(),"out")  #default: /out


def find_flights(departure):
    minutes = 0
    count = 0
    average = 0

    arrival = 'DTW'
    year = '2014'
    month = '2'
    day = '1'

    try:
        flightUrl = 'https://api.flightstats.com/flex/connections/rest/v1/json/connecting/from/%s/to/%s/arriving/%s/%s/%s?appId=f11595fd&appKey=2e17d6c63ee21ddfda46e64e172a244b&days=7' % (departure, arrival, year, month, day)
        response = urllib2.urlopen(flightUrl)
        json_response = response.read()
        response_obj = json.loads(json_response)
        all_flights = response_obj['flights']
        for flight in all_flights:
            min1 = flight['layoverDurationMinutes']
            min2 = flight['flightDurationMinutes']
            minutes = minutes + min1 + min2
            count = count + 1
        average = minutes/count
    except:
        pass
    return average

def write_city(out_file_name, city, airport_code, avg_time):
    out_file = open(out_file_name, 'a')
    writer = csv.writer(out_file)
    writer.writerow([city,airport_code,avg_time]);
    #outline = city + ',' + airport_code + "," + str(avg_time)
    #out_file.write(outline + "\n")
    out_file.close() 

#setup output file
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
date_string = datetime.datetime.now().strftime("%Y%m%d%H%M")
out_file_name = os.path.join(output_dir, "FlightTimes_" + date_string + ".csv")
out_file = open(out_file_name, 'a')
out_file.write("CITY,STATE,AIRPORT_CODE,AVG TIME" + "\n")
out_file.close() 

#read cities csv file
with open(input_cities) as city_file:
    reader = csv.reader(city_file, delimiter=',')
    # skip header row:
    reader.next()
    for row in reader:
        city = row[0]
        airport_code = row[1]
        avg_time = find_flights(airport_code)
        write_city(out_file_name, city, airport_code, avg_time);