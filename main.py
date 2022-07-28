import csv
from datetime import datetime

def analyze_flights(csv_filename):
    flight_per_arrival_time = dict()
    arrival_times = set()

    with open(csv_filename, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)

        for row in csv_reader:
            arrival_times.add(row[2])

            if row[2] in flight_per_arrival_time.keys():
                flight_per_arrival_time[row[2]].append(row)
            else:
                flight_per_arrival_time[row[2]] = [row]

    arrival_times = list(arrival_times)
    arrival_times.sort()

    with open(csv_filename, 'w', newline='') as f2:
        csv_writer = csv.writer(f2)
        nb_success = 0
        for arrival_time in arrival_times:
            flights_per_arrival_time = flight_per_arrival_time[arrival_time]

            for flight in flights_per_arrival_time:
                depart = datetime.strptime(flight[1].strip(), '%H:%M')
                arrival = datetime.strptime(flight[2].strip(), '%H:%M')
                delta = arrival - depart
                delta = int(delta.total_seconds() / 60)

                if delta >= 180 and nb_success <= 20:
                    flight[3] = 'success'
                    nb_success+=1
                else:
                    flight[3] = 'fail'

                csv_writer.writerow(flight)

if __name__ == "__main__":
    analyze_flights('flight.csv')





