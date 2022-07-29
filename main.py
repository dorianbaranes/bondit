import csv
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

class Flight(BaseModel):
    id : str
    departure: str
    arrival: str
    status: str


app = FastAPI()
csv_filename='flight.csv'

@app.get("/all_flights")
async def get_all_flights():
    df = pd.read_csv(csv_filename, sep=',')
    df = df.set_index('id', drop=False)

    all_flights = list()
    for index,row in df.iterrows():
        print(type(row))
        all_flights.append(row)

    return all_flights

@app.get("/flight/{flight_id}")
async def get_flight(flight_id):

    df = pd.read_csv(csv_filename, sep=',')
    df = df.set_index('id', drop=False)

    if flight_id in df.index:
        return df.loc[flight_id].to_dict()
    else:
        return {'message':'This flight does not exist'}

@app.put("/update_flight")
async def update_flight(flight:Flight):
    df = pd.read_csv(csv_filename, sep=',')
    df=df.set_index('id')

    if flight.id in df.index:
        try:
            datetime.strptime(flight.departure.strip(), '%H:%M')
            datetime.strptime(flight.arrival.strip(), '%H:%M')
        except ValueError:
            return {'message':'Departure / Arrival time should have the format 00:00'}


        df.loc[flight.id] = flight.departure, flight.arrival, flight.status
        df.to_csv(csv_filename, index=True)
        set_flight_status()
        return {'message':'This flight has been updated'}
    else:
        return {'message':'This flight does not exist'}


@app.put("/set_flight_status")
def set_flight_status():
    flight_per_arrival_time = dict()

    with open(csv_filename, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        header=next(csv_reader)

        for row in csv_reader:
            if row[2].strip() in flight_per_arrival_time.keys():
                flight_per_arrival_time[row[2].strip()].append(row)
            else:
                flight_per_arrival_time[row[2].strip()] = [row]

    arrival_times = list(flight_per_arrival_time.keys())
    arrival_times.sort()

    with open(csv_filename, 'w', newline='') as f2:
        csv_writer = csv.writer(f2)
        csv_writer.writerow(header)
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

    return {'message:Status updated'}

