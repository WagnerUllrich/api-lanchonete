from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import verificar_token
from app.db.dependencies import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_usuario_logado(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verificar_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "erro": True,
                "codigo": "TOKEN_INVALIDO",
                "mensagem": "Token inválido ou expirado.",
                "detalhes": None
            }
        )

    usuario_id = payload.get("sub")

    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "erro": True,
                "codigo": "USUARIO_NAO_ENCONTRADO",
                "mensagem": "Usuário do token não foi encontrado.",
                "detalhes": None
            }
        )

    return usuario