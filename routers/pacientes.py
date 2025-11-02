from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from models.paciente import Paciente
from models.usuario import Usuario
from schemas.paciente import PacienteCreate, PacienteUpdate, Paciente as PacienteSchema
from utils.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/api/v1/pacientes", tags=["Pacientes"])

@router.get("", response_model=List[PacienteSchema])
def get_pacientes(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    estado: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Paciente).filter(Paciente.id_usuario == current_user.id_usuario)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Paciente.nombre.ilike(search_filter)) |
            (Paciente.apellidos.ilike(search_filter)) |
            (Paciente.email.ilike(search_filter))
        )

    if estado:
        query = query.filter(Paciente.estado == estado)

    pacientes = query.offset(skip).limit(limit).all()
    return pacientes

@router.post("", response_model=PacienteSchema, status_code=status.HTTP_201_CREATED)
def create_paciente(
    paciente: PacienteCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_paciente = Paciente(
        id_paciente=str(uuid.uuid4()),
        id_usuario=current_user.id_usuario,
        **paciente.model_dump()
    )

    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)

    return db_paciente

@router.get("/{id_paciente}", response_model=PacienteSchema)
def get_paciente(
    id_paciente: str,
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

    return paciente

@router.put("/{id_paciente}", response_model=PacienteSchema)
def update_paciente(
    id_paciente: str,
    paciente_update: PacienteUpdate,
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

    update_data = paciente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(paciente, field, value)

    db.commit()
    db.refresh(paciente)

    return paciente
