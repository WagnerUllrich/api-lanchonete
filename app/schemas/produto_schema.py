from pydantic import BaseModel


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str | None = None
    preco: float


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco: float
    ativo: bool

    class Config:
        from_attributes = True