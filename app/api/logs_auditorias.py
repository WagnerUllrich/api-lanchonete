from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import exigir_tipos_usuario
from app.db.dependencies import get_db
from app.models.log_auditoria import LogAuditoria
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.log_auditoria_schema import LogAuditoriaResponse

router = APIRouter(
    prefix="/logs-auditorias",
    tags=["Logs Auditorias"]
)


@router.get("/", response_model=list[LogAuditoriaResponse])
def listar_logs_auditoria(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(
        exigir_tipos_usuario([TipoUsuario.ADMIN])
    )
):
    return db.query(LogAuditoria).order_by(LogAuditoria.criado_em.desc()).all()