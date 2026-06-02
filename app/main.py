from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.usuario import Usuario
from app.models.unidade import Unidade
from app.models.produto import Produto
from app.models.estoque import Estoque
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.pagamento import Pagamento
from app.models.log_auditoria import LogAuditoria
from app.api.logs_auditorias import router as logs_auditorias_router
from app.api.usuarios import router as usuarios_router
from app.api.auth import router as auth_router
from app.api.unidades import router as unidades_router
from app.api.produtos import router as produtos_router
from app.api.estoques import router as estoques_router
from app.api.pedidos import router as pedidos_router
from app.api.pagamentos import router as pagamentos_router
from app.api.fidelidades import router as fidelidades_router
from app.models.movimento_estoque import MovimentoEstoque
from app.api.movimentos_estoques import router as movimentos_estoques_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status
from app.db.database import SessionLocal
from app.core.security import gerar_hash_senha



Base.metadata.create_all(bind=engine)

def criar_admin_padrao():
    db = SessionLocal()

    admin_existente = db.query(Usuario).filter(
        Usuario.email == "admin@gmail.com"
    ).first()

    if not admin_existente:
        admin = Usuario(
            nome="Administrador",
            email="admin@gmail.com",
            senha_hash=gerar_hash_senha("123456"),
            tipo="ADMIN",
            consentimento_lgpd=True,
            ativo=True
        )

        db.add(admin)
        db.commit()

    db.close()


criar_admin_padrao()

app = FastAPI(
    title="Raízes do Nordeste — API Back-end",
    description="API backend para rede de lanchonetes com múltiplas unidades e canais de atendimento",
    version="1.0.0"
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    for erro in exc.errors():
        loc = erro.get("loc", [])

        if "canalPedido" in loc:
            return JSONResponse(
                status_code=422,
                content={
                    "detail": {
                        "erro": True,
                        "codigo": "CANAL_PEDIDO_INVALIDO",
                        "mensagem": "O campo canalPedido é obrigatório e deve ser APP, TOTEM, BALCAO, PICKUP ou WEB.",
                        "detalhes": None
                    }
                }
            )

    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "erro": True,
                "codigo": "ERRO_VALIDACAO",
                "mensagem": "Erro de validação nos dados enviados.",
                "detalhes": exc.errors()
            }
        }
    )


app.include_router(usuarios_router)
app.include_router(auth_router)
app.include_router(unidades_router)
app.include_router(produtos_router)
app.include_router(estoques_router)
app.include_router(pedidos_router)
app.include_router(pagamentos_router)
app.include_router(fidelidades_router)
app.include_router(logs_auditorias_router)
app.include_router(movimentos_estoques_router)


