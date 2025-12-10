from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión para base de datos local (MySQL)
# Para usar con RDS en AWS, deberás cambiar estos valores a tu instancia RDS.
#DATABASE_URL = "mysql+pymysql://root:@localhost:3306/mi_base_datos5"
DATABASE_URL = "mysql+pymysql://admin:Farjevasquez16*@mi-base-empleo.ch0u86saacoy.us-east-2.rds.amazonaws.com:3306/mi_base_datos"
# Configuración de la base de datos (local)
engine = create_engine(DATABASE_URL, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
