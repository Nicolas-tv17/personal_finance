from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from appv1.schemas.category import CategoryCreate
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Crear una categoria
def create_category_sql(db: Session, category: CategoryCreate):
    try:
        sql_query = text(
        "INSERT INTO category (category_id, category_name, category_description) "
        "VALUES (:category_id, :category_name, :category_description)"
        )
        params = {
            "category_id": category.category_id,
            "category_name": category.category_name,
            "category_description": category.category_description,
        }
        db.execute(sql_query, params)
        db.commit()
        return True
    except IntegrityError as e:
        db.rollback()
        print(f"Error al crear categoria: {e}")
        if 'Duplicate entry' in str(e.orig):
            if 'PRIMARY' in str(e.orig):
                raise HTTPException(status_code=400, detail="Error. La categoria ya está registrada, vuelva a intentarlo")
        else:
            raise HTTPException(status_code=400, detail="Error. No hay Integridad de datos al crear la categoria")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al crear categoria: {e}")
        raise HTTPException(status_code=500, detail="Error al crear categoria")
    
# Consultar una categoria por nombre
def get_category_by_name(db: Session, name: str):
    try:
        sql = text("SELECT * FROM category WHERE category_name = :name") 
        result = db.execute(sql, {"name": name}).fetchone()
        return result
    except SQLAlchemyError as e:
        print(f"Error al buscar una categoria por nombre: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar una categoria por nombre")
    
# Consultar todas las categorias activos
def get_all_categories(db: Session):
    try:
        sql = text("SELECT * FROM category WHERE category_status = true")
        result = db.execute(sql).fetchall()
        return result
    except SQLAlchemyError as e:
        print(f"Error al buscar categorias: {e}")
        raise HTTPException(status_code=500, detail="Error al buscar categorias")