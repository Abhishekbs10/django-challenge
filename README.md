# Django-code-challenge
Simple Django code-challenge app

Features
--------
1. User authorisation and registration
2. Basic user permissions: admin, editor, normal.
	- Editors can add posts, update/delete the existing ones for which they have suitable
	  permissions/ownership.
	- admin is superuser as usual.
3. Tags
4. Search, year/month archives, sort by post author, category, tags.
5. Basic REST API provided by Django REST framework (available at `/api`)

Main requirements
------------

1. `python` > 3
2. `Django` 2.2.17

This project also uses a few external packages (see `requirements.txt` file for details).


### How to set Up

 set up a virtual environment and activate it:

`python3 -m venv env && source env/bin/activate`

Install required packages:

`pip install -r requirements.txt`

Next, perform migration:

`python manage.py migrate`

The setup is complete. Run a local server with

`python3 manage.py runserver`

The will available at `localhost:8000`.

## What's next?

At this point, one may want to create a superuser account, create the Editors group and add a few users to this group.