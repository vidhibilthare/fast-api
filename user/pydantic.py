from pydantic import BaseModel


class Person(BaseModel):
    name : str
    email : str
    mobile : int
    password : str

