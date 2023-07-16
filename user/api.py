from fastapi import APIRouter,Request,status,Depends
from.models import *
from . pydantic import Person
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

SECRET = "super-secret-key"
app = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

manager = LoginManager(SECRET, token_url='/auth/token')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


@app.post('/')
async def registration(data:Person):
    if await Student.exists(mobile=data.mobile):
        return{"status":False,"message":"Phone number already exists"}
    elif await Student.exists(email=data.email):
        return{"status":False,"message":"Email already exits"}
    else:
        user_obj = await Student.create(name=data.name,email=data.email,mobile=data.mobile,password=get_password_hash(data.password))
        return user_obj
@app.get('/all/')
async def all_student():
    user_object = await Student.all()
    return user_object
    
@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    user = Student.get(email)
    return user

@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException
    
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}