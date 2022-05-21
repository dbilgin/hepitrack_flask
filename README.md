# hepitrack_flask
Backend project for the [hepitrack](https://github.com/dbilgin/hepitrack) application.
It takes the user data and saves it in its sqlite database. The user data is saved per user id and the user tokens are generated with sha 256. These tokens are used for basic authorization while fetching data.

## Authorization
The basic authorization uses this [login_required](https://github.com/dbilgin/hepitrack_flask/blob/master/flaskr/auth.py#L61) on endpoints like [this](https://github.com/dbilgin/hepitrack_flask/blob/master/flaskr/track.py#L13).
Whenever a user registers, they receive a verification email and this email redirects the users to https://hepitrack.web.app/verify-email address. You can take a look at this project [here](https://github.com/dbilgin/hepitrack-web). It makes a very simple request to hepitrack_flask to verify the email of the user and then the application becomes usable.

This authorization is only used for Hepitrack related stuff and the news articles actually uses a different API key that belongs to https://newsapi.org/. The news are not fetched every time a user requests them, rather they are fetched only once a day, saved to sqlite and served from there throughout the day.

## How to run
```
pip install pytest coverage wheel
pip install -r requirements.txt
export FLASK_APP=flaskr && export FLASK_ENV=development && flask run
```
