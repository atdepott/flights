import os
import datetime
import csv
import sys
import urllib2
import json
import time

# input flight data
input_flights = os.path.join(os.getcwd(), "data", "FAA_domestic_2013.csv")

# output directory for csv output
output_dir = os.path.join(os.getcwd(),"out")  #default: /out

# number of minutes for layover
layover_mins = 60

# STEP 1: read FAA csv file and organize data
all_flights = dict()
all_dests = set()
all_airports = dict()
with open(input_flights) as in_file:
    reader = csv.reader(in_file, delimiter=',')
    # skip header row:
    reader.next()
    for row in reader:
        flight_count = float(row[0])
        pass_count = float(row[1])
        ramp_time = float(row[2])
        air_time = float(row[3])
        location = row[6]
        origin = row[5]
        dest = row[8]
        flight_class = row[14]
        
        if flight_class == "F" and pass_count > 0:
            all_dests.add(dest)
            flight = {"origin":origin, "dest":dest, "flight_count":flight_count, "ramp_time":ramp_time, "air_time":air_time }
             
            if not origin in all_flights:
                all_flights[origin] = dict()
            
            o_flights = all_flights[origin]

            if not dest in o_flights:
                o_flights[dest] = [flight]
            else:
                o_flights[dest].append(flight)

            if not origin in all_airports:
                all_airports[origin] = {"code":origin, "location":location}

print "Step 1 complete"

# STEP 2: compile statistics for each origin-destination pair
sum_flights = dict()
for origin in all_flights:
    origin_flights = all_flights[origin]
    for dest in origin_flights:
        min_flight = sys.float_info.max
        max_flight = 0
        total_flight = 0
        flight_count = 0
        for flight in origin_flights[dest]:
            if flight["ramp_time"] > max_flight:
                max_flight = flight["ramp_time"]
            if flight["ramp_time"] < min_flight:
                min_flight = flight["ramp_time"]
            total_flight += flight["ramp_time"]
            flight_count += flight["flight_count"]
        dest_obj = {"count":flight_count, "min":min_flight, "max":max_flight, "avg":(total_flight/flight_count)}

        # arbitrary constraint: must fly at least 100 flights/year on this route to count
        if (flight_count > 100):
            if not origin in sum_flights:
                sum_flights[origin] = dict()
            sum_flights[origin][dest] = dest_obj

print "Step 2 complete"

# STEP 3: geocode airport locations
def geocode(location):
    try:
        geocodeUrl = r"http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % (urllib2.quote("'"+location+"'"))
        response = urllib2.urlopen(geocodeUrl)
        json_response = response.read()
        result = json.loads(json_response)
        try:
            lat_long = result["results"][0]["geometry"]["location"]
            
            lat = ""
            long = ""
            if (lat_long != ""):
                lat = lat_long["lat"]
                long = lat_long["lng"]

            return {"city":location, "lat":lat, "long":long}
        except:
            print result
            return ""
    except:
        return ""

for origin in all_airports:
    location = all_airports[origin]["location"]
    all_airports[origin] = geocode(location) 
    time.sleep(1)

print "Step 3 complete"

# STEP 4: using Dijkstra's Algorithm, calculate shortest distance between each origin and all destinations
def find_shortest_times(origin):
    edges = sum_flights

    nodes = dict()
    unvisited = []
    for dest in all_dests:
        unvisited.append(dest)
        if dest == origin:
            nodes[dest] = 0
        else:
            nodes[dest] = None

    keep_searching = True
    current_airport = origin

    while keep_searching:
        time_to_current= nodes[current_airport]
        if current_airport in edges:
            for dest in edges[current_airport]:
                if dest in unvisited:
                    time_to_dest = edges[current_airport][dest]["avg"]
                    compare_time = time_to_dest + time_to_current + layover_mins
                    if nodes[dest] == None:
                        nodes[dest] = compare_time
                    else:
                        if compare_time < nodes[dest]:
                            nodes[dest] = compare_time
        unvisited.remove(current_airport)

        closest_node = None
        closest_dist = sys.float_info.max
        for node in unvisited:
            if nodes[node] != None and nodes[node] < closest_dist:
                closest_node = node
                closest_dist = nodes[node]

        if closest_node == None:
            keep_searching = False
        else:
            current_airport = closest_node
    return nodes


rows_to_write = []
for origin in sum_flights:
    airport = all_airports[origin]
    if airport != "":
        result = find_shortest_times(origin)
    
        row = [origin, airport["city"], airport["lat"], airport["long"]]
        for dest in all_dests:
            if result[dest] == None:
                time = ""
            else:
                time = str(result[dest] - layover_mins) # we added one extra set of layovers at the beginning
            row.append(time)
        rows_to_write.append(row)
print "Step 4 complete"

# STEP 5: write output csv
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

header_row = ['ORIGIN','CITY_NAME','LAT','LONG']
for dest in all_dests:
    header_row.append(dest)

date_string = datetime.datetime.now().strftime("%Y%m%d%H%M")
out_file_name = os.path.join(output_dir, "FlightTimes_" + date_string + ".csv")
with open(out_file_name, 'wb') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(header_row)
    writer.writerows(rows_to_write)
    out_file.close() 

 