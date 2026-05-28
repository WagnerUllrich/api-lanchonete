from pydantic import BaseModel, EmailStr

from app.models.usuario import TipoUsuario


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo: TipoUsuario
    consentimento_lgpd: bool


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: TipoUsuario
    ativo: bool
    pontos_fidelidade: int
    consentimento_lgpd: bool

    class Config:
        from_attributes = True