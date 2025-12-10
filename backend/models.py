from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Modelo de la tabla Usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    ID_Usuario = Column(Integer, primary_key=True, index=True)
    Usuario = Column(String(100), unique=True)
    Contraseña = Column(String(100))
    Nombre = Column(String(150))
    Correo = Column(String(50))
    Telefono = Column(String(20))

    postulaciones = relationship("Postulacion", back_populates="usuario")
    # Relación con la tabla HojasDeVida
    hoja_de_vida = relationship("HojaDeVida", back_populates="usuario")

# Modelo de la tabla HojasDeVida
class HojaDeVida(Base):
    __tablename__ = "hojas_de_vida"
    ID_Hojadevida = Column(Integer, primary_key=True, index=True)
    ID_Usuario = Column(Integer, ForeignKey('usuarios.ID_Usuario'))
     # Relación con la tabla Usuarios
    usuario = relationship("Usuario", back_populates="hoja_de_vida")
    Estudios = Column(Text)
    Skills = Column(Text)
    Experiencia = Column(Text)

   
# Modelo de la tabla Vacantes
class Vacante(Base):
    __tablename__ = "vacantes"
    ID_Vacantes = Column(Integer, primary_key=True, index=True)
    Titulo = Column(String(500))
    Empresa = Column(String(150))
    Condiciones = Column(Text)
    Descripcion = Column(Text)
    Region = Column(String(150))
    Modalidad = Column(String(50))
    Requisitos = Column(Text)
    Aptitudes = Column(Text)
    Enlace = Column(String(500))
    Beneficios = Column(Text)
    postulaciones = relationship("Postulacion", back_populates="vacante")



# Modelo de la tabla Postulaciones
class Postulacion(Base):
    __tablename__ = "postulaciones"
    ID_Postulacion = Column(Integer, primary_key=True, index=True)
    ID_Usuario = Column(Integer, ForeignKey('usuarios.ID_Usuario'))
    ID_Vacantes = Column(Integer, ForeignKey('vacantes.ID_Vacantes'))
    usuario = relationship("Usuario", back_populates="postulaciones")
    vacante = relationship("Vacante", back_populates="postulaciones")