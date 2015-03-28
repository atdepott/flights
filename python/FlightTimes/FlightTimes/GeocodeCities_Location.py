import urllib2
import json
import os
import datetime
import csv
import time

# input cities csv file
input_locations = os.path.join("C:/temp/locations.txt")

# output directory for csv output
output_dir = os.path.join(os.getcwd(),"out")  #default: /out

# input start at line
input_line_start = 1
# number of lines to geocode - (google limit is 2500 in 24-hour period)
num_geocodes = 2500


def geocode(location):
    try:
        geocodeUrl = r"http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % (urllib2.quote("'"+location+"'"))
        response = urllib2.urlopen(geocodeUrl)
        json_response = response.read()
        result = json.loads(json_response)
        try:
            lat_long = result["results"][0]["geometry"]["location"]
            print location + str(lat_long)
            return lat_long
        except:
            print result
            return ""
    except:
        return ""

def write_city(out_file_name, location, lat_long):
    lat = ""
    long = ""
    if (lat_long != ""):
        lat = lat_long["lat"]
        long = lat_long["lng"]
    
    out_file = open(out_file_name, 'ab')
    writer = csv.writer(out_file)
    writer.writerow([location,str(lat),str(long)]);
    out_file.close() 

#setup output file
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
date_string = datetime.datetime.now().strftime("%Y%m%d%H%M")
out_file_name = os.path.join(output_dir, "GeocodedLocations_" + date_string + ".csv")
out_file = open(out_file_name, 'a')
out_file.write("LOCATION,LAT,LONG" + "\n")
out_file.close() 

#read cities csv file
with open(input_locations) as location_file:
    reader = csv.reader(location_file, delimiter='\t')
    rowNum = 0;
    for row in reader:
        if ((rowNum >= input_line_start) and (rowNum < num_geocodes + input_line_start)):
            location = row[0]
            print location
            geocode_results = geocode(location)
            write_city(out_file_name, location, geocode_results);
            time.sleep(3)
        rowNum = rowNum + 1