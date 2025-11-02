from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from db.database import engine, Base
import models

from routers import auth, pacientes, citas, notas, fotos, settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Pacientes",
    description="API REST para gestionar pacientes, citas y expedientes médicos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(pacientes.router)
app.include_router(citas.router)
app.include_router(notas.router)
app.include_router(fotos.router)
app.include_router(settings.router)

@app.get("/")
def root():
    return {
        "message": "Gestión de Pacientes API",
        "version": "1.0.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health():
    return {"status": "funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
