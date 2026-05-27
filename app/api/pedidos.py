from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_usuario_logado
from app.db.dependencies import get_db
from app.models.estoque import Estoque
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido, StatusPedido
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.schemas.pedido_schema import PedidoCreate, PedidoResponse

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):

    valor_total = 0

    novo_pedido = Pedido(
        usuario_id=usuario_logado.id,
        unidade_id=pedido.unidade_id,
        canal_pedido=pedido.canal_pedido,
        status=StatusPedido.CRIADO
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    for item in pedido.itens:

        produto = db.query(Produto).filter(
            Produto.id == item.produto_id
        ).first()

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

        estoque = db.query(Estoque).filter(
            Estoque.produto_id == item.produto_id,
            Estoque.unidade_id == pedido.unidade_id
        ).first()

        if estoque is None or estoque.quantidade < item.quantidade:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "erro": True,
                    "codigo": "ESTOQUE_INSUFICIENTE",
                    "mensagem": "Estoque insuficiente para o produto.",
                    "detalhes": None
                }
            )

        subtotal = produto.preco * item.quantidade

        novo_item = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco,
            subtotal=subtotal
        )

        estoque.quantidade -= item.quantidade

        valor_total += subtotal

        db.add(novo_item)

    novo_pedido.valor_total = valor_total

    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    return db.query(Pedido).all()


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if pedido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "erro": True,
                "codigo": "PEDIDO_NAO_ENCONTRADO",
                "mensagem": "Pedido não encontrado.",
                "detalhes": None
            }
        )

    return pedido