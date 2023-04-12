# djangotickets
A simple ticket manager made with Django, Bootstrap, and a Postgresql database.

By no means does this include best practices, but it gets a simple project started.

![Alt Text](https://i.postimg.cc/6qpVZGkD/Screenshot-2023-04-11-204628.jpg)

![Alt Text](https://i.postimg.cc/x8pv31Yq/Screenshot-2023-04-11-204722.jpg)


# Base Functionality

- Session based Authentication
- Creating Tickets
- Commenting on Tickets
- Closing / Deleting tickets
- Reopening Tickets
- Basic sorting/filtering tickets
- Searching by Ticket ID (pretty basic)
- Fairly easy Heroku deployment (you might need to change some settings)

# Planned Features

- Reporting functionality
- More search functionality (by ticket creator, ticket name, etc.)
- Separating the templates into partial renders.

# Installation

1. Install pip packages:
`pip install -r requirements.txt`

2. Create a .env file in your main folder with the variable `SECRET_KEY = 'YOUR SECRET KEY'`

3. Apply Migrations:
`python manage.py makemigrations tickets` then `python manage.py migrate`

4. Create a super user account if you wish to access the admin:
`python manage.py createsuperuser`

5. TESTING ONLY - DON'T USE THIS STEP IN PRODUCTION

    + My test app uses a single button form with pre populated credentials in the navbar, this is for a quick proof of concept and should NOT be used in production for security reasons.
    + Create a regular user (not super user) with desired credentials:
      - `python manage.py shell`
      - `from django.contrib.auth.models import User`
      - `user = User.objects.create_user(username='YOUR_USERNAME', email='YOUR_EMAIL', password='YOUR_PASSWORD')`
    + Make sure the hidden username and password fields in the index.html navbar match the user you just created.
    + You should now be able to click the login button and log in to the site with the user you just created.
    + This is not good practice so make sure to implement a proper login form.

6. Run Server:
 `python manage.py runserver`

