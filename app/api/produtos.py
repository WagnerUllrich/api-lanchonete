from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_usuario_logado, exigir_tipos_usuario
from app.db.dependencies import get_db
from app.models.produto import Produto
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(exigir_tipos_usuario([TipoUsuario.ADMIN]))
):
    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    return db.query(Produto).filter(Produto.ativo == True).all()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": True,
                "codigo": "PRODUTO_NAO_ENCONTRADO",
                "mensagem": "Produto não encontrado.",
                "detalhes": None
            }
        )

    return produto


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(
        exigir_tipos_usuario([TipoUsuario.ADMIN])
    )
):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": True,
                "codigo": "PRODUTO_NAO_ENCONTRADO",
                "mensagem": "Produto não encontrado.",
                "detalhes": None
            }
        )

    produto.nome = dados.nome
    produto.descricao = dados.descricao
    produto.preco = dados.preco
    produto.ativo = dados.ativo

    db.commit()
    db.refresh(produto)

    return produto