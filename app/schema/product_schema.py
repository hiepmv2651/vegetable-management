from pydantic import BaseModel


class ProductGet(BaseModel):
    name: str
    description: str | None
    price: float
    category_id: int
    image_url: str | None
    stock_quantity: int
    category_name: str
    
    class Config:
        from_attributes = True
        