from pydantic import BaseModel


class UnidadeCreate(BaseModel):
    nome: str
    endereco: str


class UnidadeResponse(BaseModel):
    id: int
    nome: str
    endereco: str
    ativo: bool

    class Config:
        from_attributes = True