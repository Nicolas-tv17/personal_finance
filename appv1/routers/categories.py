from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from appv1.schemas.category import CategoryCreate, CategoryResponse
from appv1.crud.categories import create_category_sql, get_category_by_name, get_all_categories
from db.database import get_db

router = APIRouter()

@router.post("/create")
async def insert_category(category: CategoryCreate, db: Session = Depends(get_db)):
    respuesta = create_category_sql(db, category)
    if respuesta: 
        return {"mensaje":"estoy usando el router de categorias"}
    
@router.get("/get-category-by-name/", response_model=CategoryResponse)
async def read_categories_by_name(name: str, db: Session= Depends(get_db)):
    categoria = get_category_by_name(db, name)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

@router.get("/get-all/", response_model=List[CategoryResponse])
async def read_all_categories(db: Session= Depends(get_db)):
    categoria = get_all_categories(db)
    if len(categoria) == 0:
        raise HTTPException(status_code=404, detail="No hay categorias")
    return categoria