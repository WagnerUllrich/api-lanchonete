from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.unidade import Unidade
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.unidade_schema import UnidadeCreate, UnidadeResponse
from app.core.auth_dependencies import get_usuario_logado, exigir_tipos_usuario

router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"]
)


@router.post("/", response_model=UnidadeResponse, status_code=status.HTTP_201_CREATED)
def criar_unidade(
    unidade: UnidadeCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(exigir_tipos_usuario([TipoUsuario.ADMIN]))
):
    nova_unidade = Unidade(
        nome=unidade.nome,
        endereco=unidade.endereco
    )

    db.add(nova_unidade)
    db.commit()
    db.refresh(nova_unidade)

    return nova_unidade


@router.get("/", response_model=list[UnidadeResponse])
def listar_unidades(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    return db.query(Unidade).filter(Unidade.ativo == True).all()