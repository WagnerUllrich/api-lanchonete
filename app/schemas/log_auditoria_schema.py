from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LogAuditoriaResponse(BaseModel):
    id: int
    usuario_id: int | None
    acao: str
    entidade: str | None
    entidade_id: int | None
    detalhes: str | None
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)