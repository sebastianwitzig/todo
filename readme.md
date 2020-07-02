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

### 5. To create a super user run
    
```
$ docker-compose exec web python manage.py createsuperuser
```
    
### 6. Get access token of user

   1. Open http://localhost:8000/admin

   2. Login with data of just created user

   3. Find and copy token from http://localhost:8000/admin/authtoken/token/


### 7. Run test
  
   1. Create virtual environment for test
    
```
$ python -m venv test_env
```
    
   2. Start virtual environment
    
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

### 8. Shut down environment
    
```
$ docker-compose down
```
