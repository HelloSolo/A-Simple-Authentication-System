# Authentication-System
A simple authentication simple that also supports social logins.

## Installation Steps
1. Ensure python3 is installed
2. Clone the repository
3. create a virtual environment using ```virtual env```
4. Activate the virtual environment by running source ```venv/bin/activate``` or On Windows use source ```venv\Scripts\activate```
5. Install the dependencies using ```pip install -r requirements.txt```
6. Migrate existing db tables by running ```python manage.py migrate```
7. Run the django development server using ```python manage.py runserver```

## Creating a User Account
Here is a demo code for interacting with the api to create a user account.
```Javascript
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "application/json");

var raw = JSON.stringify({
"email": <string($email)>
"first_name":	<string>
"last_name":	<string>
"password":	<string>
 })

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/auth/users/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

## Logging In
Logging in in using email and password
```Javascript
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "application/json");
myHeaders.append("Authorization", "Basic <credentials>");

var raw = JSON.stringify({
  "email": "<string>",
  "password": "<string>"
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/auth/jwt/create/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```

Logging in with social account
```javascript
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");
myHeaders.append("Accept", "application/json");
myHeaders.append("Authorization", "Basic <credentials>");

var raw = JSON.stringify({
  "credential": "<string>"
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("http://127.0.0.1:8000/auth/social/google/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
```
