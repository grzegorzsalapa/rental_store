# rental_store

Rental store is an application allowing to rent and return films using REST API. It is based on FastAPI framework and in
stable version stores data in memory. There is a version using PostgreSQL database and SQLAlchemy's ORM framework under
development in branch "ORM".

## How to run

#### Installation

    $ pip install .

#### Run from terminal

    $ uvicorn rental_store.store_api:store --host 127.0.0.1 --port 8080

Server is running on port 8080, does not require authenticating and can be accessed with valid REST API request (check
docs/openapi.json). To load demo data POST on /demo endpoint.

## How to test

#### Installation

    $ pip install .[test]

#### Run tests

    $ pytest

## Requirements

All packages required to run calculator module are specified in pyproject.toml file.

