from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud.users as users_crud, crud.jobs as jobs_crud, crud.applications as applications_crud, crud.resumes as resumes_crud
import schemas
from database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto a la URL de tu frontend o "*" para permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Manejo de solicitudes OPTIONS (Preflight)
@app.options("/{any_path:path}")
async def handle_options():
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",  # O pon la URL de tu frontend si prefieres restringirlo
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT, DELETE",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        }
    )

# Dependencia para obtener DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API está funcionando correctamente"}

# Rutas para usuarios

# Login
@app.post("/login")
def login(usuario: str, contraseña: str, db: Session = Depends(get_db)):
    user = users_crud.login_usuario(db=db, usuario=usuario, contraseña=contraseña)
    if not user:
        return None
    return {"ID_Usuario": user.ID_Usuario}

@app.post("/auto-login")
def login_validacion(usuario: str, contraseña: str, db: Session = Depends(get_db)):
    user = users_crud.login_usuario(db=db, usuario=usuario, contraseña=contraseña)
    if not user:
        return {"mensaje": "incorrecto"}
    return {"mensaje": "correcto"}

@app.post("/usuarios/", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return users_crud.crear_usuario(db=db, usuario=usuario)

@app.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return users_crud.obtener_usuarios(db)

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return users_crud.obtener_usuario(db=db, usuario_id=usuario_id)

@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return users_crud.actualizar_usuario(db=db, usuario_id=usuario_id, usuario=usuario)

@app.delete("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return users_crud.eliminar_usuario(db=db, usuario_id=usuario_id)

# Rutas para vacantes
@app.post("/vacantes/", response_model=schemas.VacanteOut)
def crear_vacante(vacante: schemas.VacanteCreate, db: Session = Depends(get_db)):
    return jobs_crud.crear_vacante(db=db, vacante=vacante)

@app.get("/vacantes")
def listar_vacantes(db: Session = Depends(get_db)):
    return jobs_crud.obtener_vacantes(db)

@app.get("/vacantes/{vacante_id}", response_model=schemas.VacanteOut)
def obtener_vacante(vacante_id: int, db: Session = Depends(get_db)):
    return jobs_crud.obtener_vacante(db=db, vacante_id=vacante_id)

@app.put("/vacantes/{vacante_id}", response_model=schemas.VacanteOut)
def actualizar_vacante(vacante_id: int, vacante: schemas.VacanteCreate, db: Session = Depends(get_db)):
    return jobs_crud.actualizar_vacante(db=db, vacante_id=vacante_id, vacante=vacante)

@app.delete("/vacantes/{vacante_id}", response_model=schemas.VacanteOut)
def eliminar_vacante(vacante_id: int, db: Session = Depends(get_db)):
    return jobs_crud.eliminar_vacante(db=db, vacante_id=vacante_id)

# Rutas para postulaciones

@app.get("/postulaciones")
def listar_postulaciones(db: Session = Depends(get_db)):
    return applications_crud.obtener_postulaciones(db)

@app.post("/postulaciones/", response_model=schemas.PostulacionCreate)
def crear_postulacion(postulacion: schemas.PostulacionCreate, db: Session = Depends(get_db)):
    return applications_crud.crear_postulacion(db=db, postulacion=postulacion)

@app.put("/postulaciones/{postulacion_id}", response_model=schemas.PostulacionCreate)
def actualizar_postulacion(postulacion_id: int, postulacion: schemas.PostulacionCreate, db: Session = Depends(get_db)):
    return applications_crud.actualizar_postulacion(db=db, postulacion_id=postulacion_id, postulacion=postulacion)

@app.delete("/postulaciones/{postulacion_id}", response_model=schemas.PostulacionCreate)
def eliminar_postulacion(postulacion_id: int, db: Session = Depends(get_db)):
    return applications_crud.eliminar_postulacion(db=db, postulacion_id=postulacion_id)

# Rutas para hojas de vida

@app.get("/hojas_de_vida/{usuario_id}", response_model=list[schemas.HojaDeVidaCreate])
def obtener_hojas_de_vida(usuario_id: int, db: Session = Depends(get_db)):
    return resumes_crud.obtener_hojas_de_vida_por_usuario(db=db, usuario_id=usuario_id)

@app.get("/hojas-de-vida")
def listar_hojas_de_vida(db: Session = Depends(get_db)):
    return resumes_crud.obtener_hojas_de_vida(db)

@app.post("/hojas_de_vida/", response_model=schemas.HojaDeVidaCreate)
def crear_hoja_de_vida(hoja_de_vida: schemas.HojaDeVidaCreate, db: Session = Depends(get_db)):
    return resumes_crud.crear_hoja_de_vida(db=db, hoja_de_vida=hoja_de_vida)

@app.put("/hojas_de_vida/{usuario_id}", response_model=schemas.HojaDeVidaCreate)
def actualizar_hoja_de_vida(usuario_id: int, hoja_de_vida: schemas.HojaDeVidaCreate, db: Session = Depends(get_db)):
    return resumes_crud.actualizar_hoja_de_vida(db=db, usuario_id=usuario_id, hoja_de_vida=hoja_de_vida)

@app.delete("/hojas_de_vida/{hoja_id}", response_model=schemas.HojaDeVidaCreate)
def eliminar_hoja_de_vida(hoja_id: int, db: Session = Depends(get_db)):
    return resumes_crud.eliminar_hoja_de_vida(db=db, hoja_id=hoja_id)

handler = Mangum(app)
