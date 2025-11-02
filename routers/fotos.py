from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
import shutil
from db.database import get_db
from models.foto import Foto
from models.paciente import Paciente
from models.usuario import Usuario
from schemas.foto import Foto as FotoSchema
from utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1", tags=["Fotos"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/pacientes/{id_paciente}/fotos", response_model=List[FotoSchema])
def get_fotos_paciente(
    id_paciente: str,
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )

    fotos = db.query(Foto).filter(
        Foto.id_paciente == id_paciente
    ).offset(skip).limit(limit).all()

    return fotos

@router.post("/pacientes/{id_paciente}/fotos", response_model=FotoSchema, status_code=status.HTTP_201_CREATED)
async def upload_foto(
    id_paciente: str,
    file: UploadFile = File(...),
    descripcion: str = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db_foto = Foto(
        id_foto=str(uuid.uuid4()),
        id_paciente=id_paciente,
        id_usuario=current_user.id_usuario,
        url=f"/{file_path}",
        nombre_archivo=unique_filename,
        descripcion=descripcion
    )

    db.add(db_foto)
    db.commit()
    db.refresh(db_foto)

    return db_foto

@router.delete("/fotos/{id_foto}", status_code=status.HTTP_204_NO_CONTENT)
def delete_foto(
    id_foto: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    foto = db.query(Foto).filter(Foto.id_foto == id_foto).first()

    if not foto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foto no encontrada"
        )

    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == foto.id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar esta foto"
        )

    file_path = foto.url.lstrip("/")
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(foto)
    db.commit()

    return None
