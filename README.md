
## Test BondIT

### <br/>Requirements 

[PyCharm's requirements management tool](https://www.jetbrains.com/help/pycharm/managing-dependencies.html#create-requirements)
is used to sync Python requirements.

You can use also:
` pip install -r requirement.txt`



### <br/>Launch API

Command: <br/>
`uvicorn main:app --reload`

And to see API doc go to : http://127.0.0.1:8000/docs

### <br/>Part 1: Write down code that produce the success column
Call the API endpoint: <br/>
`http://127.0.0.1:8000/set_flight_status`

### <br/>Part 2.1: Get to get info about flight
Call the API endpoint: <br/>
`http://127.0.0.1:8000/get_all_flights`

### <br/>Part 2.2: Update a flight
Call the API endpoint: <br/>
`http://127.0.0.1:8000/update_flight`
