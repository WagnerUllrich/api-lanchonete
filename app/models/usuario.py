from sqlalchemy import Column, Integer, String, Boolean, Enum

from app.db.database import Base

import enum


class TipoUsuario(str, enum.Enum):
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"
    CLIENTE = "CLIENTE"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    senha_hash = Column(String, nullable=False)

    tipo = Column(Enum(TipoUsuario), nullable=False)

    ativo = Column(Boolean, default=True)

    consentimento_lgpd = Column(Boolean, default=False)