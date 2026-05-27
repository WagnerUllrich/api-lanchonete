from sqlalchemy import Column, Integer, ForeignKey

from app.db.database import Base


class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)

    quantidade = Column(Integer, nullable=False, default=0)