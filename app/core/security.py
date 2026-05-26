from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def criar_token_acesso(dados: dict) -> str:
    dados_para_token = dados.copy()

    expiracao = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES)

    dados_para_token.update({"exp": expiracao})

    token = jwt.encode(
        dados_para_token,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return token