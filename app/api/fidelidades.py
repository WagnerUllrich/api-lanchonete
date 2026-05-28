from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth_dependencies import get_usuario_logado
from app.models.usuario import Usuario
from app.schemas.fidelidade_schema import (
    ResgatePontosRequest,
    SaldoFidelidadeResponse,
    ResgatePontosResponse
)

router = APIRouter(
    prefix="/fidelidades",
    tags=["Fidelidades"]
)


@router.get("/saldo", response_model=SaldoFidelidadeResponse)
def consultar_saldo(
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    return {
        "usuario_id": usuario_logado.id,
        "pontos_fidelidade": usuario_logado.pontos_fidelidade,
        "consentimento_lgpd": usuario_logado.consentimento_lgpd
    }


@router.post("/resgatar", response_model=ResgatePontosResponse)
def resgatar_pontos(
    dados: ResgatePontosRequest,
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    if not usuario_logado.consentimento_lgpd:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "erro": True,
                "codigo": "FIDELIDADE_SEM_CONSENTIMENTO",
                "mensagem": "Usuário não consentiu participação no programa de fidelidade.",
                "detalhes": None
            }
        )

    if dados.pontos <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "erro": True,
                "codigo": "PONTOS_INVALIDOS",
                "mensagem": "A quantidade de pontos para resgate deve ser maior que zero.",
                "detalhes": None
            }
        )

    if usuario_logado.pontos_fidelidade < dados.pontos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "erro": True,
                "codigo": "PONTOS_INSUFICIENTES",
                "mensagem": "Saldo de pontos insuficiente para resgate.",
                "detalhes": {
                    "saldo_atual": usuario_logado.pontos_fidelidade,
                    "pontos_solicitados": dados.pontos
                }
            }
        )

    usuario_logado.pontos_fidelidade -= dados.pontos

    return {
        "usuario_id": usuario_logado.id,
        "pontos_resgatados": dados.pontos,
        "saldo_atual": usuario_logado.pontos_fidelidade,
        "mensagem": "Pontos resgatados com sucesso."
    }