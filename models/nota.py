from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Nota(Base):
    __tablename__ = "notas"

    id_nota = Column(String, primary_key=True, index=True)
    id_paciente = Column(String, ForeignKey("pacientes.id_paciente"), nullable=False)
    contenido = Column(Text, nullable=False)
    peso = Column(Float)  # kg
    presion_sistolica = Column(Float)  # mmHg
    presion_diastolica = Column(Float)  # mmHg
    pulso = Column(Float)  # bpm
    autor = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    paciente = relationship("Paciente", back_populates="notas")
