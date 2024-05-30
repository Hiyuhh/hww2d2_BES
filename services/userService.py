from sqlalchemy.orm import Session
from sqlalchemy import select
from database import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from utils.util import encode_token

def save(user_data):
    with Session(db.engine) as session:
        with session.begin():
            user_query = select(User).where(User.username == user_data['username'])
            user_check = session.execute(user_query).scalars().first()
            if user_check is not None:
                raise ValueError("User with that username already exists")
            new_user = User(username=user_data['username'], password=generate_password_hash(user_data['password']), role=user_data['role'])
            session.add(new_user)
            session.commit()
        session.refresh(new_user)
        return new_user

def find_all():
    query = db.select(User)
    users = db.session.execute(query).scalars().all()
    return users

def login(username, password):
    user_query = select(User).where(User.username == username)
    user = db.session.execute(user_query).scalars().first()
    if not user:
        raise ValueError("User not found")
    if not check_password_hash(user.password, password):
        raise ValueError("Password is incorrect")
    return encode_token(user.id)