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



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Padaria",
    description="API backend para rede de padarias",
    version="1.0.0"
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



@app.get("/")
def home():
    return {"message": "API Padaria funcionando"}