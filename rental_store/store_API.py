from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel


store = FastAPI()


@store.post("/films/rent")
def rent_films():
    pass


@store.post("/films/return")
def return_films():
    pass


@store.get("/films")
def get_films():
    pass
