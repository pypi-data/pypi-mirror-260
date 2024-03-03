import json

from uuid import UUID, uuid4
from typing import Optional

from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi_pagination import paginate, add_pagination

from jsend2.jfast.pagination import Pagination
from jsend2.jfast.response import render_jsend, Response, JsendResponse

app = FastAPI()

add_pagination(app)


class Person(BaseModel):
    name: str = Field(default='amir')
    oid: Optional[str] = None
    uuid: UUID = Field(default=uuid4())


@app.get("/user/", response_model=Response[Person])
def single_user():
    person = Person(name='ali', oid=ObjectId())
    return render_jsend(person.model_dump())


@app.post("/user/", response_model=Response[Person])
def single_user(person: Person):
    return render_jsend(person.model_dump(), status_code=201)


@app.delete("/user/", response_model=Response[Person])
def single_user():
    return render_jsend({}, status_code=204)


@app.get("/users/", response_model=Pagination[Person])
def single_user():
    persons = [Person(name='ali'), Person(name='ali'), Person(name='ali')]
    return paginate(persons)
