from pydantic import BaseModel

from app.models.pagamento import MetodoPagamento, StatusPagamento


class PagamentoCreate(BaseModel):
    pedido_id: int
    metodo: MetodoPagamento
    resultado_mock: StatusPagamento = StatusPagamento.APROVADO


class PagamentoResponse(BaseModel):
    id: int
    pedido_id: int
    valor: float
    metodo: MetodoPagamento
    status: StatusPagamento
    mensagem_retorno: str | None

    class Config:
        from_attributes = True