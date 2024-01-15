Goal 
- In this exercise, I will use authentication and validation mechanisms inside DRF.
- The goal of this API is to recieve user review for menu items of a restaurant.

Objectives

- Add form validators to form data        

- Perform token and session authentication while using a DRF form      

- Use the Djoser and authtoken packages for default routes

- Use the Django admin panel for creating new users and tokens

Installation
------------

**Pipenv can be installed with Python 3.7 and above. For see the result of this little project you need python 3.9 **

For most users, we recommend installing Pipenv using `pip`:

    pip install --user pipenv

You need to be in an active pipenv shell and make sure to install these packages:

    pipenv install django

    pipenv install djangorestframework

    pipenv install djoser

You need to migrate

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver

Now open the API request client, Insomnia and perform the following actions:

Create a POST request to the URL: http://127.0.0.1:8000/api/ratings
 - You need create some users and add a user token in the Insomnia app API request create a Form URL Encoded
   Add menuitem_id as key and small integer as value, add rating as key and 0-5 as value
