from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_usuario_logado
from app.db.dependencies import get_db
from app.models.pagamento import Pagamento, StatusPagamento
from app.models.pedido import Pedido, StatusPedido
from app.models.usuario import Usuario
from app.schemas.pagamento_schema import PagamentoCreate, PagamentoResponse
from app.utils.auditoria import registrar_log

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.post("/", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_pagamento(
    pagamento: PagamentoCreate,
    db: Session = Depends(get_db),
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    pedido = db.query(Pedido).filter(Pedido.id == pagamento.pedido_id).first()

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

    status_pagamento = pagamento.resultado_mock

    if status_pagamento == StatusPagamento.APROVADO:
        mensagem_retorno = "Pagamento mock aprovado com sucesso."
        pedido.status = StatusPedido.EM_PREPARO

    elif status_pagamento == StatusPagamento.RECUSADO:
        mensagem_retorno = "Pagamento mock recusado. O pedido permanece aguardando nova tentativa de pagamento."

    elif status_pagamento == StatusPagamento.ERRO:
        mensagem_retorno = "Erro simulado na integração com o serviço de pagamento. O pedido permanece aguardando nova tentativa."

    else:
        mensagem_retorno = "Resultado de pagamento mock não reconhecido."

    novo_pagamento = Pagamento(
        pedido_id=pedido.id,
        valor=pedido.valor_total,
        metodo=pagamento.metodo,
        status=status_pagamento,
        mensagem_retorno=mensagem_retorno
    )

    db.add(novo_pagamento)
    db.commit()
    db.refresh(novo_pagamento)

    registrar_log(
        db=db,
        usuario_id=usuario_logado.id,
        acao="CRIAR_PAGAMENTO",
        entidade="Pagamento",
        entidade_id=novo_pagamento.id,
        detalhes=f"Pagamento {novo_pagamento.status.value} via {novo_pagamento.metodo.value}"
    )

    return novo_pagamento