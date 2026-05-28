from pydantic import BaseModel, Field, ConfigDict

from app.models.pedido import CanalPedido, StatusPedido


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int


class PedidoCreate(BaseModel):
    unidade_id: int
    canal_pedido: CanalPedido = Field(alias="canalPedido")
    itens: list[ItemPedidoCreate]

    model_config = ConfigDict(populate_by_name=True)


class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float

    model_config = ConfigDict(from_attributes=True)


class PedidoResponse(BaseModel):
    id: int
    usuario_id: int
    unidade_id: int
    canal_pedido: CanalPedido = Field(alias="canalPedido")
    status: StatusPedido
    valor_total: float

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class AtualizarStatusPedido(BaseModel):
    status: StatusPedido