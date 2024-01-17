from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.helper.validate_image import validate_image
from app.helper.json_response_default import JSONResponseDefault
from app.schema import product_schema
from app.service.product_service import ProductService

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
    default_response_class=ORJSONResponse,
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault)
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
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=JSONResponseDefault(
                status=False, message="No products found"
            ).model_dump(),
        )
    response = [
        product_schema.ProductGet.model_validate(product) for product in products
    ]

    return {
        "status": True,
        "message": "Success",
        "data": response,
    }


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault)
async def get_product_by_id(db: Session = Depends(get_db), id: int = Path(..., ge=1)):
    product = ProductService.get_product_by_id(db, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=JSONResponseDefault(
                status=False, message="No product found"
            ).model_dump(),
        )
    response = product_schema.ProductGet.model_validate(product).model_dump()

    return {
        "status": True,
        "message": "Success",
        "data": response,
    }


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=JSONResponseDefault
)
def create_product(
    product: product_schema.ProductCreate = Depends(),
    db: Session = Depends(get_db),
    image: Annotated[UploadFile, File] = File(None),
):
    validate_image(image)
    result = ProductService.create_product(db, product, image)
    if result != True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(message=result, status=False).model_dump(),
        )

    return {
        "status": True,
        "message": "Success",
        "data": None,
    }


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault)
def update_product(
    id: int = Path(..., ge=1),
    product: product_schema.ProductUpdate = Depends(),
    db: Session = Depends(get_db),
    image: Annotated[UploadFile, File] = File(None),
):
    if image:
        validate_image(image)
    result = ProductService.update_product(db, product, id, image)
    if result != True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(message=result, status=False).model_dump(),
        )

    return {
        "status": True,
        "message": "Success",
        "data": None,
    }


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, response_model=JSONResponseDefault
)
def delete_product(
    id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    result = ProductService.delete_product(db, id)
    if result != True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JSONResponseDefault(message=result, status=False).model_dump(),
        )

    return {
        "status": True,
        "message": "Success",
        "data": None,
    }
