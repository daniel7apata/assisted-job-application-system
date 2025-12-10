from sqlalchemy.orm import Session
import models, schemas

# Crear una postulacion
def crear_postulacion(db: Session, postulacion: schemas.PostulacionCreate):
    db_postulacion = models.Postulacion(**postulacion.dict())
    db.add(db_postulacion)
    db.commit()
    db.refresh(db_postulacion)
    return db_postulacion

# Obtener una postulacion por ID
def obtener_postulacion(db: Session, postulacion_id: int):
    postulacion = db.query(models.Postulacion).filter(models.Postulacion.ID_Postulacion == postulacion_id).first()
    if not postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    return postulacion

# Obtener todas las postulaciones
def obtener_postulaciones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Postulacion).offset(skip).limit(limit).all()

# Actualizar una postulacion por ID
def actualizar_postulacion(db: Session, postulacion_id: int, postulacion: schemas.PostulacionCreate):
    db_postulacion = db.query(models.Postulacion).filter(models.Postulacion.ID_Postulacion == postulacion_id).first()
    if not db_postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    db_postulacion.ID_Usuario = postulacion.ID_Usuario
    db_postulacion.ID_Vacantes = postulacion.ID_Vacantes
    db.commit()
    db.refresh(db_postulacion)
    return db_postulacion

# Eliminar una postulacion por ID
def eliminar_postulacion(db: Session, postulacion_id: int):
    db_postulacion = db.query(models.Postulacion).filter(models.Postulacion.ID_Postulacion == postulacion_id).first()
    if not db_postulacion:
        raise HTTPException(status_code=404, detail="Postulación no encontrada")
    db.delete(db_postulacion)
    db.commit()
    return db_postulacion
