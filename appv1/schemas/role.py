from typing import Annotated
from pydantic import BaseModel, StringConstraints

class RolBase(BaseModel):
    rol_name: Annotated[str, StringConstraints(max_length=15)]

class RolCreate(RolBase):
    rol_name: Annotated[str, StringConstraints(max_length=15)]
    
class RolResponse(RolBase):
    rol_name: str
 