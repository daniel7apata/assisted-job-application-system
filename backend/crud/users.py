from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas



#Login
# Validar usuario y contraseña
def login_usuario(db: Session, usuario: str, contraseña: str):
    return db.query(models.Usuario).filter(
        models.Usuario.Usuario == usuario,
        models.Usuario.Contraseña == contraseña
    ).first()


# Crear un usuario
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

#Obtener todos los usuarios


# Obtener un usuario por ID
def obtener_usuario(db: Session, usuario_id: int):
    usuario = db.query(models.Usuario).filter(models.Usuario.ID_Usuario == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Obtener todos los usuarios
def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()

# Actualizar un usuario por ID
def actualizar_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.ID_Usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario.Usuario = usuario.Usuario
    db_usuario.Contraseña = usuario.Contraseña
    db_usuario.Nombre = usuario.Nombre
    db_usuario.Correo = usuario.Correo
    db_usuario.Telefono = usuario.Telefono
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Eliminar un usuario por ID
def eliminar_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.ID_Usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_usuario)
    db.commit()
    return db_usuario
