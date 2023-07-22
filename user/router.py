from fastapi import APIRouter,Request,Form,status
from fastapi.templating import Jinja2Templates
from . models import *
from fastapi.responses import HTMLResponse,RedirectResponse 
from passlib.context import CryptContext
import typing
import passlib


router = APIRouter()


templates = Jinja2Templates(directory="user/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

@router.get('/',response_class=HTMLResponse)
async def read_item(request:Request):
    return templates.TemplateResponse('index.html',{
        "request":request
    })

@router.post("/registration/",response_class=HTMLResponse)
async def ragistration(request:Request,name:str = Form(...),
                       email:str = Form(...),
                       mobile: str = Form(...),
                       password:str = Form(...)):
    if await Student.filter(email = email).exists():
        flash(request, "Email already Exists")
        return RedirectResponse("/",status_code=status.HTTP_302_FOUND)
    elif await Student.filter(mobile = mobile).exists():
        flash(request, "Phone Number already Exists")
        return RedirectResponse("/",status_code=status.HTTP_302_FOUND)
    else:
        await Student.create(name=name,email=email,mobile=mobile,password = get_password_hash(password))
        flash(request, "Student sucessfull Ragistrated")
        return RedirectResponse("/",status_code=status.HTTP_201_CREATED)



@router.get('/table/',response_class=HTMLResponse)
async def read_userm(request:Request):
    user = await Student.all()
    return templates.TemplateResponse('table.html',{
        "user":user,
        "request":request
    })
    




