from sqlalchemy.orm import Session

from app.models.log_auditoria import LogAuditoria


def registrar_log(
    db: Session,
    usuario_id: int | None,
    acao: str,
    entidade: str | None = None,
    entidade_id: int | None = None,
    detalhes: str | None = None
):
    log = LogAuditoria(
        usuario_id=usuario_id,
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id,
        detalhes=detalhes
    )

    db.add(log)

    db.commit()