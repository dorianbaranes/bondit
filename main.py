import csv
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
###################################################PART 1
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


##################################################PART 2
class Flight(BaseModel):
    id : str
    departure: str
    arrival: str
    status: str


app = FastAPI()
csv_filename='flight.csv'

@app.get("/get_all_flights")
async def get_all_flights():

    with open(csv_filename, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)

        all_flights=list()
        for row in csv_reader:
            all_flights.append(row)

    return all_flights


@app.post("/update_flight")
async def update_flight(flight:Flight):
    print(flight.dict())


    df = pd.read_csv(csv_filename, sep=',')
    df=df.set_index('id')

    #update
    if flight.id in df.index:
        df.loc[flight.id] = flight.departure, flight.arrival, flight.status
        df.to_csv(csv_filename, index=True)
        return {'message':'This flight has been updated'}
    else:
        return {'message':'This flight does not exist'}

