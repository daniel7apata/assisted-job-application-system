from pydantic import BaseModel

# Esquema para los usuarios
class UsuarioBase(BaseModel):
    Usuario: str
    Contraseña: str
    Nombre: str
    Correo: str
    Telefono: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    ID_Usuario: int

    class Config:
        orm_mode = True

# Esquema para las vacantes
class VacanteBase(BaseModel):
    Titulo: str
    Empresa: str
    Condiciones: str
    Descripcion: str
    Region: str
    Modalidad: str
    Requisitos: str
    Aptitudes: str
    Enlace: str
    Beneficios: str

class VacanteCreate(VacanteBase):
    pass

class VacanteOut(VacanteBase):
    ID_Vacantes: int

    class Config:
        orm_mode = True

# Esquema para las postulaciones
class PostulacionCreate(BaseModel):
    ID_Usuario: int
    ID_Vacantes: int

# Esquema para las hojas de vida
class HojaDeVidaCreate(BaseModel):
    ID_Usuario: int
    Estudios: str
    Skills: str
    Experiencia: str

    class Config:
        orm_mode = True
