from fastapi import APIRouter, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config.coneccion import SessionLocal
from fastapi.params import Depends
from sqlalchemy.orm import Session
from models.user_model import User
from werkzeug.security import generate_password_hash
from lib.check_password import check_user

user = APIRouter()

template = Jinja2Templates(directory="./templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Pagina raiz del proyecto:
@user.get("/", response_class=HTMLResponse)
def home(req: Request):
    return template.TemplateResponse("index.html", {"request": req})


@user.post("/", response_class=HTMLResponse)
def home(req: Request):
    return template.TemplateResponse("index.html", {"request": req})


# Pagina de ingreso:
@user.get("/user", response_class=HTMLResponse)
def list_user(req: Request):
    return RedirectResponse("/")


@user.post("/user", response_class=HTMLResponse)
def list_user(req: Request, username: str = Form(), password_user: str = Form()):
    verify = check_user(username, password_user)
    if verify:
        return template.TemplateResponse(
            "user.html", {"request": req, "data_user": verify}
        )
    return RedirectResponse("/")


# Pagina de creacion de un nuevo dato:
@user.get("/signup", response_class=HTMLResponse)
def signup(req: Request):
    return template.TemplateResponse("signup.html", {"request": req})


# Creacion de un nuevo usuario:
@user.post("/data-processing")
def create_user(
    firstname: str = Form(),
    lastname: str = Form(),
    username: str = Form(),
    country: str = Form(),
    password_user: str = Form(),
    db: Session = Depends(get_db),
):
    password_cryp = generate_password_hash(
        password_user, "pbkdf2:sha256:15", 15
    ).encode()
    user = User(
        firstname,
        lastname,
        username,
        country,
        password_cryp,
    )
    db.add(user)
    db.commit()
    return RedirectResponse("/")
