from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.usuario import Usuario
from app.models.unidade import Unidade
from app.api.usuarios import router as usuarios_router
from app.api.auth import router as auth_router
from app.api.unidades import router as unidades_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Padaria",
    description="API backend para rede de padarias",
    version="1.0.0"
)

app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(unidades_router)


@app.get("/")
def home():
    return {"message": "API Padaria funcionando"}