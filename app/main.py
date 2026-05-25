from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.usuario import Usuario

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API Padaria funcionando"}