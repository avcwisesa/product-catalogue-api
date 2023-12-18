# Product Catalogue API

An HTTP-Json based API for product catalogue

## Requirements
- [Python 3.11](https://www.python.org/downloads/release/python-3116/)
- [pip](https://pypi.org/project/pip/)
- [Flask 3](https://flask.palletsprojects.com/en/3.0.x/)
- [PostgreSQL 14](https://www.postgresql.org/docs/14/)

## Usage

- Modify `test.toml` to configure database credentials
- Run DB migration
- Start API server
- Call `/login` API with existing username to get bearer token
- Call other APIs with previous bearer token as header

## Run Instruction

- Install dependencies
```
pip install
```
- Run DB migration
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

## Appendix

### Current Limitation (non-exhaustive list)

- User/tenant are only created during initial database migration or through manual database intervention
- Maximum amount of Product ID to be handled is currently capped at PostgreSQL integer limit
- Minimum to no parameter validation for API calls
- Authentication method is on par with leaving ID card(hopefully a valid one) at Office Buildings in Jakarta as a guest
