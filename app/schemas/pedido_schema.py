from pydantic import BaseModel

from app.models.pedido import CanalPedido, StatusPedido


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int


class PedidoCreate(BaseModel):
    unidade_id: int
    canal_pedido: CanalPedido
    itens: list[ItemPedidoCreate]


class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float

    class Config:
        from_attributes = True


class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    unidade_id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    valor_total: float

    class Config:
        from_attributes = True


class AtualizarStatusPedido(BaseModel):
    status: StatusPedido