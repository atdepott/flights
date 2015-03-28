import urllib2
import json
import os
import datetime
import csv
import time

# input cities csv file
input_cities = os.path.join(os.getcwd(), "data", "airports_with_time.csv") #default: /data/airports.csv

# output directory for csv output
output_dir = os.path.join(os.getcwd(),"out")  #default: /out


def geocode(city):
    try:
        geocodeUrl = r"http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % (urllib2.quote("'"+city+"'"))
        response = urllib2.urlopen(geocodeUrl)
        json_response = response.read()
        result = json.loads(json_response)
        try:
            lat_long = result["results"][0]["geometry"]["location"]
            print city + str(lat_long)
            return lat_long
        except:
            print result
            return ""
    except:
        return ""

def write_city(out_file_name, city_name, airport_code, avg_time, lat_long):
    lat = ""
    long = ""
    #print lat_long
    if (lat_long != ""):
        lat = lat_long["lat"]
        long = lat_long["lng"]
    
    out_file = open(out_file_name, 'ab')
    writer = csv.writer(out_file)
    writer.writerow([city_name,airport_code,avg_time,str(lat),str(long)]);
    #outline = city_name + "," + airport_code + "," + str(lat) + "," + str(long)
    #out_file.write(outline + "\n")
    out_file.close() 

#setup output file
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
date_string = datetime.datetime.now().strftime("%Y%m%d%H%M")
out_file_name = os.path.join(output_dir, "AirportCities_" + date_string + ".csv")
out_file = open(out_file_name, 'a')
out_file.write("CITY,AIRPORT_CODE,AVG_TIME, LAT,LONG" + "\n")
out_file.close() 

#read cities csv file
with open(input_cities) as city_file:
    reader = csv.reader(city_file, delimiter=',')
    # skip header row:
    reader.next()
    for row in reader:
        city = row[0]
        airport_code = row[1]
        avg_time = row[2]
        geocode_results = geocode(city)
        write_city(out_file_name, city, airport_code, avg_time, geocode_results);
        time.sleep(5)