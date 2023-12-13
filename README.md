# enviroment setup
create a enviroment using `pipenv shell` 

and execute the below command to install enviroment libraries `pipenv install`


# Create a Database 
Enter in python interactive mode using `flask shell` command

```sh
$ flask shell
```

then create a DB table using following script

```py
>>> from src import *
>>> db.create_all()
```

after executing this script in shell the Db file will get created in `./Path_Of_Project/ShortPythonWebDeveloperAssignment/instance/assignment.db`


# Run the app 
to run the pese run the below command in shell with corrent enviroment
```sh
$ python wsgi.py
```


# Flask Hello flask! end point
http://localhost:5000/


# RestFul CRUD Operation for RestFul api 
## Get 
curl http://localhost:5000/books
curl http://localhost:5000/books/1

## POST
curl http://localhost:5000/books -H 'Content-Type: application/json' -d '{"book_name":"Book_1"}'

## PUT 
curl http://localhost:5000/books/1 -X PUT  -H 'Content-Type: application/json' -d '{"book_name":"igikai"}'

## Delete
curl http://localhost:5000/books/2 -X DELETE 
