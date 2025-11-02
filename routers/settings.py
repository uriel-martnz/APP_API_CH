from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.settings import Settings
from models.usuario import Usuario
from schemas.settings import Settings as SettingsSchema, SettingsUpdate
from utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/settings", tags=["Ajustes"])

@router.get("", response_model=SettingsSchema)
def get_settings(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settings = db.query(Settings).filter(
        Settings.id_usuario == current_user.id_usuario
    ).first()

    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuraciones no encontradas"
        )

    return settings

@router.put("", response_model=SettingsSchema)
def update_settings(
    settings_update: SettingsUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    settings = db.query(Settings).filter(
        Settings.id_usuario == current_user.id_usuario
    ).first()

    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuraciones no encontradas"
        )

    update_data = settings_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)

    return settings
