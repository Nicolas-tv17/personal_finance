from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from appv1.schemas.role import RolCreate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Crear un rol
def create_rol_sql(db: Session, rol: RolCreate):
    try:
        sql_query = text(
        "INSERT INTO roles (rol_name) "
        "VALUES (:rol_name)"
        )
        params = {
            "rol_name": rol.rol_name,
        }
        db.execute(sql_query, params)
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()
        print(f"Error al crear rol: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. El rol ya está creado, vuelva a intentarlo")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear rol")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=500, detail="Error al crear rol")
    
# Consultar todos los roles
def get_all_rol(db: Session):
    try:
        sql = text("SELECT * FROM roles")
        result = db.execute(sql).fetchall()
        return result
    except SQLAlchemyError as e:
        print(f"Error al buscar roles: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar roles")
    
# Consultar un rol por su nombre
def get_rol_by_name(db: Session, rol_name: str):
    try:
        sql = text("SELECT * FROM roles WHERE rol_name = :rol_name")
        result = db.execute(sql, {"rol_name": rol_name}).fetchone()
        return result
    except SQLAlchemyError as e:
        print(f"Error al buscar rol por nombre: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar rol por nombre")