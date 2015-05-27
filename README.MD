Password Game inspired by the password game played by Jimmy Fallon.
Basic Scafolding based on:
https://realpython.com/blog/python/flask-by-example-part-1-project-setup/

Hosted on Heroku.

==== To Run Migrations ===

On Local
$ python manage.py db migrate
$ python manage.py db upgrade

To push changes to Heroku
$ heroku run python manage.py db upgrade --app passwordgame

