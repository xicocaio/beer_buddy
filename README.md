# Beer Buddy API - Simple Rest API project for simulating a beer delivery service

## Stack

The stack bellow was used mostly due to it's ease of installation, configuration and also efficiency and portability.
* Language: Python (3.5)
* Framework: Django (1.11)
* DB: SQLite (3.16.2)

## Pre-installation

This system was developed in Ubuntu 16.04, but will work properly on any other Operational System(OS X, Windows, etc.).

However, this guide will only include instructions for plugins and packages that are not already installed on this OS. For this reason, we assume that technologies like a python interpreter and SQLite are ready for use, and should not be on the scope of this document.

* Assuming you already have SQLite installed, add itś spatial libraries, open a bash terminal and run:

```bash

$ sudo apt-get install spatialite-bin
$ sudo apt-get install libsqlite3-mod-spatialite

```

* Now install pipenv dependency manager:

```bash

$ pip install --user pipenv

```

## Project configuration and deployment

Now we'll start setting up the project.

* Clone the repo from github and change to project root directory. After that install project dependencies and go to python virtual env, by running:

```bash
$ pipenv install
$ pipenv shell
```

* Setup DB:

```bash
$ python manage.py migrate
```

* Run tests to verify that everything is working fine:

```bash
$ python manage.py test
```

* Open a new bash terminal window on the same folder path and start server
```bash
$ python manage.py runserver
```

* Populate DB
$ python populate_db.py
```bash
$ python populate_db.py
```

* The following message should be printed indicating that some data from the provided pdvs.json had some issues with itś CNPJ

```
Failed to populate the following PDVs: 

Document: 04666182390
Trading Name: Adega Sao Paulo
400
{"non_field_errors":["This document is invalid"]}

Document: 04698149428
Trading Name: Bar do Ze
400
{"non_field_errors":["This document is invalid"]}

Document: 081.914.699-44
Trading Name: Emporio legal
400
{"non_field_errors":["This document is invalid"]}

Document: 22.15.127.213/0001-56.752/0001-90
Trading Name: Ze da Ambev
400
{"document":["Ensure this field has no more than 14 characters."]}

Document: 36211693850
Trading Name: Adega Ambev
400
{"non_field_errors":["This document is invalid"]}

Document: 960361.506-44
Trading Name: Adega do Joao
400
{"non_field_errors":["This document is invalid"]}

```

## API usage

There are 3 available Rest requests in the API:

* POST /pdvs
* GET /pdvs/{id}
* GET /search

### POST /pdvs
  Create a new PDV

* All fields on payload are required.
* Uses Json
* Responses:
  ** 201 Created
  ** 400 Bad Request

Example:

```
http://localhost:8000/pdvs
Headers
  Content-Type: application/json

{
    "tradingName": "Beer Point",
    "ownerName": "Ricardo Andrade",
    "document": "58067669000180",
    "coverageArea": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [
                        -46.674944,
                        -23.579866
                    ],
                    [
                        -46.665377,
                        -23.582828
                    ],
                    [
                        -46.676696,
                        -23.586689
                    ],
                    [
                        -46.674944,
                        -23.579866
                    ]
                ]
            ]
        ]
    },
    "address": {
        "type": "Point",
        "coordinates": [
            -46.671436,
            -23.582727
        ]
    }
}
```

### GET /pdvs/{id}
  Get PDV details by ID

* Uses Json
* Responses:
  ** 200 Ok
  ** 404 Not Found

Example:

```
http://localhost:8000/pdvs/46
  
{
    "id": 46,
    "tradingName": "Beer Point",
    "ownerName": "Ricardo Andrade",
    "document": "58067669000180",
    "coverageArea": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [
                        -46.674944,
                        -23.579866
                    ],
                    [
                        -46.665377,
                        -23.582828
                    ],
                    [
                        -46.676696,
                        -23.586689
                    ],
                    [
                        -46.674944,
                        -23.579866
                    ]
                ]
            ]
        ]
    },
    "address": {
        "type": "Point",
        "coordinates": [
            -46.671436,
            -23.582727
        ]
    }
}
```

### GET /pdvs/search
  Search for nearest PDV by longitude and latitude

* Query params
  longlat: Longitude and latitude values separated by comma
* Responses:
  ** 200 Ok

Example:

```
http://localhost:8000/pdvs/search?longlat=-46.673453,-23.584458
  
{
    "id": 46,
    "tradingName": "Beer Point",
    "ownerName": "Ricardo Andrade",
    "document": "58067669000180",
    "coverageArea": {
        "type": "MultiPolygon",
        "coordinates": [
            [
                [
                    [
                        -46.674944,
                        -23.579866
                    ],
                    [
                        -46.665377,
                        -23.582828
                    ],
                    [
                        -46.676696,
                        -23.586689
                    ],
                    [
                        -46.674944,
                        -23.579866
                    ]
                ]
            ]
        ]
    },
    "address": {
        "type": "Point",
        "coordinates": [
            -46.671436,
            -23.582727
        ]
    }
}
```

## Final considerations

* Go play around! =)
