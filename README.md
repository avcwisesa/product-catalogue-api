# Product Catalogue API

An HTTP-Json based API for product catalogue

## Requirements
- [Python 3.11](https://www.python.org/downloads/release/python-3116/)
- [Flask 3](https://flask.palletsprojects.com/en/3.0.x/)
- [PostgreSQL 14](https://www.postgresql.org/docs/14/)

## Run Instruction

### DB Migration
```
python migrate.py test
```

### Development
```
flask --app 'app:create_app("test")' run --port=8000 --debug
```

### Production
```
gunicorn -w 4 -b :8000 'app:create_app("test")'
```

## Documentation

[Swagger Document](/static/swagger.json)

When the web server is running, documentation can also be accessed through `/apidocs`
