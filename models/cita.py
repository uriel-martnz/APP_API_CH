from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Cita(Base):
    __tablename__ = "citas"

    id_cita = Column(String, primary_key=True, index=True)
    id_paciente = Column(String, ForeignKey("pacientes.id_paciente"), nullable=False)
    fecha = Column(DateTime, nullable=False)
    hora = Column(String, nullable=False)
    motivo = Column(Text)
    doctor = Column(String)
    estado = Column(String, default="programada")  # programada/completada/cancelada
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="citas")
