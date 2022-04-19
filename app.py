from ensurepip import version
from unicodedata import name
from fastapi import FastAPI
from routes.user import user

app = FastAPI(
  title="API",
  description="Mi primera API usando FASTAPI",
  version="0.0.1",
  openapi_tags=[{
    "name": "users",
    "description": "users router"

  }]
)

app.include_router(user)
