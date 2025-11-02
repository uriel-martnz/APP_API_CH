from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from db.database import get_db
from models.cita import Cita
from models.paciente import Paciente
from models.usuario import Usuario
from schemas.cita import CitaCreate, CitaUpdate, Cita as CitaSchema
from utils.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/api/v1/citas", tags=["Citas"])

@router.get("", response_model=List[CitaSchema])
def get_citas(
    skip: int = 0,
    limit: int = 100,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    doctor: Optional[str] = None,
    estado: Optional[str] = None,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pacientes_ids = [p.id_paciente for p in db.query(Paciente).filter(
        Paciente.id_usuario == current_user.id_usuario
    ).all()]

    query = db.query(Cita).filter(Cita.id_paciente.in_(pacientes_ids))

    if fecha_inicio:
        query = query.filter(Cita.fecha >= fecha_inicio)

    if fecha_fin:
        query = query.filter(Cita.fecha <= fecha_fin)

    if doctor:
        query = query.filter(Cita.doctor.ilike(f"%{doctor}%"))

    if estado:
        query = query.filter(Cita.estado == estado)

    citas = query.offset(skip).limit(limit).all()
    return citas

@router.post("", response_model=CitaSchema, status_code=status.HTTP_201_CREATED)
def create_cita(
    cita: CitaCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == cita.id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )

    db_cita = Cita(
        id_cita=str(uuid.uuid4()),
        **cita.model_dump()
    )

    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)

    return db_cita

@router.get("/{id_cita}", response_model=CitaSchema)
def get_cita(
    id_cita: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()

    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )

    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == cita.id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para acceder a esta cita"
        )

    return cita

@router.put("/{id_cita}", response_model=CitaSchema)
def update_cita(
    id_cita: str,
    cita_update: CitaUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cita = db.query(Cita).filter(Cita.id_cita == id_cita).first()

    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )

    paciente = db.query(Paciente).filter(
        Paciente.id_paciente == cita.id_paciente,
        Paciente.id_usuario == current_user.id_usuario
    ).first()

    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para modificar esta cita"
        )

    update_data = cita_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cita, field, value)

    db.commit()
    db.refresh(cita)

    return cita
