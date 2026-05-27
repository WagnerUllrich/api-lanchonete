from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_usuario_logado, exigir_tipos_usuario
from app.db.dependencies import get_db
from app.models.estoque import Estoque
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.estoque_schema import EstoqueCreate, EstoqueResponse

router = APIRouter(
    prefix="/estoques",
    tags=["Estoques"]
)


@router.post("/", response_model=EstoqueResponse, status_code=status.HTTP_201_CREATED)
def criar_estoque(
    estoque: EstoqueCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(exigir_tipos_usuario([TipoUsuario.ADMIN]))
):
    novo_estoque = Estoque(
        produto_id=estoque.produto_id,
        unidade_id=estoque.unidade_id,
        quantidade=estoque.quantidade
    )

    db.add(novo_estoque)
    db.commit()
    db.refresh(novo_estoque)

    return novo_estoque


@router.get("/", response_model=list[EstoqueResponse])
def listar_estoques(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    return db.query(Estoque).all()


@router.get("/unidade/{unidade_id}", response_model=list[EstoqueResponse])
def listar_estoque_por_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    return db.query(Estoque).filter(Estoque.unidade_id == unidade_id).all()