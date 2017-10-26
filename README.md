# beer_buddy
Simple API project for simulating a beer delivery service

To use this API service you must have installed SQLite, SpatiaLite, Python 3.5 and Pipenv

$ sudo apt-get install spatialite-bin

$ sudo apt-get install libsqlite3-mod-spatialite

On project root directory run:

$ pipenv install

$ pipenv shell

$ python manage.py migrate

$ python manage.py test

$ python populate_db.py 

before deploying 
$ python manage.py check --deploy


Go play around

Paths

GET /pdvs/{id}
POST /pdvs
GET /search
