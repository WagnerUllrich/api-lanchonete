from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth_dependencies import exigir_tipos_usuario
from app.db.dependencies import get_db
from app.models.estoque import Estoque
from app.models.movimento_estoque import (
    MovimentoEstoque,
    TipoMovimentoEstoque
)
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.movimento_estoque_schema import (
    MovimentoEstoqueCreate,
    MovimentoEstoqueResponse
)

router = APIRouter(
    prefix="/estoques",
    tags=["Estoques"]
)


@router.post(
    "/entradas",
    response_model=MovimentoEstoqueResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_entrada_estoque(
    dados: MovimentoEstoqueCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(
        exigir_tipos_usuario([
            TipoUsuario.ADMIN,
            TipoUsuario.FUNCIONARIO
        ])
    )
):
    estoque = db.query(Estoque).filter(
        Estoque.produto_id == dados.produto_id,
        Estoque.unidade_id == dados.unidade_id
    ).first()

    if estoque is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": True,
                "codigo": "ESTOQUE_NAO_ENCONTRADO",
                "mensagem": "Estoque não encontrado.",
                "detalhes": None
            }
        )

    estoque.quantidade += dados.quantidade

    movimento = MovimentoEstoque(
        produto_id=dados.produto_id,
        unidade_id=dados.unidade_id,
        tipo=TipoMovimentoEstoque.ENTRADA,
        quantidade=dados.quantidade,
        motivo=dados.motivo
    )

    db.add(movimento)

    db.commit()
    db.refresh(movimento)

    return movimento


@router.get("/movimentos", response_model=list[MovimentoEstoqueResponse])
def listar_movimentos_estoque(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(
        exigir_tipos_usuario([
            TipoUsuario.ADMIN,
            TipoUsuario.FUNCIONARIO
        ])
    )
):
    return db.query(MovimentoEstoque).order_by(
        MovimentoEstoque.criado_em.desc()
    ).all()