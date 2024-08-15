from typing import Annotated
from pydantic import BaseModel, StringConstraints


class CategoryBase(BaseModel):
    category_name: Annotated[str, StringConstraints(max_length=30)]
    category_description: Annotated[str, StringConstraints(max_length=50)]

class CategoryCreate(CategoryBase):
    category_id: Annotated[str, StringConstraints(max_length=3)]
    
class CategoryResponse(CategoryBase):
    category_id: int
    category_status: bool = True