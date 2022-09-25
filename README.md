# djangotickets
A simple ticket manager made with Django, Bootstrap, and Django templates.

By no means does this include best practices, but it gets a simple project started.

![Alt Text](https://i.ibb.co/KmnjTJR/djangoticketmanager.jpg)

# Installation

1. Install pip packages:
`pip install -r requirements.txt`

2. Create a super user account:
`python manage.py createsuperuser`

3. Apply Migrations:
`python manage.py makemigrations tickets` then `python manage.py migrate`

4. TESTING ONLY - DON'T USE THIS STEP IN PRODUCTION

    + This test app uses a form with pre populated credentials in index.html, this is for a quick proof of concept and should not be used in production for security reasons.
    + Create a regular user (not super user) with desired credentials, and then update the index.html login form with those credentials.
      - `python manage.py shell`
      - `from django.contrib.auth.models import User`
      - `user = User.objects.create_user(username='YOUR_USERNAME', email='YOUR_EMAIL', password='YOUR_PASSWORD')`
    + Ideally if using this app you'd implement a proper login form, I added this for development purposes.

 5. Run Server:
 `python manage.py runserver`

