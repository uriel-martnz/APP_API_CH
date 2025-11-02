from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.nota import Nota
from models.paciente import Paciente
from models.usuario import Usuario
from schemas.nota import NotaCreate, NotaUpdate, Nota as NotaSchema
from utils.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/api/v1", tags=["Notas Médicas"])

@router.get("/pacientes/{id_paciente}/notas", response_model=List[NotaSchema])
def get_notas_paciente(
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

    notas = db.query(Nota).filter(
        Nota.id_paciente == id_paciente
    ).offset(skip).limit(limit).all()

    return notas

@router.post("/pacientes/{id_paciente}/notas", response_model=NotaSchema, status_code=status.HTTP_201_CREATED)
def create_nota(
    id_paciente: str,
    nota: NotaCreate,
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

    nota_data = nota.model_dump()
    nota_data['id_paciente'] = id_paciente

    db_nota = Nota(
        id_nota=str(uuid.uuid4()),
        **nota_data
    )

    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)

    return db_nota

@router.get("/notas/{id_nota}", response_model=NotaSchema)
def get_nota(
    id_nota: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()

    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nota no encontrada"
        )

    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == nota.id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta nota"
        )

    return nota

@router.put("/notas/{id_nota}", response_model=NotaSchema)
def update_nota(
    id_nota: str,
    nota_update: NotaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    nota = db.query(Nota).filter(Nota.id_nota == id_nota).first()

    if not nota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nota no encontrada"
        )

    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == nota.id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta nota"
        )

    update_data = nota_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(nota, field, value)

    db.commit()
    db.refresh(nota)

    return nota
