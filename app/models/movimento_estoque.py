import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey

from app.db.database import Base


class TipoMovimentoEstoque(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"
    DEVOLUCAO = "DEVOLUCAO"
    AJUSTE = "AJUSTE"


class MovimentoEstoque(Base):
    __tablename__ = "movimentos_estoque"

    id = Column(Integer, primary_key=True, index=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)

    tipo = Column(Enum(TipoMovimentoEstoque), nullable=False)

    quantidade = Column(Integer, nullable=False)

    motivo = Column(String, nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)