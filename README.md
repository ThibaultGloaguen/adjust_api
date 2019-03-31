# Adjust API

This application is written in python 3.7  and uses the Flask framework.
It was developed and tested on macOS High Sierra distribution.
It allow you to query metrics throught an http API.

query the API:
```sh
GET  /metrics
```
Optional parameters:

| Parameter | Exemple | README |
| ------ | ------ | ------ |
| fields | /metrics?fields=field_1,field_2 | get particular fields in the above list (impressions,clicks,installs,spend,revenue,cpi). if fields is empty, default value is all fields  |
| group_by | /metrics?group_by=field_1,field_2 | group by particular fields in the above list (date,channel,country,os). if fields is empty, default value is no fields|
| sort_by | /metrics?sort_by=field | sort by particular field, only one field possible at the time. It is possible to sort by any field of the model |
| direction | /metrics?sort_by=field&direction=desc | set a particular direction desc (for descending) or asc (ascending). default value is ascending |
| date_from | /metrics?date_from=01.06.2017 | filter results setting a date from. the date format accepted is mm.dd.yyyy |
| date_to | /metrics?date_to=01.06.2017 | filter results setting a date to. the date format accepted is mm.dd.yyyy |
| operation | /metrics?operation=sum | allow you to make SUM operation queries when grouping results |
| os | /metrics?os=iOS |filter by os |
| country | /metrics?country=CA |filter by country |
| channel | /metrics?channel=adwords |filter by channel |

Example of query:
```sh
GET  /metrics?date_from=01.06.2017&date_to=01.07.2017&sort_by=cpi&direction=desc&group_by=channel&country=CA&fields=cpi
```


# Installation

This application requires Docker to run.
By default, the Docker will expose port 5000. To change this configuration, you can modify the docker-compose.yml to choose another port.
To install and run the server application:
```sh
$ docker-compose build
```

# Run
```sh
$ docker-compose up application
```
The server should now run on http://0.0.0.0:5000

### Tests

This solution is provided with tests.
To run those tests:
```sh
$ docker-compose up test
```

### Architecture
The entry point of the application is the run.py file. This is where the Flask server application is launched
The application is separated in 3 directories
* /application
* /instance
* /test

### Application
The application is divided into 4 python files.

**__init.py__**

This is where the Flask app is created, configured and binded to the SQL database

**metrics_view.py**

This part of the application handles all the http requests from the client and route them to the right service.
It also handles the differents errors that the application can throws such as Bad Request of Internal Error

**metrics_model.py**

This file is the representation of the schema for the Metrics table in database

**database_service.py**

This part of the application handles the parameters given by the client, construct the database query and provides the results throught the get_results method.
Thanks for reading ;)