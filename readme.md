# Introduction

The goal of this project is to design an e-commerce website with hybrid recommendation system with django.  

Template is written with django 2.2+ and python 3 in mind.

[You can view a demonstration of this project by visiting this link](https://cuetsoftengecomproject.herokuapp.com/)

![Default Home View](__screenshots/home.png?raw=true "Title")

### Main features

* Has to apps Accounts and Products

* Example app with custom user model

* Bootstrap static files included

* User registration and login

* User profile with profile pictures included

* Requirements file given

* Run on Postgresql

* Uses two recommendation system apriori and collaborative filtering.

* Has a voting system to perform hybrid recommendation

# Usage

Can be used a start up point for an E-commerce website
      

# {{ project_name|title }}

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/simon7426/ecom-project.git
    $ cd {{ project_name }}
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r piprequirements.txt

For Anaconda run:

	$ conda create --name <env> --file requirements.txt

Replace <env> with custom enviroment name.    
    
Then simply apply the migrations:

    $ python manage.py migrate
    
You can create a superuser for your use using 

	$ python manage.py createsuperuser

You can now run the development server:

    $ python manage.py runserver