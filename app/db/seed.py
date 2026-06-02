# app/db/seed.py

from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import gerar_hash_senha

def criar_admin_padrao():
    db = SessionLocal()

    admin = db.query(Usuario).filter(
        Usuario.email == "admin@gmail.com"
    ).first()

    if not admin:
        admin = Usuario(
            nome="Administrador",
            email="admin@gmail.com",
            senha=gerar_hash_senha("123456"),
            tipo="ADMIN",
            consentimento_lgpd=True
        )

        db.add(admin)
        db.commit()

    db.close()