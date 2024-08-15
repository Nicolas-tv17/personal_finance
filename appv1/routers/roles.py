from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from appv1.schemas.role import RolCreate, RolResponse
from appv1.crud.roles import create_rol_sql, get_all_rol, get_rol_by_name
from db.database import get_db

router = APIRouter()

@router.post("/create")
async def insert_role(rol: RolCreate, db: Session = Depends(get_db)):
    respuesta = create_rol_sql(db, rol)
    if respuesta: 
        return {"mensaje":"estoy usando el router de roles"}
    
@router.get("/get-rol-by-name/", response_model=RolResponse)
async def read_rol_by_name(rol_name: str, db: Session= Depends(get_db)):
    rol = get_rol_by_name(db, rol_name)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

@router.get("/get-all/", response_model=List[RolResponse])
async def read_all_rol(db: Session= Depends(get_db)):
    roles = get_all_rol(db)
    if len(roles) == 0:
        raise HTTPException(status_code=404, detail="No hay roles")
    return roles