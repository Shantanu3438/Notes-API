# Notes API

## Overview
This Notes API has endpoints to create, view, delete, update and share notes. You can also create your account and share notes with other users. This API uses token based authentication.

## Installation
1. Clone the repository  
`git clone https://github.com/Shantanu3438/Notes-API.git`

2. Change directory to the project folder  
`cd Notes-API`

3. Install all the required packages using `pip`  
`pip install -r requirements.txt`

4. Make all the necessary migrations and then migrate  
`python3 manage.py makemigrations`  
`python3 manage.py migrate`

5. Run the development server  
`python3 manage.py runserver`

## API endpoints
1. Signup  `/signup/`
2. Login `/login/`
3. Create note `/notes/create/`
4. Get note `/notes/<id>/`
5. Delete note `/notes/<id>/delete`
6. update note `/notes/<id>/update`
6. Note history `/notes/<id>/history`
6. Share note `/notes/share/<id>/<userid>`
