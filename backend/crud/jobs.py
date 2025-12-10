from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

# Crear una vacante
def crear_vacante(db: Session, vacante: schemas.VacanteCreate):
    db_vacante = models.Vacante(**vacante.dict())
    db.add(db_vacante)
    db.commit()
    db.refresh(db_vacante)
    return db_vacante

# Obtener una vacante por ID
def obtener_vacante(db: Session, vacante_id: int):
    vacante = db.query(models.Vacante).filter(models.Vacante.ID_Vacantes == vacante_id).first()
    if not vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    return vacante

# Obtener todas las vacantes
def obtener_vacantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vacante).offset(skip).limit(limit).all()

# Actualizar una vacante por ID
def actualizar_vacante(db: Session, vacante_id: int, vacante: schemas.VacanteCreate):
    db_vacante = db.query(models.Vacante).filter(models.Vacante.ID_Vacantes == vacante_id).first()
    if not db_vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    db_vacante.Titulo = vacante.Titulo
    db_vacante.Empresa = vacante.Empresa
    db_vacante.Condiciones = vacante.Condiciones
    db_vacante.Descripcion = vacante.Descripcion
    db_vacante.Region = vacante.Region
    db_vacante.Modalidad = vacante.Modalidad
    db_vacante.Requisitos = vacante.Requisitos
    db_vacante.Aptitudes = vacante.Aptitudes
    db_vacante.Enlace = vacante.Enlace
    db_vacante.Beneficios = vacante.Beneficios
    db.commit()
    db.refresh(db_vacante)
    return db_vacante

# Eliminar una vacante por ID
def eliminar_vacante(db: Session, vacante_id: int):
    db_vacante = db.query(models.Vacante).filter(models.Vacante.ID_Vacantes == vacante_id).first()
    if not db_vacante:
        raise HTTPException(status_code=404, detail="Vacante no encontrada")
    db.delete(db_vacante)
    db.commit()
    return db_vacante
