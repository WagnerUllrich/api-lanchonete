from pydantic import BaseModel


class ResgatePontosRequest(BaseModel):
    pontos: int


class SaldoFidelidadeResponse(BaseModel):
    usuario_id: int
    pontos_fidelidade: int
    consentimento_lgpd: bool


class ResgatePontosResponse(BaseModel):
    usuario_id: int
    pontos_resgatados: int
    saldo_atual: int
    mensagem: str