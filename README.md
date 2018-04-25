# Flask backend server with JWT authorization

## Sources
[https://pythonhosted.org/Flask-JWT/](https://pythonhosted.org/Flask-JWT/)
[http://polyglot.ninja/jwt-authentication-python-flask/](http://polyglot.ninja/jwt-authentication-python-flask/)



```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MjQ0MjAyMTUsImlhdCI6MTUyNDQxOTkxNSwibmJmIjoxNTI0NDE5OTE1LCJpZGVudGl0eSI6MX0.RIzLFtgR7w_qhKE0ZAu-Gl4S6Jp4duOMotCpUcp9Nws"
}
```


1. Install git on respberry
`sudo apt-get install git`

1. Clone Flask backend server
`git clone https://github.com/antonioiksi/FlaskJWT_test.git`

1. Install module virtualenv
`pip install virtualenv`

1. Add path to virtualenv in PATH
`export PATH="/home/pi/.local/bin/:$PATH"`

1. Create virtual environment for project
`virtualenv venv36`

1. Activate project's virtualenv
`source venv36/bin/activate`

1. Install all packages
`pip install -r requirements.txt`

1. Run flask
`python FlaskJWT_test.py`