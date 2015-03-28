import os
import datetime
import csv

# input flight data
input_flights = os.path.join(os.getcwd(), "data", "FAA_flights_proc.csv") #default: /data/FAA_flights_proc.csv

# output directory for csv output
output_dir = os.path.join(os.getcwd(),"out")  #default: /out

# target destination airport (FAA code)
target_dest = 'DTW'

#TODO dest origin key

#read cities csv file
avg_flights = dict()
min_flights = dict()
max_flights = dict()
with open(input_flights) as in_file:
    reader = csv.reader(in_file, delimiter=',')
    # skip header row:
    reader.next()
    for row in reader:
        dest = row[0]
        origin = row[1]
        air_time = float(row[2])
        key = dest, origin
        
        if air_time > 0:
            if key in avg_flights:
                avg_time = (avg_flights[key] + air_time) / 2
                avg_flights[key] = avg_time
            else:
                avg_flights[key] = air_time
        
            if (not key in min_flights) or min_flights[key] > air_time:
                #if dest == 'MSP' and origin == 'LAN':
                #    print "MIN " + str(air_time)
                min_flights[key] = air_time

            if (not key in max_flights) or max_flights[key] < air_time:
                max_flights[key] = air_time

flights = []
for key in avg_flights:
    #print avg_flights[key]
    flights.append([key[0],key[1],avg_flights[key],min_flights[key],max_flights[key]])

#write output
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
date_string = datetime.datetime.now().strftime("%Y%m%d%H%M")
out_file_name = os.path.join(output_dir, "FlightTimes_" + date_string + ".csv")
with open(out_file_name, 'wb') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["DEST","ORIGIN","AVG_TIME","MIN_TIME","MAX_TIME"])
    writer.writerows(flights)
    out_file.close() 