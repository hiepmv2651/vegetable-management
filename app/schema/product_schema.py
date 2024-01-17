from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class ProductGet(BaseModel):
    name: str
    description: str | None
    price: float
    image_url: str | None
    stock_quantity: int
    category: CategoryBase

    class Config:
        from_attributes = True
        
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(..., gt=0, description="Must be greater than 0")
    stock_quantity: int
    category_id: int

    class Config:
        from_attributes = True
        
class ProductUpdate(ProductCreate):
    pass
