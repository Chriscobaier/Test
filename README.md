# Test

### INSTALL
```commandline
    pip install -U Flask
    pip install -U Flask-SQLAlchemy
    pip install flask-login
    pip install flask-bcrypt
    pip install -U Flask-WTF
    pip install -U WTForms
    pip install email-validator
```

### ?
```commandline

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "-----linux------"
        export FLASK_APP=main.py
        export FLASK_DEBUG=1

    elif [[ "$OSTYPE" == "darwin"* ]]; then
       echo "-----Mac OSX-----"
       export FLASK_APP=main.py
       export FLASK_DEBUG=1
       
    elif [[ "$OSTYPE" == "freebsd"* ]]; then
        echo "FreeBSD"
    else
        echo "-----Windows----"
        set FLASK_APP=main.py
        set FLASK_DEBUG=1
    fi

```

### add changes to the db
```commandline
    python
    from main import db, app, User
    app.app_context().push()
    db.create_all()
```


### If the changes have been applied or not -
```commandline
    
    sqlite3 instance/inner-air.db
    .table
```

###
```commandline

    Python 3.11.1 (main, Jan 21 2023, 22:20:32) [GCC 11.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from main import db,app,User
    >>> app.app_context().push()
    >>> db.create_all()
    >>> user1 = User(first_name="jc", email="jc@123.com", password="12345")
    >>> user2 = User(first_name="js", email="js@456.com", password="qwert")
    >>> db.session.add(user1)
    >>> db.session.add(user2)
    >>> db.session.commit()
    >>> User.query.all()
    output ->   [<User 1>, <User 2>]
```

### SQLITE3
```commandline
    (venv) jrchavez07@jrchavez07 ~/PycharmProjects/Test $ sqlite3 instance/inner-air.db 
    SQLite version 3.39.4 2022-09-29 15:55:41
    Enter ".help" for usage hints.
    sqlite> SELECT * FROM user;
    output ->   1|jc|jc@123.com|12345
    output ->   2|js|js@456.com|qwert
    sqlite> 


```
