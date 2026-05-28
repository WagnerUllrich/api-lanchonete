from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.movimento_estoque import TipoMovimentoEstoque


class MovimentoEstoqueCreate(BaseModel):
    produto_id: int
    unidade_id: int
    quantidade: int
    motivo: str | None = None


class MovimentoEstoqueResponse(BaseModel):
    id: int
    produto_id: int
    unidade_id: int
    tipo: TipoMovimentoEstoque
    quantidade: int
    motivo: str | None
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)