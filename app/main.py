from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.usuario import Usuario
from app.api.usuarios import router as usuarios_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Padaria",
    description="API backend para rede de padarias",
    version="1.0.0"
)

app.include_router(usuarios_router)


@app.get("/")
def home():
    return {"message": "API Padaria funcionando"}