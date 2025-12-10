from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

# Crear una hoja de vida
def crear_hoja_de_vida(db: Session, hoja_de_vida: schemas.HojaDeVidaCreate):
    db_hoja_de_vida = models.HojaDeVida(**hoja_de_vida.dict())
    db.add(db_hoja_de_vida)
    db.commit()
    db.refresh(db_hoja_de_vida)
    return db_hoja_de_vida

# Obtener una hoja de vida por ID
def obtener_hoja_de_vida(db: Session, usuario_id: int):
    hoja = db.query(models.HojaDeVida).filter(models.HojaDeVida.ID_Usuario == usuario_id).first()
    if not hoja:
        raise HTTPException(status_code=404, detail="Hoja de vida no encontrada")
    return hoja

def obtener_hojas_de_vida_por_usuario(db: Session, usuario_id: int):
    hojas = db.query(models.HojaDeVida).filter(models.HojaDeVida.ID_Usuario == usuario_id).all()
    if not hojas:
        raise HTTPException(status_code=404, detail="No se encontraron hojas de vida para este usuario")
    return hojas

# Obtener todas las hojas de vida
def obtener_hojas_de_vida(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.HojaDeVida).offset(skip).limit(limit).all()

# Actualizar una hoja de vida por ID
def actualizar_hoja_de_vida(db: Session, usuario_id: int, hoja_de_vida: schemas.HojaDeVidaCreate):
    db_hoja = db.query(models.HojaDeVida).filter(models.HojaDeVida.ID_Usuario == usuario_id).first()
    if not db_hoja:
        raise HTTPException(status_code=404, detail="Hoja de vida no encontrada")
    db_hoja.Estudios = hoja_de_vida.Estudios
    db_hoja.Skills = hoja_de_vida.Skills
    db_hoja.Experiencia = hoja_de_vida.Experiencia
    db.commit()
    db.refresh(db_hoja)
    return db_hoja

# Eliminar una hoja de vida por ID
def eliminar_hoja_de_vida(db: Session, hoja_id: int):
    db_hoja = db.query(models.HojaDeVida).filter(models.HojaDeVida.ID_Hojadevida == hoja_id).first()
    if not db_hoja:
        raise HTTPException(status_code=404, detail="Hoja de vida no encontrada")
    db.delete(db_hoja)
    db.commit()
    return db_hoja
