from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.usuario import Usuario, TipoUsuario
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from app.core.security import gerar_hash_senha
from app.core.auth_dependencies import get_usuario_logado, exigir_tipos_usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):


    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "erro": True,
                "codigo": "EMAIL_JA_CADASTRADO",
                "mensagem": "Já existe um usuário cadastrado com este e-mail.",
                "detalhes": None
            }
        )

    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha),
        tipo=usuario.tipo,
        consentimento_lgpd=usuario.consentimento_lgpd
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.get("/me", response_model=UsuarioResponse)
def obter_meu_usuario(
    usuario_logado: Usuario = Depends(get_usuario_logado)
):
    return usuario_logado


@router.get("/admin")
def rota_admin(
    usuario: Usuario = Depends(
        exigir_tipos_usuario([TipoUsuario.ADMIN])
    )
):
    return {
        "mensagem": f"Bem-vindo admin {usuario.nome}"
    }