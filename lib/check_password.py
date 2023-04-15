from models.user_model import User
from werkzeug.security import check_password_hash
from config.coneccion import SessionLocal

db = SessionLocal()

def check_user(username, password):
    user = db.query(User).filter(User.username == username).first()
    if user:
        same_password = check_password_hash(user.password, password)
        if same_password:
            return user
    return None


