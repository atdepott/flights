import os
import datetime
import csv

# input flight data
input_flights = os.path.join(os.getcwd(), "data", "FAA_flights.csv") #default: /data/FAA_flights.csv

# output directory for csv output
output_dir = os.path.join(os.getcwd(),"out")  #default: /out

# target destination airport (FAA code)
target_dest = 'DTW'

#read cities csv file
flights = []
with open(input_flights) as in_file:
    reader = csv.reader(in_file, delimiter=',')
    # skip header row:
    reader.next()
    for row in reader:
        flight_class = row[11]
        pass_count = row[0]
        if flight_class == "F" and pass_count > 0:
            air_time = row[1]
            origin = row[4]
            dest = row[7]
            flights.append([dest, origin, air_time]);


#write output
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
date_string = datetime.datetime.now().strftime("%Y%m%d%H%M")
out_file_name = os.path.join(output_dir, "FlightTimes_" + date_string + ".csv")
with open(out_file_name, 'wb') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(["DEST","ORIGIN","AIR_TIME"])
    writer.writerows(flights)
    out_file.close() 