import enum
from datetime import datetime
from sqlalchemy import DateTime

from sqlalchemy import Column, Integer, Float, Enum, ForeignKey

from app.db.database import Base


class CanalPedido(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"


class StatusPedido(str, enum.Enum):
    CRIADO = "CRIADO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)

    criado_em = Column(DateTime, default=datetime.utcnow)

    atualizado_em = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)

    canal_pedido = Column(Enum(CanalPedido), nullable=False)

    status = Column(
        Enum(StatusPedido),
        default=StatusPedido.CRIADO,
        nullable=False
    )

    valor_total = Column(Float, default=0)

