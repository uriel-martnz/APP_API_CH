from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.usuario import Usuario
from models.settings import Settings
from schemas.usuario import UsuarioCreate, UsuarioLogin, Usuario as UsuarioSchema, Token, UsuarioUpdate
from utils.security import verify_password, get_password_hash, create_access_token
from utils.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioSchema, status_code=status.HTTP_201_CREATED)
def register(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    hashed_password = get_password_hash(usuario.contrasena)
    db_usuario = Usuario(
        id_usuario=str(uuid.uuid4()),
        nombre=usuario.nombre,
        email=usuario.email,
        contrasena=hashed_password,
        rol=usuario.rol
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    # Crear settings por defecto para el usuario
    db_settings = Settings(
        id_settings=str(uuid.uuid4()),
        id_usuario=db_usuario.id_usuario
    )
    db.add(db_settings)
    db.commit()

    return db_usuario

@router.post("/login", response_model=Token)
def login(credentials: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == credentials.email).first()

    if not usuario or not verify_password(credentials.contrasena, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": usuario.email})

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(current_user: Usuario = Depends(get_current_user)):
    return {"message": "Sesión cerrada exitosamente"}

@router.get("/me", response_model=UsuarioSchema)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UsuarioSchema)
def update_me(
    usuario_update: UsuarioUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if usuario_update.nombre is not None:
        current_user.nombre = usuario_update.nombre

    if usuario_update.contrasena is not None:
        current_user.contrasena = get_password_hash(usuario_update.contrasena)

    db.commit()
    db.refresh(current_user)

    return current_user
