from sqlalchemy import Column, Integer, String
from config.coneccion import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(200), unique=False)
    lastname = Column(String(200), unique=False, default="")
    username = Column(String(200), unique=True)
    country = Column(String(200), unique=False)
    password = Column(String(300))

    def __init__(self, firstname, lastname, username, country, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.country = country
        self.password = password


Base.metadata.create_all(bind=engine)
