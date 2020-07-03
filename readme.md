# Todo app with docker environment

## Requirements
- Docker Engine 19.03.x
- docker-compose 1.26.x
- Python 3.8.x
- Git

## Get started

### 1. clone reposetory
    
```
$ git clone https://github.com/sebastianwitzig/todo.git
```
    
### 2. Change to reposetory directory
    
```
$ cd todo
```
    
### 3. Set allwed hosts (if needed)
Edit ```.env.prod``` file and set host:
    
```
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
```

### 4. Start up the environment
    
```
$ docker-compose up -d
```

### 5. API Interface / Documentation
    
   Open http://localhost:8000/admin


### 6. To create a super user run
    
```
$ docker-compose run web python manage.py createsuperuser
```
    
### 7. Get access token of user

   1. Open http://localhost:8000/admin

   2. Login with data of just created user.

   3. Find and copy token from http://localhost:8000/admin/authtoken/token/

   4. Add accesstoken to environment variable(TODO_ACCESS_TOKEN) or paste it later while running the test directly.


### 8. Run test
  
   1. Create virtual environment for test
    
```
$ python -m venv test_env
```
    
   2. Activate virtual environment
    
```
$ source test_env/bin/activate
```
    
   3. Install dependencies
    
```
$ pip install -r app/test_requirements.txt
```
    
   4. Run test
    
```
$ python -m unittest test_todo.py
```
    
   5. Deactivate virtual environment
    
```
$ deactivate
```

### 9. Shut down environment

```
$ docker-compose down
```

## API Documentation

### Authentication
Authentication in header of request.
Example: "Authentication: Bearer <TOKEN>"

### APIs

#### GET
    /todo/

##### Parameters

| Variable    | Type                 | Example         | Required | Description                                                      |
| --------    | ----                 | -------         | -------- | -----------                                                      |
| title       | text                 | Wash            | no       | Search for title                                                 |
| description | text                 | Wash the car    | no       | Search for description                                           |
| due_date    | date                 | 2020-02-14      | no       | Search for todos at this date                                    |
| state       | int                  | 0               | no       | Filter todos with given status(TODO: 0, IN PROGRESS: 1, DONE: 2) |
| ordering    | comma separated text | due_date,-state | no       | Order by given fields (add '-' to order desc).                   |

##### POST
    /todo/

##### PATCH
    /todo/<id>/

##### DELETE
    /todo/<id>/
