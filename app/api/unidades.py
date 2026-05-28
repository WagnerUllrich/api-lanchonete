from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.unidade import Unidade
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.unidade_schema import UnidadeCreate, UnidadeResponse, UnidadeUpdate
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


@router.get("/{unidade_id}", response_model=UnidadeResponse)
def buscar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()

    if unidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": True,
                "codigo": "UNIDADE_NAO_ENCONTRADA",
                "mensagem": "Unidade não encontrada.",
                "detalhes": None
            }
        )

    return unidade


@router.put("/{unidade_id}", response_model=UnidadeResponse)
def atualizar_unidade(
    unidade_id: int,
    dados: UnidadeUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(
        exigir_tipos_usuario([TipoUsuario.ADMIN])
    )
):
    unidade = db.query(Unidade).filter(Unidade.id == unidade_id).first()

    if unidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": True,
                "codigo": "UNIDADE_NAO_ENCONTRADA",
                "mensagem": "Unidade não encontrada.",
                "detalhes": None
            }
        )

    unidade.nome = dados.nome
    unidade.endereco = dados.endereco
    unidade.ativo = dados.ativo

    db.commit()
    db.refresh(unidade)

    return unidade