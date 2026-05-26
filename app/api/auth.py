from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.usuario import Usuario
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.core.security import verificar_senha, criar_token_acesso

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=TokenResponse)
def login(dados_login: LoginRequest, db: Session = Depends(get_db)):

    usuario = db.query(Usuario).filter(Usuario.email == dados_login.email).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "erro": True,
                "codigo": "CREDENCIAIS_INVALIDAS",
                "mensagem": "Email ou senha inválidos.",
                "detalhes": None
            }
        )

    if not verificar_senha(dados_login.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "erro": True,
                "codigo": "CREDENCIAIS_INVALIDAS",
                "mensagem": "Email ou senha inválidos.",
                "detalhes": None
            }
        )

    token = criar_token_acesso({
        "sub": str(usuario.id),
        "email": usuario.email,
        "tipo": usuario.tipo.value
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }