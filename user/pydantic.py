from pydantic import BaseModel


class Person(BaseModel):
    email:str
    name:str
    phone:int
    password:str


class Login(BaseModel):
    email : str
    password : str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User_data(BaseModel):
    id:int

class update_data(BaseModel):
    id : int
    name : str
    email : str
    mobile : str 


