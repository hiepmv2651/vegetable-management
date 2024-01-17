from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.service.product_service import ProductService

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = "",
    sort_value: str = "id",
    sort_type: bool = True,
):
    products = ProductService.get_all_products(
        db, skip, limit, search, sort_value, sort_type
    )
    if products is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products not found"
        )
    return products
