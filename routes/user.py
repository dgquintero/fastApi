from fastapi import APIRouter, Response, status
from config.db import conn
from models.user import users
from schemas.user import User
from starlette.status import HTTP_204_NO_CONTENT

from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)


user = APIRouter()

# trae usuarios de la db


@user.get("/users", response_model=list[User], tags=["users"])
def get_users():
    return conn.execute(users.select()).fetchall()

# crea usuario en la db


@user.post("/users", response_model=User, tags=["users"])
def create_user(user: User):
    new_user = {
        "name": user.name,
        "email": user.email
    }
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))

    result = conn.execute(users.insert().values(new_user))
    # print(result.lastrowid)
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first()

# trae un unico usuario por id


@user.get("/users/{id}", response_model=User, tags=["users"])
def get_user(id: str):
    return conn.execute(users.select().where(users.c.id == id)).first()

# Elimina usuarios de la db


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)

@user.put("/users/{id}", response_model=User, tags=["users"])
def update_user(id: str, user: User):
    conn.execute(users.update().values(name=user.name,
                 email=user.email, password=f.encrypt(user.password.encode("utf-8"))).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()
