from pydantic import BaseModel


class CategoryGet(BaseModel):
    name: str

    class Config:
        from_attributes = True


class CategoryCreate(CategoryGet):
    pass


class CategoryUpdate(CategoryGet):
    pass
