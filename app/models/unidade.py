from sqlalchemy import Column, Integer, String, Boolean

from app.db.database import Base


class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)