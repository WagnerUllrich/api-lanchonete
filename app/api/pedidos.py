from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_usuario_logado, exigir_tipos_usuario
from app.db.dependencies import get_db
from app.models.estoque import Estoque
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido, StatusPedido
from app.models.produto import Produto
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.pedido_schema import PedidoCreate, PedidoResponse, AtualizarStatusPedido

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
    if usuario_logado.tipo == TipoUsuario.CLIENTE:
        return db.query(Pedido).filter(
            Pedido.usuario_id == usuario_logado.id
        ).all()

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

    if (
        usuario_logado.tipo == TipoUsuario.CLIENTE
        and pedido.usuario_id != usuario_logado.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "erro": True,
                "codigo": "PERMISSAO_NEGADA",
                "mensagem": "Você não possui permissão para acessar este pedido.",
                "detalhes": None
            }
        )

    return pedido

@router.patch("/{pedido_id}/status", response_model=PedidoResponse)
def atualizar_status_pedido(
    pedido_id: int,
    dados: AtualizarStatusPedido,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(
        exigir_tipos_usuario([
            TipoUsuario.ADMIN,
            TipoUsuario.FUNCIONARIO
        ])
    )
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

    transicoes_permitidas = {
        StatusPedido.CRIADO: [StatusPedido.EM_PREPARO, StatusPedido.CANCELADO],
        StatusPedido.EM_PREPARO: [StatusPedido.PRONTO, StatusPedido.CANCELADO],
        StatusPedido.PRONTO: [StatusPedido.ENTREGUE],
        StatusPedido.ENTREGUE: [],
        StatusPedido.CANCELADO: []
    }

    if dados.status not in transicoes_permitidas[pedido.status]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "erro": True,
                "codigo": "TRANSICAO_STATUS_INVALIDA",
                "mensagem": "Transição de status do pedido não permitida.",
                "detalhes": {
                    "status_atual": pedido.status.value,
                    "status_solicitado": dados.status.value
                }
            }
        )

    if dados.status == StatusPedido.CANCELADO:
        itens = db.query(ItemPedido).filter(
            ItemPedido.pedido_id == pedido.id
        ).all()

        for item in itens:
            estoque = db.query(Estoque).filter(
                Estoque.produto_id == item.produto_id,
                Estoque.unidade_id == pedido.unidade_id
            ).first()

            if estoque:
                estoque.quantidade += item.quantidade

    pedido.status = dados.status

    db.commit()
    db.refresh(pedido)

    return pedido