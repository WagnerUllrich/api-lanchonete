import enum

from sqlalchemy import Column, Integer, Float, Enum, String, ForeignKey

from app.db.database import Base


class MetodoPagamento(enum.Enum):
    PIX = "PIX"
    CARTAO = "CARTAO"
    DINHEIRO = "DINHEIRO"
    MOCK = "MOCK"


class StatusPagamento(enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)

    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)

    valor = Column(Float, nullable=False)

    metodo = Column(Enum(MetodoPagamento), nullable=False)

    status = Column(
        Enum(StatusPagamento),
        default=StatusPagamento.PENDENTE,
        nullable=False
    )

    mensagem_retorno = Column(String, nullable=True)