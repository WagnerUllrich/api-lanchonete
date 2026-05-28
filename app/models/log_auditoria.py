from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.db.database import Base


class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    acao = Column(String, nullable=False)

    entidade = Column(String, nullable=True)

    entidade_id = Column(Integer, nullable=True)

    detalhes = Column(String, nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)